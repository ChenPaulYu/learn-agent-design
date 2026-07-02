# rules/organization.md — repo & folder structure

Where things go, why they go there, and when to prune. `rules/pages.md` covers the mechanics of
building an interactive page; this file covers everything upstream of that — how a topic is
laid out, how `docs/` relates to `pages/`, when a doc's job is done.

## `BACKLOG.md` is a living list, not a history log

`BACKLOG.md` (repo root) tracks candidate topics not yet started — not a history log (git log /
the notes themselves cover that). When a tangent surfaces a topic worth studying later but out
of scope for the current thread, add a line there instead of chasing it immediately. Delete an
item's line once its own topic/note actually exists.

## Relationship to `../grains`

Borrows `grains`' knowledge-organization pattern (a bounded topic = one folder, flat dated notes,
a navigational `_index.md`, point-first writing) but is **not** the same contract. `grains` is
pure curated memory — no tool code allowed. This repo is the opposite case on purpose: the code
*is* part of learning here, so it's not exiled to a separate repo. The two repos are otherwise
unrelated (no shared governance, no cross-repo ADRs).

## Layout

| where | what |
|---|---|
| `studies/<topic>/` | a bounded concept area. `_index.md` (the topic's front door — navigation only, stays outside `docs/`) + `docs/` (dated, distilled, point-first notes — the verification/citation substrate a page gets built from, see below) + `code/` (that topic's hands-on experiments) + `mockups/` (that topic's disposable interactive artifacts, dated subfolder per decision — `/shape:mockup` convention) + `pages/` (durable interactive teaching pages, the thing actually read/revisited — see `rules/pages.md`) |

**Code stays inside its topic's `code/` folder by default (N+1 rule).** Only extract a shared
`toolkit/` at the root once a *second* study genuinely reuses the same code — don't pre-split by
type (notes vs. code) before that happens; that's a temporal/type decomposition, not a knowledge
one.

**Mockups always stay inside their topic's `mockups/` folder — no N+1 exception.** A mockup
converges one decision and is disposable by design (per `/shape:mockup`); there's no realistic
case of two topics sharing one, so there's no shared-tool exception to wait for like `code/` has.
Delete it once its pick has landed in the real thing (a doc, a page, the layout) — same rule
that governs `docs/` below.

## `docs/` is a thought, not a canon

Same relationship as `/shape`'s thought → canon. A doc is where research/verification actually
happens (official quotes, hedges, "which part is inferred vs. quoted" — things a page's
chip/card format can't hold), written *before* the page so the page has something checked to
compress from. But a doc's job ends once its content is absorbed into a page: prune it, the same
way a mockup gets pruned once its pick lands in the owning doc (ADR-037's pattern).

**Absorption is substance-level, not "a page roughly covers the topic."** Before deleting a doc,
diff what it says against what the page actually renders; a caveat/correction/methodology-aside
the doc carries and the page doesn't is a real gap, not noise. Fold the gap into the page first
(a `note` field, a References-section line — whatever fits that page's existing pattern), *then*
delete the doc. A doc with no page yet, or a doc carrying content a page hasn't absorbed, stays —
it hasn't finished its job.

## Every topic with published pages needs its own topic-index page

Otherwise its base URL 404s / shows a bare directory listing. `/mcp/101/` and `/mcp/security/`
each have their own `index.html`, but `/mcp/` itself has nothing unless you add one — Jekyll
never auto-generates a directory index. Fix: add `studies/<topic>/pages/index.md` (frontmatter
+ the reading-path `groups` schema are in `rules/pages.md`). Do this the same turn a topic's
first page ships, not as an afterthought.

## Writing a study note (`docs/*.md`)

- Distilled conclusion, point-first — not a transcript of how the conclusion was reached.
- Frontmatter: `date` · `tags` (tags answer "about what", never maturity/status).
- Content in Traditional Chinese is fine (matches how Paul thinks); `CLAUDE.md`, `README.md`,
  files under `rules/`, and any ADRs stay English.
- If a note's finding was first derived while working on another repo (e.g. a paper's research
  notes), link back to that source doc as provenance — don't copy it in.
