# PixelLoom website

A static HTML, CSS and JavaScript website for a web designer serving Coimbatore and Tiruppur. It has 20 pages plus a 404 page, clean SEO-friendly URLs and no build tools needed to host it.

## Folder structure

```
/                           Home page (index.html)
/services/                  All services
/custom-website-development/   Platform hub: HTML
/wordpress-website-development/ Platform hub: WordPress
/shopify-website-development/   Platform hub: Shopify
/ecommerce-website-development/ Service
/landing-page-design/           Service
/website-maintenance/           Service
/website-for-boutiques/         Industry page
/website-for-saree-sellers/     Industry page
/website-designer-coimbatore/   City page
/website-designer-tiruppur/     City page
/pricing/  /work/  /about/  /contact/  /blog/
/privacy-policy/  /terms/  /thank-you/ (noindex)  404.html
sitemap.xml  robots.txt

assets/css/base/        tokens (colours, type, spacing), reset, typography
assets/css/layout/      layout, header, footer
assets/css/components/  buttons, animations, weave, marquee, service list, process, FAQ, forms, CTA
assets/css/pages/       one file per page type (home, service, city, pricing, work, about, contact, blog, legal)
assets/js/              main (header, menu, scroll thread), reveal, weave, process, faq, pricing tabs, contact form, work filter
assets/img/             favicon.svg, og-image.png (social sharing)
_dev/                   page generator (Python). Do not upload this folder to your host.
```

Each page loads only the CSS and JS files it needs.

## Preview on your computer

Pages link to folders (for example `pricing/`), so open the site through a local server, not by double-clicking files:

- VS Code: install the "Live Server" extension, right-click `index.html`, choose "Open with Live Server".
- Or in a terminal inside this folder: `python -m http.server` and open http://localhost:8000

## Before you publish: replace these

| What | Where |
| --- | --- |
| Prices shown as ₹X,XXX | `_dev/content_services.py` (PRICE) and `_dev/build.py` (pricing tables), then rebuild |
| WhatsApp number, phone, email, Instagram, domain | Top of `_dev/layout.py`, then rebuild |
| Brand name "PixelLoom" | `BRAND` in `_dev/layout.py` (and `assets/img/og-image.png`) |
| Case study text and results | `WORK` list in `_dev/build.py`. Add real results (speed, orders) once you have them |
| Your photo | About page: replace the initial in `.portrait` with an `<img>` |
| Privacy policy date | `build_utility()` in `_dev/build.py` |

Easiest way to edit: change the Python files in `_dev/`, then run `python _dev/build.py` from this folder. Every page is regenerated with the same header, footer and SEO tags. You can also edit the HTML files directly, but then don't rebuild, or your edits will be overwritten.

## What's built in for SEO

- One H1 per page, title tags and meta descriptions per page, canonical URLs.
- Structured data (JSON-LD): ProfessionalService, Service, FAQPage, BreadcrumbList, Person, WebSite.
- Open Graph tags for WhatsApp and social previews.
- sitemap.xml and robots.txt (update the domain in `_dev/layout.py` first).
- Fast by design: no frameworks, small CSS and JS, deferred scripts, system-font fallbacks.
- Accessible: skip link, keyboard-friendly menus, tabs and FAQ, visible focus, reduced-motion support.

## After launch

1. Submit `https://yourdomain/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
2. Add Google Analytics 4 and mark WhatsApp clicks and the thank-you page as conversions.
3. Set up your Google Business Profile with the same name, phone and service areas.
4. Test with PageSpeed Insights and Google's Rich Results Test.

## Next pages to add (from the SEO plan)

Business websites, Shopify theme customization, website redesign, migration and speed optimization service pages; Erode, Chennai and Bengaluru city pages; and the blog posts listed on the blog page. Add new services to `SERVICES` in `_dev/content_services.py` and they get the full page template automatically.
