"""Shared building blocks: site settings, icons, <head>, header, footer, page shell."""
import json
import re
from html import escape
from pathlib import Path

# ---------------------------------------------------------------------------
# Site settings: change these once and rebuild (python _dev/build.py)
# ---------------------------------------------------------------------------
BRAND = "Site to Scale"
DOMAIN = "https://sitetoscale.in"        # your final domain, no trailing slash
EMAIL = "projectnest20@gmail.com"
INSTAGRAM = "https://www.instagram.com/"  # your profile URL
GBP_URL = ""                              # Google Business Profile URL once live
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbxQ-VYTuXCd4So8m5C9oxdv8knOl9UM2TTU7mVE-JDnd9IRsF2YQGwMwmy_LZlyvydFSw/exec"  # Apps Script Web App URL that logs quote-form leads to a Sheet — see _dev/leads-apps-script.gs
CITIES = ["Coimbatore", "Tiruppur"]

# Fraunces is split into its own request with display=optional: it's the large display/heading
# font, and swapping it in late reflows the hero heading enough to shift everything below it
# (measured ~0.12 CLS). display=optional means the browser only uses it if it's already cached
# by the time layout starts, so there's no later swap-triggered reflow; worst case a first-time
# visitor sees the fallback serif for that one load, and gets Fraunces on every visit after.
FONTS_DISPLAY = "https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,600;0,700;1,500;1,600&display=optional"
FONTS = ("https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700"
         "&family=IBM+Plex+Mono:wght@400;500&family=Caveat:wght@600;700&display=swap")

BASE_CSS = ["base/tokens.css", "base/reset.css", "base/typography.css",
            "layout/layout.css", "layout/header.css", "layout/footer.css",
            "components/buttons.css", "components/animations.css", "components/cta.css"]
BASE_JS = ["main.js", "reveal.js"]

# ---------------------------------------------------------------------------
# CSS is inlined (not linked) so first paint never waits on a second request.
# On a high-latency mobile connection, one extra round trip for an external
# stylesheet costs more than the CSS itself does, so every file is combined
# and minified once at import time and dropped straight into <head> as
# <style>. Source files stay split under assets/css/ for editing.
# ---------------------------------------------------------------------------
CSS_BUNDLE = [
    "base/tokens.css", "base/reset.css", "base/typography.css",
    "layout/layout.css", "layout/header.css", "layout/footer.css",
    "components/buttons.css", "components/animations.css", "components/cta.css",
    "components/weave.css", "components/marquee.css", "components/service-list.css",
    "components/process.css", "components/faq.css", "components/forms.css",
    "pages/home.css", "pages/service.css", "pages/pricing.css", "pages/city.css",
    "pages/work.css", "pages/about.css", "pages/contact.css", "pages/blog.css",
    "pages/legal.css",
]
_ASSETS_CSS = Path(__file__).resolve().parent.parent / "assets" / "css"


def _minify_css(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,])\s*", r"\1", text)
    text = re.sub(r";}", "}", text)
    return text.strip()


INLINE_CSS = "".join(_minify_css((_ASSETS_CSS / f).read_text(encoding="utf-8")) for f in CSS_BUNDLE)

