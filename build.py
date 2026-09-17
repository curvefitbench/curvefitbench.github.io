#!/usr/bin/env python3
"""Generate the Curve Fit Bench website: one shared header/footer, seven pages."""
import os, html, json

EMAIL = 'puhansatyajit@gmail.com'
REPO = 'https://github.com/satyajitpuhan/curve-fit-bench'
SPONSOR = 'https://github.com/sponsors/satyajitpuhan'
SITE = 'https://satyajitpuhan.github.io/fitbench/'
_mjs = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'models.js'), encoding='utf-8').read()
N_MODELS = len(json.loads(_mjs[_mjs.index('=') + 1:].rstrip().rstrip(';')))

def mail(subject, body=''):
    from urllib.parse import quote
    q = 'mailto:' + EMAIL + '?subject=' + quote(subject)
    if body:
        q += '&body=' + quote(body)
    return html.escape(q, quote=True)

NAV = [('index.html', 'Home'), ('features.html', 'Features'), ('models.html', 'Models'),
       ('benchmark.html', 'Benchmark'), ('docs.html', 'Docs'), ('about.html', 'About')]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800'
         '&family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:wght@400;500;600;650&display=swap">')

def head(page, title, desc):
    full = title if page == 'index.html' else title + ' · Curve Fit Bench'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="canonical" href="{SITE}{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}assets/img/complex-fit.png">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
'''

def header(page):
    links = ''.join(
        '<a href="' + href + '"' + (' aria-current="page"' if href == page else '') + '>' + label + '</a>' for href, label in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/logo.svg" alt="">Curve Fit Bench</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {links}
      <a class="plans" href="plans.html"{' aria-current="page"' if page == 'plans.html' else ''}>Plans &amp; licensing</a>
      <a class="btn btn-primary btn-sm" href="app/">Launch the bench</a>
    </nav>
  </div>
</header>
<main id="main">
'''

FOOTER = f'''</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/logo.svg" alt="">Curve Fit Bench</a>
        <p style="margin-top:12px;max-width:40ch">Least-squares curve fitting for physicists and materials scientists. Runs in your browser; your data never leaves your computer.</p>
      </div>
      <div><h4>Product</h4><a href="app/">Launch the bench</a><a href="features.html">Features</a><a href="models.html">Model library</a><a href="benchmark.html">Benchmark</a></div>
      <div><h4>Learn</h4><a href="docs.html">Documentation</a><a href="assets/curve-fit-bench-manual.pdf">Manual (PDF)</a><a href="about.html#cite">How to cite</a><a href="{REPO}">Source on GitHub</a></div>
      <div><h4>Work with us</h4><a href="plans.html">Plans &amp; licensing</a><a href="plans.html#sponsor">Sponsor development</a><a href="{mail('Curve Fit Bench - custom model')}">Request a model</a><a href="about.html">About the authors</a></div>
    </div>
    <div class="foot-legal">
      <span>© 2026 Shivani Malvi &amp; Satyajit Puhan. Free to use for research and teaching; modification and redistribution need written permission (<a href="{REPO}/blob/main/LICENSE">licence</a>).</span>
      <span><a href="mailto:{EMAIL}">{EMAIL}</a></span>
    </div>
  </div>
</footer>
'''

def page(name, title, desc, body, scripts=''):
    return head(name, title, desc) + header(name) + body + FOOTER + '<script src="assets/site.js" defer></script>\n' if not scripts else \
           head(name, title, desc) + header(name) + body + FOOTER + scripts + '<script src="assets/site.js" defer></script>\n'

def close(s):
    return s + '</body>\n</html>\n'

_M0 = mail('Curve Fit Bench - custom model', 'Model name / equation:\n\nWhat x and y are:\n\nA sample dataset (optional):\n')
_M1 = mail('Curve Fit Bench - lab licence', 'Group / institution:\n\nNumber of users:\n\nInstruments or file formats:\n\nModels you would like added:\n')
_M2 = mail('Curve Fit Bench - commercial licence', 'Company:\n\nHow you would like to use the bench:\n\nTimeline:\n')
_M3 = mail('Curve Fit Bench - custom work', 'What you need:\n\nDeadline:\n')

