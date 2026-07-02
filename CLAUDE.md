# CLAUDE.md — learn-agent-design

A personal learning workspace for agent-design concepts: read/reason about a concept, distill it
into a note, then try it hands-on in code. Not a product repo — no shipping, no users.

`BACKLOG.md` (repo root) is a living list of candidate topics not yet started — not a history
log (git log / the notes themselves cover that). When a tangent surfaces a topic worth studying
later but out of scope for the current thread, add a line there instead of chasing it
immediately. Delete an item's line once its own topic/note actually exists.

## Relationship to `../grains`

Borrows `grains`' knowledge-organization pattern (a bounded topic = one folder, flat dated notes,
a navigational `_index.md`, point-first writing) but is **not** the same contract. `grains` is
pure curated memory — no tool code allowed. This repo is the opposite case on purpose: the code
*is* part of learning here, so it's not exiled to a separate repo. The two repos are otherwise
unrelated (no shared governance, no cross-repo ADRs).

## Layout

| where | what |
|---|---|
| `studies/<topic>/` | a bounded concept area. `_index.md` (the topic's front door — navigation only, stays outside `docs/`) + `docs/` (dated, distilled, point-first notes — the topic's source of truth) + `code/` (that topic's hands-on experiments) + `mockups/` (that topic's disposable interactive artifacts, dated subfolder per decision — `/shape:mockup` convention) + `pages/` (durable interactive teaching pages derived from `docs/`, see below) |

**Code stays inside its topic's `code/` folder by default (N+1 rule).** Only extract a shared
`toolkit/` at the root once a *second* study genuinely reuses the same code — don't pre-split by
type (notes vs. code) before that happens; that's a temporal/type decomposition, not a knowledge
one.

**Mockups always stay inside their topic's `mockups/` folder — no N+1 exception.** A mockup
converges one decision and is disposable by design (per `/shape:mockup`); there's no realistic
case of two topics sharing one, so there's no shared-tool exception to wait for like `code/` has.

**Pages (`pages/*.html`) are durable, not disposable — don't sweep them with mockups.** A page
is an interactive teaching view derived from that topic's `docs/` notes, meant to be revisited
and published via the repo's Jekyll site. Rules: (1) `docs/` stays the source of truth — the
page may differ in wording/presentation but must match the notes in substance; (2) each page
carries Jekyll front matter (`title`/`date`/`tags`, `layout: none`, `render_with_liquid: false`)
so it auto-appears in the site nav while keeping its own standalone HTML; (3) its top comment
states *Derived from* (which docs) + *Last synced* (date) — when the docs change materially,
re-sync the page and bump the date; (4) published URL is `/<topic>/<content>/` (e.g.
`studies/mcp/pages/101.html` → `/mcp/101/`) — one per-topic permalink entry in `site/_config.yml`,
added when a topic publishes its first page.

**Every topic with published pages needs its own topic-index page, or its base URL 404s /
shows a bare directory listing.** `/mcp/101/` and `/mcp/security/` each have their own
`index.html`, but `/mcp/` itself has nothing unless you add one — Jekyll never auto-generates
a directory index. Fix: add `studies/<topic>/pages/index.md` with front matter
`title: <Topic>` · `topic: <topic>` · `permalink: /<topic>/` · `layout: default`, plus one
short intro sentence as its body. The shared layout (`site/_layouts/default.html`) branches on
`page.topic`: set → scope the card list to just that topic's own pages; unset → the homepage's
full all-topics view. Do this the same turn a topic's first page ships, not as an afterthought.

## Writing a study note

- Distilled conclusion, point-first — not a transcript of how the conclusion was reached.
- Frontmatter: `date` · `tags` (tags answer "about what", never maturity/status).
- Content in Traditional Chinese is fine (matches how Paul thinks); this file, README, and any
  ADRs stay English.
- If a note's finding was first derived while working on another repo (e.g. a paper's research
  notes), link back to that source doc as provenance — don't copy it in.
