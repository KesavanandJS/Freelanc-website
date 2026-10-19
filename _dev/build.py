"""Builds the static site. Run from anywhere:  python _dev/build.py
Every page is written to <slug>/index.html so URLs stay clean (/website-designer-coimbatore/)."""
from pathlib import Path
from html import escape
from layout import (BRAND, DOMAIN, OWNER, EMAIL, WHATSAPP, PHONE_DISPLAY, ICON, why_icon, wa_link, rel, page, breadcrumb,
                    business_schema, faq_schema, service_schema, faq_block, process_block, cta_block)
from content_services import SERVICES, PRICE

ROOT = Path(__file__).resolve().parent.parent
BUILT = []

# Deferred scripts are bundled into one file at build time (CSS is inlined
# straight into <head> instead, see layout.py's INLINE_CSS). Each script is
# a self-checking IIFE that no-ops when its target element isn't on the
# page, so one bundle is safe to include everywhere and saves a request per
# script on every page. Source files stay split under assets/js/ for editing.
JS_BUNDLE = [
    "main.js", "reveal.js", "weave.js", "process.js", "faq.js",
    "contact.js", "pricing.js", "work-filter.js",
]


def bundle_assets():
    js_dir = ROOT / "assets/js"
    bundled_js = "\n".join((js_dir / f).read_text(encoding="utf-8").strip() for f in JS_BUNDLE)
    (js_dir / "app.min.js").write_text(bundled_js + "\n", encoding="utf-8")


def write(path, html):
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    BUILT.append(path)


SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}
EXTRA_LABELS = {"website-designer-coimbatore/": "Website designer in Coimbatore",
                "website-designer-tiruppur/": "Website designer in Tiruppur"}


def label(slug):
    return SVC_BY_SLUG[slug]["nav"] if slug in SVC_BY_SLUG else EXTRA_LABELS.get(slug, slug)


def includes_list(items):
    return '<ul class="includes">' + "".join(f"<li>{ICON['check']}<span>{escape(i)}</span></li>" for i in items) + "</ul>"


def tiers_html(packages, colors=("#2448B8", "#2F5BE0", "#8FA8F0"), flag_middle=True):
    out = []
    for i, (name, price, items) in enumerate(packages):
        flag = '<span class="tier__flag">Most popular</span>' if flag_middle and len(packages) == 3 and i == 1 else ""
        lis = "".join(f"<li>{escape(x)}</li>" for x in items)
        price_html = escape(price).replace(" / month", " <small>/ month</small>")
        out.append(f'<div class="tier" style="--c:{colors[i % 3]};--d:{i*0.1}s" data-reveal>{flag}<h3>{escape(name)}</h3>'
                   f'<p class="tier__price">From {price_html}</p><ul>{lis}</ul></div>')
    return '<div class="tiers">' + "".join(out) + "</div>"


WORK = [
    dict(name="Gourmet Bakes Sweets Cafe", platform="shopify", tags=["Shopify", "Food and sweets"],
         line="Fresh from the counter, now online", fabric="repeating-linear-gradient(135deg,#1C1D22 0 18px,#24262D 18px 36px)",
         text="A Shopify store for a sweets, savouries and bakes cafe, with festive collections, gift boxes and simple ordering for local customers."),
    dict(name="Herbie", platform="website", tags=["Website", "Copywriting", "D2C"],
         line="Flavoured nuts with a personality", fg="#1C1D22", fabric="radial-gradient(circle at 20% 30%,#FFFFFF 0 10%,transparent 11%) 0 0/60px 60px,#EDEAE4",
         text="A brand website and product copy for a flavoured cashew and badam brand, written to make each flavour feel worth trying."),
    dict(name="Bright Digi World", platform="shopify", tags=["Shopify", "B2B equipment"],
         line="Office automation, made easy to order", fabric="repeating-linear-gradient(90deg,#2F5BE0 0 22px,#2A53D4 22px 44px)",
         text="A Shopify store for office automation and cleaning equipment, organised so business buyers can find the right machine quickly."),
]


def work_rows(path, limit=None, with_filter_attr=False):
    p = rel(path)
    rows = []
    for w in WORK[:limit]:
        tags = "".join(f'<span class="tag">{t}</span>' for t in w["tags"])
        attr = f' data-platform="{w["platform"]}"' if with_filter_attr else ""
        rows.append(f"""<article class="work-row"{attr}>
  <div class="work-row__visual" data-reveal><div class="mock"><div class="mock__bar" aria-hidden="true"><i></i><i></i><i></i></div>
    <div class="mock__body" style="--fabric:{w['fabric']};--fg:{w.get('fg', '#FFFFFF')}" role="img" aria-label="Preview of the {escape(w['name'])} website"><b>{escape(w['line'])}</b><small>{escape(w['name'])}</small></div></div></div>
  <div data-reveal style="--d:.15s"><div class="work-row__meta">{tags}</div><h3>{escape(w['name'])}</h3><p>{escape(w['text'])}</p>
    <a class="text-link" href="{p}contact/">Start a project like this</a></div>
</article>""")
    return '<div class="work-rows">' + "".join(rows) + "</div>"


# ===========================================================================
# HOME
# ===========================================================================
HOME_FAQS = [
    ("How much does a website cost?", f"A simple business website starts from {PRICE} and a Shopify store from {PRICE}. The price depends on pages or products, design and features. You get a fixed quote before any work begins."),
    ("How long does it take?", "Most business websites take 1 to 3 weeks and online stores 2 to 4 weeks, depending on content and the number of products."),
    ("Which platform should I choose?", "Shopify if you sell online every day, WordPress if you publish often, and a custom HTML site if you want something fast and low-maintenance. I'll recommend one honestly."),
    ("Can I update the website myself?", "Yes. Shopify and WordPress sites come with a short training video made for your site, so you can change products, prices and offers yourself."),
    ("Will my website show up on Google?", "Every site is built with SEO basics: fast loading, proper titles, schema and Search Console setup. Local and brand searches usually appear within weeks."),
    ("Do you work outside Coimbatore and Tiruppur?", "Yes. Most work happens over WhatsApp and video calls, so I work with businesses across Tamil Nadu and India."),
    ("தமிழில் பேசலாமா?", "ஆம்! நீங்கள் தமிழிலோ ஆங்கிலத்திலோ பேசலாம். உங்கள் இணையதளம் பற்றி WhatsApp-இல் தொடர்பு கொள்ளுங்கள்."),
]


