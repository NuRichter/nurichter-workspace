/* ================================================================
   NuRichter Workspace — Main JavaScript
   ================================================================ */

// Navbar scroll behavior
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar-nu');
  if (nav) {
    if (window.scrollY > 50) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  }
});

// Footer year
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.footer-year').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  // AOS init
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      offset: 80
    });
  }

  // Active nav link
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-nav-overlay a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Counter animation
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10);
          const suffix = el.dataset.suffix || '';
          animateCounter(el, target, suffix);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(el => observer.observe(el));
  }
});

function animateCounter(el, target, suffix, duration = 2000) {
  const start = performance.now();
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target) + suffix;
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// Smooth scroll for anchor links
document.addEventListener('click', (e) => {
  const anchor = e.target.closest('a[href^="#"]');
  if (anchor) {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
});

// Alpine: Contact form
document.addEventListener('alpine:init', () => {
  Alpine.data('contactForm', () => ({
    form: { name: '', email: '', whatsapp: '', need: '', message: '' },
    submitted: false,
    submitForm() {
      const msg = `Halo NuRichter Workspace!\n\nNama: ${this.form.name}\nEmail: ${this.form.email}\nWhatsApp: ${this.form.whatsapp}\nKebutuhan: ${this.form.need}\n\nPesan:\n${this.form.message}`;
      const url = `https://wa.me/6281280717345?text=${encodeURIComponent(msg)}`;
      window.open(url, '_blank');
      this.submitted = true;
    }
  }));
});