CTA_BAND = f'''<section class="band cta-band">
  <div class="wrap">
    <div>
      <span class="eyebrow">Keep it free for students</span>
      <h2>Your lab uses it. Help keep it growing.</h2>
      <p class="lead">Curve Fit Bench is built by two early-career physicists. Licences, sponsorship and custom work pay for new models, verification and support — and keep the bench free for every student who needs it.</p>
      <div class="btn-row" style="margin-top:24px">
        <a class="btn btn-primary" href="plans.html">See plans &amp; licensing</a>
        <a class="btn btn-ghost" href="{mail('Curve Fit Bench - quote request')}">Request a quote</a>
      </div>
    </div>
    <div class="offer-list">
      <div><h3>Lab licence</h3><p>Priority model requests, your file formats, email support.</p></div>
      <div><h3>Commercial &amp; OEM</h3><p>Embed, modify or host the bench in your product or instrument.</p></div>
      <div><h3>Custom models</h3><p>The model your analysis needs, verified like the rest of the library.</p></div>
      <div><h3>Workshops</h3><p>A hands-on fitting and statistics session for your department.</p></div>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- home
HOME = f'''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Curve fitting for physicists</span>
      <h1>Fit the curve <span class="fit">nobody wrote down.</span></h1>
      <p class="lead">Drop in x, y and σ. Curve Fit Bench searches {N_MODELS} physical models, and when none of them describes your data it builds the model itself, piece by piece, until what is left is noise. You get the formula, every parameter with its uncertainty, and χ².</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="app/">Launch the bench — free</a>
        <a class="btn btn-ghost" href="plans.html">Licences for labs &amp; companies</a>
      </div>
      <p class="fine">Runs in the browser · nothing to install · data never leaves your computer</p>
    </div>
    <figure class="scope" style="margin:0" aria-label="Animation: a model being built for a complex dataset, one component at a time">
      <div class="scope-bar"><b>hard_composite.csv</b> · 450 points with σ <span class="step" id="scope-step">step 0</span></div>
      <canvas id="scope" width="720" height="475"></canvas>
      <div class="scope-read">
        <div>component<b id="scope-comp">—</b></div>
        <div>reduced χ²<b id="scope-red">—</b></div>
        <div>verdict<b id="scope-verdict">searching</b></div>
      </div>
    </figure>
  </div>
</section>

<div class="strip">
  <div class="wrap">
    <div><b>{N_MODELS}</b><span>named physical models</span></div>
    <div><b>994 / 1000</b><span>complex test spectra fitted within the noise</span></div>
    <div><b>~1 s</b><span>median time to build a model</span></div>
    <div><b>0</b><span>installs, accounts or uploads</span></div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Why it exists</span>
      <h2>Most fitting tools answer the question you already knew.</h2>
      <p>You pick a model, the software fits it, and a small χ² tells you nothing about whether the model was the right one. Curve Fit Bench starts from the data instead.</p>
    </div>
    <div class="grid-3">
      <div class="pa stack"><div><span class="k no">Usually</span><p>You guess a Lorentzian, it fits “well enough”, and the shoulder on the left is quietly absorbed into the background.</p></div><div><span class="k yes">Here</span><p>Every model family competes, extra parameters must earn their place by BIC and an F-test, and the residuals are tested for leftover structure.</p></div></div>
      <div class="pa stack"><div><span class="k no">Usually</span><p>Real spectra — bands on a curved background, a step with a dip, oscillations on a power law — match no textbook form, so the fit is the least bad wrong answer.</p></div><div><span class="k yes">Here</span><p>Adaptive decomposition adds peaks, Fano lines, steps and chirped oscillations where the residual demands them, and stops at the noise.</p></div></div>
      <div class="pa stack"><div><span class="k no">Usually</span><p>One χ² for the whole curve hides the region the model misses, and the parameter errors say nothing about what the data actually constrain.</p></div><div><span class="k yes">Here</span><p>The fit is judged region by region, and the parameter explorer shows how each value moves the curve against your points.</p></div></div>
    </div>
  </div>
</section>

