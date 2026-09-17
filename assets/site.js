(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var css = function (n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); };
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* mobile menu */
  var mb = $('.menu-btn'), nav = $('.nav');
  if (mb && nav) mb.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    mb.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* copy buttons: data-copy="#id" */
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var el = $(b.getAttribute('data-copy'));
      if (!el) return;
      var label = b.textContent;
      var done = function (ok) { b.textContent = ok ? 'Copied' : 'Select the text and copy'; setTimeout(function () { b.textContent = label; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(el.textContent.trim()).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  });

  /* ---------------------------------------------------------------
     Home hero: a real fit being built, component by component.
     The data are the hardest benchmark set (450 points with sigma);
     the components are exactly what the bench returned for it, so the
     reduced chi-square shown at every step is computed, not staged.
     --------------------------------------------------------------- */
  var cv = $('#scope');
  if (cv && window.HERO) {
    var H = window.HERO, n = H.x.length, ctx = cv.getContext('2d');
    var NP = function (label) {
      if (/background/.test(label)) {
        var deg = ['constant', 'linear', 'quadratic', 'cubic', 'quartic', 'quintic', 'sextic', 'septic'].indexOf(label.split(' ')[0]);
        return deg + 1;
      }
      if (/packet/.test(label)) return 6;
      if (/oscillation/.test(label)) return 5;
      if (/Fano|Voigt/.test(label)) return 4;
      return 3;
    };
    var stages = [];
    var acc = new Float64Array(n), k = 0;
    stages.push({ model: null, k: 0, label: 'data only' });
    H.comps.forEach(function (c, i) {
      var m = new Float64Array(n);
      for (var j = 0; j < n; j++) { acc[j] += c.v[j]; m[j] = acc[j]; }
      k += NP(c.label);
      stages.push({ model: m, k: k, label: c.label, comp: c.v, idx: i });
    });
    var red = function (m, kk) {
      var s = 0;
      for (var j = 0; j < n; j++) { var r = (H.y[j] - (m ? m[j] : 0)) / H.s[j]; s += r * r; }
      return s / (n - kk);
    };
    // the "before" reference: what a mean line leaves — shown only as the start value
    stages.forEach(function (st, i) { st.red = i === 0 ? NaN : red(st.model, st.k); });

    var ymin = Infinity, ymax = -Infinity;
    for (var j = 0; j < n; j++) { ymin = Math.min(ymin, H.y[j] - H.s[j]); ymax = Math.max(ymax, H.y[j] + H.s[j]); }
    var pad = (ymax - ymin) * 0.06; ymin -= pad; ymax += pad;
    var xmin = H.x[0], xmax = H.x[n - 1];

    var W = 0, Hh = 0, dpr = 1;
    var size = function () {
      var w = cv.clientWidth || 600;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = w; Hh = Math.round(w * 0.66);
      cv.width = Math.round(W * dpr); cv.height = Math.round(Hh * dpr);
      cv.style.height = Hh + 'px';
    };
    size();
    window.addEventListener('resize', function () { size(); draw(cur, 1); });

    var cur = 0, t0 = 0;
    var elStep = $('#scope-step'), elComp = $('#scope-comp'), elRed = $('#scope-red'), elVerdict = $('#scope-verdict');

    function draw(si, prog) {
      var C = { grid: css('--grid'), rule: css('--grid-strong'), ink3: css('--ink-3'), data: css('--data'), fit: css('--fit'), paper: css('--paper') };
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, Hh);
      var L = 40, R = W - 12, T = 12, resH = Math.max(46, Hh * 0.17), B = Hh - resH - 36, RT = B + 14, RB = Hh - 22;
      var X = function (x) { return L + (x - xmin) / (xmax - xmin) * (R - L); };
      var Y = function (y) { return B - (y - ymin) / (ymax - ymin) * (B - T); };
      // grid
      ctx.strokeStyle = C.grid; ctx.lineWidth = 1;
      for (var g = 0; g <= 5; g++) { var yy = Math.round(T + (B - T) * g / 5) + .5; ctx.beginPath(); ctx.moveTo(L, yy); ctx.lineTo(R, yy); ctx.stroke(); }
      for (var g2 = 0; g2 <= 6; g2++) { var xx = Math.round(L + (R - L) * g2 / 6) + .5; ctx.beginPath(); ctx.moveTo(xx, T); ctx.lineTo(xx, B); ctx.stroke(); }
      ctx.strokeStyle = C.rule; ctx.strokeRect(L + .5, T + .5, R - L, B - T); ctx.strokeRect(L + .5, RT + .5, R - L, RB - RT);
      ctx.fillStyle = C.ink3; ctx.font = '11px "IBM Plex Mono", monospace'; ctx.textAlign = 'center';
      for (var t = 0; t <= 6; t++) ctx.fillText(String(Math.round((xmin + (xmax - xmin) * t / 6) * 10) / 10), L + (R - L) * t / 6, Hh - 6);
      ctx.textAlign = 'right';
      for (var g3 = 0; g3 <= 5; g3++) { var v = ymax - (ymax - ymin) * g3 / 5; ctx.fillText(v.toFixed(1), L - 6, T + (B - T) * g3 / 5 + 4); }
      ctx.save(); ctx.translate(12, (RT + RB) / 2); ctx.rotate(-Math.PI / 2); ctx.textAlign = 'center'; ctx.fillText('pull', 0, 0); ctx.restore();
      // data with error bars
      ctx.strokeStyle = C.data; ctx.globalAlpha = 0.28;
      for (var i = 0; i < n; i += 1) { var px = X(H.x[i]); ctx.beginPath(); ctx.moveTo(px, Y(H.y[i] - H.s[i])); ctx.lineTo(px, Y(H.y[i] + H.s[i])); ctx.stroke(); }
      ctx.globalAlpha = 0.85; ctx.fillStyle = C.data;
      for (var i2 = 0; i2 < n; i2++) { ctx.beginPath(); ctx.arc(X(H.x[i2]), Y(H.y[i2]), 1.8, 0, 6.283); ctx.fill(); }
      ctx.globalAlpha = 1;
      var st = stages[si], prev = stages[Math.max(0, si - 1)];
      var modelAt = function (j) {
        var a = prev.model ? prev.model[j] : NaN, b = st.model ? st.model[j] : NaN;
        if (!st.model) return NaN;
        if (!prev.model) return b;
        return a + (b - a) * prog;
      };
      // newest component, faint, drawn about the axis bottom so its shape reads
      if (st.comp && st.idx > 0) {
        var cmin = Infinity; for (var q = 0; q < n; q++) cmin = Math.min(cmin, st.comp[q]);
        ctx.strokeStyle = C.fit; ctx.globalAlpha = 0.35 * prog; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]); ctx.beginPath();
        for (var q2 = 0; q2 < n; q2++) { var yv = ymin + (st.comp[q2] - cmin) + (ymax - ymin) * 0.03; if (q2) ctx.lineTo(X(H.x[q2]), Y(yv)); else ctx.moveTo(X(H.x[q2]), Y(yv)); }
        ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha = 1;
      }
      // total model
      if (st.model) {
        ctx.save(); ctx.beginPath(); ctx.rect(L, T, R - L, B - T); ctx.clip();
        ctx.strokeStyle = C.fit; ctx.lineWidth = 2.4; ctx.lineJoin = 'round'; ctx.beginPath();
        for (var m = 0; m < n; m++) { var yy2 = Y(modelAt(m)); if (m) ctx.lineTo(X(H.x[m]), yy2); else ctx.moveTo(X(H.x[m]), yy2); }
        ctx.stroke(); ctx.restore();
      }
      // residual pulls, clipped to +-6
      var RM = (RT + RB) / 2, RS = (RB - RT) / 2 / 6;
      ctx.strokeStyle = C.rule; ctx.beginPath(); ctx.moveTo(L, RM + .5); ctx.lineTo(R, RM + .5); ctx.stroke();
      if (st.model) {
        ctx.fillStyle = C.data; ctx.globalAlpha = 0.75;
        for (var p = 0; p < n; p++) {
          var pull = (H.y[p] - modelAt(p)) / H.s[p];
          pull = Math.max(-6, Math.min(6, pull));
          ctx.fillRect(X(H.x[p]) - 1, RM - pull * RS - 1, 2, 2);
        }
        ctx.globalAlpha = 1;
      }
    }
    function readout(si) {
      var st = stages[si];
      if (elStep) elStep.textContent = 'step ' + si + ' of ' + (stages.length - 1);
      if (elComp) elComp.textContent = si === 0 ? '—' : (si === 1 ? 'background' : '+ ' + st.label.replace(/ \d+$/, ''));
      if (elRed) {
        elRed.textContent = si === 0 ? '—' : (st.red >= 100 ? Math.round(st.red) : st.red.toFixed(st.red < 10 ? 2 : 1));
        elRed.className = si === 0 ? '' : (st.red < 1.5 ? 'ok' : 'bad');
      }
      if (elVerdict) {
        elVerdict.textContent = si === 0 ? 'searching' : (st.red < 1.5 ? 'within the noise' : 'structure left');
        elVerdict.className = si > 0 && st.red < 1.5 ? 'ok' : '';
      }
    }
    var DUR = 1100, HOLD = 1500, END = 3600;
    if (reduced) { cur = stages.length - 1; draw(cur, 1); readout(cur); }
    else {
      readout(0);
      var frame = function (now) {
        if (!t0) t0 = now;
        var el = now - t0, hold = cur === stages.length - 1 ? END : HOLD;
        var prog = Math.min(1, el / DUR);
        var e = 1 - Math.pow(1 - prog, 3);
        draw(cur, e);
        if (el > DUR + hold) { cur = (cur + 1) % stages.length; t0 = now; readout(cur); }
        requestAnimationFrame(frame);
      };
      // pause the loop while the hero is off screen
      requestAnimationFrame(frame);
    }
  }

  /* ---------------------------------------------------------------
     Models page
     --------------------------------------------------------------- */
  var ml = $('#mlist');
  if (ml && window.MODELS) {
    var M = window.MODELS; // [group, name, note, expr, auto]
    var groups = {};
    M.forEach(function (m) { groups[m[0]] = (groups[m[0]] || 0) + 1; });
    var order = Object.keys(groups).sort(function (a, b) { return groups[b] - groups[a]; });
    var chips = $('#chips'), active = '', q = '', limit = 60;
    var mk = function (label, count, key) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.setAttribute('aria-pressed', key === active ? 'true' : 'false');
      b.innerHTML = '';
      b.appendChild(document.createTextNode(label + ' '));
      var s = document.createElement('b'); s.textContent = count; b.appendChild(s);
      b.addEventListener('click', function () { active = key; limit = 60; renderChips(); render(); });
      return b;
    };
    var renderChips = function () {
      chips.innerHTML = '';
      chips.appendChild(mk('All', M.length, ''));
      order.forEach(function (g) { chips.appendChild(mk(g, groups[g], g)); });
    };
    var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };
    var render = function () {
      var words = q.toLowerCase().split(/\s+/).filter(Boolean);
      var hits = M.filter(function (m) {
        if (active && m[0] !== active) return false;
        if (!words.length) return true;
        var hay = (m[0] + ' ' + m[1] + ' ' + m[2]).toLowerCase();
        return words.every(function (w) { return hay.indexOf(w) >= 0; });
      });
      $('#mcount').textContent = hits.length + (hits.length === 1 ? ' model' : ' models');
      ml.innerHTML = hits.slice(0, limit).map(function (m) {
        return '<article class="model"><span class="g">' + esc(m[0]) + (m[4] ? '' : '<span class="opt">click-to-use</span>') + '</span>' +
          '<h3>' + esc(m[1]) + '</h3>' + (m[2] ? '<p>' + esc(m[2]) + '</p>' : '') +
          '<code>y = ' + esc(m[3]) + '</code></article>';
      }).join('') || '<p class="muted">No model matches. Email us — custom models are one of the things we build.</p>';
      var more = $('#mmore');
      more.hidden = hits.length <= limit;
      more.textContent = 'Show ' + Math.min(60, hits.length - limit) + ' more of ' + (hits.length - limit) + ' remaining';
    };
    $('#mq').addEventListener('input', function (e) { q = e.target.value; limit = 60; render(); });
    $('#mmore').addEventListener('click', function () { limit += 60; render(); });
    var h = decodeURIComponent((location.hash || '').slice(1));
    if (h && groups[h]) active = h;
    renderChips(); render();
  }

  /* ---------------------------------------------------------------
     Benchmark chart: reduced chi-square before and after, log scale
     --------------------------------------------------------------- */
  var bc = $('#bench-chart');
  if (bc) {
    var rows = JSON.parse(bc.getAttribute('data-rows'));
    var tip = $('#bench-tip');
    var drawChart = function () {
      var C = { ink: css('--ink'), ink2: css('--ink-2'), ink3: css('--ink-3'), grid: css('--grid'), rule: css('--grid-strong'), before: css('--fit'), after: css('--data'), paper: css('--paper'), good: css('--good') };
      var Wd = 760, rowH = 34, top = 30, left = 214, right = 40, Hd = top + rows.length * rowH + 30;
      var lo = Math.log10(0.7), hi = Math.log10(400);
      var X = function (v) { return left + (Math.log10(v) - lo) / (hi - lo) * (Wd - left - right); };
      var s = '<svg viewBox="0 0 ' + Wd + ' ' + Hd + '" role="img" aria-label="Reduced chi-square before and after, per dataset, on a log scale">';
      [1, 3, 10, 30, 100, 300].forEach(function (v) {
        var x = X(v);
        s += '<line x1="' + x + '" x2="' + x + '" y1="' + (top - 8) + '" y2="' + (Hd - 26) + '" stroke="' + (v === 1 ? C.good : C.grid) + '" stroke-width="' + (v === 1 ? 1.5 : 1) + '"' + (v === 1 ? ' stroke-dasharray="4 4"' : '') + '/>';
        s += '<text x="' + x + '" y="' + (Hd - 8) + '" fill="' + C.ink3 + '" font-family="IBM Plex Mono, monospace" font-size="12" text-anchor="middle">' + v + '</text>';
      });
      s += '<text x="' + (X(1) + 6) + '" y="' + (top - 12) + '" fill="' + C.good + '" font-family="Public Sans, sans-serif" font-size="12">χ²/ν = 1: a correct model</text>';
      rows.forEach(function (r, i) {
        var y = top + i * rowH + rowH / 2, xb = X(r[1]), xa = X(r[2]);
        s += '<g class="brow" data-i="' + i + '">';
        s += '<rect x="0" y="' + (y - rowH / 2) + '" width="' + Wd + '" height="' + rowH + '" fill="transparent"/>';
        s += '<text x="0" y="' + (y + 4) + '" fill="' + C.ink2 + '" font-family="Public Sans, sans-serif" font-size="13.5">' + r[0] + '</text>';
        s += '<line x1="' + xa + '" x2="' + xb + '" y1="' + y + '" y2="' + y + '" stroke="' + C.rule + '" stroke-width="2"/>';
        s += '<circle cx="' + xb + '" cy="' + y + '" r="6" fill="' + C.before + '" stroke="' + C.paper + '" stroke-width="2"/>';
        s += '<circle cx="' + xa + '" cy="' + y + '" r="6" fill="' + C.after + '" stroke="' + C.paper + '" stroke-width="2"/>';
        s += '<text x="' + (xb + 11) + '" y="' + (y + 4) + '" fill="' + C.ink2 + '" font-family="IBM Plex Mono, monospace" font-size="12">' + r[1] + '</text>';
        s += '</g>';
      });
      s += '</svg>';
      bc.innerHTML = s;
      bc.querySelectorAll('.brow').forEach(function (g) {
        g.addEventListener('pointermove', function (ev) {
          var r = rows[+g.getAttribute('data-i')], box = bc.getBoundingClientRect();
          tip.innerHTML = '<b>' + r[0] + '</b><br>before ' + r[1] + ' &nbsp;→&nbsp; now ' + r[2];
          tip.hidden = false;
          var x = ev.clientX - box.left + bc.scrollLeft + 14, y = ev.clientY - box.top - 10;
          tip.style.left = Math.min(x, box.width - 190) + 'px'; tip.style.top = y + 'px';
        });
        g.addEventListener('pointerleave', function () { tip.hidden = true; });
      });
    };
    drawChart();
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      if (mq.addEventListener) mq.addEventListener('change', drawChart);
    }
    new MutationObserver(drawChart).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }
})();
