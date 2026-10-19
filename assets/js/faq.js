/* Smooth open/close for <details> FAQ items */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.faq details').forEach(function (d) {
    var summary = d.querySelector('summary');
    var body = d.querySelector('.faq__body');
    if (!summary || !body || reduce) return;
    summary.addEventListener('click', function (e) {
      e.preventDefault();
      if (d.open) {
        var h = body.scrollHeight;
        body.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 350, easing: 'cubic-bezier(.65,0,.35,1)' }).onfinish = function () { d.open = false; };
        d.classList.remove('is-open');
      } else {
        d.open = true;
        var h2 = body.scrollHeight;
        body.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.22,.8,.2,1)' });
      }
    });
  });
})();
