const menuButton = document.querySelector('.menu-toggle');
const siteNav = document.querySelector('.site-nav');

if (menuButton && siteNav) {
  const closeMenu = () => {
    siteNav.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open menu');
    document.body.classList.remove('menu-open');
  };

  menuButton.addEventListener('click', () => {
    const isOpen = siteNav.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('menu-open', isOpen);
  });

  siteNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) closeMenu();
  });
}


// YouTube video modal
const videoModal = document.querySelector('#video-modal');
const videoFrame = document.querySelector('#video-frame');
const videoLaunchers = document.querySelectorAll('[data-youtube]');

function closeVideoModal() {
  if (!videoModal || !videoFrame) return;
  videoFrame.src = '';
  videoModal.classList.remove('is-open');
  videoModal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('modal-open');
}

videoLaunchers.forEach((button) => {
  button.addEventListener('click', () => {
    if (!videoModal || !videoFrame) return;
    const id = button.dataset.youtube;
    videoFrame.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    videoModal.classList.add('is-open');
    videoModal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
  });
});

document.querySelectorAll('[data-video-close]').forEach((button) => {
  button.addEventListener('click', closeVideoModal);
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeVideoModal();
});

// Lightweight consultation request calendar.
// It creates the next 14 weekdays and opens an email request; it does not
// claim real-time availability until an external booking provider is connected.
const bookingDates = document.querySelector('#booking-dates');
const bookingRequest = document.querySelector('#booking-request');

if (bookingDates && bookingRequest) {
  const dates = [];
  const cursor = new Date();

  while (dates.length < 14) {
    cursor.setDate(cursor.getDate() + 1);
    const day = cursor.getDay();
    if (day !== 0 && day !== 6) dates.push(new Date(cursor));
  }

  dates.forEach((date) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'booking-date';
    button.innerHTML = `<strong>${date.toLocaleDateString('en-US', { weekday: 'short' })}</strong><span>${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>`;
    button.addEventListener('click', () => {
      bookingDates.querySelectorAll('.booking-date').forEach((item) => item.classList.remove('is-selected'));
      button.classList.add('is-selected');
      const label = date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
      const subject = encodeURIComponent('30 Minute Video Consult');
      const body = encodeURIComponent(`Hi Thrill Wave,\n\nI'd like to request a 30-minute video consult on ${label}. Please send available times.\n\nThanks!`);
      bookingRequest.href = `mailto:hi@thrillwave.com?subject=${subject}&body=${body}`;
      bookingRequest.setAttribute('aria-disabled', 'false');
    });
    bookingDates.appendChild(button);
  });
}
