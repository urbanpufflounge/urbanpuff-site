#!/usr/bin/env python3
"""
Build the static Urban Puff site.

Edit the SITE dict and the page bodies below, then run:  python3 tools/build.py
Output: plain .html files in the repo root, ready for GitHub Pages.
"""
import os, re, json, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import art

SITE = {
    "name": "Urban Puff",
    # Matches the Google Business Profile exactly (ampersand, not "and").
    # HTML-escaped because it is written into markup; full_plain is for JSON-LD.
    "full": "Urban Puff Lounge &amp; Bar",
    "full_plain": "Urban Puff Lounge & Bar",
    # Kept for search: people type and link both spellings.
    "full_alt": "Urban Puff Lounge and Bar",
    "tagline": "Hookah • Mocktails • Food • Good Vibes",
    "domain": "https://urbanpufflounge.com",
    # No inbox address is stored anywhere in this repository. Forms post to the
    # FormSubmit "invisible email" endpoint below, which resolves to the inbox on
    # their side. To point the forms at a different inbox, activate it with
    # FormSubmit and swap the string in form_token.
    "email_b64": "",

    # What the form actually posts to. Two ways to fill this in:
    #   "hash:<string>"  a FormSubmit hashed endpoint (get it from the activation
    #                    email after your first live submission) — the address is
    #                    then completely absent from the site. BEST.
    #   ""               leave empty and the address is base64-encoded into
    #                    assets/js/forms.js instead. Keeps mail harvesters and
    #                    search engines off it, but it is obfuscation, not removal.
    "form_token": "hash:107255ed9e810f4577564bb36d288488",
    "instagram": "https://www.instagram.com/urbanpuff.562/",
    "street": "562 Wylie Rd SE, Suite 3",
    "city": "Marietta",
    "state": "GA",
    "zip": "30067",
    # ---- SINGLE SOURCE OF TRUTH FOR HOURS -------------------------------
    # "close" may exceed 24:00 to mean "closes after midnight" (25:00 = 1 AM).
    # days: 0 = Sunday ... 6 = Saturday
    "hours_data": [
        {"label": "Sunday \u2013 Thursday", "days": [0, 1, 2, 3, 4], "open": "13:00", "close": "25:00"},
        {"label": "Friday \u2013 Saturday", "days": [5, 6],          "open": "13:00", "close": "27:00"},
    ],
    "age": "21+ with valid ID",

    # Exact coordinates from the Google Maps listing.
    "lat": "33.9381686",
    "lon": "-84.511845",

    # The venue's own Google Maps listing.
    "maps_share": "https://maps.app.goo.gl/qtieLH7uMNx3AroJ8",
    "maps_cid": "https://maps.google.com/?cid=3518202901293435740",

    # Places we genuinely serve, used in the local-relevance copy and schema.
    "area_served": ["Marietta", "Kennesaw", "Smyrna", "Austell", "Powder Springs",
                    "Mableton", "Vinings", "Dobbins ARB", "Cobb County", "Atlanta"],

    # Leave blank until you have a public number. Fill it in and the call
    # buttons, the sticky mobile bar, the footer and the Google schema all
    # light up automatically.
    "phone": "(404) 706-5717",
    "phone_intl": "+14047065717",

    # What's on this week. Edit freely — this is the bit worth keeping fresh.
    "specials": [
        ("Monday", "Industry Night", "Service and hospitality staff get the lounge rate all night. Bring your badge."),
        ("Tuesday", "Two-for-Tuesday", "Second hookah bowl half price when you order food."),
        ("Wednesday", "Game Night", "Cards, dominoes and whatever's on the big screen."),
        ("Thursday", "Ladies Night", "Complimentary mocktail with any hookah, all night."),
        ("Friday &amp; Saturday", "Late Sessions", "DJ on the decks, kitchen open late, room full."),
        ("Sunday", "Slow Sunday", "Sports on every screen and the unhurried version of us."),
    ],

    # Shisha flavours — the thing hookah guests actually come to browse.
    "flavours": [
        ("Mint &amp; Fresh", ["Double Apple", "Mint", "Lemon Mint", "Blue Mist", "Ice Watermelon", "Gum Mint"]),
        ("Fruit", ["Watermelon", "Grape", "Peach", "Mango", "Passion Fruit", "Berry Mix", "Pineapple", "Guava"]),
        ("Sweet &amp; Dessert", ["Vanilla", "Chocolate Mint", "Bubblegum", "Cinnamon Roll", "Rose", "Love 66"]),
        ("House Mixes", ["Urban Sunset", "562 Blend", "Wylie Chill", "Midnight Mint", "Peach Paradise", "Ask the Floor"]),
    ],

    "faqs": [
        ("Do I need a reservation?",
         "Walk-ins are always welcome, but Friday and Saturday fill up fast and big groups almost always need a table held. Reserving takes a minute and costs nothing."),
        ("How old do I have to be?",
         "21 and over, with valid photo ID. Everyone gets carded at the door \u2014 no exceptions, no matter who you came with."),
        ("Can we book the place for a birthday or private party?",
         "Yes. Tell us the date, the headcount and roughly what you have in mind and we'll put a plan together. Birthdays, graduations, watch parties, work nights out \u2014 we do all of it."),
        ("Is there parking?",
         "Free lot parking right in front of the suite. No meters, no garage, no walking three blocks in the cold."),
        ("Do you serve alcohol?",
         "We're a mocktail bar \u2014 everything at the bar is zero proof, made fresh and built to actually taste like something."),
        ("Can you handle dietary requirements?",
         "Plenty of the kitchen is vegetarian, and we can adapt a lot of the grill. Message us before you come and we'll sort it out properly."),
        ("How long can we stay?",
         "As long as you like. Coals get refreshed through the night and nobody is going to hover over your table."),
    ],
}


def _fmt(hhmm):
    """16:00 -> 4:00 PM ; 26:00 -> 2:00 AM ; 24:00 -> 12:00 AM"""
    h, m = (int(x) for x in hhmm.split(":"))
    h %= 24
    suffix = "AM" if h < 12 else "PM"
    disp = h % 12 or 12
    return "%d:%02d %s" % (disp, m, suffix)


_SCHEMA_DAYS = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
_SCHEMA_FULL_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday"]

SITE["hours"] = [
    (b["label"], "%s \u2013 %s" % (_fmt(b["open"]), _fmt(b["close"])))
    for b in SITE["hours_data"]
]
SITE["hours_schema"] = [
    '"%s %s-%s"' % (
        ",".join(_SCHEMA_DAYS[d] for d in b["days"]),
        b["open"],
        "%02d:%02d" % (int(b["close"].split(":")[0]) % 24, int(b["close"].split(":")[1])),
    )
    for b in SITE["hours_data"]
]
SITE["place_id"] = ""   # fill in to enable live Google hours (see assets/js/hours.js)
SITE["phone_tel"] = SITE.get("phone_intl") or "".join(
    c for c in SITE["phone"] if c.isdigit() or c == "+")
SITE["has_phone"] = bool(SITE["phone"])

