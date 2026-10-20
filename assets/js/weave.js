/* Builds an animated woven swatch (warp + weft) inside every [data-weave] */
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var palettes = {
    hero: { warp: ['#DCCBA8', '#E8DBC0'], weft: ['#D9713F', '#F3C94D', '#B8572B', '#E8936A'] },
    pink: { warp: ['#2B241C', '#453A2C'], weft: ['#D9713F', '#F6D9C4'] },
    peacock: { warp: ['#2B241C', '#453A2C'], weft: ['#B8572B', '#E8936A'] },
    turmeric: { warp: ['#2B241C', '#453A2C'], weft: ['#F3C94D', '#FBE9AE'] }
  };

  function el(name, attrs) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }

  document.querySelectorAll('[data-weave]').forEach(function (box) {
    var pal = palettes[box.getAttribute('data-weave')] || palettes.hero;
    var gap = parseInt(box.getAttribute('data-gap') || '34', 10);
    var w = 720, h = 720;
    var cols = Math.ceil(w / gap) + 1, rows = Math.ceil(h / gap) + 1;
    var sw = gap * 0.56;
    var svg = el('svg', { viewBox: '0 0 ' + w + ' ' + h, preserveAspectRatio: 'xMidYMid slice', 'aria-hidden': 'true', focusable: 'false' });
    var gWarp = el('g', {}), gWeft = el('g', {}), gOver = el('g', {});
    var i, j, x, y, d;

    // warp: vertical threads, drawn top to bottom
    for (i = 0; i < cols; i++) {
      x = i * gap + gap / 2;
      d = (i * 0.045).toFixed(3) + 's';
      gWarp.appendChild(el('path', { class: 'warp', d: 'M' + x + ' -10V' + (h + 10), stroke: pal.warp[i % pal.warp.length], 'stroke-width': sw, style: '--len:' + (h + 20) + ';--d:' + d }));
    }
    // weft: horizontal threads, drawn left to right after the warp
    for (j = 0; j < rows; j++) {
      y = j * gap + gap / 2;
      d = (0.6 + j * 0.06).toFixed(3) + 's';
      gWeft.appendChild(el('path', { class: 'weft', d: 'M-10 ' + y + 'H' + (w + 10), stroke: pal.weft[j % pal.weft.length], 'stroke-width': sw, style: '--len:' + (w + 20) + ';--d:' + d }));
    }
    // over-segments: warp passes over weft on alternate crossings, giving the plain-weave look
    for (j = 0; j < rows; j++) {
      for (i = 0; i < cols; i++) {
        if ((i + j) % 2) continue;
        x = i * gap + gap / 2; y = j * gap + gap / 2;
        d = (1.5 + j * 0.06 + i * 0.012).toFixed(3) + 's';
        gOver.appendChild(el('path', { class: 'over', d: 'M' + x + ' ' + (y - gap / 2 + 1) + 'V' + (y + gap / 2 - 1), stroke: pal.warp[i % pal.warp.length], 'stroke-width': sw, style: '--d:' + d }));
      }
    }
    svg.appendChild(gWarp); svg.appendChild(gWeft); svg.appendChild(gOver);
    box.appendChild(svg);
    if (reduce) box.classList.add('weave--static');
  });
})();