<section class="paper">
  <div class="wrap">
    <div class="feature">
      <div class="txt">
        <span class="eyebrow">Adaptive decomposition</span>
        <h3>When no textbook model fits, it builds one.</h3>
        <p>At a conference demo, ten deliberately hard datasets broke every named model — reduced χ² from 3 to 217. The same ten now land between 0.93 and 1.21, and on 1000 random complex spectra with known truth, 999 fits sit closer to the true curve than the noise itself.</p>
        <ul class="ticks">
          <li>Components kept only on strong BIC evidence, never for a one-point gain</li>
          <li>Tried in x, ln x or 1/x against y or ln y — a log-periodic power law becomes simple</li>
          <li>Every component drawn, every parameter with an error bar</li>
        </ul>
        <p style="margin-top:18px"><a href="benchmark.html">Read the benchmark →</a></p>
      </div>
      <img class="shot" src="assets/img/complex-fit.png" alt="The hardest benchmark dataset fitted, with its components drawn and residuals that scatter randomly about zero" loading="lazy">
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Built for the bench, not the brochure</span>
      <h2>Everything a results section needs.</h2>
    </div>
    <div class="grid-3">
      <div class="card"><span class="tag">Library</span><h3>{N_MODELS} named models</h3><p>BCS gap and superfluid density, WHH H<sub>c2</sub>, Bloch–Grüneisen and Debye integrals, Lifshitz–Kosevich, BTK, Fano, Tauc–Urbach, Havriliak–Negami and many more.</p></div>
      <div class="card"><span class="tag">Honest statistics</span><h3>Says when nothing fits</h3><p>Noise measured from your data, runs test on residuals, fit quality per region, and physical bounds so a linewidth never goes negative.</p></div>
      <div class="card"><span class="tag">Your equations</span><h3>Type any model</h3><p><code>A*exp(-x/tau) + c ; tau&gt;0</code> — 65 functions, bounds, fixed parameters, and several equations compared side by side.</p></div>
      <div class="card"><span class="tag">Explorer</span><h3>See what the data constrain</h3><p>Sweep any fitted parameter over several values and watch χ²/ν change, in a second plot with its own editor.</p></div>
      <div class="card"><span class="tag">Figures</span><h3>Origin-style plot editing</h3><p>Stats box on the plot, axis ranges, mirrored ticks, fonts and colours; PNG and PDF at 3× resolution.</p></div>
      <div class="card"><span class="tag">Private</span><h3>Nothing is uploaded</h3><p>The whole bench is a single page that runs on your computer — usable on confidential and pre-publication data.</p></div>
    </div>
  </div>
</section>

{CTA_BAND}
'''

# ---------------------------------------------------------------- features
FEATURES = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Features</span>
    <h1>From a CSV to a publishable fit.</h1>
    <p class="lead">Paste two or three columns, press nothing, and read the answer: the best functional form, parameters with uncertainties, χ² and whether the residuals are really noise.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="feature">
      <div class="txt">
        <span class="eyebrow">Automatic search</span>
        <h3>Every family competes, fairly.</h3>
        <p>Polynomials, power laws, exponentials, peaks, periodic forms, sums of two components, a symbolic dictionary search and the physics library are all fitted with Levenberg–Marquardt in y-space. The ranking charges searched forms for having been picked, and the headline goes to the simplest model the best one does not significantly beat.</p>
        <ul class="ticks"><li>Weighted χ² when σ is given, relative weighting when y spans decades</li><li>BIC, AICc and an F-test parsimony rule</li><li>Outlier rejection with Tukey biweights</li></ul>
      </div>
      <img class="shot" src="assets/img/ranking.png" alt="Ranking table of every model tried with reduced chi-square, R squared and AICc" loading="lazy">
    </div>
    <div class="feature flip">
      <div class="txt">
        <span class="eyebrow">Adaptive decomposition</span>
        <h3>A model built from the residual.</h3>
        <p>When nothing comes within the noise, the bench starts from a polynomial background and adds the component that best explains the largest structure still left — a Gaussian, Lorentzian or Fano band, a step, a kink, a damped or chirped oscillation or a wave packet — refits everything together, and keeps it only if the evidence is strong.</p>
        <ul class="ticks"><li>Components drawn separately on the plot</li><li>Parameters in your own units with error bars</li><li>Explorer and export work on it like any other model</li></ul>
      </div>
      <img class="shot" src="assets/img/complex-result.png" alt="Result card for an adaptive decomposition: formula, parameters with uncertainties and region-by-region fit quality" loading="lazy">
    </div>
    <div class="feature">
      <div class="txt">
        <span class="eyebrow">Fit quality by region</span>
        <h3>A good χ² can hide a bad region.</h3>
        <p>The x range is split into up to ten parts with equal numbers of points, each with its own χ²/N or noise-normalised miss, coloured green, orange or red. The runs test flags residuals that arrive in long same-sign stretches — the signature of a missing term.</p>
      </div>
      <img class="shot" src="assets/img/result.png" alt="Result card with parameters, chi-square statistics and a verdict" loading="lazy">
    </div>
    <div class="feature flip">
      <div class="txt">
        <span class="eyebrow">Parameter explorer</span>
        <h3>What does each number really do?</h3>
        <p>Choose a fitted parameter and give it a list of values — ×0.5 to ×2, a range, or exact numbers. Every other parameter stays at its fitted value, each curve gets its own χ²/ν, and the explorer plot has its own editor: title, fonts, viridis or plasma schemes, dashed curves, limits, ticks and a legend that can carry χ²/ν.</p>
      </div>
      <img class="shot" src="assets/img/explorer-editor.png" alt="Parameter explorer with its plot editor open and five curves in a viridis colour scheme" loading="lazy">
    </div>
    <div class="feature">
      <div class="txt">
        <span class="eyebrow">Figures</span>
        <h3>Ready for the paper.</h3>
        <p>Put χ², χ²/ν, R² and the parameters in a box on the plot, set ranges and tick steps, point ticks inward and mirror them, pick fonts and colours, overlay up to four models or show only the one you selected, then save PNG or PDF at three times screen resolution.</p>
      </div>
      <img class="shot" src="assets/img/editor.png" alt="Plot editor with results box, mirrored ticks and a title" loading="lazy">
    </div>
  </div>
</section>
{CTA_BAND}
'''

