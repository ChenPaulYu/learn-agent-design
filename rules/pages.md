# rules/pages.md — building & wiring `pages/*.html`

Engineering reference for the `pages/` genre — the concrete "how do I make this correctly"
rules. `CLAUDE.md` covers the *why* (docs vs. pages relationship, when a topic needs a page);
this file covers the *how* (frontmatter schemas, CSS/JS conventions, the shared layout's
contract). Read `CLAUDE.md` first for context, come here when actually writing code.

## Page frontmatter & URL scheme

Every `pages/<content>.html` file needs this frontmatter (real HTML page, not the topic-index
markdown page):

```yaml
title: <Topic> <Content> — 互動圖解
summary: <one line — what the interactive diagrams cover, shown as the card summary on the topic-index and homepage>
date: 2026-07-02
tags: [<topic>, <content-specific tags>, interactive]
layout: none
render_with_liquid: false
```

`layout: none` + `render_with_liquid: false` keep the file a self-contained standalone HTML page
— Jekyll registers it (so it gets a URL, appears in `site.pages`) but doesn't wrap it in the
shared layout or touch its `{{ }}`/`{% %}` syntax (the page's own JS template literals use `${}`
freely without Jekyll trying to interpret them).

Right after `<!DOCTYPE html>`, a top HTML comment states:
- **Derived from** — which `docs/*.md` file(s) this page's content traces back to (if that doc
  still exists — see `CLAUDE.md`'s docs-as-thought rule; many get pruned once absorbed)
- **Last synced** — the date this page was last checked against its source; bump it whenever
  the underlying facts change
- **What it is** — one line per section/diagram, so an agent can `head -30` the file and know
  the page's shape without reading the body

Published URL is `/<topic>/<content>/` (e.g. `studies/mcp/pages/101.html` → `/mcp/101/`) via a
per-topic `permalink: /<topic>/:basename/` entry under `defaults` → `scope` in `site/_config.yml`
— add that entry the same turn a topic publishes its *first* page, or every page in that topic
falls back to Jekyll's default permalink shape instead.

The topic-index page itself (`pages/index.md`, one per topic) is different — real Jekyll
markdown, front matter `title` / `topic: <name>` / `permalink: /<topic>/` / `layout: default`,
body is just a one-sentence intro (becomes that topic's homepage-card summary, see below). The
`groups` schema below lives in *this* file's frontmatter.

## Topic-index reading path (`pages/index.md` → `site/_layouts/default.html`)

A topic-index page (the one with `topic: <name>` + `permalink: /<topic>/` in its frontmatter)
can define a curated reading order via a `groups` field:

```yaml
groups:
  - label: 先讀這篇
    note: 一句話說明為什麼從這篇開始
    pages: ["101"]
  - label: 進階主題(任意順序)
    note: 各自獨立,讀完前面之後想先看哪個都可以
    parallel: true
    pages: [security, tool-scaling, ecosystem]
```

- `pages` is a list of **basenames** (the page's filename without extension) — always quote
  ones that look numeric (`"101"`, not `101`), otherwise YAML parses it as an integer and the
  basename match in the layout silently fails (renders an empty group, no error).
- `parallel: true` (only meaningful with 2+ pages) tells the layout to render that group as a
  forked dashed row instead of a single sequential line — visually distinguishes "these have no
  order between them" from "read these in order." A group without `parallel` (or with only one
  page) always renders as a normal single-line entry.
- No `groups` defined → the layout falls back to a flat, date-sorted card list. A brand-new
  topic with only one page doesn't need `groups` yet.
- The matching logic (`site/_layouts/default.html`) strips `.html`/`.md` from each page's actual
  filename and compares to the basenames in `pages:` — this is why the frontmatter list has to
  use plain basenames, not full paths or titles.

## Every page needs nav links back — and they must be relative paths

Every individual `pages/*.html` file needs a small nav row (near the top, inside `.wrap` before
`<header>`) with two links: back to that topic's index, back to the site home.

```html
<div class="page-nav">
  <a href="../">← <Topic> 導覽</a>
  <a href="../../">🏠 回首頁</a>
</div>
```

**Use relative paths (`../`, `../../`) — never absolute paths (`/mcp/`) and never Liquid tags
(`{{ site.baseurl }}`).** Two constraints force this:

1. These pages carry `render_with_liquid: false` in their frontmatter (so their own HTML/JS
   stays untouched by Jekyll) — any `{{ ... }}` in the body is left as literal text, not
   interpolated.
2. The site's `baseurl` differs between environments: empty locally (dev serve overrides it with
   `-b ""`, see the Jekyll-local-Ruby-workaround memory) but `/learn-agent-design` on the
   deployed GitHub Pages site. An absolute path hardcoded for one environment breaks the other.

