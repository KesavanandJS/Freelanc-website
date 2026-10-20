/* Featured-work carousel: pagination dots, autoplay, pauses on hover/focus/off-screen */
(function () {
  var wraps = document.querySelectorAll('.work-carousel-wrap');
  if (!wraps.length) return;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  wraps.forEach(function (wrap) {
    var track = wrap.querySelector('.work-carousel');
    var dotsBox = wrap.querySelector('[data-work-dots]');
    var cards = Array.prototype.slice.call(track.querySelectorAll('.work-card'));
    if (!track || !cards.length) return;

    function cardLeft(card) {
      return card.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
    }

    function setActive() {
      var pos = track.scrollLeft;
      var closest = 0;
      var best = Infinity;
      cards.forEach(function (card, i) {
        var d = Math.abs(cardLeft(card) - pos);
        if (d < best) { best = d; closest = i; }
      });
      dots.forEach(function (dot, i) { dot.classList.toggle('is-active', i === closest); });
    }

    function settleActive() {
      setActive();
      clearTimeout(settleActive._t1);
      clearTimeout(settleActive._t2);
      settleActive._t1 = setTimeout(setActive, 350);
      settleActive._t2 = setTimeout(setActive, 650);
    }

    var dots = cards.map(function (card, i) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'work-dots__dot';
      dot.setAttribute('aria-label', 'Go to project ' + (i + 1));
      dot.addEventListener('click', function () {
        track.scrollTo({ left: cardLeft(card), behavior: 'smooth' });
        settleActive();
      });
      if (dotsBox) dotsBox.appendChild(dot);
      return dot;
    });

    setActive();

    var scrollTimer = null;
    track.addEventListener('scroll', function () {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(setActive, 80);
    }, { passive: true });

    if (reduceMotion) return;

    var delay = 3500;
    var timer = null;

    function step() {
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return cards[0].getBoundingClientRect().width + gap;
    }
    function advance() {
      var max = track.scrollWidth - track.clientWidth;
      if (track.scrollLeft >= max - 4) {
        track.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        track.scrollBy({ left: step(), behavior: 'smooth' });
      }
      settleActive();
    }
    function start() {
      if (timer || track.scrollWidth <= track.clientWidth + 4) return;
      timer = setInterval(advance, delay);
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) start(); else stop();
      });
    }, { threshold: .3 });
    io.observe(track);

    ['pointerenter', 'focusin', 'touchstart'].forEach(function (evt) {
      track.addEventListener(evt, stop, { passive: true });
    });
    ['pointerleave', 'focusout'].forEach(function (evt) {
      track.addEventListener(evt, start, { passive: true });
    });
  });
})();