SITE["address_one_line"] = "{street}, {city}, {state} {zip}".format(**SITE)
# Directions / listing links go to the venue's own Google Maps place.
SITE["maps"] = SITE["maps_share"]
# The iframe still needs a query URL — short links can't be embedded.
SITE["maps_embed"] = ("https://www.google.com/maps?q="
                      + SITE["address_one_line"].replace(" ", "%20").replace(",", "%2C")
                      + "&output=embed")

NAV = [
    ("index.html", "Home"),
    ("menu.html", "Menu"),
    ("gallery.html", "Gallery"),
    ("visit.html", "Visit"),
]

# --------------------------------------------------------------------------- #
#  Shared chrome
# --------------------------------------------------------------------------- #

def business_schema():
    """LocalBusiness / BarOrPub — the block Google reads for the knowledge panel."""
    spec = ",".join(
        '''
    {"@type":"OpeningHoursSpecification","dayOfWeek":[%s],"opens":"%s","closes":"%s"}'''
        % (",".join('"%s"' % _SCHEMA_FULL_DAYS[d] for d in b["days"]),
           b["open"],
           "%02d:%02d" % (int(b["close"].split(":")[0]) % 24, int(b["close"].split(":")[1])))
        for b in SITE["hours_data"]
    )
    areas = ",".join('{"@type":"City","name":"%s"}' % a for a in SITE["area_served"])
    phone = ('\n  "telephone": "%s",' % SITE["phone_tel"]) if SITE["has_phone"] else ""
    return f'''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": ["BarOrPub", "Restaurant"],
  "@id": "{SITE['domain']}/#business",
  "name": "{SITE['full_plain']}",
  "alternateName": ["{SITE['name']}", "{SITE['full_alt']}", "Urban Puff Hookah Lounge"],
  "description": "Premium hookah lounge and bar in Marietta, Georgia. Top-shelf shisha and house flavour mixes, Mediterranean mezze, kabobs and desi bites, mocktails shaken to order, sports on the big screens, free Wi-Fi and comfortable seating. Open late seven nights a week.",
  "url": "{SITE['domain']}/",
  "image": ["{SITE['domain']}/assets/img/og-image.jpg"],
  "logo": "{SITE['domain']}/assets/img/logo.svg",
{phone}
  "priceRange": "$$",
  "currenciesAccepted": "USD",
  "paymentAccepted": "Cash, Credit Card, Debit Card, Mobile Payment",
  "servesCuisine": ["Hookah", "Indian", "Pakistani", "Middle Eastern", "American"],
  "acceptsReservations": "True",
  "smokingAllowed": true,
  "publicAccess": true,
  "hasMenu": "{SITE['domain']}/menu.html",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{SITE['street']}",
    "addressLocality": "{SITE['city']}",
    "addressRegion": "{SITE['state']}",
    "postalCode": "{SITE['zip']}",
    "addressCountry": "US"
  }},
  "geo": {{"@type": "GeoCoordinates", "latitude": "{SITE['lat']}", "longitude": "{SITE['lon']}"}},
  "hasMap": "{SITE['maps']}",
  "areaServed": [{areas}],
  "openingHoursSpecification": [{spec}
  ],
  "amenityFeature": [
    {{"@type":"LocationFeatureSpecification","name":"Premium hookah","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Free Wi-Fi","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Free parking","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Live sports on screen","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Group and private bookings","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Vegetarian options","value":true}},
    {{"@type":"LocationFeatureSpecification","name":"Open late","value":true}}
  ],
  "potentialAction": {{
    "@type": "ReserveAction",
    "target": {{
      "@type": "EntryPoint",
      "urlTemplate": "{SITE['domain']}/reserve.html",
      "actionPlatform": [
        "http://schema.org/DesktopWebPlatform",
        "http://schema.org/MobileWebPlatform"
      ]
    }},
    "result": {{"@type": "Reservation", "name": "Table reservation at {SITE['full_plain']}"}}
  }},
  "sameAs": ["{SITE['instagram']}"]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "{SITE['domain']}/#website",
  "url": "{SITE['domain']}/",
  "name": "{SITE['full_plain']}",
  "alternateName": "{SITE['full_alt']}",
  "publisher": {{"@id": "{SITE['domain']}/#business"}},
  "inLanguage": "en-US"
}}
</script>'''


def breadcrumb_schema(page, label):
    return '''
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},
{"@type":"ListItem","position":2,"name":"%s","item":"%s/%s"}]}
</script>''' % (SITE["domain"], label, SITE["domain"], page)