# ---------------------------------------------------------------- models
MODELS = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Model library</span>
    <h1>{N_MODELS} models, written by physicists.</h1>
    <p class="lead">Each one carries starting values read from your data and, where physics demands it, bounds. Numerical models — the BCS gap equation, Bloch–Grüneisen and Debye integrals, WHH, Callaway — are solved properly rather than approximated.</p>
  </div>
</section>
<section style="padding-top:clamp(28px,4vw,44px)">
  <div class="wrap">
    <div class="filters">
      <label class="search" for="mq"><span class="muted" aria-hidden="true">⌕</span><input id="mq" type="search" placeholder="Search: BCS, Fano, Urbach, hopping, Curie…" autocomplete="off"></label>
      <span class="count" id="mcount" aria-live="polite"></span>
    </div>
    <div class="chips" id="chips" aria-label="Filter by subject"></div>
    <div class="mlist" id="mlist"></div>
    <div class="more-row"><button class="btn btn-ghost" id="mmore" type="button" hidden>Show more</button></div>
    <div class="callout" style="margin-top:36px"><p><b>Missing the model your analysis needs?</b> We write custom models and verify them on synthetic data the same way as the library. <a href="{_M0}">Request a model</a> or see <a href="plans.html">plans</a>.</p></div>
  </div>