# ---------------------------------------------------------------------------
# Icons (inline SVG, inherit currentColor where possible)
# ---------------------------------------------------------------------------
ICON = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>',
    "needle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "caret": '<svg class="nav__caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
    "mail": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#F0E3CC"/><rect x="13" y="16" width="22" height="16" rx="3" fill="none" stroke="#B8572B" stroke-width="2.4"/><path d="M14 18l10 7 10-7" fill="none" stroke="#B8572B" stroke-width="2.4"/></svg>',
    "glyph": '<svg viewBox="0 0 28 28" aria-hidden="true"><g stroke-width="4" stroke-linecap="round" fill="none"><path d="M9 3v22M19 3v22" stroke="#2B241C"/><path d="M3 9h22" stroke="#D9713F"/><path d="M3 19h22" stroke="#B8572B"/><path d="M9 5v8M19 15v8" stroke="#2B241C"/></g></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/><path d="M12 3c2.5 2.5 2.5 15.5 0 18M12 3c-2.5 2.5-2.5 15.5 0 18"/></svg>',
    # Generic stroke icons for "fit"/"values" style benefit cards across the site.
    "briefcase": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="3" y1="13" x2="21" y2="13"/></svg>',
    "store": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l1.5-5h15L21 9"/><rect x="4" y="9" width="16" height="11"/><line x1="9" y1="20" x2="9" y2="14"/><line x1="15" y1="20" x2="15" y2="14"/></svg>',
    "megaphone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10v4h3l9 5V5l-9 5H3z"/><line x1="18" y1="9" x2="21" y2="8"/><line x1="18" y1="15" x2="21" y2="16"/></svg>',
    "edit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 3l4 4L8 20H4v-4L17 3z"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12L12 20 4 12V5a1 1 0 0 1 1-1h7l8 8z"/><circle cx="8.5" cy="8.5" r="1.3"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8h12l1 12H5L6 8z"/><path d="M9 8a3 3 0 0 1 6 0"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><line x1="12" y1="11" x2="12" y2="21"/></svg>',
    "help": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1 .9-1 1.7"/><line x1="12" y1="17" x2="12" y2="17.1"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="9" width="18" height="12"/><line x1="3" y1="13" x2="21" y2="13"/><line x1="12" y1="9" x2="12" y2="21"/><path d="M12 9c-2 0-4-1-4-3a2 2 0 0 1 4 0 2 2 0 0 1 4 0c0 2-2 3-4 3z"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
    "rocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2c3 2 5 6 4 11l-4 4-4-4c-1-5 1-9 4-11z"/><circle cx="12" cy="10" r="1.6"/><path d="M8 15l-3 3M16 15l3 3M9 19l1-2M15 19l-1-2"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-2h6l2 2h3v11H4V8z"/><circle cx="12" cy="13" r="3.5"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.5-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.5-9.5 9-9.5 9z"/></svg>',
    "spool": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><line x1="12" y1="9" x2="12" y2="15"/><path d="M9 9c3 1.5 3 4.5 0 6M15 9c-3 1.5-3 4.5 0 6"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9" r="2.8"/><path d="M15.5 20a5.6 5.6 0 0 1 6-5.5"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2l2 11h11l2-7H7"/><circle cx="9" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/></svg>',
    "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v12H8l-4 4V4z"/><line x1="8" y1="9" x2="16" y2="9"/><line x1="8" y1="13" x2="13" y2="13"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="10" r="6"/><line x1="12" y1="16" x2="12" y2="20"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="2"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="15" r="4"/><line x1="11" y1="12" x2="20" y2="3"/><line x1="16" y1="7" x2="19" y2="10"/><line x1="18" y1="5" x2="21" y2="8"/></svg>',
    # Official brand marks (Simple Icons, CC0), used wherever a platform itself needs an icon.
    "html5": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M1.5 0h21l-1.91 21.563L11.977 24l-8.564-2.438L1.5 0zm7.031 9.75l-.232-2.718 10.059.003.23-2.622L5.412 4.41l.698 8.01h9.126l-.326 3.426-2.91.804-2.955-.81-.188-2.11H6.248l.33 4.171L12 19.351l5.379-1.443.744-8.157H8.531z"/></svg>',
    "wordpress": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.469 6.825c.84 1.537 1.318 3.3 1.318 5.175 0 3.979-2.156 7.456-5.363 9.325l3.295-9.527c.615-1.54.82-2.771.82-3.864 0-.405-.026-.78-.07-1.11m-7.981.105c.647-.03 1.232-.105 1.232-.105.582-.075.514-.93-.067-.899 0 0-1.755.135-2.88.135-1.064 0-2.85-.15-2.85-.15-.585-.03-.661.855-.075.885 0 0 .54.061 1.125.09l1.68 4.605-2.37 7.08L5.354 6.9c.649-.03 1.234-.1 1.234-.1.585-.075.516-.93-.065-.896 0 0-1.746.138-2.874.138-.2 0-.438-.008-.69-.015C4.911 3.15 8.235 1.215 12 1.215c2.809 0 5.365 1.072 7.286 2.833-.046-.003-.091-.009-.141-.009-1.06 0-1.812.923-1.812 1.914 0 .89.513 1.643 1.06 2.531.411.72.89 1.643.89 2.977 0 .915-.354 1.994-.821 3.479l-1.075 3.585-3.9-11.61.001.014zM12 22.784c-1.059 0-2.081-.153-3.048-.437l3.237-9.406 3.315 9.087c.024.053.05.101.078.149-1.12.393-2.325.609-3.582.609M1.211 12c0-1.564.336-3.05.935-4.39L7.29 21.709C3.694 19.96 1.212 16.271 1.211 12M12 0C5.385 0 0 5.385 0 12s5.385 12 12 12 12-5.385 12-12S18.615 0 12 0"/></svg>',
    "shopify": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.337 23.979l7.216-1.561s-2.604-17.613-2.625-17.73c-.018-.116-.114-.192-.211-.192s-1.929-.136-1.929-.136-1.275-1.274-1.439-1.411c-.045-.037-.075-.057-.121-.074l-.914 21.104h.023zM11.71 11.305s-.81-.424-1.774-.424c-1.447 0-1.504.906-1.504 1.141 0 1.232 3.24 1.715 3.24 4.629 0 2.295-1.44 3.76-3.406 3.76-2.354 0-3.54-1.465-3.54-1.465l.646-2.086s1.245 1.066 2.28 1.066c.675 0 .975-.545.975-.932 0-1.619-2.654-1.694-2.654-4.359-.034-2.237 1.571-4.416 4.827-4.416 1.257 0 1.875.361 1.875.361l-.945 2.715-.02.01zM11.17.83c.136 0 .271.038.405.135-.984.465-2.064 1.639-2.508 3.992-.656.213-1.293.405-1.889.578C7.697 3.75 8.951.84 11.17.84V.83zm1.235 2.949v.135c-.754.232-1.583.484-2.394.736.466-1.777 1.333-2.645 2.085-2.971.193.501.309 1.176.309 2.1zm.539-2.234c.694.074 1.141.867 1.429 1.755-.349.114-.735.231-1.158.366v-.252c0-.752-.096-1.371-.271-1.871v.002zm2.992 1.289c-.02 0-.06.021-.078.021s-.289.075-.714.21c-.423-1.233-1.176-2.37-2.508-2.37h-.115C12.135.209 11.669 0 11.265 0 8.159 0 6.675 3.877 6.21 5.846c-1.194.365-2.063.636-2.16.674-.675.213-.694.232-.772.87-.075.462-1.83 14.063-1.83 14.063L15.009 24l.927-21.166z"/></svg>',
}