def head(page, title, desc, extra_schema=""):
    canonical = SITE["domain"] + "/" + ("" if page == "index.html" else page)
    noindex = page in ("thank-you.html", "404.html")
    robots = ("noindex, follow" if noindex
              else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    schema = "" if noindex else (business_schema() if page == "index.html" else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b0a09">
<meta name="author" content="{SITE['full']}">
<meta name="keywords" content="Urban Puff Lounge &amp; Bar, Urban Puff Lounge and Bar, Urban Puff Marietta, hookah lounge Marietta GA, hookah bar near me, premium hookah lounge Atlanta, shisha Marietta, hookah and food Marietta, mocktail bar Marietta, Cobb County hookah lounge">

<meta name="geo.region" content="US-GA">
<meta name="geo.placename" content="{SITE['city']}, {SITE['state']}">
<meta name="geo.position" content="{SITE['lat']};{SITE['lon']}">
<meta name="ICBM" content="{SITE['lat']}, {SITE['lon']}">

<meta property="og:type" content="{"business.business" if page == "index.html" else "website"}">
<meta property="og:site_name" content="{SITE['full']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{SITE['domain']}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{SITE['full']} \u2014 premium hookah lounge in Marietta, Georgia">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE['domain']}/assets/img/og-image.jpg">

<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/logo.svg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.className += " js";</script>{schema}{extra_schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>'''


def header(page):
    parts = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ''
        parts.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    links = "".join(parts)
    return f'''
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="index.html">
      <img class="brand__mark" src="assets/img/logo.svg" alt="" width="38" height="38">
      <span class="brand__name">{SITE['name']}<span class="brand__sub">Lounge &amp; Bar</span></span>
    </a>
    <button class="nav__toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <div class="nav__links" id="nav-links">
      {links}
      <a class="btn btn--solid nav__cta" href="reserve.html">Reserve</a>
    </div>
  </nav>
</header>
<main id="main">'''


IG_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.07-1.1.05-1.7.24-2.1.4-.5.2-.9.44-1.3.83-.4.4-.63.8-.83 1.3-.16.4-.35 1-.4 2.1C2.6 9.9 2.6 10.3 2.6 12s0 2.1.07 3.3c.05 1.1.24 1.7.4 2.1.2.5.44.9.83 1.3.4.4.8.63 1.3.83.4.16 1 .35 2.1.4 1.2.07 1.6.07 4.7.07s3.5 0 4.7-.07c1.1-.05 1.7-.24 2.1-.4.5-.2.9-.44 1.3-.83.4-.4.63-.8.83-1.3.16-.4.35-1 .4-2.1.07-1.2.07-1.6.07-3.3s0-2.1-.07-3.3c-.05-1.1-.24-1.7-.4-2.1-.2-.5-.44-.9-.83-1.3-.4-.4-.8-.63-1.3-.83-.4-.16-1-.35-2.1-.4C15.5 4 15.1 4 12 4zm0 3.1a4.9 4.9 0 110 9.8 4.9 4.9 0 010-9.8zm0 8a3.1 3.1 0 100-6.2 3.1 3.1 0 000 6.2zm6.3-8.2a1.15 1.15 0 11-2.3 0 1.15 1.15 0 012.3 0z"/></svg>'
MAIL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4.24l-8 4.99-8-4.99V6l8 5 8-5v2.24z"/></svg>'
MAP_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>'


def footer():
    if SITE["has_phone"]:
        primary_action = (
            '<a href="tel:%s"><svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M6.5 3h3l1.5 4-2 1.5a12 12 0 006.5 6.5L17 13l4 1.5v3a2 2 0 01-2.2 2A16.5 16.5 0 014.5 5.2 2 2 0 016.5 3z"/>'
            '</svg><span>Call</span></a>' % SITE["phone_tel"]
        )
    else:
        primary_action = (
            '<a href="contact.html"><svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M21 15a2 2 0 01-2 2H8l-4 4V5a2 2 0 012-2h13a2 2 0 012 2z"/>'
            '</svg><span>Message</span></a>'
        )
    hours = "".join(
        f'<li><span style="color:var(--text)">{d}</span><br><span style="color:var(--text-faint);font-size:.86rem">{h}</span></li>'
        for d, h in SITE["hours"]
    )
    return f'''</main>

<div class="action-bar" aria-label="Quick actions">
  {primary_action}
  <a href="reserve.html"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg><span>Reserve</span></a>
  <a href="{SITE['maps']}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-7.2 7-12a7 7 0 10-14 0c0 4.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.6"/></svg><span>Directions</span></a>
</div>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:1.1rem">
          <img class="brand__mark" src="assets/img/logo.svg" alt="" width="38" height="38">
          <span class="brand__name">{SITE['name']}<span class="brand__sub">Lounge &amp; Bar</span></span>
        </a>
        <p style="color:var(--text-faint);font-size:.9rem;max-width:30ch">{SITE['tagline']}</p>
        <div class="socials" style="margin-top:1.2rem">
          <a href="{SITE['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
          <a href="contact.html" aria-label="Send us a message">{MAIL_SVG}</a>
          <a href="{SITE['maps']}" target="_blank" rel="noopener" aria-label="Directions">{MAP_SVG}</a>
        </div>
      </div>
      <div>
        <h2 class="footer-head">Visit</h2>
        <p>{SITE['street']}<br>{SITE['city']}, {SITE['state']} {SITE['zip']}</p>
        <p><a href="tel:{SITE['phone_tel']}">{SITE['phone']}</a></p>
        <p><a href="{SITE['maps']}" target="_blank" rel="noopener">Get directions &rarr;</a></p>
        <p style="font-size:.82rem;color:var(--text-faint);margin-top:.8rem">{SITE['age']}</p>
      </div>
      <div>
        <h2 class="footer-head">Hours</h2>
        <ul style="font-size:.9rem;line-height:1.5">{hours}</ul>
      </div>
      <div>
        <h2 class="footer-head">Explore</h2>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="menu.html">Menu</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="visit.html">Visit &amp; Hours</a></li>
          <li><a href="reserve.html">Reserve a Table</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>{datetime.date.today().year}</span> {SITE['full']}. All rights reserved.</span>
      <span>Marietta, Georgia &middot; <a href="tel:{SITE['phone_tel']}">{SITE['phone']}</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
<script src="assets/js/hours.js"></script>
<script src="assets/js/forms.js"></script>
</body>
</html>'''


def hours_panel(note=True):
    """Hours block: renders instantly, upgraded live by assets/js/hours.js."""
    rows = "".join(
        '<div class="hours-row" data-days="%s"><span>%s</span><span>%s</span></div>'
        % (",".join(str(d) for d in b["days"]), label, times)
        for b, (label, times) in zip(SITE["hours_data"], SITE["hours"])
    )
    data = json.dumps([
        {"days": b["days"], "open": b["open"], "close": b["close"]}
        for b in SITE["hours_data"]
    ], separators=(",", ":"))
    source = ""
    if note:
        source = (
            '<p class="hours-source" data-hours-note>Hours can change for holidays and '
            'private events \u2014 <a href="%s" target="_blank" rel="noopener">check our '
            'Google listing</a> for the latest.</p>' % SITE["maps"]
        )
    return (
        '<div class="hours-panel" data-hours>'
        '<span class="hours-status" data-hours-status></span>'
        '<div data-hours-list>%s</div>%s'
        '<script type="application/json" data-hours-data>%s</script>'
        '</div>' % (rows, source, data)
    )


def page(filename, title, desc, body, extra_schema=""):
    html = head(filename, title, desc, extra_schema) + header(filename) + body + footer()
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, len(html), "bytes")


def page_head(eyebrow, h1, lede):
    return f'''
<section class="page-head">
  <div class="wrap page-head__inner">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>'''


def icon(path):
    return f'<div class="card__icon"><svg viewBox="0 0 24 24" aria-hidden="true">{path}</svg></div>'


ICONS = {
    "hookah": '<path d="M12 3v3M9.5 3h5M10 6h4l-.8 4h-2.4z"/><path d="M12 10v4"/><path d="M12 14c-3.3 0-5.5 2.2-5.5 4.9S8.7 22 12 22s5.5-1.4 5.5-3.1S15.3 14 12 14z"/><path d="M12 12c3.2 0 5.4 1.1 6.3 3.3"/>',
    "seat": '<path d="M4 11V7a2 2 0 012-2h12a2 2 0 012 2v4"/><path d="M3 11h18v6H3z"/><path d="M6 17v3M18 17v3"/>',
    "wifi": '<path d="M2.5 9a15 15 0 0119 0"/><path d="M5.5 12.5a10.5 10.5 0 0113 0"/><path d="M8.5 16a6 6 0 017 0"/><circle cx="12" cy="19.5" r="1"/>',
    "music": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    "tv": '<rect x="2.5" y="4" width="19" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "chef": '<path d="M7 21h10M7 21v-4h10v4"/><path d="M17 17a5 5 0 001-9.9A4 4 0 0012 5a4 4 0 00-6 2.1A5 5 0 007 17"/>',
    "glass": '<path d="M5 4h14l-6 8v6"/><path d="M9 20h6"/><path d="M6.5 7.5h11"/>',
    "cake": '<path d="M3 21h18"/><path d="M4 21v-6a2 2 0 012-2h12a2 2 0 012 2v6"/><path d="M12 13V9M9 13V9M15 13V9"/><path d="M12 6.5c0-1 1-1.5 1-2.5M9 6.5c0-1 1-1.5 1-2.5M15 6.5c0-1 1-1.5 1-2.5"/>',
}


# --------------------------------------------------------------------------- #
#  Pages
# --------------------------------------------------------------------------- #

def build_home():
    features = [
        ("hookah", "Premium Hookah", "Top-shelf shisha, clean heat management and a flavour list that runs from classic mint to house-blend mixes. Set up fresh, tended all night."),
        ("seat", "Comfortable Seating", "Deep lounge sofas, low tables and booths made for long sessions with a big group or a quiet two."),
        ("wifi", "Free Wi-Fi", "Fast, free and open to every guest \u2014 work late, stream, or just keep the group chat going."),
        ("music", "Great Music", "Afrobeats, hip-hop, R&B and Desi hits \u2014 the playlist moves with the room, and the volume stays talk-friendly."),
        ("tv", "Sports on Screen", "Big screens on the wall for the game \u2014 football, cricket, basketball, the fights. Come early for a good seat."),
        ("chef", "Kitchen Till Late", "Mezze, kabobs, tikka and bar bites \u2014 with wings, fries, samosas and Chicken 65 still coming out after midnight."),
    ]
    cards = "".join(
        '''
      <article class="card reveal">
        %s
        <h3>%s</h3>
        <p>%s</p>
      </article>''' % (icon(ICONS[k]), t, d) for k, t, d in features
    )

    showcase_items = [
        ("hookah",   "hookah.jpg",   "The Bowl",    "Premium Hookah",      "House mixes and single-origin shisha, packed fresh and coal-managed all night so the last pull is as good as the first."),
        ("grill",    "grill.jpg",    "The Grill",   "Kabobs &amp; Tikka",  "Chicken kabob, hariyali tikka, paneer tikka and weekend lamb chops \u2014 skewered to order and charred hard over open heat."),
        ("mocktail", "mocktail.jpg", "The Bar",     "Mocktails",           "Zero proof, full flavour. Fresh fruit, real citrus and a proper shake \u2014 built to stand up to the grill."),
        ("lounge",   "latenight.jpg", "After Midnight", "Late-Night Bites", "Wings, fries, samosas and Chicken 65 \u2014 the kitchen keeps going long after most places have closed."),
    ]
    showcase = "".join(
        '''
      <article class="card art-card reveal">
        %s
        <div class="art-card__body">
          <span class="tag">%s</span>
          <h3>%s</h3>
          <p>%s</p>
        </div>
      </article>''' % (art.art_slot(kind, alt, photo), tag, alt, desc)
        for kind, photo, tag, alt, desc in showcase_items
    )

    specials = "".join(
        '''
      <article class="special reveal">
        <span class="special__day">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </article>''' % (day, name, blurb) for day, name, blurb in SITE["specials"]
    )

    return '''
<section class="hero">
  <div class="hero__smoke" aria-hidden="true"></div>
  <div class="wrap hero__grid">
    <div class="hero__inner">
      <p class="hero__tag">Marietta, Georgia \u00b7 Open Late</p>
      <h1>Premium hookah lounge &amp; bar in <em>Marietta</em>.</h1>
      <p class="hero__poem">Where the smoke settles and the night opens up.</p>
      <p class="lede">Urban Puff Lounge &amp; Bar is a premium hookah lounge and bar on Wylie Road SE \u2014 top-shelf shisha and house flavour mixes, a kitchen turning out Mediterranean mezze, kabobs and desi bites, mocktails shaken to order, sports on the big screens, and a room built for staying a while.</p>
      <div class="btn-row" style="margin-top:2.2rem">
        <a class="btn btn--solid" href="reserve.html">Reserve a table</a>
        <a class="btn btn--ghost" href="menu.html">See the menu</a>
      </div>
      <div class="hero__meta">
        <span>Premium Hookah</span>
        <span>Mocktails</span>
        <span>Kitchen &amp; Grill</span>
        <span>Sports on Screen</span>
        <span>Free Wi-Fi</span>
      </div>
    </div>
    <div class="hero__art">
      %s
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">The Lounge</p>
        <h2>Good vibes, on purpose.</h2>
      </div>
      <div class="reveal">
        <p class="lede">We built Urban Puff around the simple things that make a night worth staying out for: a hookah that actually pulls right, food that comes out hot, a drink that doesn\u2019t need alcohol to be interesting, and seats you don\u2019t want to get up from.</p>
        <p class="lede">Whether it\u2019s a birthday table of fifteen, a game night with the guys, or a slow Tuesday with one friend and one bowl \u2014 the room makes space for it.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--3">%s
    </div>
  </div>
</section>

<section class="section band">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="center" style="margin-bottom:3.2rem">
      <p class="eyebrow">From the Kitchen &amp; Bar</p>
      <h2>Eat well. Sip well. Stay late.</h2>
      <p class="lede">Four things we care about more than we probably should.</p>
    </div>
    <div class="showcase">%s
    </div>
    <div class="center btn-row" style="margin-top:3rem">
      <a class="btn" href="menu.html">Explore the full menu</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center" style="margin-bottom:3rem">
      <p class="eyebrow">What\u2019s On</p>
      <h2>Every night has a reason.</h2>
      <p class="lede">A different excuse to come out, seven days a week.</p>
    </div>
    <div class="specials">%s
    </div>
  </div>
</section>

<section class="section band">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Parties &amp; Private Hire</p>
        <h2>Birthdays, done properly.</h2>
        <p class="lede">Fifteen people, three hookahs, a table covered in food and the music exactly where you want it. Tell us the date and the headcount and the room is ready before you walk in.</p>
        <ul class="tick-list">
          <li>Tables for up to 25, or the whole room on quieter nights</li>
          <li>Bring your own cake and decorations</li>
          <li>Pre-order platters so nobody waits</li>
          <li>Tell us what to put on the screens</li>
        </ul>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn btn--solid" href="reserve.html">Plan your night</a>
        </div>
      </div>
      <div class="reveal">
        %s
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap" style="max-width:900px">
    <div class="reveal center">
      <p class="eyebrow">Near You</p>
      <h2>A hookah lounge for the whole of Cobb County.</h2>
      <p class="lede">We\u2019re on Wylie Road SE, just off South Marietta Parkway and a couple of minutes from I-75 \u2014 which makes us an easy run from most of the county. Regulars come from <strong>Marietta</strong> and <strong>Kennesaw</strong>, from <strong>Smyrna</strong> and <strong>Vinings</strong> on the way back into the city, and from <strong>Austell</strong>, <strong>Mableton</strong> and <strong>Powder Springs</strong>. Dobbins Air Reserve Base is up the road, and students from Life University and Kennesaw State tend to fill the back booths midweek.</p>
      <p class="lede">We open at <strong>1:00 PM</strong> every day \u2014 earlier than most lounges around here \u2014 so the afternoon crowd gets the room before the night crowd arrives. If you\u2019ve been searching for a hookah bar near you that is still serving food at 1 AM \u2014 or 3 AM on Fridays and Saturdays \u2014 this is it.</p>
      <div class="btn-row center" style="margin-top:1.8rem">
        <a class="btn btn--ghost" href="menu.html">Browse the shisha flavour board</a>
        <a class="btn btn--ghost" href="visit.html">Hours, parking and FAQ</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Find Us</p>
        <h2>562 Wylie Rd SE, Suite&nbsp;3</h2>
        <p class="lede">Tucked just off Wylie Road in Marietta, minutes from South Marietta Parkway with easy parking out front.</p>
        <div style="margin:2rem 0 1.5rem">%s</div>
        <p style="font-size:.84rem;color:var(--text-faint)">%s. Follow along on <a href="%s" target="_blank" rel="noopener">Instagram</a> for what\u2019s on tonight.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--solid" href="%s" target="_blank" rel="noopener">Get directions</a>
          %s
        </div>
      </div>
      <div class="reveal map-frame">
        <iframe title="Map to Urban Puff Lounge &amp; Bar" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="%s"></iframe>
      </div>
    </div>
  </div>
</section>

<section class="section band">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap center" style="position:relative;z-index:2">
    <h2>Bringing the whole crew?</h2>
    <p class="lede">Tell us the date and the headcount and we\u2019ll get a table ready. Birthdays, watch parties, after-work sessions \u2014 send us a message.</p>
    <div class="btn-row" style="margin-top:1.8rem">
      <a class="btn btn--solid" href="contact.html">Send us a message</a>
    </div>
  </div>
</section>''' % (
        art.art_slot("lounge", "Inside the Urban Puff lounge", "lounge.jpg"),
        cards,
        showcase,
        specials,
        art.art_slot("grill", "A table set for a group", "party.jpg"),
        hours_panel(),
        SITE["age"],
        SITE["instagram"],
        SITE["maps"],
        ('<a class="btn btn--ghost" href="tel:%s">Call %s</a>'
         % (SITE["phone_tel"], SITE["phone"])) if SITE["has_phone"]
        else '<a class="btn btn--ghost" href="reserve.html">Reserve a table</a>',
        SITE["maps_embed"],
    )


def build_menu():
    cats = [
        ("Premium Hookah", "hookah", "Fresh bowls, clean heat, tended all night.", [
            ("Classic Single Hose", "Your pick of flavour, set up fresh with managed coals.", ""),
            ("Double Hose Setup", "Built for sharing — two hoses, one bowl, same session.", "Popular"),
            ("House Mixes", "Our own blends — ask the floor for tonight's board.", "House"),
            ("Fruit Bowl Head", "Shisha packed in a fresh-cut pineapple, melon or grapefruit.", "Signature"),
            ("Mint &amp; Citrus Range", "Double apple, mint, lemon-mint, blue mist and the classics.", ""),
            ("Coal Refresh", "Coals swapped through the night so the bowl never goes flat.", ""),
        ]),
        ("Mezze &amp; Dips", "chef", "Mediterranean small plates, made for the table.", [
            ("Hummus", "Chickpea dip, olive oil, warm pita.", ""),
            ("Baba Ganoush", "Smoky roasted eggplant dip, warm pita.", ""),
            ("Falafel (6 pc)", "Crispy chickpea balls, tahini.", "Veg"),
            ("Mezze Platter", "Hummus, baba ganoush, falafel, olives, warm pita. Made for the table.", "To Share"),
        ]),
        ("From the Grill", "chef", "Marinated, skewered and charred to order.", [
            ("Chicken Kabob", "Grilled skewers, Mediterranean rice, garlic sauce.", ""),
            ("Hariyali Chicken Tikka", "Mint-cilantro marinade, charred on the grill.", ""),
            ("Paneer Tikka", "Hariyali-marinated paneer, peppers, onion.", "Veg"),
            ("Lamb Chops (4 pc)", "Chef\u2019s special, mint yogurt. Fri &amp; Sat, while they last.", "Chef\u2019s Special"),
        ]),
        ("Bar Bites", "chef", "Desi and classic bites while the bowl gets going.", [
            ("Chicken Wings (8 pc)", "Lemon pepper \u00b7 Buffalo \u00b7 Peri-peri.", ""),
            ("Fries", "Classic \u00b7 Za\u2019atar \u00b7 Masala.", "Veg"),
            ("Samosas (3 pc)", "Spiced potato &amp; peas, mint and tamarind chutney.", "Veg"),
            ("Chicken 65", "Crispy fried chicken, curry leaf, red chili.", ""),
        ]),
        ("Wraps &amp; Plates", "chef", "Something more filling.", [
            ("Chicken Shawarma", "Wrap, or plate with rice &amp; Greek salad. Garlic sauce, pickles.", ""),
            ("Greek Salad", "Feta, olives, cucumber, tomato, red onion. Add chicken.", "Veg"),
        ]),
        ("Refreshing Mocktails", "glass", "Zero proof, full flavour — shaken to order.", [
            ("Passion Fruit Cooler", "Passion fruit, citrus and soda over crushed ice.", "Signature"),
            ("Virgin Mojito", "Lime, mint and sugar, muddled fresh.", ""),
            ("Mango Lassi", "Thick, cold and lightly sweet.", ""),
            ("Berry Crush", "Mixed berries, lemon and a long pour of soda.", ""),
            ("Ginger Lemonade", "Sharp, fizzy and made to cut through the grill.", ""),
            ("Fresh Juices &amp; Sodas", "Ask what's fresh tonight.", ""),
        ]),
    ]

    blocks = []
    for title, ic, blurb, items in cats:
        rows = "".join(f'''
        <div class="menu-item">
          <p class="menu-item__name">{n}{f'<span class="tag">{tag}</span>' if tag else ''}</p>
          <p class="menu-item__desc">{d}</p>
        </div>''' for n, d, tag in items)
        blocks.append(f'''
    <div class="menu-cat reveal">
      <div class="menu-cat__head">
        <h3>{title}</h3>
        <hr class="rule">
      </div>
      <p class="menu-item__desc" style="margin-bottom:1.6rem;font-style:italic">{blurb}</p>
      <div class="menu-list">{rows}
      </div>
    </div>''')

    return page_head(
        "The Menu",
        "Off the grill, out of the bar,<br>onto your table.",
        "Mediterranean \u00b7 Desi bites. Prices and daily specials are on the in-house menu \u2014 ask your server what\u2019s on tonight."
    ) + flavour_section() + f'''
<section class="section">
  <div class="wrap">{''.join(blocks)}
    <div class="center reveal" style="margin-bottom:2.5rem">
      <p class="eyebrow">Late Night \u00b7 After Midnight</p>
      <p class="lede">Wings \u00b7 Fries \u00b7 Samosas \u00b7 Chicken 65</p>
    </div>
    <hr class="rule">
    <p class="center" style="margin-top:2rem;font-size:.9rem;opacity:.75">Please tell your server about any allergies. Consuming raw or undercooked meats may increase your risk of foodborne illness.</p>
    <p class="center lede" style="margin-top:1.5rem">Dietary needs, allergies or a big group order? <a href="contact.html">Message us</a> and we'll sort it out before you arrive.</p>
  </div>
</section>'''


def flavour_section():
    blocks = "".join(
        '''
      <div class="flavour-group reveal">
        <h3>%s</h3>
        <ul class="flavour-list">%s</ul>
      </div>''' % (title, "".join("<li>%s</li>" % f for f in items))
        for title, items in SITE["flavours"]
    )
    return '''
<section class="section section--tight band">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="center" style="margin-bottom:2.6rem">
      <p class="eyebrow">The Flavour Board</p>
      <h2>Pick your bowl.</h2>
      <p class="lede">Single or double hose, packed fresh, coals managed all night. Mixes change with what\u2019s good \u2014 ask the floor for tonight\u2019s board.</p>
    </div>
    <div class="flavour-grid">%s
    </div>
    <p class="center form__note" style="margin-top:2rem">Can\u2019t decide? Tell us what you usually like and we\u2019ll build you something.</p>
  </div>
</section>''' % blocks


def faq_section():
    items = "".join(
        '''
      <details class="faq reveal">
        <summary>%s</summary>
        <div class="faq__body"><p>%s</p></div>
      </details>''' % (q, a) for q, a in SITE["faqs"]
    )
    return '''
<section class="section section--tight">
  <div class="wrap" style="max-width:820px">
    <div class="center" style="margin-bottom:2.4rem">
      <p class="eyebrow">Before You Come</p>
      <h2>Good to know.</h2>
    </div>
    <div class="faq-list">%s
    </div>
  </div>
</section>''' % items


def faq_schema():
    entries = ",".join(
        '''
    {"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'''
        % (json.dumps(q.replace("&amp;", "&")), json.dumps(a.replace("\u2014", "-")))
        for q, a in SITE["faqs"]
    )
    return '''
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s
]}
</script>''' % entries


def build_gallery():
    tiles = [
        ("The lounge floor", "tile--wide"),
        ("Hookah setup", ""),
        ("Off the grill", ""),
        ("Mocktail bar", ""),
        ("Game night", "tile--wide"),
        ("Late night", ""),
        ("The booths", ""),
        ("Sweet endings", ""),
    ]
    ph_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.5" cy="10" r="1.5"/><path d="M21 16l-5-5-5.5 6"/></svg>'
    cells = "".join(f'''
      <figure class="tile {cls} reveal">
        <!-- Replace this placeholder with: <img src="assets/img/{i+1:02d}.jpg" alt="{label}" loading="lazy"> -->
        <figcaption class="tile__ph">{ph_icon}{label}</figcaption>
      </figure>''' for i, (label, cls) in enumerate(tiles))

    return page_head(
        "Gallery",
        "A look inside.",
        "Smoke, plates, screens and the room after dark. Follow along on Instagram for the latest from the floor."
    ) + f'''
<section class="section">
  <div class="wrap">
    <div class="gallery">{cells}
    </div>
    <div class="center" style="margin-top:3rem">
      <a class="btn" href="{SITE['instagram']}" target="_blank" rel="noopener">Follow @urbanpuff.562</a>
    </div>
  </div>
</section>'''


def build_visit():
    hours_rows = hours_panel()
    return page_head(
        "Visit Us",
        "562 Wylie Rd SE, Suite&nbsp;3",
        "Marietta, Georgia — minutes from South Marietta Parkway, with parking out front."
    ) + f'''
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Hours</p>
        <div style="margin-bottom:2rem">{hours_rows}</div>
        <p class="eyebrow">Good to know</p>
        <ul class="info-list">
          <li><span class="info-list__label">Entry</span><span class="info-list__value">{SITE['age']}. Everyone gets carded — no exceptions.</span></li>
          <li><span class="info-list__label">Parking</span><span class="info-list__value">Free lot parking directly in front of the suite.</span></li>
          <li><span class="info-list__label">Groups</span><span class="info-list__value">Large tables and private-hire nights are welcome — <a href="contact.html">message us first</a> so we can hold the space.</span></li>
          <li><span class="info-list__label">Wi-Fi</span><span class="info-list__value">Free for all guests. Ask the floor for the password.</span></li>
          <li><span class="info-list__label">Sports</span><span class="info-list__value">Screens on for the big fixtures. Tell us what you want on and we'll try to get it up.</span></li>
          <li><span class="info-list__label">Payments</span><span class="info-list__value">Card and mobile payments accepted at the bar.</span></li>
        </ul>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn btn--solid" href="{SITE['maps']}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
      <div class="reveal">
        <div class="map-frame" style="margin-bottom:1.6rem">
          <iframe title="Map to Urban Puff Lounge &amp; Bar" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="{SITE['maps_embed']}"></iframe>
        </div>
        <div class="card">
          <h2 class="panel-head">Urban Puff Lounge &amp; Bar</h2>
          <p>{SITE['street']}<br>{SITE['city']}, {SITE['state']} {SITE['zip']}<br><br>
          <a href="tel:{SITE['phone_tel']}">{SITE['phone']}</a><br>
          <a href="contact.html">Send us a message</a><br>
          <a href="{SITE['instagram']}" target="_blank" rel="noopener">@urbanpuff.562</a></p>
        </div>
      </div>
    </div>
  </div>
</section>''' + faq_section()


def build_reserve():
    times = []
    for h in range(13, 24):
        for m in ("00", "30"):
            disp = "%d:%s %s" % (h % 12 or 12, m, "PM" if h >= 12 else "AM")
            times.append(disp)
    times += ["12:00 AM", "12:30 AM", "1:00 AM", "1:30 AM", "2:00 AM", "2:30 AM"]
    time_opts = "".join('<option>%s</option>' % t for t in times)
    size_opts = "".join('<option>%s</option>' % n for n in
                        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                         "11", "12", "13\u201316", "17\u201324", "25+"])
    occasions = ["Just a night out", "Birthday", "Anniversary", "Watch party / game",
                 "Work or team night", "Graduation", "Private hire", "Something else"]
    occ_opts = "".join('<option>%s</option>' % o for o in occasions)

    return page_head(
        "Reservations",
        "Hold your table.",
        "Walk-ins are always welcome \u2014 but Fridays and Saturdays fill up, and groups almost always need a table set aside. Takes a minute, costs nothing."
    ) + f'''
<section class="section">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="reveal">
        <div class="form-panel">
          <h2 class="panel-head">Request a table</h2>
          <p class="form__note" style="margin-bottom:1.8rem">We\u2019ll confirm by text or call as soon as we can. Nothing is charged and nothing is locked in until we come back to you. Coming tonight? <a href="tel:{SITE['phone_tel']}">Call {SITE['phone']}</a> instead.</p>

          <div class="form-status" data-form-status aria-live="polite"></div>

          <!-- Endpoint set at runtime by assets/js/forms.js \u2014 see the note on the
               contact page and SITE["form_token"] in tools/build.py. -->
          <form class="form" data-validate data-form{form_action()} method="POST">
            <input type="hidden" name="_subject" value="TABLE REQUEST from urbanpufflounge.com">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="{SITE['domain']}/thank-you.html">
            <input type="hidden" name="_autoresponse" value="Thanks for your table request at Urban Puff Lounge &amp; Bar. We've received it and will confirm by text or call as soon as we can. Nothing is booked until you hear back from us. \u2014 562 Wylie Rd SE, Suite 3, Marietta, GA 30067">
            <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

            <div class="form__row">
              <div class="field">
                <label for="rdate">Date <span class="req">*</span></label>
                <input id="rdate" name="Date" type="date" required>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="rtime">Time <span class="req">*</span></label>
                <select id="rtime" name="Time" required>
                  <option value="">Choose a time</option>
                  {time_opts}
                </select>
                <span class="err"></span>
              </div>
            </div>

            <div class="form__row">
              <div class="field">
                <label for="rsize">Party size <span class="req">*</span></label>
                <select id="rsize" name="Party Size" required>
                  <option value="">How many of you?</option>
                  {size_opts}
                </select>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="rocc">Occasion</label>
                <select id="rocc" name="Occasion">
                  {occ_opts}
                </select>
                <span class="err"></span>
              </div>
            </div>

            <hr class="rule" style="margin:.6rem 0">

            <div class="form__row">
              <div class="field">
                <label for="rfirst">First name <span class="req">*</span></label>
                <input id="rfirst" name="First Name" type="text" autocomplete="given-name" placeholder="Jordan" required>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="rlast">Last name <span class="req">*</span></label>
                <input id="rlast" name="Last Name" type="text" autocomplete="family-name" placeholder="Ellis" required>
                <span class="err"></span>
              </div>
            </div>

            <div class="form__row">
              <div class="field">
                <label for="rphone">Phone <span class="req">*</span></label>
                <input id="rphone" name="Phone" type="tel" autocomplete="tel" placeholder="(770) 000-0000" required>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="remail">Email <span class="opt">(optional)</span></label>
                <input id="remail" name="Email" type="email" autocomplete="email" placeholder="you@email.com">
                <span class="err"></span>
              </div>
            </div>

            <div class="field">
              <label for="rnotes">Anything we should know? <span class="opt">(optional)</span></label>
              <textarea id="rnotes" name="Notes" style="min-height:110px" placeholder="Birthday for 10, we&#39;d love a booth if there is one. Two of us are vegetarian."></textarea>
              <span class="err"></span>
            </div>

            <p class="form__note">This is a request, not a confirmed booking \u2014 we\u2019ll come straight back to you.</p>
            <div class="btn-row">
              <button class="btn btn--solid" type="submit">Request this table</button>
            </div>
          </form>
        </div>
      </div>

      <div class="reveal">
        <p class="eyebrow">Big group?</p>
        <h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">We do birthdays properly.</h2>
        <p class="lede">Fifteen people, three hookahs, a table of food and the music where you want it. Tell us the date and we\u2019ll set the room up before you get here.</p>
        <ul class="info-list" style="margin-top:1.5rem">
          <li><span class="info-list__label">Groups</span><span class="info-list__value">Tables for up to 25, and the room can be held privately on quieter nights.</span></li>
          <li><span class="info-list__label">Bring</span><span class="info-list__value">Your own cake and decorations are welcome \u2014 just tell us in advance.</span></li>
          <li><span class="info-list__label">Food</span><span class="info-list__value">Pre-order platters for the table so nobody waits when you arrive.</span></li>
          <li><span class="info-list__label">Notice</span><span class="info-list__value">A few days is plenty for most groups. Weekends, the earlier the better.</span></li>
          <li><span class="info-list__label">Entry</span><span class="info-list__value">{SITE['age']} \u2014 every guest, every time.</span></li>
        </ul>
        <div class="map-frame" style="margin-top:2rem">
          <iframe title="Map to Urban Puff Lounge &amp; Bar" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="{SITE['maps_embed']}"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>'''


def build_contact():
    return page_head(
        "Contact",
        "Say hello.",
        "Booking a table, planning a birthday, asking about the menu, or just want to know what's on tonight — drop us a line and we'll come straight back to you."
    ) + f'''
<section class="section">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="reveal">
        <div class="form-panel">
          <h2 class="panel-head">Send us a message</h2>
          <p class="form__note" style="margin-bottom:1.8rem">Everything below goes straight to our inbox &mdash; you stay right here. We\u2019ll get back to you as soon as we can.</p>

          <div class="form-status" data-form-status aria-live="polite"></div>

          <!-- Delivered by FormSubmit (https://formsubmit.co) — no server, no signup.
               data-endpoint is the AJAX endpoint: assets/js/main.js posts there in the
               background, so the visitor stays on this page and sees an inline
               confirmation instead of being bounced to a third-party screen.
               `action` and `_next` are the fallback for visitors with JavaScript off. -->
          <!-- Endpoint set at runtime by assets/js/forms.js \u2014 see the note on the
               contact page and SITE["form_token"] in tools/build.py. -->
          <form class="form" data-validate data-form{form_action()} method="POST">
            <input type="hidden" name="_subject" value="New message from urbanpufflounge.com">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_next" value="{SITE['domain']}/thank-you.html">
            <input type="hidden" name="_autoresponse" value="Thanks for reaching out to Urban Puff Lounge &amp; Bar. We've got your message and someone from the team will get back to you as soon as we can. — 562 Wylie Rd SE, Suite 3, Marietta, GA 30067">
            <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

            <div class="form__row">
              <div class="field">
                <label for="first">First name <span class="req">*</span></label>
                <input id="first" name="First Name" type="text" autocomplete="given-name" placeholder="Jordan" required>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="last">Last name <span class="req">*</span></label>
                <input id="last" name="Last Name" type="text" autocomplete="family-name" placeholder="Ellis" required>
                <span class="err"></span>
              </div>
            </div>

            <div class="form__row">
              <div class="field">
                <label for="phone">Phone <span class="req">*</span></label>
                <input id="phone" name="Phone" type="tel" autocomplete="tel" placeholder="(770) 000-0000" required>
                <span class="err"></span>
              </div>
              <div class="field">
                <label for="email">Email <span class="opt">(optional)</span></label>
                <input id="email" name="Email" type="email" autocomplete="email" placeholder="you@email.com">
                <span class="err"></span>
              </div>
            </div>

            <div class="field">
              <label for="message">Message <span class="req">*</span></label>
              <textarea id="message" name="Message" placeholder="Table for 8 on Saturday around 9pm — is that doable?" required></textarea>
              <span class="err"></span>
            </div>

            <p class="form__note">We'll call or text you back on the number above.</p>
            <div class="btn-row">
              <button class="btn btn--solid" type="submit">Send message</button>
            </div>
          </form>
        </div>
      </div>

      <div class="reveal">
        <p class="eyebrow">Other ways to reach us</p>
        <ul class="info-list">
          <li><span class="info-list__label">Phone</span><span class="info-list__value"><a href="tel:{SITE['phone_tel']}"><strong>{SITE['phone']}</strong></a><br>Quickest way to reach the floor \u2014 call or text.</span></li>
          <li><span class="info-list__label">Message</span><span class="info-list__value">Use the form \u2014 it lands in our inbox and we\u2019ll get back to you as soon as we can.</span></li>
          <li><span class="info-list__label">Instagram</span><span class="info-list__value"><a href="{SITE['instagram']}" target="_blank" rel="noopener">@urbanpuff.562</a> — fastest for what's on tonight</span></li>
          <li><span class="info-list__label">Address</span><span class="info-list__value"><strong>{SITE['street']}</strong><br>{SITE['city']}, {SITE['state']} {SITE['zip']}<br><a href="{SITE['maps']}" target="_blank" rel="noopener">Get directions &rarr;</a></span></li>
          <li><span class="info-list__label">Groups</span><span class="info-list__value">Tell us the date, the headcount and the vibe — we'll hold the right table.</span></li>
        </ul>
        <div class="map-frame" style="margin-top:2rem">
          <iframe title="Map to Urban Puff Lounge &amp; Bar" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="{SITE['maps_embed']}"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>'''


def build_thanks():
    return f'''
<section class="page-head" style="min-height:70svh;display:flex;align-items:center">
  <div class="wrap page-head__inner center">
    <p class="eyebrow">Message sent</p>
    <h1>Thanks — we've got it.</h1>
    <p class="lede">Your message is on its way to the Urban Puff team. We\u2019ll come back to you on the number you gave us as soon as we can.</p>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--solid" href="index.html">Back to home</a>
      <a class="btn btn--ghost" href="menu.html">Browse the menu</a>
    </div>
  </div>
</section>'''


def build_404():
    return f'''
<section class="page-head" style="min-height:70svh;display:flex;align-items:center">
  <div class="wrap page-head__inner center">
    <p class="eyebrow">404</p>
    <h1>This page went up in smoke.</h1>
    <p class="lede">The link you followed doesn't exist — but the lounge does. Try one of these instead.</p>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--solid" href="index.html">Home</a>
      <a class="btn btn--ghost" href="menu.html">Menu</a>
      <a class="btn btn--ghost" href="contact.html">Contact</a>
    </div>
  </div>
</section>'''


PAGES = [
    ("index.html",
     f"Premium Hookah Lounge &amp; Bar in Marietta, GA | {SITE['name']}",
     "Premium hookah lounge and bar at 562 Wylie Rd SE, Marietta GA. Top-shelf shisha, mezze, kabobs and desi bites, mocktails, sports on screen, free Wi-Fi. Open late.",
     build_home, ""),

    ("menu.html",
     f"Hookah Flavours &amp; Food Menu | {SITE['name']}, Marietta GA",
     "The full shisha flavour board and kitchen menu at Urban Puff Lounge, Marietta \u2014 house hookah mixes, mezze and dips, kabobs and tikka, wings, shawarma and mocktails.",
     build_menu, "Menu"),

    ("gallery.html",
     f"Inside Our Hookah Lounge | {SITE['name']}, Marietta GA",
     "A look inside Urban Puff Lounge &amp; Bar in Marietta, Georgia \u2014 the lounge floor, hookah setups, food off the grill, the mocktail bar and the room after dark.",
     build_gallery, "Gallery"),

    ("visit.html",
     f"Hours, Location &amp; FAQ | {SITE['name']} Lounge, Marietta",
     "Urban Puff Lounge hours, parking, age policy and directions. 562 Wylie Rd SE Suite 3, Marietta GA 30067. Open daily from 1:00 PM \u2014 till 1 AM Sun\u2013Thu, 3 AM Fri\u2013Sat.",
     build_visit, "Visit &amp; Hours"),

    ("reserve.html",
     f"Reserve a Table | {SITE['name']} Hookah Lounge, Marietta",
     "Reserve a table at Urban Puff hookah lounge and bar in Marietta, GA. Birthdays, watch parties and groups up to 25 welcome. Takes a minute and costs nothing.",
     build_reserve, "Reserve a Table"),

    ("contact.html",
     f"Contact Us | {SITE['name']} Hookah Lounge &amp; Bar, Marietta",
     "Get in touch with Urban Puff Lounge &amp; Bar, Marietta GA about bookings, large groups, birthdays or the menu. We\u2019ll get back to you as soon as we can.",
     build_contact, "Contact"),

    ("thank-you.html", f"Thank you | {SITE['full']}",
     "Thanks for contacting Urban Puff Lounge &amp; Bar.", build_thanks, ""),

    ("404.html", f"Page not found | {SITE['full']}",
     "That page doesn't exist. Find the menu, hours and reservations for Urban Puff Lounge &amp; Bar in Marietta, GA.", build_404, ""),
]


def form_action():
    """
    With a FormSubmit hashed endpoint there is no address to hide, so the action
    can sit in the HTML again and the form keeps working without JavaScript.
    Without a hash we emit nothing and assets/js/forms.js wires it at runtime.
    """
    tok = SITE["form_token"]
    if tok.startswith("hash:"):
        return ' action="https://formsubmit.co/%s"' % tok[5:]
    return ""


def build_forms_js():
    """
    Writes assets/js/forms.js. The delivery address is never placed in any HTML
    file; this script attaches the endpoint at runtime.
    """
    tok = SITE["form_token"]
    if tok.startswith("hash:"):
        value, hashed = tok[5:], "true"
        note = ("A FormSubmit hashed endpoint. The inbox address does not appear\n"
                "   anywhere in this site.")
    else:
        value = SITE["email_b64"]
        hashed = "false"
        note = ("The address, base64-encoded. This keeps it out of the page source\n"
                "   and away from mail harvesters and crawlers, but anyone who reads\n"
                "   this file can decode it. To remove it properly, set\n"
                '   SITE["form_token"] = "hash:<your FormSubmit string>" and rebuild.')

    js = '''/* Urban Puff — form delivery endpoint.
   %s
   The endpoint is never written into the HTML or into the DOM: it is held in a
   closure here and handed to the submit handler only at the moment of sending,
   so nothing a crawler renders or a scraper parses contains the address.
   Set SITE["form_token"] in tools/build.py; this file is generated. */
(function () {
  'use strict';
  var T = '%s';
  var HASHED = %s;
  var to = HASHED ? T : (window.atob ? window.atob(T) : '');
  window.UP_FORM_TARGET = function (ajax) {
    if (!to) return '';
    return 'https://formsubmit.co/' + (ajax ? 'ajax/' : '') + to;
  };
})();
''' % (note, value, hashed)
    open(os.path.join(ROOT, "assets", "js", "forms.js"), "w").write(js)
    print("wrote assets/js/forms.js (%s)" % ("hashed endpoint" if hashed == "true" else "encoded address"))


def build_sitemap():
    today = datetime.date.today().isoformat()
    weights = {
        "index.html": ("1.0", "weekly"),
        "menu.html": ("0.9", "weekly"),
        "reserve.html": ("0.9", "monthly"),
        "visit.html": ("0.8", "monthly"),
        "gallery.html": ("0.6", "monthly"),
        "contact.html": ("0.6", "monthly"),
    }
    urls = ""
    for f, *_ in PAGES:
        if f not in weights:
            continue
        prio, freq = weights[f]
        loc = SITE["domain"] + "/" + ("" if f == "index.html" else f)
        urls += ('\n  <url><loc>%s</loc><lastmod>%s</lastmod>'
                 '<changefreq>%s</changefreq><priority>%s</priority></url>'
                 % (loc, today, freq, prio))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)
    # GitHub Pages serves everything in the repo, including the docs and the
    # generator. Keep those out of the index — only the pages should rank.
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /thank-you.html\n"
        "Disallow: /docs/\n"
        "Disallow: /tools/\n"
        "Disallow: /README.md\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % SITE["domain"])
    print("wrote sitemap.xml, robots.txt")


def menu_schema():
    sections = ",".join(
        '{"@type":"MenuSection","name":%s}' % json.dumps(name.replace("&amp;", "&"))
        for name in ["Premium Hookah", "Mezze & Dips", "From the Grill", "Bar Bites",
                     "Wraps & Plates", "Refreshing Mocktails"]
    )
    return '''
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Menu","name":"Urban Puff Lounge & Bar menu",
"url":"%s/menu.html","inLanguage":"en-US",
"hasMenuSection":[%s]}
</script>''' % (SITE["domain"], sections)


if __name__ == "__main__":
    for filename, title, desc, fn, crumb in PAGES:
        extra = ""
        if crumb:
            extra += breadcrumb_schema(filename, crumb.replace("&amp;", "&"))
        if filename == "visit.html":
            extra += faq_schema()
        if filename == "menu.html":
            extra += menu_schema()
        page(filename, title, desc, fn(), extra)
    build_forms_js()
    build_sitemap()
    print("\nDone.")