</section>
'''

# ---------------------------------------------------------------- benchmark
BENCH_ROWS = [["Multi-scale resonance", 5.71, 1.04], ["Two overlapping resonances", 5.43, 0.96],
              ["Threshold cusp + oscillations", 8.21, 1.18], ["Log-periodic power law", 217, 1.10],
              ["Fano interference", 36.9, 1.13], ["Damped chirp", 4.68, 0.93], ["Double sigmoid + dip", 4.04, 0.97],
              ["Broad peak + narrow spike", 3.35, 1.21], ["Rational crossover + ripple", 43.6, 1.04], ["Hard composite", 5.07, 1.05]]
rows_html = ''.join(f'<tr><td>{r[0]}</td><td class="n bad">{r[1]}</td><td class="n ok">{r[2]:.2f}</td></tr>' for r in BENCH_ROWS)
BENCH = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Benchmark</span>
    <h1>Tested where fitting tools fail.</h1>
    <p class="lead">Ten deliberately hard datasets from a live conference demo, then a thousand random complex spectra with known truth. A correct model gives a reduced χ² near 1 and a curve closer to the truth than the noise.</p>
  </div>
</section>
<section style="padding-top:clamp(32px,5vw,56px)">
  <div class="wrap">
    <div class="kpis">
      <div class="kpi"><b>994 / 1000</b><span>random complex spectra fitted within the noise (χ²/ν &lt; 1.5); 964 below 1.25</span></div>
      <div class="kpi"><b>999 / 1000</b><span>fits closer to the true noiseless curve than the noise itself</span></div>
      <div class="kpi"><b>1.0 s</b><span>median time to build the model; 90 % within 5 s</span></div>
    </div>
  </div>
</section>
<section class="paper">
  <div class="wrap" style="display:grid;gap:24px">
    <div class="chartcard">
      <h3>Ten hard datasets: best reduced χ²</h3>
      <p class="sub">Before and after adaptive decomposition, log scale. Hover a row for values.</p>
      <div class="legend"><span><i style="background:var(--fit)"></i>Before</span><span><i style="background:var(--data)"></i>Now</span></div>
      <div class="chart-wrap"><div id="bench-chart" data-rows='{json.dumps(BENCH_ROWS)}'></div><div class="tip" id="bench-tip" hidden></div></div>
    </div>
    <div class="chartcard">
      <h3>The same results as a table</h3>
      <p class="sub">Each dataset has σ<sub>y</sub>; the noiseless truth was never shown to the fitter.</p>
      <div class="tbl-wrap"><table class="data"><thead><tr><th>Dataset</th><th class="n">Before</th><th class="n">Now</th></tr></thead><tbody>{rows_html}</tbody></table></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap narrow">
    <div class="sec-head" style="margin-bottom:20px">
      <span class="eyebrow">Method</span>
      <h2>How the 1000 spectra were made</h2>
    </div>
    <div class="prose">
      <p>Each synthetic spectrum stacks 2 to 6 features — Lorentzian, Gaussian, Voigt and Fano bands, dips, steps, cusps, damped and chirped oscillations, wave packets, Shubnikov–de Haas oscillations periodic in 1/x and log-periodic terms — on a linear, quadratic, exponential, power-law, activated or logarithmic background. Grids are linear or logarithmic with 120 to 900 points; noise is 0.4–4 % of the range, constant or growing along x; 61 % of the spectra carry σ and the rest do not.</p>
      <p>Two numbers are scored against the known truth: the reduced χ² of the fit to the noisy data, and the RMS distance between the fitted curve and the noiseless curve in units of σ. Below 1 means the fit recovered the underlying function better than any single measurement could.</p>
      <div class="callout"><p><b>What it is and is not.</b> An adaptive decomposition is an accurate description of the data — positions, widths, frequencies and a curve you can trust — not an identification of the physics. When you know the mechanism, fit the named model for it; the bench shows both.</p></div>
    </div>
  </div>
</section>
{CTA_BAND}
'''

# ---------------------------------------------------------------- docs
DOCS = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Documentation</span>
    <h1>Using the bench.</h1>
    <p class="lead">Everything you need for a first fit in five minutes. The full manual, with every model in the library, is a <a href="assets/curve-fit-bench-manual.pdf">162-page PDF</a>.</p>
  </div>
</section>
<section>
  <div class="wrap doc">
    <nav class="toc" aria-label="On this page">
      <a href="#start">Quick start</a><a href="#data">Data format</a><a href="#modes">Fitting modes</a><a href="#equations">Writing equations</a><a href="#reading">Reading the result</a><a href="#adaptive">Adaptive decomposition</a><a href="#explorer">Parameter explorer</a><a href="#export">Figures &amp; export</a><a href="#cite">Citing</a>
    </nav>
    <div class="prose">
      <h2 id="start">Quick start</h2>
      <ol>
        <li>Open <a href="app/">the bench</a>. It loads with a sample dataset already fitted.</li>
        <li>Drop your CSV or TXT file on the data panel, or paste x&nbsp;y pairs, one per line.</li>
        <li>Read the best fit: the formula, parameters with uncertainties, reduced χ² and the region strip. Click any row in the ranking to see another model.</li>
      </ol>
      <h2 id="data">Data format</h2>
      <p>Two columns are x and y. A third column is read as the uncertainty σ<sub>y</sub> — the bench asks before assuming — and a header row names the axes. Commas, tabs and spaces all work, and instrument files with a few text lines at the top are handled.</p>
