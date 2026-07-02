# rules — 導覽

This repo's operating rules, split out of `CLAUDE.md` once the engineering-level detail (schemas,
CSS/JS conventions) got too code-heavy to sit next to the philosophy/organization rules. Read
this file first — it's navigation only, not content; each rule lives in its own file below.

## 檔案

- [organization.md](organization.md) — repo & folder structure: the `studies/<topic>/` layout,
  `code/`/`mockups/` N+1 rules, why `docs/` is a thought (not a canon) and when to prune it,
  the topic-index-page requirement, study-note writing style.
- [pages.md](pages.md) — building & wiring `pages/*.html`: page frontmatter + URL scheme, the
  topic-index `groups`/`parallel` reading-path schema, every page's relative-path nav links, why
  the homepage shows topics not pages, the fade-in convention, the `.zone` SVG-scene pattern.

## Relationship to `CLAUDE.md`

`CLAUDE.md` stays a short entry point only (what the repo is, a pointer here) — all the actual
rules, both the *why* (`organization.md`) and the *how* (`pages.md`), live under `rules/`. Don't
duplicate content across files; if a rule is philosophical/organizational it belongs in
`organization.md`, if it's "here's the exact CSS/frontmatter to write" it belongs in `pages.md`.
