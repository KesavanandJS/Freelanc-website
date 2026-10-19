/* Scroll reveals and headline word split (keeps accent spans) */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var i = 0;
  function wrap(word, cls) {
    var w = '<span class="split-word' + (cls ? ' ' + cls : '') + '" style="--i:' + (i++) + '">' + word + '</span>';
    return '<span class="split-line" aria-hidden="true">' + w + '</span>';
  }
  document.querySelectorAll('[data-split]').forEach(function (el) {
    if (reduce) return;
    i = 0;
    el.setAttribute('aria-label', el.textContent.trim().replace(/\s+/g, ' '));
    var out = [];
    el.childNodes.forEach(function (node) {
      var cls = node.nodeType === 1 ? node.className : '';
      node.textContent.split(/\s+/).forEach(function (w) { if (w) out.push(wrap(w, cls)); });
    });
    el.innerHTML = out.join(' ');
  });

  var items = document.querySelectorAll('[data-reveal]');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
})();