<pre class="code"><span class="c"># temperature (K), resistivity (µΩ cm), sigma</span>
T, rho, sigma
2.0, 1.842, 0.004
4.0, 1.843, 0.004
6.0, 1.847, 0.004</pre>
      <h2 id="modes">Fitting modes</h2>
      <p><b>Best form</b> searches every enabled family and ranks them. <b>My equations</b> fits only what you type, and still shows the automatic pick as a dashed comparison. Under <i>Model families</i> you can switch groups on and off — the materials-science library is off by default.</p>
      <h2 id="equations">Writing equations</h2>
      <p>Every letter that is not <code>x</code> becomes a parameter. After a semicolon give starting values, bounds and fixed values:</p>
<pre class="code">A*exp(-x/tau) + c ; A=2, tau=5, tau&gt;0
<span class="c"># fixed parameter with !</span>
rho0 + a*x^n ; n=2, !rho0=1.84
<span class="c"># several equations, one per line, are fitted and compared</span>
A/(1+((x-x0)/g)^2) + b ; g&gt;0</pre>
      <p>Functions include <code>exp log sqrt sin cos tanh erf erfc gamma voigt digamma brillouin lambertw</code> and more — 65 in all.</p>
      <h2 id="reading">Reading the result</h2>
      <p><b>Reduced χ²</b> (χ²/ν) is near 1 for a correct model when σ is given. Without σ, look at the <i>misfit</i>: how far the curve sits from the points in units of the point-to-point noise. The <b>runs z</b> flags residuals in long same-sign stretches, and the <b>by region</b> strip shows χ²/N in up to ten parts of the x range.</p>
      <div class="callout"><p>A green headline with an orange or red region means the model is right on average and wrong somewhere specific — look there first.</p></div>
      <h2 id="adaptive">Adaptive decomposition</h2>
      <p>It runs only when nothing else comes within the noise. The result is listed as <i>Adaptive decomposition: …</i> with its components; switch on <b>components</b> to draw them. Use it to read positions, widths and frequencies, then fit the named model that matches your mechanism. The <b>Best named physics model</b> card always shows the best library model alongside.</p>
      <h2 id="explorer">Parameter explorer</h2>
      <p>Below the ranking, pick a parameter, choose multiples of the fitted value or absolute values (<code>0.5, 1, 2</code> or <code>from:to:count</code>) and compare curves and χ²/ν. <b>Edit this plot</b> opens its own styling panel.</p>
      <h2 id="export">Figures &amp; export</h2>
      <p><b>Edit plot</b> controls titles, ranges, ticks, fonts, colours and the statistics box. <b>Only selected curve</b> hides everything but the model chosen in the ranking. PNG and PDF save at 3× resolution; <b>copy fitted y</b> puts the curve on your clipboard.</p>
      <h2 id="cite">Citing</h2>
      <p>If the bench helped your work, please cite it — citations are how we justify the time to keep improving it. See <a href="about.html#cite">About</a> for BibTeX.</p>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- plans
PLANS = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Plans &amp; licensing</span>
    <h1>Free for science. Licensed for scale.</h1>
    <p class="lead">Students and researchers use Curve Fit Bench free, forever. Labs, facilities and companies that need more — support, custom models, or the right to build on it — keep the project alive.</p>
  </div>