# ---------------------------------------------------------------------------
# Navigation data
# ---------------------------------------------------------------------------
NAV_SERVICES = [
    ("custom-website-development/", "Custom HTML websites", "Fast, hand-coded, no platform fees"),
    ("wordpress-website-development/", "WordPress websites", "Easy to edit, great for content"),
    ("shopify-website-development/", "Shopify stores", "Sell online with payments and COD"),
    ("ecommerce-website-development/", "Ecommerce websites", "Online stores on Shopify"),
    ("landing-page-design/", "Landing pages", "One page built to convert ad traffic"),
    ("website-maintenance/", "Website maintenance", "Updates, backups and fixes every month"),
]
NAV_MAIN = [("work/", "Work"), ("pricing/", "Pricing"), ("about/", "About"), ("blog/", "Blog")]


def rel(path):
    """Relative prefix back to site root from a page path like 'services/'."""
    return "../" * path.count("/")


# ---------------------------------------------------------------------------
# Page parts
# ---------------------------------------------------------------------------
def head(path, title, desc, css, schema=None, noindex=False, preload=""):
    p = rel(path)
    url = f"{DOMAIN}/{path}"
    # CSS is inlined (INLINE_CSS, built once at import time) rather than linked,
    # so first paint never waits on a second network round trip.
    links = f"  <style>{INLINE_CSS}</style>"
    ld = ""
    if schema:
        ld = "\n".join(f'  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en-IN" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  {robots}
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#FFFFFF">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.png">
  <meta property="og:locale" content="en_IN">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS_DISPLAY}" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS_DISPLAY}"><link rel="stylesheet" href="{FONTS}"></noscript>
{preload}
{links}
{ld}
</head>"""


def header(path):
    p = rel(path)
    body_cls = ""
    def cur(target):
        return ' aria-current="page"' if path == target else ""
    drop = "".join(f'<li><a href="{p}{href}">{name}<span>{sub}</span></a></li>' for href, name, sub in NAV_SERVICES)
    drop += f'<li><a href="{p}services/">All services<span>Everything I build, in one place</span></a></li>'
    main_links = "".join(f'<li><a class="nav__link" href="{p}{h}"{cur(h)}>{n}</a></li>' for h, n in NAV_MAIN)
    mob_sub = "".join(f'<li><a href="{p}{href}">{name}</a></li>' for href, name, _ in NAV_SERVICES)
    mob_main = "".join(f'<li><a href="{p}{h}">{n}</a></li>' for h, n in NAV_MAIN)
    return f"""<body{body_cls}>