def build_home():
    path = ""
    p = rel(path)
    industries = ["Boutiques", "Saree sellers", "Kidswear brands", "Knitwear exporters", "Sweets and bakeries", "D2C brands", "Clinics", "Local services"]
    marquee_items = "".join(f'<span class="marquee__item">{i}{ICON["glyph"]}</span>' for i in industries)
    svc_rows = "".join(
        f'<li><a class="svc-row" href="{p}{s["slug"]}"><h3>{escape(s["nav"])}</h3><p>{escape(s["lead"].split(". ")[0].rstrip("."))}.</p>'
        f'<span class="svc-row__needle" aria-hidden="true">{ICON["needle"]}</span></a></li>'
        for s in SERVICES if s["slug"] not in ("website-for-boutiques/", "website-for-saree-sellers/"))
    why = [("You talk to the person building it", "No sales team or account managers. Every message reaches the designer working on your site.", "#2F5BE0", "#8FA8F0"),
           ("Built to be found", "Clean code, fast pages and proper SEO setup, so Google and your customers can find you.", "#2448B8", "#2F5BE0"),
           ("Fast on every phone", "Designed mobile-first and tested on real devices, because that's where your customers shop.", "#8FA8F0", "#2448B8"),
           ("Tamil and English", "Talk through your project in the language you're comfortable with.", "#2F5BE0", "#2448B8")]
    why_html = "".join(f'<div class="why__item" data-reveal style="--d:{i*0.08}s">{why_icon(c1, c2)}<div><h3>{t}</h3><p>{d}</p></div></div>'
                       for i, (t, d, c1, c2) in enumerate(why))
    body = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="container hero__grid">
    <div>
      <h1 id="hero-title" data-split>Website designer for <span class="accent">Coimbatore and Tiruppur</span> brands</h1>
      <p class="lead hero__fade" style="--d:.9s">I design and build Shopify stores, WordPress sites and hand-coded websites for boutiques, clothing brands and local businesses. Fast on mobile, easy to update, and set up to be found on Google.</p>
      <div class="btn-row hero__fade" style="--d:1.1s">
        <a class="btn" href="{p}contact/">Get a free quote</a>
        <a class="btn btn--ghost" href="{p}work/">See my work</a>
      </div>
      <p class="hero__note hero__fade" style="--d:1.3s"><i aria-hidden="true"></i><span>Now booking projects for <span data-booking-month>next month</span>. I reply within 24 hours.</span></p>
    </div>
    <div class="hero__visual" aria-hidden="true">
      <div class="weave" data-weave="hero" data-gap="36"></div>
      <div class="phone"><div class="phone__screen">
        <div class="phone__bar"><span>Your Boutique</span><i></i></div>
        <div class="phone__banner"><small>New arrivals</small><b>Festive silks are here</b></div>
        <div class="phone__grid"><div class="phone__item" data-price="₹2,450"></div><div class="phone__item" data-price="₹1,890"></div><div class="phone__item" data-price="₹3,200"></div><div class="phone__item" data-price="₹999"></div></div>
        <div class="phone__cta">Add to cart</div>
      </div><div class="phone__toast"><i></i>New order received</div></div>
    </div>
  </div>
</section>

<div class="marquee" aria-label="Industries I work with"><div class="marquee__track">{marquee_items}{marquee_items}</div></div>

<section class="band" aria-labelledby="platforms-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="platforms-title">A website that works <span class="accent">your way.</span></h2>
      <p class="lead">Three ways to get online, each suited to a different kind of business. Not sure which fits? I'll tell you honestly.</p></div>
    <div class="platforms">
      <div class="platform" style="--c:#2448B8" data-reveal><span class="platform__swatch" style="--sw:repeating-linear-gradient(90deg,#2448B8 0 8px,#5B7FE8 8px 16px)" aria-hidden="true"></span>
        <h3>Custom HTML</h3><p class="platform__best">For a fast, low-cost profile or landing page.</p>
        <ul><li>Loads in under 2 seconds</li><li>No monthly platform fee</li><li>Nothing to update or hack</li></ul>
        <p class="platform__price">From {PRICE}</p><a class="text-link" href="{p}custom-website-development/">Custom HTML websites</a></div>
      <div class="platform" style="--c:#8FA8F0;--d:.1s" data-reveal><span class="platform__swatch" style="--sw:repeating-linear-gradient(45deg,#8FA8F0 0 8px,#C3D1F7 8px 16px)" aria-hidden="true"></span>
        <h3>WordPress</h3><p class="platform__best">For businesses that publish and update often.</p>
        <ul><li>Edit pages and posts yourself</li><li>Strong for blogs and Google traffic</li><li>Add a WooCommerce store later</li></ul>
        <p class="platform__price">From {PRICE}</p><a class="text-link" href="{p}wordpress-website-development/">WordPress websites</a></div>
      <div class="platform" style="--c:#2F5BE0;--d:.2s" data-reveal><span class="platform__swatch" style="--sw:radial-gradient(circle at 30% 30%,#DCE4FB 0 22%,transparent 23%) 0 0/16px 16px,#2F5BE0" aria-hidden="true"></span>
        <h3>Shopify</h3><p class="platform__best">For brands that sell online every day.</p>
        <ul><li>Payments, UPI and cash on delivery</li><li>Run your store from your phone</li><li>Shipping and GST built in</li></ul>
        <p class="platform__price">From {PRICE}</p><a class="text-link" href="{p}shopify-website-development/">Shopify stores</a></div>
    </div>
  </div>
</section>

<section class="band band--mist" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="services-title">What I can <span class="accent">build</span> for you</h2></div>
    <ul class="svc-list">{svc_rows}</ul>
  </div>
</section>

<section class="band" aria-labelledby="work-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="work-title">Made with <span class="accent">intention.</span></h2>
      <p class="lead">Stores and websites for Tamil Nadu brands in food, sweets, nuts and equipment.</p></div>
    {work_rows(path)}
  </div>
</section>

{process_block(mist=True)}

<section class="band" aria-labelledby="why-title">
  <div class="container split">
    <div class="section-head" data-reveal><h2 id="why-title">Why work with me</h2>
      <p class="lead">A website is a long relationship. Here's what you can count on.</p></div>
    <div class="why">{why_html}</div>
  </div>
</section>

<section class="band band--ink" aria-labelledby="cities-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="cities-title">Where I work most</h2>
      <p class="lead">Two cities full of brands that are ready to sell online.</p></div>
    <div class="cities">
      <a class="city-link" href="{p}website-designer-coimbatore/"><span class="city-link__name">Coimbatore</span>
        <span><p>Boutiques, bridal and ethnic wear, and local businesses from RS Puram to Avinashi Road.</p><span class="text-link">Website designer in Coimbatore</span></span></a>
      <a class="city-link" href="{p}website-designer-tiruppur/"><span class="city-link__name">Tiruppur</span>
        <span><p>Knitwear, kidswear and activewear brands, plus garment exporters who need a catalogue buyers trust.</p><span class="text-link">Website designer in Tiruppur</span></span></a>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="pricing-title">
  <div class="container">
    <div class="section-head" data-reveal><h2 id="pricing-title">Simple, <span class="accent">fixed</span> prices</h2>
      <p class="lead">Agree the price before work starts. No hidden monthly charges from me.</p></div>
    {tiers_html([("Starter", PRICE, ["Business website, up to 5 pages", "WhatsApp, form and map", "Basic SEO setup"]),
                 ("Business", PRICE, ["Custom design, up to 10 pages", "Full SEO and schema", "Training video"]),
                 ("Online store", PRICE, ["Shopify or WooCommerce", "Payments, COD and shipping", "Up to 100 products"])])}
    <p style="margin-top:2.5rem"><a class="text-link" href="{p}pricing/">See full pricing</a></p>
  </div>
