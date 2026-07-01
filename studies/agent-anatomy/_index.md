---
date: 2026-07-01
tags:
  - agent-anatomy
  - index
---

# agent-anatomy — 導覽

> 一套「怎麼把任何 agent 系統拆開來看」的五層框架(Pattern → Computation Model → Runtime →
> Tool → Environment),以及對它做的獨立性(orthogonal)/根本定義(first-principles)分析。
> 起於跟 Paul 的 Notion 筆記「Agent 解剖學」同一條線,但這裡是通用框架本身,不綁定任何一篇論文。

## 文件

- [five-layer-framework](docs/2026-07-01-five-layer-framework.md) — 五層各自的定義、回答的問題、例子
- [orthogonal-analysis](docs/2026-07-01-orthogonal-analysis.md) — 五層是不是真的互相獨立?找到的隱藏邊
- [computation-model-first-principles](docs/2026-07-01-computation-model-first-principles.md) —
  Computation Model 這一層,從第一原理重新挖出來的定義
- [runtime-first-principles](docs/2026-07-01-runtime-first-principles.md) —
  Runtime 這一層,從第一原理重新挖出來的定義 + Runtime state 的具體拆法
- [harness-engineering-reference](docs/2026-07-01-harness-engineering-reference.md) —
  OpenAI「harness engineering」查證記錄,解釋為什麼 Harness 這一層改名叫 Tool
- [human-analogy-elicit](docs/2026-07-01-human-analogy-elicit.md) —
  五句「回答的問題」從人類經驗重建的 elicit 收斂記錄(身體=Runtime、Tool 層名確認不用換、
  Enact P1 證明 Tool 是獨立第五層)
- [mockups/2026-07-01-agent-anatomy-layers](mockups/2026-07-01-agent-anatomy-layers/index.html) —
  互動圖解:五層 + 那條沒名字的 conditioning edge

## 出處

框架第一次被具體套用在一篇論文的定位論證上,是 `enact` repo 的
`research/raws/2026-06-12-layer-taxonomy-and-gap-framing.md`(Paper 1: Actor-Based Agent
Runtime 的 Gap section 推導)——那份混了論文專屬的分析,留在 enact 那邊,不搬過來;這裡只放
通用、不綁論文的框架本體。
