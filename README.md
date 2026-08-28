# Urban Puff Lounge and Bar — website

Static site for **urbanpufflounge.com**. No frameworks, no build step required to
deploy — GitHub Pages serves the `.html` files in this folder as-is.

```
index.html        Home
menu.html         Flavour board + food menu (categories, no prices)
gallery.html      Photo gallery (placeholders — drop real photos in)
visit.html        Address, hours, parking, FAQ
reserve.html      Table request form (the main conversion page)
contact.html      General contact form -> your inbox
thank-you.html    Shown after the form is submitted
404.html          Not-found page
CNAME             Custom domain for GitHub Pages
.nojekyll         Stops GitHub from running Jekyll over the files
sitemap.xml       Generated
robots.txt        Generated
assets/css/       styles.css — the whole design system
assets/js/        main.js — nav, scroll reveals, form validation
assets/img/       logo.svg + your photos
tools/build.py    Optional generator (see below)
```

## Making changes

Two options — pick one and stick with it.

**A. Edit the HTML directly.** Perfectly fine for a typo or a new menu item.
The header and footer are repeated in every page, so a nav change means
touching each file.

**B. Use the generator (recommended for bigger edits).** All page content lives
in `tools/build.py`. Change the `SITE` dict (hours, address, email) or a page
body, then:

```bash
python3 tools/build.py
```

That rewrites every `.html` file plus `sitemap.xml` and `robots.txt`.
Python 3 only, no dependencies.

## Opening hours

Hours live in **one place**: `SITE["hours_data"]` in `tools/build.py`. Edit that,
run `python3 tools/build.py`, and the home page, the visit page, the footer and
the Google `openingHours` schema all update together. `close` may run past
midnight — `"26:00"` means 2 AM.

The page also computes an **Open now / Closed** badge from those hours, in
`America/New_York`, with no network call.

### Live sync from your Google listing (optional)

`assets/js/hours.js` can pull the current hours straight from the Google Places
listing and replace what's on the page. It is off until you fill in the two
values at the top of that file:

```js
var CONFIG = {
  placeId: '',   // ChIJ...
  apiKey:  ''    // AIza...
};
```

1. Get the Place ID: <https://developers.google.com/maps/documentation/places/web-service/place-id>
2. Google Cloud Console → enable **Places API (New)** → create an API key
3. **Restrict the key** — Application restriction "Websites", allowing
   `https://urbanpufflounge.com/*` and `https://www.urbanpufflounge.com/*`;
   API restriction to Places API (New) only. The key ships in the page source,
   so the restriction is what protects it.

If the call fails, is rate-limited, or the key is missing, the hours written
into the HTML stay on screen. The page is never blank or wrong.

## Reservations

`reserve.html` is the primary conversion page and the CTA in the header, the
hero and the sticky mobile bar all point at it. It collects date, time, party
size, occasion, name, phone and notes, and emails the request through the same
FormSubmit relay with the subject prefixed `TABLE REQUEST`, so it is easy to
filter in Gmail. Past dates are blocked automatically.

It is deliberately a *request*, not an instant booking — you confirm by text or
call. If you ever want real-time availability, that means a booking platform
(OpenTable, Resy, SevenRooms, Tock); the page would then link out to it.

## What's on / weekly specials

`SITE["specials"]` in `tools/build.py` — one line per night. This is the single
most valuable thing to keep fresh; it gives people a reason to pick a Tuesday.
The current entries are plausible placeholders, not real offers — replace them
before launch or people will turn up expecting a free mocktail.

## Shisha flavour board

`SITE["flavours"]` in `tools/build.py`. Hookah guests browse flavours more than
anything else on the site, so this sits at the top of the menu page. Grouped by
family; the house mixes are the ones worth naming after the lounge.

## FAQ

`SITE["faqs"]` in `tools/build.py`. Also emitted as `FAQPage` schema on the
visit page, so Google can show the answers directly in search results.

## Sticky mobile bar

Fixed to the bottom of the screen under 760px: Message (or Call), Reserve,
Directions. The moment you set `SITE["phone"]`, the first button becomes a real
tap-to-call and the number also appears in the Google schema.

## The inbox address is not in this repository

The forms post to a FormSubmit **"invisible email"** endpoint — a random string
that resolves to the inbox on FormSubmit's side:

```
https://formsubmit.co/107255ed9e810f4577564bb36d288488
```

So there is no address in any page, in the rendered DOM, in the visible text, in
the schema, or anywhere in this repo. There are no `mailto:` links on the site.

