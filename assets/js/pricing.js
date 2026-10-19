/* Accessible tabs for the pricing page, with a sliding pill */
(function () {
  var tablist = document.querySelector('[role="tablist"]');
  if (!tablist) return;
  var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
  var pill = tablist.querySelector('.tabs__pill');

  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (pill) { pill.style.width = tab.offsetWidth + 'px'; pill.style.transform = 'translateX(' + tab.offsetLeft + 'px)'; }
    if (focus) tab.focus();
    if (history.replaceState) history.replaceState(null, '', '#' + tab.dataset.slug);
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') select(tabs[(i + 1) % tabs.length], true);
      if (e.key === 'ArrowLeft') select(tabs[(i - 1 + tabs.length) % tabs.length], true);
    });
  });
  var start = tabs.filter(function (t) { return '#' + t.dataset.slug === location.hash; })[0] || tabs[0];
  select(start);
  window.addEventListener('resize', function () { select(tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0]); });
})();
