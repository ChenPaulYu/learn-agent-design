# CLAUDE.md — learn-agent-design

A personal learning workspace for agent-design concepts: read/reason about a concept, distill it
into a note, then try it hands-on in code. Not a product repo — no shipping, no users.

## Relationship to `../grains`

Borrows `grains`' knowledge-organization pattern (a bounded topic = one folder, flat dated notes,
a navigational `_index.md`, point-first writing) but is **not** the same contract. `grains` is
pure curated memory — no tool code allowed. This repo is the opposite case on purpose: the code
*is* part of learning here, so it's not exiled to a separate repo. The two repos are otherwise
unrelated (no shared governance, no cross-repo ADRs).

## Layout

| where | what |
|---|---|
| `studies/<topic>/` | a bounded concept area — dated notes (distilled, point-first) + a `code/` subfolder for that topic's hands-on experiments |
| `mockups/` | interactive HTML artifacts (diagrams / renders) used to converge a design question, one dated subfolder per artifact (`/shape:mockup` convention) |

**Code stays inside its topic's `code/` folder by default (N+1 rule).** Only extract a shared
`toolkit/` at the root once a *second* study genuinely reuses the same code — don't pre-split by
type (notes vs. code) before that happens; that's a temporal/type decomposition, not a knowledge
one.

## Writing a study note

- Distilled conclusion, point-first — not a transcript of how the conclusion was reached.
- Frontmatter: `date` · `tags` (tags answer "about what", never maturity/status).
- Content in Traditional Chinese is fine (matches how Paul thinks); this file, README, and any
  ADRs stay English.
- If a note's finding was first derived while working on another repo (e.g. a paper's research
  notes), link back to that source doc as provenance — don't copy it in.