To point the forms at a different inbox: activate it at
[formsubmit.co](https://formsubmit.co), take the random string from the
confirmation email, and set it in `tools/build.py`:

```python
"form_token": "hash:<your string>",
```

Rebuild and both forms follow it. The string is not a secret — it only lets
someone send you a message, which is what the form is for.

## Contact form

The form posts in the background to FormSubmit's AJAX endpoint and shows an
inline "Message sent" panel — the visitor never leaves the site. If JavaScript
is off, it falls back to a normal POST and lands on `thank-you.html`.

Phone is required (10+ digits); email is optional but validated when filled.

## Artwork

`tools/art.py` holds the SVG illustrations — the lounge scene in the hero and the
hookah / grill / mocktail / dessert cards. They're vector, animated in CSS, and
weigh almost nothing.

**Swapping in real photos:** each illustration sits in an `.art` wrapper with a
commented-out `<img>` right above it. Drop a photo at the named path and
uncomment that line — CSS hides the artwork automatically:

| Slot | Photo path |
| --- | --- |
| Hero scene | `assets/img/lounge.jpg` |
| Premium Hookah card | `assets/img/hookah.jpg` |
| Tikka & Kababs card | `assets/img/grill.jpg` |
| Mocktails card | `assets/img/mocktail.jpg` |
| Sweet Endings card | `assets/img/dessert.jpg` |

## SEO

Everything on-page is in place:

- **Titles** 50–56 characters, keyword first, brand last — e.g. "Premium Hookah
  Lounge & Bar in Marietta, GA | Urban Puff".
- **Meta descriptions** 143–157 characters, each one written for the page.
- **One `<h1>` per page**, no skipped heading levels, keyword-led on the home page.
- **JSON-LD**: `BarOrPub` + `Restaurant` on the home page with geo coordinates,
  `openingHoursSpecification`, amenities, `acceptsReservations`, `hasMenu`,
  `areaServed`, `smokingAllowed` and a `ReserveAction`; plus `WebSite`,
  `BreadcrumbList` on every inner page, `Menu` on the menu page and `FAQPage`
  on the visit page.
- **`robots`** meta with `max-image-preview:large` so Google can show a big
  thumbnail; `noindex, follow` on the thank-you and 404 pages.
- **Open Graph + Twitter cards** complete, including image dimensions and alt.
- **`geo.position` / `ICBM`** meta with the venue's coordinates.
- **sitemap.xml** with lastmod, changefreq and priority; **robots.txt** points at it.
- Local relevance copy on the home page naming the areas actually served.

### The honest part

On-page work is roughly **a fifth** of what decides local ranking. The biggest
lever by far is the **Google Business Profile** — category, description, photos
posted regularly — followed by **review volume and recency**. A perfect website
will not outrank a competitor with 200 recent reviews.

So, in priority order:

1. Claim and complete the Google Business Profile. Primary category
   **"Hookah bar"**. Post photos weekly.
2. Ask every happy guest for a Google review. Volume and recency both count.
3. Make the name, address and phone **identical** everywhere — website, Google,
   Yelp, Instagram, Facebook. One inconsistent phone number fragments the entity
   and costs you trust across all of them.
4. Submit `sitemap.xml` in Google Search Console.
5. Get a few local links: Cobb Chamber of Commerce, Marietta event listings,
   local blogs. One local news mention beats fifty directory listings.

### NAP warning

The US Census geocoder resolves 562 Wylie Rd SE to ZIP **30067**, not 30060.
Check which one your Google listing and your mail actually use, and make the
site match it exactly — `SITE["zip"]` in `tools/build.py`.

## Things to update before/after launch

| What | Where |
| --- | --- |
| Real opening hours | `SITE["hours_data"]` in `tools/build.py` |
| Phone number | not on the site yet — say the word and it goes in the header, footer and schema |
| Real photos | drop JPGs into `assets/img/`, then swap the placeholders in `build_gallery()` |
| Social preview image | add `assets/img/og-image.jpg` (1200×630) — the meta tags already point at it |
| Age policy | `SITE["age"]` (currently "21+ with valid ID") |
| Menu items | `build_menu()` in `tools/build.py` |

## Photos

Gallery tiles are marked with an HTML comment showing exactly what to paste:

```html
<img src="assets/img/01.jpg" alt="The lounge floor" loading="lazy">
```

Save photos around 1600px on the long edge and keep each under ~400KB so the
site stays fast on phones.
