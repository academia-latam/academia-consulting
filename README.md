# AcademIA — website

Bilingual (English + Spanish) marketing site for **AcademIA**, an AI-in-education consultancy serving universities, schools, and faculty in Mexico. Founder: Hesus Garcia Cobos.

Static, dependency-free (HTML + CSS + a little JS). No build step. Deploys to Vercel as-is.

> **Canonical repo:** `academia-latam/academia-consulting` (this is the source connected to Vercel, scoped to the AcademIA org). `HesusG/academia-consulting` is kept only as a personal reference mirror.

## Structure
```
index.html         # root: detects language, redirects to /en/ or /es/
en/index.html      # English homepage
es/index.html      # Spanish homepage (primary market)
assets/
  styles.css       # design system (OKLCH, blue brand)
  main.js          # scroll reveals + small enhancements (site works without JS)
  logo.svg         # mark / favicon
vercel.json        # clean URLs, caching
PRODUCT.md         # brand brief (impeccable context)
```

## Preview locally
No tooling needed. Either open `en/index.html` in a browser, or serve the folder so absolute `/assets/...` paths resolve:
```bash
python3 -m http.server 5173
# then visit http://localhost:5173/
```

## Deploy to Vercel
1. Push this repo to GitHub (see below).
2. In Vercel: **Add New > Project > Import** this repo.
3. Framework preset: **Other**. Build command: *(none)*. Output directory: **/** (root). Deploy.
   - Or from the CLI: `npm i -g vercel && vercel` (accept defaults; it's a static site).

## Custom domain (recommended: academiaconsulting.com)
You must buy the domain yourself; then connecting it is ~2 minutes.
1. **Check/buy** `academiaconsulting.com` (you may already own it — it's your `info@` domain). Cheapest at-cost: **Cloudflare Registrar**; simplest with Vercel: **Namecheap**. Fallbacks if taken: `academia.consulting`, `academ-ia.mx`, `academiaedu.mx`.
2. In Vercel: **Project > Settings > Domains > Add** `academiaconsulting.com` (and `www`).
3. At your registrar, set the DNS records Vercel shows (typically an `A` record to `76.76.21.21` for the apex and a `CNAME` for `www` to `cname.vercel-dns.com`). HTTPS is automatic.
4. Update the `og:` / `canonical` URLs in `en/index.html` and `es/index.html` if you choose a different domain.

## Editing
- Copy lives directly in `en/index.html` and `es/index.html` (mirror each other).
- Brand colors / type are CSS variables at the top of `assets/styles.css`.
- Add pages (e.g., `/en/ai-for-teachers/`) by copying a page and linking it in the nav.

## TODO / nice next steps
- Real contact form (Vercel + a form service) instead of mailto.
- A dedicated page for the `ai-for-teachers` course and the policy artifacts.
- OpenGraph share image (`/assets/og.png`).
