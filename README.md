# Arcade Games Hub 🕹️

A free online collection of 6 classic mini games. Pure static site — no build step, no backend, no dependencies. Open the page and play instantly on desktop and mobile.

## Games

| Game | Path |
|---|---|
| 🐍 Snake | `/games/snake/` |
| 🔢 2048 | `/games/2048/` |
| 🧱 Tetris | `/games/tetris/` |
| 💣 Minesweeper | `/games/minesweeper/` |
| ⚫ Gomoku (vs AI) | `/games/gomoku/` |
| 🃏 Memory Match | `/games/memory/` |

## Internationalization

7 languages, each with its own directory and full SEO tags (hreflang, canonical, JSON-LD):

| Language | Path |
|---|---|
| English (default) | `/` |
| 中文 | `/zh/` |
| Español | `/es/` |
| العربية (RTL) | `/ar/` |
| Русский | `/ru/` |
| 日本語 | `/ja/` |
| 한국어 | `/ko/` |

All game UI text, instructions, tips and in-game messages are fully translated. Arabic pages are right-to-left adapted.

## Structure

```
├── index.html              English home (default)
├── zh/ es/ ar/ ru/ ja/ ko/ Language subdirectories
├── games/                  English game pages
├── assets/css|js/          Shared styles and game scripts
├── sitemap.xml             All 49 pages with hreflang alternates
├── vercel.json             Vercel redirects (legacy /en/ → /)
├── _redirects              Cloudflare Pages redirects
└── tools/build_i18n.py     i18n page generator
```

## Deploy

Pure static files. Upload the whole folder to any static host (Vercel, Cloudflare Pages, GitHub Pages, Netlify, OSS...). No build command needed.

**Before deploying:** replace the placeholder domain `games.example.com` with your real domain:

```bash
grep -rl "games.example.com" . | xargs sed -i "s|games.example.com|your-domain.com|g"
sed -i "s|games.example.com|your-domain.com|g" tools/build_i18n.py
```

## Regenerate pages

To edit copy or add a language/game, edit the translation data in `tools/build_i18n.py` and re-run:

```bash
python3 tools/build_i18n.py
```
