# Static site

Plain HTML, CSS and JavaScript. No framework, no build step required to deploy —
the `.html` files in the repository root are served as-is by GitHub Pages.

## Build

Page content is generated from a single Python file. Edit `tools/build.py`, then:

```bash
python3 tools/build.py
```

That rewrites every `.html` file plus `sitemap.xml` and `robots.txt`.
Python 3 only, no dependencies.

## Layout

```
*.html          generated pages
assets/css/     styles.css
assets/js/      main.js, hours.js, forms.js
assets/img/     logo and photography
tools/          build.py, art.py
docs/           site guide and deployment notes
```

## Documentation

- [`docs/site-guide.md`](docs/site-guide.md) — content, hours, forms, artwork, SEO
- [`docs/deploy.md`](docs/deploy.md) — hosting and DNS