</section>

{faq_block(HOME_FAQS, mist=True)}
{cta_block(path)}
"""
    css = ["components/weave.css", "components/marquee.css", "components/service-list.css", "components/process.css", "components/faq.css", "pages/home.css"]
    js = ["weave.js", "process.js", "faq.js"]
    schema = [business_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": f"{DOMAIN}/"}, faq_schema(HOME_FAQS)]
    write(path, page(path, "Website Designer in Coimbatore & Tiruppur | PixelLoom",
                     "Website designer for Coimbatore and Tiruppur boutiques, clothing brands and businesses. Shopify, WordPress and custom sites that sell on mobile. Free quote on WhatsApp.",
                     body, css, js, schema))


# ===========================================================================
# SERVICES HUB
# ===========================================================================
def build_services_hub():
    path = "services/"
    p = rel(path)
    crumb, crumb_ld = breadcrumb(path, [("Services", None)])
    rows = "".join(
        f'<li><a class="svc-row" href="{p}{s["slug"]}"><h3>{escape(s["nav"])}</h3><p>{escape(s["lead"].split(". ")[0].rstrip("."))}.</p>'
        f'<span class="svc-row__needle" aria-hidden="true">{ICON["needle"]}</span></a></li>' for s in SERVICES)
    faqs = [("How do I know which service I need?", "Tell me what you sell, how customers reach you today and your budget. I'll suggest the simplest option that does the job."),
            ("Do you write the website content?", "Yes. I can write the page copy or polish what you have, so every page is clear and ready for Google.")]
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <div class="page-hero__grid"><div>
    <h1 data-split>Web design and development services</h1>
    <p class="lead hero__fade" style="--d:.8s">Custom HTML, WordPress and Shopify websites for Coimbatore and Tiruppur businesses, plus the care to keep them working.</p>
    <div class="btn-row hero__fade" style="--d:1s"><a class="btn" href="{p}contact/">Get a free quote</a><a class="btn btn--ghost" href="{p}pricing/">See pricing</a></div>
  </div>
  <div class="page-hero__swatch" aria-hidden="true"><div class="weave" data-weave="hero" data-gap="30"></div></div></div>
</div></section>
<section class="band band--tight"><div class="container"><ul class="svc-list">{rows}</ul></div></section>
<section class="band band--mist" aria-labelledby="choose-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="choose-title">How to choose</h2></div>
  <div class="fit">
    <div class="fit__item" style="--c:#2F5BE0" data-reveal><h3>You want to sell online</h3><p>Choose a Shopify store, or WooCommerce if you already use WordPress.</p></div>
    <div class="fit__item" style="--c:#8FA8F0;--d:.1s" data-reveal><h3>You update content often</h3><p>Choose WordPress, so you can add pages, posts and offers yourself.</p></div>
    <div class="fit__item" style="--c:#2448B8;--d:.2s" data-reveal><h3>You want fast and simple</h3><p>Choose a custom HTML site with no platform fees or plugins.</p></div>
  </div></div></section>
{process_block()}
{faq_block(faqs, mist=True)}
{cta_block(path)}
"""
    write(path, page(path, "Web Design & Development Services in Tamil Nadu | PixelLoom",
                     "Web design and development services: custom HTML websites, WordPress, Shopify and ecommerce stores, landing pages and maintenance for Coimbatore and Tiruppur businesses.",
                     body, ["components/weave.css", "components/service-list.css", "components/process.css", "components/faq.css", "pages/service.css", "pages/home.css"],
                     ["weave.js", "process.js", "faq.js"], [crumb_ld, faq_schema(faqs)]))


