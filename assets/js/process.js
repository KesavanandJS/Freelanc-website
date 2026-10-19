/* Fills the process thread as the steps scroll through the viewport */
(function () {
  var lists = document.querySelectorAll('.process');
  if (!lists.length) return;
  function update() {
    lists.forEach(function (list) {
      var r = list.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
      var track = list.parentElement.querySelector('.process__track');
      if (track) track.style.setProperty('--p', p.toFixed(3));
      var steps = list.querySelectorAll('li');
      steps.forEach(function (li, i) { li.classList.toggle('is-done', p >= (i + 0.5) / steps.length); });
    });
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