</section>
<section style="padding-top:clamp(32px,5vw,56px)">
  <div class="wrap">
    <div class="plans">
      <div class="plan">
        <span class="who">Students &amp; researchers</span>
        <h3>Free</h3>
        <div class="price">₹0 <small>forever</small></div>
        <p>The complete bench for personal, academic and teaching use.</p>
        <ul><li>Every model and the adaptive decomposition</li><li>Explorer, plot editor, PNG &amp; PDF export</li><li>Use results in papers and theses, with citation</li><li>Community help through GitHub issues</li></ul>
        <a class="btn btn-ghost" href="app/">Launch the bench</a>
      </div>
      <div class="plan feat">
        <span class="ribbon">Most requested</span>
        <span class="who">Research groups &amp; facilities</span>
        <h3>Lab licence</h3>
        <div class="price">Annual <small>quoted per group</small></div>
        <p>For groups that fit data every week and want it to fit their workflow.</p>
        <ul><li>Priority model requests for your group</li><li>Readers for your instruments' file formats</li><li>A lab-branded offline copy for your group</li><li>Direct email support</li><li>Your group acknowledged as a supporter</li></ul>
        <a class="btn btn-primary" href="{_M1}">Request a quote</a>
      </div>
      <div class="plan">
        <span class="who">Companies &amp; instrument makers</span>
        <h3>Commercial</h3>
        <div class="price">Custom <small>quoted per product</small></div>
        <p>The free licence forbids modifying, embedding or hosting the bench. This one allows it.</p>
        <ul><li>Modify and embed in your software or instrument</li><li>Host for your customers, white-label option</li><li>Integration help and a maintenance contract</li><li>Commercial use of results without restriction</li></ul>
        <a class="btn btn-ink" href="{_M2}">Talk to us</a>
      </div>
      <div class="plan">
        <span class="who">Any analysis</span>
        <h3>Custom work</h3>
        <div class="price">Per project <small>scoped with you</small></div>
        <p>A model, a dataset or a workshop, scoped to what you need.</p>
        <ul><li>New physical models, verified on synthetic data</li><li>Fitting and statistics consultation on your data</li><li>Half- or full-day workshops for departments</li><li>Course versions with your own sample sets</li></ul>
        <a class="btn btn-ghost" href="{_M3}">Describe your project</a>
      </div>
    </div>
    <p class="muted" style="margin-top:18px;font-size:14.5px">Prices are quoted in INR, USD or EUR to suit your institution, and invoices can be issued for grant or purchase-order payment.</p>
  </div>
</section>

<section class="band" id="sponsor">
  <div class="wrap grid-2" style="align-items:center">
    <div>
      <span class="eyebrow">Sponsor development</span>
      <h2 style="font-size:clamp(30px,4vw,46px);line-height:1.08;margin:12px 0 14px">Not buying a licence? Sponsor the next model.</h2>
      <p class="lead">A monthly sponsorship, of any size, directly funds new models, verification against synthetic data and keeping the bench free for students. Institutional sponsors are listed on this site and in the app.</p>
    </div>
    <div class="btn-row" style="justify-content:flex-start">
      <a class="btn btn-primary" href="{SPONSOR}">Sponsor on GitHub</a>
      <a class="btn btn-ghost" href="{mail('Curve Fit Bench - institutional sponsorship')}">Institutional sponsorship</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <div class="sec-head" style="margin-bottom:22px"><span class="eyebrow">Questions</span><h2>Before you write to us</h2></div>
    <div class="faq">
      <details><summary>Is the free version limited in any way?</summary><p>No. The free bench has every model, the adaptive decomposition, the explorer and export. Paid plans add support, custom work and rights the free licence does not grant — not features taken away from the free one.</p></details>
      <details><summary>Can I publish results obtained with the free version?</summary><p>Yes — in papers, theses and reports. Please cite Curve Fit Bench; see <a href="about.html#cite">how to cite</a>.</p></details>
      <details><summary>Our company wants to use it internally. Do we need a licence?</summary><p>Using the unmodified bench to analyse your own data is allowed. You need a commercial licence to modify it, build it into a product or instrument, host it for others or sell it.</p></details>
      <details><summary>Does any of our data reach you?</summary><p>No. The bench runs entirely in the browser; nothing is uploaded, with any plan. For custom work you choose what to share.</p></details>
      <details><summary>How long does a custom model take?</summary><p>It depends on the model: a closed-form expression is quick, a model that needs its own numerical solver takes longer. Every quote includes a timeline, and every model is verified on synthetic data with known parameters before delivery.</p></details>
      <details><summary>Can we pay from a grant or with a purchase order?</summary><p>Yes. We issue quotes and invoices suitable for grant accounts and institutional purchase orders.</p></details>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- about
