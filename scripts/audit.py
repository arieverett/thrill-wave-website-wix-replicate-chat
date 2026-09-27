#!/usr/bin/env python3
"""Offline integrity audit for the Thrill Wave static site."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")
errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def local_target(source: Path, ref: str) -> Path | None:
    ref = ref.strip()
    if not ref or ref.startswith("#") or ref.startswith(SKIP_SCHEMES):
        return None
    path = urlsplit(ref).path
    if not path:
        return None
    if path.startswith("/"):
        candidate = ROOT / path.lstrip("/")
    else:
        candidate = source.parent / path
    candidate = candidate.resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"{source.relative_to(ROOT)}: reference escapes repository: {ref}")
        return None
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


html_files = sorted(ROOT.rglob("*.html"))
if not html_files:
    fail("No HTML files found.")

for file in html_files:
    rel = file.relative_to(ROOT)
    text = file.read_text(encoding="utf-8")

    title_count = len(re.findall(r"<title>[^<]+</title>", text, re.I))
    h1_count = len(re.findall(r"<h1\b", text, re.I))
    if title_count != 1:
        fail(f"{rel}: expected exactly one <title>, found {title_count}")
    if h1_count != 1:
        fail(f"{rel}: expected exactly one <h1>, found {h1_count}")

    if rel.name != "404.html":
        if not re.search(r'<meta\s+name=["\']description["\']', text, re.I):
            fail(f"{rel}: missing meta description")
        if not re.search(r'<link\s+rel=["\']canonical["\']', text, re.I):
            fail(f"{rel}: missing canonical URL")

    ids = re.findall(r'\sid=["\']([^"\']+)["\']', text, re.I)
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        fail(f"{rel}: duplicate ids: {', '.join(duplicates)}")

    for tag in re.findall(r"<img\b[^>]*>", text, re.I):
        if not re.search(r'\salt=["\'][^"\']*["\']', tag, re.I):
            fail(f"{rel}: image missing alt attribute: {tag[:100]}")

    for ref in re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text, re.I):
        target = local_target(file, ref)
        if target is not None and not target.exists():
            fail(f"{rel}: missing local reference {ref} -> {target.relative_to(ROOT)}")

for css_file in ROOT.rglob("*.css"):
    css = css_file.read_text(encoding="utf-8")
    for ref in re.findall(r"url\((?:['\"])?([^)'\"]+)", css):
        target = local_target(css_file, ref)
        if target is not None and not target.exists():
            fail(f"{css_file.relative_to(ROOT)}: missing CSS asset {ref}")

for required in ("robots.txt", "sitemap.xml", "llms.txt", "site.webmanifest", "_headers", "_redirects"):
    if not (ROOT / required).exists():
        fail(f"Missing required production file: {required}")

ds = list(ROOT.rglob(".DS_Store"))
if ds:
    fail("macOS metadata committed: " + ", ".join(str(p.relative_to(ROOT)) for p in ds))

for asset in (ROOT / "assets").rglob("*") if (ROOT / "assets").exists() else []:
    if asset.is_file() and asset.stat().st_size > 2_500_000:
        warn(f"Large asset: {asset.relative_to(ROOT)} ({asset.stat().st_size / 1_000_000:.1f} MB)")

for item in warnings:
    print(f"WARNING: {item}")

if errors:
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    print(f"\nAudit failed with {len(errors)} error(s).", file=sys.stderr)
    raise SystemExit(1)

print(f"Audit passed: {len(html_files)} HTML files checked; local references are intact.")
