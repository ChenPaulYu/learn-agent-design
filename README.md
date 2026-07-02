# learn-agent-design

> A personal workspace for learning agent design — read a concept, distill it into a note,
> then try it hands-on in code.
> 個人學習 agent design 的地方——讀懂一個概念、蒸餾成筆記,然後動手寫 code 驗證看看。

**Not a product.** No shipping, no users, nothing here is meant to go anywhere but this
workspace's own use. Disposable by nature — a study can be abandoned, a mockup thrown away, a
code experiment rewritten from scratch, all without ceremony.

## What lives here

One `studies/<topic>/` per bounded concept area. Each topic bundles everything about that one
idea in a single folder — notes, code, and any disposable diagrams — rather than splitting by
artifact type across parallel trees:

```
site/                  ← Jekyll machinery (config, layout, Gemfile) — content source stays the repo root
studies/
  agent-anatomy/       ← e.g. the 5-layer Pattern/Computation-Model/Runtime/Tool/Environment split
    _index.md          ← the topic's front door (navigation only)
    docs/               ← dated, distilled, point-first notes — the source of truth
    code/                ← hands-on experiments testing this topic's ideas
    mockups/             ← disposable interactive artifacts used to converge one decision
    pages/               ← durable interactive teaching pages, derived from docs/ (see below)
```

- **Code stays inside its own topic by default.** Only pulled out to a shared `toolkit/` at the
  root once a *second* topic genuinely reuses the same code (N+1) — never pre-split "notes vs.
  code" before that happens.
- **Mockups always stay inside their topic — no exception.** A mockup converges one decision and
  is disposable by design; there's no realistic case of two topics sharing one.
- **Pages are the one durable HTML genre.** A `pages/*.html` file is an interactive teaching
  view derived from that topic's `docs/` notes — meant to be revisited (and published), unlike
  mockups. The notes stay the source of truth: the page may differ in wording and presentation,
  but must match them in substance. Each page carries Jekyll front matter (so it lands in the
  site nav automatically, with `layout: none` to keep its own standalone HTML) and a top comment
  stating *Derived from* (which docs) + *Last synced* (bump the date whenever the docs change
  materially and the page is re-synced). Published URL follows `/<topic>/<content>/` (e.g.
  `studies/mcp/pages/101.html` → `/mcp/101/`), via one per-topic permalink entry in `site/_config.yml`.

## Relationship to `../grains`

Borrows `grains`' knowledge-organization habits (a bounded topic = one folder, dated notes,
point-first writing, a navigational `_index.md`) but is a **different contract**: `grains` is
pure curated memory with a hard "no tool code" rule; this repo exists specifically to hold code,
because the whole point is testing what's learned. The two repos share no governance and no
cross-repo ADRs — the resemblance is borrowed habit, not coupling.

## Current studies

- [`agent-anatomy`](studies/agent-anatomy/_index.md) — a 5-layer framework for reading any agent
  system apart (Pattern → Computation Model → Runtime → Tool → Environment), plus an
  orthogonal-independence check and a first-principles dig into what "Computation Model" really is.
- [`mcp`](studies/mcp/_index.md) — the Model Context Protocol: architecture, the six primitives,
  wire-protocol internals, the security model, and the tool-scaling problem.

---

## 中文

**這不是產品。** 不上線、沒有使用者,這裡的東西只為了個人學懂而存在。用完即丟是常態——一個
study 可以放棄、一份 mockup 可以丟掉、一段 code 可以整段重寫,都不用有心理負擔。

**結構**:一個 `studies/<topic>/` 對應一個有邊界的概念。每個主題把「這個想法的一切」都收在同一個
資料夾裡——筆記、code、一次性的圖解——不照「這是文字還是 code」這種類型分開放。`_index.md` 是
主題的門面(只放導覽);`docs/` 放蒸餾過的筆記(真相來源);`code/` 放動手驗證的實驗;`mockups/`
放收斂某個決定用的一次性互動圖解;`pages/` 放可長期回看的互動教學頁——內容衍生自 `docs/`,
措辭/呈現可以不同但概念要一致,檔頭記「衍生自哪幾篇 + 最後同步日期」,docs 大改時回來同步;
發布網址走 `/<主題>/<內容>/`(如 `studies/mcp/pages/101.html` → `/mcp/101/`)。

**跟 `../grains` 的關係**:借用它的知識組織習慣(有邊界的主題=一個資料夾、日期化筆記、point-first
寫法、一份導覽用的 `_index.md`),但合約不同——grains 是純粹的記憶庫,硬性規定不放 code;這裡剛好
反過來,寫 code 就是學習的一部分。兩個 repo 沒有共用治理、也沒有跨 repo 的 ADR,借的是習慣,不是
綁定關係。
