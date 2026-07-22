document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  if (window.lucide) {
    lucide.createIcons();
  }

  // Text Reveal Observer
  const revealTextEls = document.querySelectorAll('.reveal-text');
  const textIo = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        const spans = e.target.querySelectorAll(':scope > span');
        spans.forEach((span, i) => {
          span.style.transitionDelay = `${i * 0.15}s`;
        });
        textIo.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  revealTextEls.forEach(el => textIo.observe(el));

  // Scroll reveal observer
  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => io.observe(el));

  // Process steps stagger + line fill
  const steps = document.querySelectorAll('.reveal-step');
  const fill = document.getElementById('processFill');
  const stepIO = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        if (fill) fill.style.width = '100%';
        steps.forEach((s, i) => {
          setTimeout(() => s.classList.add('in'), i * 160);
        });
        stepIO.disconnect();
      }
    });
  }, { threshold: 0.3 });
  const processSection = document.querySelector('.process');
  if (steps.length && processSection) stepIO.observe(processSection);

  // Custom Cursor Logic
  const cursorDot = document.getElementById('cursor-dot');
  const cursorRing = document.getElementById('cursor-ring');
  const cursorGlow = document.getElementById('cursor-glow');

  let mouseX = 0, mouseY = 0;
  let ringX = 0, ringY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    if (cursorDot) cursorDot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
    if (cursorGlow) cursorGlow.style.transform = `translate(${mouseX}px, ${mouseY}px)`;

    // 3D Tilt for Hero Art
    const heroArt = document.querySelector('.hero-art svg');
    if (heroArt) {
      const rect = heroArt.getBoundingClientRect();
      const artX = rect.left + rect.width / 2;
      const artY = rect.top + rect.height / 2;
      const deltaX = (mouseX - artX) / 15;
      const deltaY = (mouseY - artY) / 15;
      heroArt.style.transform = `rotateX(${-deltaY}deg) rotateY(${deltaX}deg)`;
    }
  });

  // Ring follow animation
  function animateRing() {
    ringX += (mouseX - ringX) * 0.2;
    ringY += (mouseY - ringY) * 0.2;
    if (cursorRing) cursorRing.style.transform = `translate(${ringX}px, ${ringY}px)`;
    requestAnimationFrame(animateRing);
  }
  animateRing();

  // Hover states for cursor
  const interactiveEls = document.querySelectorAll('a, button, input, textarea, select, .glass-card, .showcase-item');
  interactiveEls.forEach(el => {
    el.addEventListener('mouseenter', () => {
      if (cursorRing) {
        cursorRing.style.width = '48px';
        cursorRing.style.height = '48px';
        cursorRing.style.borderColor = 'var(--signal-bright)';
        cursorRing.style.backgroundColor = 'rgba(20, 184, 166, 0.1)';
      }
    });
    el.addEventListener('mouseleave', () => {
      if (cursorRing) {
        cursorRing.style.width = '32px';
        cursorRing.style.height = '32px';
        cursorRing.style.borderColor = 'var(--copper-bright)';
        cursorRing.style.backgroundColor = 'transparent';
      }
    });
  });
});
