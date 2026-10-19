/* Global behaviour: header, menus, scroll thread, booking month, year */
(function () {
  document.documentElement.classList.remove('no-js');

  // Local preview: when opened straight from disk (file://), point folder links at their index.html.
  // On a real web server this does nothing, so URLs stay clean for SEO.
  if (window.location.protocol === 'file:') {
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (/^(https?:|mailto:|tel:|#)/.test(href)) return;
      if (href === './' || href === '' ) { a.setAttribute('href', 'index.html'); return; }
      if (href.slice(-1) === '/') a.setAttribute('href', href + 'index.html');
    });
    var form = document.querySelector('[data-quote-form]');
    if (form && form.getAttribute('action').slice(-1) === '/') form.setAttribute('action', form.getAttribute('action') + 'index.html');
  }

  var header = document.querySelector('.site-header');
  var lastY = window.scrollY;
  var thread = document.querySelector('.scroll-thread span');

  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('is-scrolled', y > 20);
      // hide on scroll down, show on scroll up (not while mobile menu is open)
      var menuOpen = document.body.classList.contains('menu-open');
      header.classList.toggle('is-hidden', !menuOpen && y > 400 && y > lastY);
    }
    if (thread) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      thread.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var sheet = document.getElementById('mobile-menu');
  if (toggle && sheet) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      sheet.classList.toggle('is-open', open);
      document.body.classList.toggle('menu-open', open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sheet.classList.contains('is-open')) toggle.click();
    });
  }

  // Desktop services dropdown: click / keyboard support
  document.querySelectorAll('.nav__item--drop').forEach(function (item) {
    var btn = item.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) { item.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });

  // "Now booking projects for <next month>"
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var next = months[(new Date().getMonth() + 1) % 12];
  document.querySelectorAll('[data-booking-month]').forEach(function (el) { el.textContent = next; });

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