<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-thread" aria-hidden="true"><span></span></div>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="{p or './'}" aria-label="{BRAND} home"><span>{BRAND}</span></a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
        <li class="nav__item--drop">
          <button class="nav__link" aria-expanded="false" aria-controls="services-menu">Services {ICON['caret']}</button>
          <div class="nav__drop" id="services-menu"><ul>{drop}</ul></div>
        </li>
        {main_links}
      </ul>
    </nav>
    <a class="btn btn--sm header-cta" href="{p}contact/">Get a free quote</a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <ul>
    <li><a href="{p}services/">Services</a><ul class="mobile-menu__sub">{mob_sub}</ul></li>
    {mob_main}
    <li><a href="{p}contact/">Contact</a></li>
  </ul>
  <a class="btn" href="mailto:{EMAIL}">{ICON['mail']} Email me</a>
</div>
<main id="main">"""


def footer(path, js):
    p = rel(path)
    svc = "".join(f'<li><a href="{p}{h}">{n}</a></li>' for h, n, _ in NAV_SERVICES)
    # All page scripts are bundled into one deferred file at build time (see
    # bundle_assets() in build.py); each script is a self-checking IIFE that
    # no-ops when its target element isn't on the page, so one bundle is safe
    # to include everywhere and saves a request per script on every page.
    scripts = f'<script src="{p}assets/js/app.min.js" defer></script>'
    return f"""</main>
<footer class="site-footer">
  <div class="footer-selvedge" aria-hidden="true"></div>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{p or './'}"><span>{BRAND}</span></a>
        <p>Websites for boutiques, clothing brands and local businesses in Coimbatore, Tiruppur and across Tamil Nadu.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>{svc}</ul>
      </div>
      <div>
        <h2>Where I work</h2>
        <ul>
          <li><a href="{p}website-designer-coimbatore/">Website designer in Coimbatore</a></li>
          <li><a href="{p}website-designer-tiruppur/">Website designer in Tiruppur</a></li>
          <li><a href="{p}website-for-boutiques/">Websites for boutiques</a></li>
          <li><a href="{p}website-for-saree-sellers/">Websites for saree sellers</a></li>
        </ul>
      </div>
      <div>
        <h2>Talk to me</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
          <li>Meetings by appointment</li>
        </ul>
      </div>
    </div>
    <div class="footer-wordmark" aria-hidden="true">{BRAND}</div>
    <div class="footer-bottom">
      <p>&copy; <span data-year></span> {BRAND}. All rights reserved.</p>
      <ul><li><a href="{p}privacy-policy/">Privacy</a></li><li><a href="{p}terms/">Terms</a></li><li><a href="{p}contact/">Contact</a></li></ul>
    </div>
  </div>