BIB = '''@software{malvi_puhan_curvefitbench_2026,
  author = {Malvi, Shivani and Puhan, Satyajit},
  title  = {Curve Fit Bench: least-squares curve fitting with automatic model selection},
  year   = {2026},
  url    = {https://github.com/satyajitpuhan/curve-fit-bench}
}'''
ABOUT = f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">About</span>
    <h1>Made by physicists who fit data every day.</h1>
    <p class="lead">Curve Fit Bench began as a question in a lab: why does every fit start with a guess? It grew into a tool that lets the data choose — and, when no known model is right, builds one.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid-2">
      <div class="person"><span class="role">Idea &amp; first developer</span><h3>Shivani Malvi</h3><p>PhD scholar, UGC-DAE Consortium for Scientific Research, Indore, India.</p></div>
      <div class="person"><span class="role">Developer</span><h3>Satyajit Puhan</h3><p>Postdoctoral researcher, Institute of Physics, Academia Sinica, Taipei, Taiwan. <a href="https://satyajitpuhan.github.io/">Personal website</a></p></div>
    </div>
  </div>
</section>
<section class="paper" id="cite">
  <div class="wrap grid-2" style="align-items:start">
    <div>
      <span class="eyebrow">How to cite</span>
      <h2 style="font-size:clamp(28px,3.6vw,40px);margin:12px 0 12px">If it helped, cite it.</h2>
      <p style="color:var(--ink-2)">Citations are what let two early-career researchers justify the hours that go into new models and verification. A line in your methods section makes a real difference.</p>
      <div class="cite" style="margin-top:16px"><pre id="cite-plain">S. Malvi and S. Puhan, Curve Fit Bench (2026). https://github.com/satyajitpuhan/curve-fit-bench</pre><button class="btn btn-ghost btn-sm" type="button" data-copy="#cite-plain">Copy citation</button></div>
    </div>
    <div class="cite"><pre id="cite-bib">{html.escape(BIB)}</pre><button class="btn btn-ghost btn-sm" type="button" data-copy="#cite-bib">Copy BibTeX</button></div>
  </div>
</section>
<section>
  <div class="wrap grid-2" style="align-items:start">
    <div>
      <span class="eyebrow">Contact</span>
      <h2 style="font-size:clamp(28px,3.6vw,40px);margin:12px 0 12px">Talk to us.</h2>
      <p style="color:var(--ink-2)">Licences, custom models, workshops, bug reports or a dataset that beats the bench — we read everything.</p>
      <div class="btn-row" style="margin-top:18px"><a class="btn btn-primary" href="mailto:{EMAIL}">{EMAIL}</a><a class="btn btn-ghost" href="{REPO}/issues">GitHub issues</a></div>
    </div>
    <div class="card">
      <h3>Licence in one paragraph</h3>
      <p>Free to use, download unmodified copies of and publish results from, with citation. Modifying, redistributing, hosting or selling the bench needs written permission — which is what the <a href="plans.html">commercial licence</a> provides.</p>
    </div>
  </div>
</section>
'''

PAGES = [
    ('index.html', 'Curve Fit Bench — curve fitting for physicists', f'Free in-browser least-squares fitting with {N_MODELS} physical models and adaptive decomposition for complex data. By Shivani Malvi and Satyajit Puhan.', HOME, '<script src="assets/hero-data.js" defer></script>\n'),
    ('features.html', 'Features', 'Automatic model search, adaptive decomposition, fit quality by region, parameter explorer and publication figures.', FEATURES, ''),
    ('models.html', 'Model library', f'Search all {N_MODELS} physical models in Curve Fit Bench.', MODELS, '<script src="assets/models.js" defer></script>\n'),
    ('benchmark.html', 'Benchmark', 'Ten hard datasets and 1000 random complex spectra with known truth.', BENCH, ''),
    ('docs.html', 'Documentation', 'Quick start, data format, equations and how to read a Curve Fit Bench result.', DOCS, ''),
    ('plans.html', 'Plans & licensing', 'Free for students and researchers; lab, commercial and custom-work licences for groups and companies.', PLANS, ''),
    ('about.html', 'About', 'The authors, how to cite Curve Fit Bench, and how to contact us.', ABOUT, ''),
]

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    for name, title, desc, body, scripts in PAGES:
        open(os.path.join(here, name), 'w', encoding='utf-8').write(close(page(name, title, desc, body, scripts)))
    open(os.path.join(here, '.nojekyll'), 'w').write('')
    print('built', len(PAGES), 'pages')
