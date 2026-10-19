/* Filters case studies by platform on the Work page */
(function () {
  var buttons = document.querySelectorAll('[data-filter]');
  if (!buttons.length) return;
  var rows = document.querySelectorAll('[data-platform]');
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      buttons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      rows.forEach(function (r) { r.classList.toggle('is-hidden', f !== 'all' && r.getAttribute('data-platform').indexOf(f) === -1); });
    });
  });
})();