</footer>
{scripts}
</body>
</html>
"""


def breadcrumb(path, trail):
    """trail: list of (label, href or None). Returns nav HTML and schema dict."""
    p = rel(path)
    items = [("Home", "")] + trail
    lis = []
    for label, href in items:
        if href is None:
            lis.append(f'<li aria-current="page">{escape(label)}</li>')
        else:
            lis.append(f'<li><a href="{p}{href}">{escape(label)}</a></li>')
    html = f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": label,
         "item": f"{DOMAIN}/{href if href is not None else path}"} for i, (label, href) in enumerate(items)]}
    return html, schema


def business_schema():
    s = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": f"{DOMAIN}/#business",
         "name": BRAND, "url": f"{DOMAIN}/", "email": EMAIL, "priceRange": "₹₹",
         "address": {"@type": "PostalAddress", "addressRegion": "Tamil Nadu", "addressCountry": "IN"},
         "areaServed": [{"@type": "City", "name": "Coimbatore", "alternateName": ["Kovai", "CBE"]},
                        {"@type": "City", "name": "Tiruppur", "alternateName": ["Tirupur"]}],
         "knowsAbout": ["Web design", "Shopify", "WordPress", "HTML", "SEO"],
         "sameAs": [u for u in [INSTAGRAM, GBP_URL] if u]}
    return s


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def service_schema(name, service_type, area=("Coimbatore", "Tiruppur")):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": service_type,
            "provider": {"@id": f"{DOMAIN}/#business"},
            "areaServed": [{"@type": "City", "name": a} for a in area]}


# ---------------------------------------------------------------------------
# Reusable sections
# ---------------------------------------------------------------------------
def faq_block(faqs, title="Questions people ask", intro="", mist=False):
    items = "".join(
        f'<details><summary>{escape(q)}<span class="faq__icon" aria-hidden="true"></span></summary>'
        f'<div class="faq__body"><p>{escape(a)}</p></div></details>' for q, a in faqs)
    intro_html = f'<p class="lead">{intro}</p>' if intro else ""
    return f"""<section class="band{' band--mist' if mist else ''}" aria-labelledby="faq-title">
  <div class="container split split--sticky">
    <div class="section-head" data-reveal><h2 id="faq-title">{title}</h2>{intro_html}</div>
    <div class="faq">{items}</div>
  </div>
</section>"""


PROCESS_STEPS = [
    ("Free call", "Twenty minutes on a call or WhatsApp video to understand your business and how you sell today."),
    ("Plan and quote", "A written scope, timeline and fixed price, so you know exactly what you get."),
    ("Design", "You see the homepage and one key page first, and your feedback shapes the rest."),
    ("Build", "Pages, products, payments, enquiry flows and Google setup, all tested on real phones."),
    ("Launch and training", "Your site goes live and you get a short video showing how to update it yourself."),
]


def process_block(title="How we'll work together", mist=False, note=""):
    lis = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in PROCESS_STEPS)
    note_html = f'<p class="muted" style="margin-top:3rem">{note}</p>' if note else ""
    return f"""<section class="band{' band--mist' if mist else ''}" aria-labelledby="process-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="process-title">{title}</h2>
      <p class="lead">Five clear steps from first message to a site you can run on your own.</p></div>
    <div class="process-wrap"><span class="process__track" aria-hidden="true"><span></span></span><ol class="process">{lis}</ol></div>
    {note_html}
  </div>
</section>"""


def cta_block(path, title="Let's build your <span class=\"accent\">website.</span>", text="Tell me what you sell and how you take orders today. I'll reply within 24 hours with ideas and a price range."):
    p = rel(path)
    return f"""<section class="cta-band" aria-labelledby="cta-title">
  <div class="cta-band__threads" aria-hidden="true"></div>
  <div class="container">
    <h2 id="cta-title" data-reveal>{title}</h2>
    <div data-reveal style="--d:.15s">
      <p>{text}</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn" href="{p}contact/">Get a free quote</a>
        <a class="btn btn--ghost" href="mailto:{EMAIL}">{ICON['mail']} Email me</a>
      </div>
    </div>
  </div>
</section>"""


def page(path, title, desc, body, css=(), js=(), schema=None, noindex=False, preload=""):
    return head(path, title, desc, list(css), schema, noindex, preload) + "\n" + header(path) + "\n" + body + "\n" + footer(path, list(js))
