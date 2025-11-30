document.addEventListener('DOMContentLoaded', function () {
  const track = document.querySelector('.carousel-track');
  if (!track) return;
  const slides = Array.from(track.children);
  const prevButton = document.querySelector('.carousel-prev');
  const nextButton = document.querySelector('.carousel-next');
  const indicators = document.querySelectorAll('.carousel-indicators button');
  let index = 0;
  const moveTo = (i) => {
    index = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
    indicators.forEach((btn, idx) => btn.classList.toggle('active', idx === index));
    // mark the active slide so CSS effects (zoom/less blur) can apply
    slides.forEach((s, idx) => s.classList.toggle('active', idx === index));
  };
  nextButton && nextButton.addEventListener('click', () => moveTo(index + 1));
  prevButton && prevButton.addEventListener('click', () => moveTo(index - 1));
  indicators.forEach((btn, idx) => btn.addEventListener('click', () => moveTo(idx)));
  // Auto play with configurable interval (ms). Default 10000 (10s).
  const carousel = document.querySelector('.carousel');
  const DEFAULT_INTERVAL = 10000; // 10 seconds
  const interval = (carousel && parseInt(carousel.dataset.interval, 10)) || DEFAULT_INTERVAL;

  // start autoplay and provide helper to restart
  let autoplay = null;
  const startAutoplay = () => {
    clearInterval(autoplay);
    autoplay = setInterval(() => moveTo(index + 1), interval);
  };

  // initialize
  moveTo(0);
  startAutoplay();

  // pause on hover/focus, resume on leave
  if (carousel) {
    carousel.addEventListener('mouseover', () => clearInterval(autoplay));
    carousel.addEventListener('mouseout', () => startAutoplay());
    carousel.addEventListener('focusin', () => clearInterval(autoplay));
    carousel.addEventListener('focusout', () => startAutoplay());
  }
});
