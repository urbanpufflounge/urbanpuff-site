# Deploying Urban Puff to GitHub Pages

Three stages: **push the code**, **point the domain**, **switch the form on**.
Budget about 20 minutes of work and up to 24 hours of waiting for DNS.

---

## Stage 1 — Push the code to GitHub

### 1. Create the repository

Already done: <https://github.com/urbanpufflounge/urbanpuff-site>

Make sure it is **Public** — GitHub Pages is only free on public repos.
(Settings -> General -> Danger Zone -> Change visibility, if it is currently private.)

### 2. Push from your machine

The files are already in `V:\\Projects\\UrbanPuff\\code\\urbanpuff-site`, the remote is
already set, and the commit is already made. All that is left is the push — run
this in **PowerShell on Windows**, where your GitHub credentials live:

```powershell
cd V:\Projects\UrbanPuff\code\urbanpuff-site
git push -u origin main
```

If it asks for a password, use a
[personal access token](https://github.com/settings/tokens) with `repo` scope,
not your account password. (Or install [GitHub CLI](https://cli.github.com) and
run `gh auth login` once — after that, pushes just work.)

### 3. Turn on Pages

In the repo: **Settings → Pages**

- **Source:** `Deploy from a branch`
- **Branch:** `main`, folder `/ (root)` → **Save**

Wait ~1 minute. The page will show a live URL like
`https://urbanpufflounge.github.io/urbanpuff-site/`. Open it — the site should be there
(the custom domain comes next, so some links may look odd until Stage 2 finishes).

---

## Stage 2 — Point urbanpufflounge.com at it

### 1. Tell GitHub about the domain

**Settings → Pages → Custom domain** → type `urbanpufflounge.com` → **Save**.

(The repo already contains a `CNAME` file with that domain, so this may already
be filled in. Leave it.)

### 2. Add the DNS records at your registrar

Wherever you bought `urbanpufflounge.com` (GoDaddy, Namecheap, Cloudflare,
Google Domains/Squarespace…), open its DNS settings and add:

**Four A records** — host/name `@` (or blank, meaning the root domain):

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| A | @ | `185.199.108.153` | default |
| A | @ | `185.199.109.153` | default |
| A | @ | `185.199.110.153` | default |
| A | @ | `185.199.111.153` | default |

**One CNAME record** so `www` works too:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| CNAME | www | `urbanpufflounge.github.io` | default |

Note the trailing dot in `urbanpufflounge.github.io.` that some registrars add
automatically — that's fine. Do **not** include the repo name.

Optional, for IPv6 visitors — four AAAA records on `@`:
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`

> **On Cloudflare?** Set the proxy status to **DNS only** (grey cloud) for these
> records until GitHub has issued the certificate, otherwise HTTPS gets stuck.

### 3. Delete conflicting records

Remove any existing A, AAAA or CNAME record on `@` or `www` left over from a
parking page or a previous host. Two conflicting records will break the site.

### 4. Wait, then enforce HTTPS

DNS usually propagates in 10–60 minutes (occasionally up to 24 hours). Back on
**Settings → Pages** you'll see "DNS check successful", then a few minutes later
the **Enforce HTTPS** checkbox becomes available. **Tick it.**

Check progress from a terminal:

```bash
dig urbanpufflounge.com +short      # should list the four 185.199.x.x addresses
```

---

## Stage 3 — Activate the contact form

The form posts to **FormSubmit** (<https://formsubmit.co>), a free relay that
forwards submissions to an inbox. No account, no API key, no server.

1. Once the site is live at `https://urbanpufflounge.com`, open the **Contact**
   page and send yourself a real test message.
2. FormSubmit emails **your inbox** a one-time activation link.
   **Click it.** (Check spam if it doesn't show up within a minute.)
3. Send a second test message. It should now land in the inbox, formatted as a
   table with First Name / Last Name / Email / Phone / Message, and the browser
   should land on the "Thanks — we've got it" page.
4. The sender also gets an automatic acknowledgement — the wording is the
   `_autoresponse` hidden field in `contact.html`, edit it to taste.

### Already done: the inbox address is hidden

The forms use FormSubmit's "invisible email" endpoint — a random string that
resolves to the inbox on their side — so no address appears on the site or in
the repository. Nothing further to do here.

### If you'd rather not use FormSubmit

Same form markup works with these — change only the `action` and, where noted,
add one hidden field:

- **Web3Forms** — `action="https://api.web3forms.com/submit"` + `<input type="hidden" name="access_key" value="YOUR-KEY">`
- **Formspree** — `action="https://formspree.io/f/YOUR-ID"`
- **Getform / Basin / Netlify Forms** — all accept a plain POST the same way

---

## Day-to-day updates

```powershell
cd V:\Projects\UrbanPuff\code\urbanpuff-site
# edit files (or tools/build.py then: python tools\build.py)
git add .
git commit -m "Update hours"
git push
```

GitHub Pages rebuilds automatically — live in about a minute. If you don't see
the change, hard-refresh (Cmd/Ctrl + Shift + R).

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Site loads but has no styling | The `.nojekyll` file is missing, or you deployed the wrong folder. Confirm Pages is set to `main` / `/ (root)`. |
| "Domain does not resolve to the GitHub Pages server" | DNS hasn't propagated, or an old A/CNAME record is still on `@`. Re-check Stage 2.2 and 2.3. |
| Enforce HTTPS is greyed out | GitHub is still issuing the certificate. Wait — it can take up to 24h after DNS is correct. |
| Custom domain keeps clearing itself | The `CNAME` file was deleted by a push. It must stay in the repo root containing exactly `urbanpufflounge.com`. |
| Form does nothing / 404s | FormSubmit hasn't been activated yet — see Stage 3. |
| Form works but no email arrives | Check Gmail spam, and confirm the activation link was clicked. |
| Google Maps embed is blank locally | Expected — it needs internet and works once deployed. |


---

## Keeping the repository out of search results

The site itself is clean: `urbanpufflounge.github.io` 301s to the custom domain,
every page carries a canonical URL pointing at `urbanpufflounge.com`, and
`robots.txt` keeps `/docs/`, `/tools/` and the README out of the index. Nothing
on the site competes with itself.

The **GitHub repository page** is a different matter, and worth being clear about:

- GitHub controls `github.com/robots.txt`. Nothing you put in a repository —
  a robots.txt, a meta tag, a setting — changes how Google crawls the repo page.
  There is no "noindex this repository" option.
- What *can* be reduced is how well the repo page matches a search for the
  business. Google leans on the repository **name**, its **description**, its
  **topics**, and the rendered **README**. The README here is deliberately
  generic and carries no business name, address, phone or hours.

To go further, in order of effect:

1. **Rename the repository** to something that doesn't contain the brand
   (Settings -> General -> Repository name). GitHub redirects the old URL, so
   pushes keep working and Pages is unaffected.
2. **Clear the About panel** on the repo page — remove the description, the
   website link and any topics.
3. **Make the repository private.** This is the only complete fix, and it needs
   a paid plan: GitHub Pages only serves private repositories on Pro, Team or
   Enterprise. On the Free plan a Pages site must come from a public repository.

Note that "not indexed" and "not public" are different things. While the
repository is public, anyone with the URL can read every file in it whether or
not Google lists it.