# ===========================================================================
# SERVICE / PLATFORM / INDUSTRY TEMPLATE
# ===========================================================================
def build_service(s):
    path = s["slug"]
    p = rel(path)
    is_industry = path.startswith("website-for-")
    crumb, crumb_ld = breadcrumb(path, [("Industries" if is_industry else "Services", None if is_industry else "services/"), (s["nav"], None)])
    pains = "".join(f'<li data-reveal style="--d:{i*0.08}s"><span>{i+1}</span>{escape(t)}</li>' for i, t in enumerate(s["pains"]))
    fit = "".join(f'<div class="fit__item" style="--c:{c}" data-reveal><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d, c in s["fit"])
    related = "".join(f'<a href="{p}{r}">{escape(label(r))}</a>' for r in s["related"])
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <div class="page-hero__grid"><div>
    <h1 data-split>{escape(s['h1'])}</h1>
    <p class="lead hero__fade" style="--d:.8s">{escape(s['lead'])}</p>
    <div class="btn-row hero__fade" style="--d:1s"><a class="btn" href="{p}contact/">Get a free quote</a>
      <a class="btn btn--ghost" href="{wa_link('Hi! I would like to know more about ' + s['nav'].lower() + '.')}" target="_blank" rel="noopener">{ICON['whatsapp']} Chat on WhatsApp</a></div>
  </div>
  <div class="page-hero__swatch" aria-hidden="true"><div class="weave" data-weave="{s['weave']}" data-gap="30"></div></div></div>
</div></section>

<section class="band band--tight" aria-labelledby="pains-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="pains-title">{escape(s['pains_title'])}</h2></div>
  <ol class="pains" role="list">{pains}</ol>
</div></section>

<section class="band band--mist" aria-labelledby="inc-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="inc-title">What's included</h2><p class="lead">Everything you need to launch, with nothing you'll never use.</p></div>
  {includes_list(s['includes'])}
</div></section>

<section class="band" aria-labelledby="fit-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="fit-title">{escape(s['fit_title'])}</h2></div>
  <div class="fit">{fit}</div>
</div></section>

<section class="band band--mist" aria-labelledby="pkg-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="pkg-title">Packages</h2><p class="lead">Fixed prices, agreed before work begins.</p></div>
  {tiers_html(s['packages'])}
  <p style="margin-top:2.5rem"><a class="text-link" href="{p}pricing/">Compare all prices</a></p>
</div></section>

{process_block()}
{faq_block(s['faqs'], mist=True)}
<section class="band band--tight" aria-labelledby="rel-title"><div class="container">
  <h2 id="rel-title" style="font-size:var(--step-3);margin-bottom:1.5rem">Related services</h2>
  <div class="related">{related}</div>
</div></section>
{cta_block(path)}
"""
    css = ["components/weave.css", "components/process.css", "components/faq.css", "pages/home.css", "pages/service.css"]
    schema = [crumb_ld, service_schema(s["h1"], s["service_type"]), faq_schema(s["faqs"])]
    write(path, page(path, s["title"], s["meta"], body, css, ["weave.js", "process.js", "faq.js"], schema))


# ===========================================================================
# CITY PAGES (copy from the SEO plan document)
# ===========================================================================
CITIES = [
    dict(
        slug="website-designer-coimbatore/", name="Coimbatore", alt=["Kovai", "CBE"],
        title="Website Designer in Coimbatore | Boutique & Shopify Sites",
        meta="Website designer for Coimbatore boutiques and brands. Shopify, WordPress and custom sites that sell on mobile. Fixed prices. Chat on WhatsApp.",
        h1="Website designer in Coimbatore for boutiques, brands and local businesses",
        lead="Your customers already find you on Instagram. Give them a store they can buy from at 11 pm without waiting for a DM reply. I design and build Shopify, WordPress and custom websites for Coimbatore businesses: fast on mobile, easy to update, and set up to rank on Google.",
        intro_title="Websites for Coimbatore businesses that are ready to sell online",
        intro=["Coimbatore is one of Tamil Nadu's busiest shopping cities, from the designer boutiques of RS Puram to the retail stretch of Gandhipuram and the showrooms on Avinashi Road. Yet many of these businesses still take orders through Instagram comments, WhatsApp photos and phone calls. That works until it doesn't: messages get missed, customers ask the same questions twice, and nobody can browse your full collection in one place.",
               "A proper website fixes that. Customers see every product with prices and sizes, pay online or choose cash on delivery, and get an order confirmation instantly. You get fewer repeated questions, more orders while you sleep, and a business that shows up when someone in Kovai searches Google for what you sell."],
        niche_title="Boutique website design in Coimbatore",
        niche_lead="Boutiques have needs a generic business site doesn't meet. Your website should feel like your store: curated, personal and easy to shop on a phone.",
        niche=["Collections by occasion: bridal, festive, party wear, daily wear", "Size charts, blouse-stitching and customisation options at checkout",
               "Instagram feed and shop-the-look sections, so posts lead straight to products", "WhatsApp button on every product for customers who want to ask first",
               "Razorpay, UPI and cash on delivery, with Shiprocket or Delhivery", "New-arrival and sale banners you can change yourself in minutes"],
        niche_link=("website-for-boutiques/", "Website design for boutiques"),
        table=None,
        prices=[("Business website (custom HTML or WordPress)", PRICE), ("Boutique or brand Shopify store", PRICE), ("Store with custom design, many products or integrations", PRICE)],
        timeline="Most boutique stores go live in 3 to 4 weeks. I work with Coimbatore clients mainly over WhatsApp and video calls; an in-person meeting can be arranged when it helps.",
        areas=["RS Puram", "Gandhipuram", "Peelamedu", "Saibaba Colony", "Race Course", "Avinashi Road", "Saravanampatti", "Singanallur", "Ramanathapuram", "Vadavalli"],
        other=("website-designer-tiruppur/", "Tiruppur"),
        faqs=[("How much does a website cost in Coimbatore?", f"A simple business website usually starts from {PRICE}, and a Shopify store for a boutique from {PRICE}. Price depends on pages or products, design and features. You get a fixed quote before any work begins, with no hidden monthly charges from me."),
              ("How long does it take to build a boutique website?", "Most boutique Shopify stores take 3 to 4 weeks from the first call to launch. Adding 100 or more products, custom features or waiting on photos can add time. You'll get a clear timeline in your quote."),
              ("Can I update products and prices myself?", "Yes. Shopify and WordPress both let you add products, change prices and post offers from your phone. I record a short training video for your site so you can manage everyday changes without paying anyone."),
              ("Will my website show up on Google?", "Every site is built with SEO basics: fast loading, proper titles and descriptions, schema and a Google Search Console setup. Ranking for competitive searches takes time and content, but your business name and local searches usually appear within weeks."),
              ("Do I still need a website if I sell on Instagram?", "Instagram brings attention; a website turns it into orders. It lets customers browse everything, pay instantly and come back without messaging you. It also protects your business if your Instagram account is ever restricted."),
              ("Do you meet clients in Coimbatore?", "Most work happens smoothly over WhatsApp and video calls, which keeps projects fast. If an in-person meeting will help, for example a product photo session or training, we can arrange one in Coimbatore."),
              ("தமிழில் பேசலாமா?", "ஆம்! நீங்கள் தமிழிலோ ஆங்கிலத்திலோ பேசலாம். உங்கள் கடைக்கான இணையதளத்தைப் பற்றி WhatsApp-இல் தொடர்பு கொள்ளுங்கள்.")],
        services=[("Boutique website design in Coimbatore", "Website design and development")],
        cta=("Ready to take your Coimbatore business online?", "Send me a message with what you sell and how you take orders today. I'll reply within 24 hours with ideas and a price range."),
    ),
    dict(
        slug="website-designer-tiruppur/", name="Tiruppur", alt=["Tirupur"],
        title="Website Designer in Tiruppur | Clothing Brand & Export Sites",
        meta="Website designer for Tiruppur clothing brands and garment exporters. Shopify stores that sell direct and catalogue sites that win buyers. Free quote.",
        h1="Website designer in Tiruppur for clothing brands and garment exporters",
        lead="Tiruppur makes clothes for the world. Your website should sell them just as well. I build Shopify stores for knitwear, kidswear and activewear brands selling direct to customers, and clean product-catalogue websites that help manufacturers and exporters win new buyers.",
        intro_title="Two kinds of Tiruppur businesses, two kinds of websites",
        intro=["Tell me which one you are, or if you're both, and I'll plan the right site. Brands selling to customers need a store; manufacturers selling to buyers need a catalogue that builds trust."],
        table=[("A brand selling T-shirts, kidswear, innerwear, loungewear or activewear to customers", "An online store with sizes, colours, payments, COD and shipping", "Shopify"),
               ("A manufacturer, job-work unit or exporter selling to buyers and brands", "A catalogue website showing capacity, products and certifications, with an enquiry form and WhatsApp", "WordPress or custom")],
        niche_title="Shopify stores for Tiruppur clothing brands",
        niche_lead="More Tiruppur manufacturers are launching their own labels and selling online first. A Shopify store gives your brand a home that marketplaces can't: your own customers, your own margins and your own data.",
        niche=["Product variants for size, colour and pack (for example, pack of 3)", "Size guides for men, women and kids, plus a fit-finder for best sellers",
               "Bulk-buy and combo pricing for families and resellers", "Razorpay, UPI and cash on delivery; Shiprocket or Delhivery for pan-India shipping",
               "GST-ready invoices and automatic order emails and WhatsApp updates", "Product and collection pages written and structured to rank on Google"],
        niche_link=("shopify-website-development/", "Shopify website development"),
        niche2_title="Catalogue websites for garment manufacturers and exporters",
        niche2_lead="Many Tirupur units still win new accounts by sending PDFs and WhatsApp photos. A catalogue website does that work around the clock and looks more credible to a sourcing manager checking you out from Europe, the US or another Indian state.",
        niche2=["Product categories in the order buyers check them: fabric, GSM, product type, MOQ", "Factory capacity, machinery and process photos",
                "Certifications you hold, shown clearly and kept up to date", "A short enquiry form plus WhatsApp and email, so buyers reach you in their time zone",
                "Fast loading even on slow overseas connections, with an English-first layout"],
        prices=[("Catalogue website for a manufacturer or exporter", PRICE), ("Shopify store for a clothing brand", PRICE), ("Large store or custom features (B2B pricing, wholesale login)", PRICE)],
        timeline="Most catalogue sites go live in 2 to 3 weeks and brand stores in 3 to 5 weeks. Work happens over WhatsApp and video calls; an in-person visit to Tiruppur can be arranged when it helps.",
        areas=["Khaderpet", "PN Road", "Mangalam Road", "Avinashi Road", "Palladam Road", "Kangeyam Road", "Anupparpalayam", "Velampalayam", "Export Knitwear Industrial Complex"],
        other=("website-designer-coimbatore/", "Coimbatore"),
        faqs=[("How much does a website cost in Tiruppur?", f"A catalogue website for a manufacturer usually starts from {PRICE}, and a Shopify store for a clothing brand from {PRICE}. The price depends on products, features and design. You get a fixed quote before any work begins, with no surprise charges from me."),
              ("Should my garment brand use Shopify or WooCommerce?", "For most new Tirupur brands, Shopify is simpler: hosting, security and checkout are handled for you, and you can run it from your phone. WooCommerce suits businesses that already use WordPress or need deep customisation without monthly app fees."),
              ("Can my website handle sizes, colours and combo packs?", "Yes. Every product can have size, colour and pack options with separate prices and stock. Combo offers, bulk discounts and buy-more-save-more pricing can be set up for families and resellers."),
              ("Do exporters really need a website if buyers come through agents?", "Yes. Buyers and agents check you online before placing orders. A clear catalogue site with capacity, products and certifications builds trust faster than PDFs and helps new buyers find you directly on Google."),
              ("How long does it take to build?", "Catalogue sites usually take 2 to 3 weeks and Shopify stores 3 to 5 weeks, depending on how many products you have and how quickly photos and details are ready. Your quote includes a clear timeline."),
              ("Will I be able to add new designs myself?", "Yes. Adding a product takes a few minutes from your phone or computer. I provide a short training video made for your site, so your team can add new designs, change prices and run offers without help."),
              ("தமிழில் பேசலாமா?", "ஆம்! உங்கள் பிராண்ட் அல்லது ஏற்றுமதி நிறுவனத்துக்கான இணையதளம் பற்றி தமிழில் WhatsApp-இல் பேசலாம்.")],
        services=[("Shopify store development for clothing brands in Tiruppur", "Ecommerce website development"),
                  ("Catalogue website design for garment exporters in Tiruppur", "Website design")],
        cta=("Ready to sell your Tiruppur brand online?", "Send me your product range and how you sell today. I'll reply within 24 hours with a recommended platform and price range."),
    ),
]


def build_city(c):
    path = c["slug"]
    p = rel(path)
    crumb, crumb_ld = breadcrumb(path, [("Locations", None), (c["name"], None)])
    intro = "".join(f"<p>{escape(x)}</p>" for x in c["intro"])
    table = ""
    if c.get("table"):
        rows = "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td><td>{escape(d)}</td></tr>" for a, b, d in c["table"])
        table = f'<div class="table-scroll" data-reveal style="margin-top:2rem"><table class="split-table"><thead><tr><th scope="col">If you are</th><th scope="col">You need</th><th scope="col">Built on</th></tr></thead><tbody>{rows}</tbody></table></div>'
    niche2 = ""
    if c.get("niche2"):
        niche2 = f"""<section class="band" aria-labelledby="n2-title"><div class="container split split--sticky">
  <div class="section-head" data-reveal><h2 id="n2-title">{escape(c['niche2_title'])}</h2><p class="lead">{escape(c['niche2_lead'])}</p></div>
  {includes_list(c['niche2'])}</div></section>"""
    prices = "".join(f"<li><span>{escape(a)}</span><span>From {escape(b)}</span></li>" for a, b in c["prices"])
    areas = "".join(f"<li>{escape(a)}</li>" for a in c["areas"])
    schema_business = business_schema()
    schema_business = dict(schema_business, areaServed=[{"@type": "City", "name": c["name"], "alternateName": c["alt"]}])
    schema = [schema_business, crumb_ld, faq_schema([f for f in c["faqs"] if not f[0].startswith("தமிழ")])] + \
             [dict(service_schema(n, t, (c["name"],))) for n, t in c["services"]]
    body = f"""
<section class="city-hero"><div class="container">{crumb}
  <p class="city-hero__name" aria-hidden="true">{c['name']}</p>
  <h1>{escape(c['h1'])}</h1>
  <p class="lead">{escape(c['lead'])}</p>
  <div class="btn-row"><a class="btn" href="{p}contact/">Get a free quote</a>
    <a class="btn btn--ghost" href="{wa_link('Hi! I have a business in ' + c['name'] + ' and need a website.')}" target="_blank" rel="noopener">{ICON['whatsapp']} Chat on WhatsApp</a></div>
  <p class="hero__note" style="margin-top:1.6rem;color:var(--ink-soft)"><i aria-hidden="true"></i><span>Now booking projects for <span data-booking-month>next month</span>.</span></p>
</div></section>

<section class="band band--mist" aria-labelledby="intro-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="intro-title">{escape(c['intro_title'])}</h2></div>
  <div class="prose" data-reveal style="--d:.1s">{intro}{table}</div>
</div></section>

<section class="band" aria-labelledby="niche-title"><div class="container split split--sticky">
  <div class="section-head" data-reveal><h2 id="niche-title">{escape(c['niche_title'])}</h2><p class="lead">{escape(c['niche_lead'])}</p>
    <a class="text-link" href="{p}{c['niche_link'][0]}">{escape(c['niche_link'][1])}</a></div>
  {includes_list(c['niche'])}
</div></section>
{niche2}

<section class="band band--mist" aria-labelledby="plat-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="plat-title">Shopify, WordPress or a custom website?</h2></div>
  <div class="fit">
    <div class="fit__item" style="--c:#2F5BE0" data-reveal><h3>Shopify</h3><p>For boutiques and brands that sell online every day. Products, payments, stock and orders in one dashboard.</p><a class="text-link" href="{p}shopify-website-development/">Shopify stores</a></div>
    <div class="fit__item" style="--c:#8FA8F0" data-reveal><h3>WordPress</h3><p>For businesses that publish often or want a blog that brings Google traffic. WooCommerce adds a store when you need it.</p><a class="text-link" href="{p}wordpress-website-development/">WordPress websites</a></div>
    <div class="fit__item" style="--c:#2448B8" data-reveal><h3>Custom HTML</h3><p>For a fast, low-maintenance business profile or a landing page for ads, with no monthly platform fee.</p><a class="text-link" href="{p}custom-website-development/">Custom HTML websites</a></div>
  </div></div></section>

<section class="band" aria-labelledby="work-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="work-title">Recent work</h2></div>
  {work_rows(path, limit=2)}
  <p style="margin-top:3rem"><a class="text-link" href="{p}work/">See all projects</a></p>
</div></section>

<section class="band band--mist" aria-labelledby="cost-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="cost-title">Website design cost in {c['name']}</h2>
    <p class="lead">Every project has a fixed price agreed before work starts. The final price depends on pages or products, features, and whether you supply photos and text.</p>
    <a class="text-link" href="{p}pricing/">See full pricing</a></div>
  <ul class="addons" style="grid-template-columns:1fr" data-reveal>{prices}</ul>
</div></section>

{process_block(note=c['timeline'])}

<section class="band band--tight band--mist" aria-labelledby="areas-title"><div class="container">
  <h2 id="areas-title" style="font-size:var(--step-3);margin-bottom:1.6rem">Areas I serve in {c['name']}</h2>
  <ul class="areas">{areas}</ul>
  <p class="muted" style="margin-top:1.6rem">And businesses across {c['name']} district. I also work with brands in <a class="link" href="{p}{c['other'][0]}">{c['other'][1]}</a> and Erode.</p>
</div></section>

{faq_block(c['faqs'], title=f"Questions {c['name']} business owners ask")}
{cta_block(path, c['cta'][0], c['cta'][1])}
"""
    css = ["components/process.css", "components/faq.css", "pages/home.css", "pages/service.css", "pages/pricing.css", "pages/city.css"]
    write(path, page(path, c["title"], c["meta"], body, css, ["process.js", "faq.js"], schema))


# ===========================================================================
# PRICING
# ===========================================================================
PRICING = {
    "html": ("Custom HTML", [("HTML Starter", PRICE, ["Up to 3 pages", "WhatsApp and contact form", "Basic SEO setup", "1 to 2 weeks"]),
                             ("HTML Business", PRICE, ["Up to 6 pages", "Custom design and animation", "Full SEO and schema", "2 to 3 weeks"]),
                             ("Landing Page", PRICE, ["One page for ads", "Tracking setup", "About 1 week"])]),
    "wordpress": ("WordPress", [("WordPress Starter", PRICE, ["Up to 5 pages", "Lean theme setup", "SEO plugin configured", "About 2 weeks"]),
                                ("WordPress Business", PRICE, ["Up to 10 pages plus blog", "Custom design", "Speed and security setup", "About 3 weeks"]),
                                ("WooCommerce Store", PRICE, ["Up to 50 products", "Payments, UPI and COD", "Shipping and GST", "About 4 weeks"])]),
    "shopify": ("Shopify", [("Starter Store", PRICE, ["Up to 20 products", "Theme setup and branding", "Payments, COD and shipping", "About 2 weeks"]),
                            ("Growth Store", PRICE, ["Up to 100 products", "Custom homepage and sections", "SEO and speed setup", "About 3 weeks"]),
                            ("Premium Store", PRICE, ["Unlimited products", "Custom-coded sections", "Advanced apps and automations", "4 to 5 weeks"])]),
}
PRICING_FAQS = [
    ("Are domain and hosting included?", "Domain and hosting are paid by you, in your name, so you always own them. I set everything up and tell you exactly what to buy."),
    ("How do payments work?", "Usually 50% to start and 50% at launch, by UPI or bank transfer. Larger projects can be split into three stages."),
    ("Do you provide a GST invoice?", "Invoice details depend on registration status; ask when you request your quote."),
    ("What if I need changes after launch?", "You get 30 days of free fixes. After that, small edits are covered by a care plan or charged per change."),
]


def build_pricing():
    path = "pricing/"
    p = rel(path)
    crumb, crumb_ld = breadcrumb(path, [("Pricing", None)])
    tabs = "".join(f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" data-slug="{k}" aria-selected="false" tabindex="-1">{v[0]}</button>' for k, v in PRICING.items())
    panels = "".join(f'<div class="tab-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0" hidden>{tiers_html(v[1])}</div>' for k, v in PRICING.items())
    addons = [("Extra page", PRICE), ("Product upload (per 25 products)", PRICE), ("Copywriting per page", PRICE), ("Logo and brand colours", PRICE),
              ("Google Business Profile setup", PRICE), ("SEO starter pack", PRICE), ("Care plan", PRICE + " / month"), ("Growth care plan", PRICE + " / month")]
    addons_html = "".join(f"<li><span>{a}</span><span>{b}</span></li>" for a, b in addons)
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <h1 data-split>Website packages and prices</h1>
  <p class="lead hero__fade" style="--d:.8s">Fixed prices, no surprises. Pick your platform to see what each package includes.</p>
</div></section>
<section class="band band--tight"><div class="container">
  <div class="tabs" role="tablist" aria-label="Choose a platform"><span class="tabs__pill" aria-hidden="true"></span>{tabs}</div>
  {panels}
</div></section>
<section class="band band--mist" aria-labelledby="addons-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="addons-title">Add-ons and monthly plans</h2><p class="lead">Add only what you need, now or later.</p></div>
  <ul class="addons" style="grid-template-columns:1fr">{addons_html}</ul>
</div></section>
<section class="band" aria-labelledby="affects-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="affects-title">What affects the price</h2></div>
  <div class="prose" data-reveal><p>The number of pages or products, how custom the design is, the features you need (bookings, wholesale pricing, integrations) and whether you supply photos and text all shape the final price.</p>
  <p>You'll always get a written quote with a fixed price and timeline before any work begins. If something new comes up mid-project, we agree the cost before I build it.</p></div>
</div></section>
{faq_block(PRICING_FAQS, mist=True)}
{cta_block(path, "Not sure which package fits?", "Tell me about your business and I'll recommend one, with a custom quote if you need something different.")}
"""
    write(path, page(path, "Website Development Cost in India | Packages & Prices | PixelLoom",
                     "Clear, fixed prices for HTML, WordPress and Shopify websites. See what each package includes, add-ons and payment terms. No hidden costs.",
                     body, ["components/faq.css", "pages/home.css", "pages/service.css", "pages/pricing.css"], ["pricing.js", "faq.js"], [crumb_ld, faq_schema(PRICING_FAQS)]))


# ===========================================================================
# WORK, ABOUT, CONTACT, BLOG, LEGAL, UTILITY
# ===========================================================================
def build_work():
    path = "work/"
    crumb, crumb_ld = breadcrumb(path, [("Work", None)])
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <h1 data-split>Recent work</h1>
  <p class="lead hero__fade" style="--d:.8s">Stores and websites for Tamil Nadu brands. Filter by platform to see similar projects.</p>
</div></section>
<section class="band band--tight"><div class="container">
  <div class="filter" role="group" aria-label="Filter projects">
    <button data-filter="all" aria-pressed="true">All</button><button data-filter="shopify" aria-pressed="false">Shopify</button>
    <button data-filter="website" aria-pressed="false">Websites</button></div>
  {work_rows(path, with_filter_attr=True)}
</div></section>
{cta_block(path, "Want a site like these?")}
"""
    write(path, page(path, "Website Design Portfolio | Projects by PixelLoom",
                     "Shopify stores and websites built for Tamil Nadu brands in food, sweets, nuts and equipment. See recent web design work.",
                     body, ["pages/home.css", "pages/service.css", "pages/work.css"], ["work-filter.js"], [crumb_ld]))


def build_about():
    path = "about/"
    p = rel(path)
    crumb, crumb_ld = breadcrumb(path, [("About", None)])
    skills = ["HTML", "CSS", "JavaScript", "WordPress", "Elementor", "WooCommerce", "Shopify", "Shopify Liquid", "Figma", "SEO", "Copywriting", "Google Analytics"]
    person = {"@context": "https://schema.org", "@type": "Person", "name": OWNER, "jobTitle": "Web designer and developer",
              "worksFor": {"@id": f"{DOMAIN}/#business"}, "knowsAbout": skills, "url": f"{DOMAIN}/about/"}
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <div class="page-hero__grid" style="align-items:center"><div>
    <h1 data-split>Hi, I'm {OWNER}. I design and build websites.</h1>
    <p class="lead hero__fade" style="--d:.8s">I work with boutiques, clothing brands and local businesses who want a website that looks like them and actually brings in customers. I also write the words, so your site says the right things as well as looking good.</p>
    <div class="btn-row hero__fade" style="--d:1s"><a class="btn" href="{p}contact/">Work with me</a><a class="btn btn--ghost" href="{p}work/">See my work</a></div>
  </div>
  <div class="portrait" role="img" aria-label="Portrait of {OWNER}">{OWNER[0]}</div></div>
</div></section>
<section class="band band--mist" aria-labelledby="story-title"><div class="container split">
  <div class="section-head" data-reveal><h2 id="story-title">How I work</h2></div>
  <div class="prose" data-reveal>
    <p>I take on a small number of projects at a time, so every client gets my full attention. You'll talk to me directly from the first call to launch day, with no hand-offs.</p>
    <p>Before designing anything, I learn how you sell today: who your customers are, what they ask before buying and where orders get stuck. The website is built around those answers.</p>
    <p>Every site I build is fast on mobile, set up properly for Google and simple for you to update. When it launches, you get a short training video and 30 days of free fixes.</p>
  </div>
</div></section>
<section class="band" aria-labelledby="skills-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="skills-title">Tools I use</h2></div>
  <ul class="skills" data-reveal>{"".join(f"<li>{s}</li>" for s in skills)}</ul>
</div></section>
<section class="band band--mist" aria-labelledby="values-title"><div class="container">
  <div class="section-head" data-reveal><h2 id="values-title">What you can expect</h2></div>
  <div class="values">
    <div data-reveal><h3>Clear communication</h3><p>Regular updates on WhatsApp, in Tamil or English, and answers within 24 hours.</p></div>
    <div data-reveal style="--d:.1s"><h3>Honest advice</h3><p>I'll tell you when you don't need a big site, an expensive app or a feature that won't pay off.</p></div>
    <div data-reveal style="--d:.2s"><h3>You own everything</h3><p>Domain, hosting, store and logins are all in your name from day one.</p></div>
  </div>
</div></section>
{cta_block(path)}
"""
    write(path, page(path, f"About {OWNER} | Web Designer & Developer for Coimbatore & Tiruppur",
                     f"Meet {OWNER}, a web designer and developer building Shopify, WordPress and custom websites for boutiques, clothing brands and local businesses.",
                     body, ["pages/home.css", "pages/service.css", "pages/about.css"], [], [crumb_ld, person]))


def build_contact():
    path = "contact/"
    p = rel(path)
    crumb, crumb_ld = breadcrumb(path, [("Contact", None)])
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <h1 data-split>Let's talk about your website</h1>
  <p class="lead hero__fade" style="--d:.8s">I reply within 24 hours with ideas and a price range. Pick whichever way suits you.</p>
</div></section>
<section class="band band--tight"><div class="container split">
  <div>
    <div class="contact-ways">
      <a class="contact-way" href="{wa_link()}" target="_blank" rel="noopener">{ICON['wa-circle']}<span><strong>WhatsApp</strong><span>Fastest way to reach me</span></span></a>
      <a class="contact-way" href="tel:{PHONE_DISPLAY.replace(' ', '')}">{ICON['phone']}<span><strong>Call</strong><span>{PHONE_DISPLAY}</span></span></a>
      <a class="contact-way" href="mailto:{EMAIL}">{ICON['mail']}<span><strong>Email</strong><span>{EMAIL}</span></span></a>
    </div>
    <p class="muted" style="margin-top:2rem">Serving Coimbatore, Tiruppur and all of Tamil Nadu. Meetings by appointment.</p>
  </div>
  <form class="form" action="{p}thank-you/" data-quote-form data-whatsapp="{WHATSAPP}" novalidate>
    <h2 style="font-size:var(--step-3)">Request a free quote</h2>
    <div class="form__row">
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required><span class="field__error">Enter your name.</span></div>
      <div class="field"><label for="f-phone">Phone or WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" pattern="[0-9+ ]{{10,15}}" required><span class="field__error">Enter a 10-digit phone number.</span></div>
    </div>
    <div class="field"><label for="f-business">Business name and what you sell</label><input id="f-business" name="business" required><span class="field__error">Tell me a little about your business.</span></div>
    <div class="form__row">
      <div class="field"><label for="f-type">Website type</label><select id="f-type" name="type" required><option value="">Choose one</option><option>Shopify store</option><option>WordPress website</option><option>Custom HTML website</option><option>Landing page</option><option>Not sure yet</option></select><span class="field__error">Choose a website type.</span></div>
      <div class="field"><label for="f-budget">Budget range</label><select id="f-budget" name="budget" required><option value="">Choose one</option><option>Under ₹15,000</option><option>₹15,000 to ₹30,000</option><option>₹30,000 to ₹60,000</option><option>Above ₹60,000</option></select><span class="field__error">Choose a budget range.</span></div>
    </div>
    <div class="field"><label for="f-msg">Anything else? <span class="field__hint">(optional)</span></label><textarea id="f-msg" name="message"></textarea></div>
    <div class="btn-row"><button class="btn" type="submit">Send on WhatsApp</button></div>
    <p class="form__status" role="status" aria-live="polite"></p>
  </form>
</div></section>
"""
    write(path, page(path, "Contact a Website Designer in Coimbatore & Tiruppur | Free Quote",
                     "Request a free website quote. Message on WhatsApp, call or email. Replies within 24 hours.",
                     body, ["components/forms.css", "pages/home.css", "pages/service.css", "pages/contact.css"], ["contact.js"], [crumb_ld, business_schema()]))


BLOG_PLAN = [("Pricing", "How much does a website cost in India? (2026 price guide)"), ("Platforms", "HTML vs WordPress vs Shopify: which is right for your business?"),
             ("Boutiques", "How to take your Instagram boutique online"), ("Sarees", "Saree business website: sell beyond WhatsApp"),
             ("Shopify", "How to add Razorpay and cash on delivery to Shopify"), ("Shopify", "Shopify GST settings for Indian stores, explained"),
             ("Local", "Website checklist for Coimbatore and Tiruppur businesses"), ("Buying", "How to choose a website designer: 12 questions to ask")]


def build_blog():
    path = "blog/"
    crumb, crumb_ld = breadcrumb(path, [("Blog", None)])
    posts = "".join(f'<li data-reveal><span class="tag">{c}</span><h3>{escape(t)}</h3><span class="posts__soon">Coming soon</span></li>' for c, t in BLOG_PLAN)
    body = f"""
<section class="page-hero"><div class="container">{crumb}
  <h1 data-split>Website tips for small businesses</h1>
  <p class="lead hero__fade" style="--d:.8s">Plain-English guides on costs, platforms and getting found on Google.</p>
</div></section>
<section class="band band--tight"><div class="container"><ul class="posts">{posts}</ul></div></section>
{cta_block(path)}
"""
    write(path, page(path, "Website Tips for Small Businesses | PixelLoom Blog",
                     "Guides on website costs in India, choosing between HTML, WordPress and Shopify, and getting your business found on Google.",
                     body, ["pages/home.css", "pages/service.css", "pages/blog.css"], [], [crumb_ld]))


def build_legal(path, title, heading, paras):
    crumb, crumb_ld = breadcrumb(path, [(heading, None)])
    body = f'<section class="legal"><div class="container--narrow">{crumb}<h1>{heading}</h1><div class="prose">' + \
           "".join(f"<h2>{h}</h2><p>{t}</p>" if h else f"<p>{t}</p>" for h, t in paras) + "</div></div></section>"
    write(path, page(path, title, f"{heading} for {BRAND}.", body, ["pages/legal.css"], [], [crumb_ld]))


def build_utility():
    build_legal("privacy-policy/", f"Privacy Policy | {BRAND}", "Privacy policy", [
        (None, f"This page explains what information {BRAND} collects and how it is used. Last updated: [date]."),
        ("What I collect", "When you contact me by form, WhatsApp, phone or email, I receive the details you choose to share, such as your name, phone number and business information."),
        ("How I use it", "Only to reply to your enquiry, prepare a quote and deliver your project. I don't sell or share your details with anyone else."),
        ("Analytics", "This site may use Google Analytics to understand how visitors use it. You can block analytics cookies in your browser settings."),
        ("Contact", f"Questions about your data? Email {EMAIL}.")])
    build_legal("terms/", f"Terms | {BRAND}", "Terms", [
        (None, "These terms apply to website projects. Your written quote lists the exact scope, price and timeline for your project."),
        ("Payments", "Projects usually start with a 50% advance, with the balance due at launch."),
        ("Ownership", "Once paid in full, you own your website content, design and accounts. Domains and hosting are registered in your name."),
        ("Changes", "Work outside the agreed scope is quoted and approved before it starts.")])
    # thank-you (noindex)
    path = "thank-you/"
    p = rel(path)
    body = f"""<section class="notfound"><div class="container--narrow"><h1 style="font-size:var(--step-5);background:none;color:var(--ink)">Thank you!</h1>
<p class="lead">Your enquiry is ready in WhatsApp. Press send there, and I'll reply within 24 hours.</p>
<div class="btn-row" style="justify-content:center"><a class="btn" href="{p or './'}">Back to home</a><a class="btn btn--ghost" href="{p}work/">See my work</a></div></div></section>"""
    write(path, page(path, f"Thank you | {BRAND}", "Your enquiry has been sent.", body, ["pages/legal.css"], [], None, noindex=True))
    # 404 at root as 404.html
    html = page("", f"Page not found | {BRAND}", "This page could not be found.",
                """<section class="notfound"><div class="container--narrow"><h1>404</h1><p class="lead">This page has come loose. Try the homepage or see what I build.</p>
<div class="btn-row" style="justify-content:center"><a class="btn" href="/">Go to homepage</a><a class="btn btn--ghost" href="/services/">See services</a></div></div></section>""",
                ["pages/legal.css"], [], None, noindex=True)
    html = html.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="./"', 'href="/"')
    html = html.replace('href="services/', 'href="/services/').replace('href="work/', 'href="/work/').replace('href="pricing/', 'href="/pricing/')
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def build_seo_files():
    urls = [u for u in BUILT if u != "thank-you/"]
    priority = lambda u: "1.0" if u == "" else ("0.9" if u.startswith("website-designer") else "0.8")
    items = "".join(f"<url><loc>{DOMAIN}/{u}</loc><changefreq>monthly</changefreq><priority>{priority(u)}</priority></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_dev/\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    bundle_assets()
    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    for c in CITIES:
        build_city(c)
    build_pricing()
    build_work()
    build_about()
    build_contact()
    build_blog()
    build_utility()
    build_seo_files()
    print(f"Built {len(BUILT)} pages + 404.html, sitemap.xml, robots.txt")