Relative paths sidestep both — `../` from `/mcp/101/` always resolves to `/mcp/` and `../../`
always resolves to `/`, regardless of what sits in front of that URL.

## Homepage shows topics, not pages

The homepage (`/`) renders **one card per topic**, not one card per page — a topic's own page
count keeps growing (mcp already has 5), so a flat "every page from every topic" list on the
homepage doesn't scale. The full page listing (with the reading-path groups above) belongs on
that topic's own `/<topic>/` index page.

The homepage's card data comes from `site.pages | where_exp: "p", "p.topic"` — i.e. exactly the
pages carrying `topic:` in frontmatter (each topic's own `pages/index.md`). Each card reuses that
page's title + its markdown body (the one-sentence intro) as the summary — no separate content
needs authoring for the homepage.

**Don't let a topic's own `index.md` leak into a page-level listing.** Any query that walks
`site.pages` scoped to a topic (e.g. the topic-index page's own reading-path renderer) must
exclude `p.path != page.path` — otherwise the topic-index page shows up as a bogus extra card
with a bare title and no summary, mixed in with its own page list.

## Fade-in on every content swap

Every page that swaps panel/box content via `.innerHTML =` on a click or toggle needs this pair,
so the swap doesn't snap in instantly:

```css
.fade-in{animation:fadeInPanel .28s ease}
@keyframes fadeInPanel{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
```

```js
function fadeIn(el){ if(!el) return; el.classList.remove('fade-in'); void el.offsetWidth; el.classList.add('fade-in'); }
```

Call `fadeIn(theElement)` on the line right after every `.innerHTML = ...` assignment in that
page's render functions. The `remove` + `void el.offsetWidth` (forces a reflow) + `add` sequence
is what lets the animation restart on repeated clicks — just adding the class once doesn't replay
on the second click.

## `.zone` — the reusable interactive-SVG-scene pattern

When a page needs a clickable diagram (not just chip cards) — a role/architecture scene, a
metaphor illustration, a flow diagram — build it as an SVG with `<g class="zone" data-key="...">`
groups, using this CSS:

```css
.zone{cursor:pointer}
.zone .st{transition:stroke .15s ease}
.zone .stf{transition:fill .15s ease}
.zone:hover .st,.zone.active .st{stroke:currentColor}
.zone:hover .stf,.zone.active .stf{fill:currentColor}
.zone.active .fillable{fill:color-mix(in srgb,currentColor 8%,var(--panel))}
.zone.active text{fill:currentColor}
```

Each zone's outlined shapes get `class="st fillable"`, small filled accents get `class="stf"` —
`currentColor` is driven by the `style="color:#xxxxxx"` set on the `<g>` itself, so each zone can
have its own accent color without repeating it per-shape.

**Sync SVG zones with any parallel chip/card row that represents the same keys**, so clicking
either one highlights both and shows the same detail panel. The established pattern (see
`studies/mcp/pages/101.html`'s `activeForKey` helper) is: collect every element across every
UI surface (node row, chip row, SVG zones) that shares a `data-key`, toggle `.active` on all of
them together from one render function — don't wire the SVG and the chips to two separate
render paths that could drift out of sync.

Used in: `studies/mcp/pages/101.html` (role scene), `studies/mcp/pages/security.html` (OAuth
wristband scene, Client/Server building scene), `studies/agent-anatomy/pages/101.html` (human
body scene).
