# medical-literature

Archive and website for two scheduled Claude Code routines:

- **Daily medical literature brief** — 14:00 UTC → `_briefs/YYYY-MM-DD.md`
- **Daily guidelines watch** — 14:20 UTC → `_guidelines/YYYY-MM-DD.md`

Published with GitHub Pages (Jekyll, no plugins) at
<https://nicusilviuu.github.io/medical-literature/> — homepage lists every day
newest-first with a filter box; each day has its own permanent page.

## Layout

| Path | Purpose |
|---|---|
| `_briefs/`, `_guidelines/` | One Markdown file per day. The archive **and** the dedupe source — each file's `items:` front matter is what future runs check against. |
| `.claude/skills/` | The instructions each routine follows. Edit these to change what the routines do. |
| `claude/source-notes.md` | Running notes on which journal/society sites are reachable. |
| `_layouts/`, `index.html`, `assets/` | The site itself. |

## Local preview

```bash
gem install jekyll
jekyll serve   # http://localhost:4000/medical-literature/
```

## Setup note

GitHub Pages must be enabled once: **Settings → Pages → Source: Deploy from a
branch → `main` / `/ (root)`**. The repo is public, so the site is publicly
readable by anyone with the link.
