"""Shared building blocks: site settings, icons, <head>, header, footer, page shell."""
import json
from html import escape

# ---------------------------------------------------------------------------
# Site settings: change these once and rebuild (python _dev/build.py)
# ---------------------------------------------------------------------------
BRAND = "PixelLoom"
DOMAIN = "https://pixelloom.in"          # your final domain, no trailing slash
OWNER = "Poornima"
WHATSAPP = "91XXXXXXXXXX"                 # country code + number, digits only
PHONE_DISPLAY = "+91 XXXXX XXXXX"
EMAIL = "hello@pixelloom.in"
INSTAGRAM = "https://www.instagram.com/"  # your profile URL
GBP_URL = ""                              # Google Business Profile URL once live
CITIES = ["Coimbatore", "Tiruppur"]

FONTS = ("https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400..700"
         "&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap")

BASE_CSS = ["base/tokens.css", "base/reset.css", "base/typography.css",
            "layout/layout.css", "layout/header.css", "layout/footer.css",
            "components/buttons.css", "components/animations.css", "components/cta.css"]
BASE_JS = ["main.js", "reveal.js"]

# ---------------------------------------------------------------------------
# Icons (inline SVG, inherit currentColor where possible)
# ---------------------------------------------------------------------------
def logo_mark(light=False):
    warp = "#F6F5F1" if light else "currentColor"
    return (f'<svg viewBox="0 0 34 34" aria-hidden="true" focusable="false"><g fill="none" stroke-width="5" stroke-linecap="round">'
            f'<path d="M9 4v26M17 4v26M25 4v26" stroke="{warp}"/>'
            f'<path d="M4 9h26" stroke="#2F5BE0"/><path d="M4 17h26" stroke="#2F5BE0"/><path d="M4 25h26" stroke="#2F5BE0"/>'
            f'<path d="M9 6v6M25 6v6M17 14v6M9 22v6M25 22v6" stroke="{warp}"/></g></svg>')

ICON = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>',
    "needle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "caret": '<svg class="nav__caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>',
    "phone": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#EDEAE4"/><path d="M19 14l3 6-2.5 2a14 14 0 0 0 6.5 6.5l2-2.5 6 3-1 4.5c-9.5 0-18-8.5-18-18z" fill="#2F5BE0"/></svg>',
    "mail": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#EDEAE4"/><rect x="13" y="16" width="22" height="16" rx="3" fill="none" stroke="#2448B8" stroke-width="2.4"/><path d="M14 18l10 7 10-7" fill="none" stroke="#2448B8" stroke-width="2.4"/></svg>',
    "wa-circle": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#EDEAE4"/><g transform="translate(12 12)" fill="#22A06B"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></g></svg>',
    "glyph": '<svg viewBox="0 0 28 28" aria-hidden="true"><g stroke-width="4" stroke-linecap="round" fill="none"><path d="M9 3v22M19 3v22" stroke="#1C1D22"/><path d="M3 9h22" stroke="#2F5BE0"/><path d="M3 19h22" stroke="#8FA8F0"/><path d="M9 5v8M19 15v8" stroke="#1C1D22"/></g></svg>',
}

def why_icon(c1, c2):
    return (f'<svg viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="26" fill="{c1}" opacity=".14"/>'
            f'<g stroke-width="4" stroke-linecap="round" fill="none"><path d="M18 14v24M34 14v24" stroke="#1C1D22"/>'
            f'<path d="M12 20h28" stroke="{c1}"/><path d="M12 32h28" stroke="{c2}"/><path d="M18 16v8M34 28v8" stroke="#1C1D22"/></g></svg>')

# ---------------------------------------------------------------------------
# Navigation data
# ---------------------------------------------------------------------------
NAV_SERVICES = [
    ("custom-website-development/", "Custom HTML websites", "Fast, hand-coded, no platform fees"),
    ("wordpress-website-development/", "WordPress websites", "Easy to edit, great for content"),
    ("shopify-website-development/", "Shopify stores", "Sell online with payments and COD"),
    ("ecommerce-website-development/", "Ecommerce websites", "Online stores on Shopify or WooCommerce"),
    ("landing-page-design/", "Landing pages", "One page built to convert ad traffic"),
    ("website-maintenance/", "Website maintenance", "Updates, backups and fixes every month"),
]
NAV_MAIN = [("work/", "Work"), ("pricing/", "Pricing"), ("about/", "About"), ("blog/", "Blog")]


def wa_link(text="Hi! I'd like a quote for a website."):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


def rel(path):
    """Relative prefix back to site root from a page path like 'services/'."""
    return "../" * path.count("/")


# ---------------------------------------------------------------------------
# Page parts
# ---------------------------------------------------------------------------
def head(path, title, desc, css, schema=None, noindex=False):
    p = rel(path)
    url = f"{DOMAIN}/{path}"
    # All page CSS is bundled into one file at build time (see bundle_assets() in
    # build.py) so a page needs a single stylesheet request instead of a dozen.
    links = f'  <link rel="stylesheet" href="{p}assets/css/app.min.css">'
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
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
{links}
{ld}
</head>"""


def header(path):
    p = rel(path)
    body_cls = ' class="has-dark-hero"' if path == "" else ""
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
    <a class="brand" href="{p or './'}" aria-label="{BRAND} home">{logo_mark()}<span>{BRAND}</span></a>
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
  <a class="btn" href="{wa_link()}" target="_blank" rel="noopener">{ICON['whatsapp']} Chat on WhatsApp</a>
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
        <a class="brand" href="{p or './'}">{logo_mark(light=True)}<span>{BRAND}</span></a>
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
          <li><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
          <li>Meetings by appointment</li>
        </ul>
      </div>
    </div>
    <div class="footer-wordmark" aria-hidden="true">{BRAND}</div>
    <div class="footer-bottom">
      <p>&copy; <span data-year></span> {BRAND}. Designed and built by {OWNER}.</p>
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
         "name": BRAND, "url": f"{DOMAIN}/", "email": EMAIL, "telephone": PHONE_DISPLAY, "priceRange": "₹₹",
         "founder": {"@type": "Person", "name": OWNER, "jobTitle": "Web designer and developer"},
         "address": {"@type": "PostalAddress", "addressRegion": "Tamil Nadu", "addressCountry": "IN"},
         "areaServed": [{"@type": "City", "name": "Coimbatore", "alternateName": ["Kovai", "CBE"]},
                        {"@type": "City", "name": "Tiruppur", "alternateName": ["Tirupur"]}],
         "knowsAbout": ["Web design", "Shopify", "WordPress", "WooCommerce", "HTML", "SEO"],
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
        <a class="btn btn--ghost" href="{wa_link()}" target="_blank" rel="noopener">{ICON['whatsapp']} Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""


def page(path, title, desc, body, css=(), js=(), schema=None, noindex=False):
    return head(path, title, desc, list(css), schema, noindex) + "\n" + header(path) + "\n" + body + "\n" + footer(path, list(js))
