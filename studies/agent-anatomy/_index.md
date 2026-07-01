---
date: 2026-07-01
tags:
  - agent-anatomy
  - index
---

# agent-anatomy — 導覽

> 一套「怎麼把任何 agent 系統拆開來看」的五層框架(Pattern → Computation Model → Runtime →
> Harness → Environment),以及對它做的獨立性(orthogonal)/根本定義(first-principles)分析。
> 起於跟 Paul 的 Notion 筆記「Agent 解剖學」同一條線,但這裡是通用框架本身,不綁定任何一篇論文。

## 文件

- [five-layer-framework](docs/2026-07-01-five-layer-framework.md) — 五層各自的定義、回答的問題、例子
- [orthogonal-analysis](docs/2026-07-01-orthogonal-analysis.md) — 五層是不是真的互相獨立?找到的隱藏邊
- [computation-model-first-principles](docs/2026-07-01-computation-model-first-principles.md) —
  Computation Model 這一層,從第一原理重新挖出來的定義

## 出處

框架第一次被具體套用在一篇論文的定位論證上,是 `enact` repo 的
`research/raws/2026-06-12-layer-taxonomy-and-gap-framing.md`(Paper 1: Actor-Based Agent
Runtime 的 Gap section 推導)——那份混了論文專屬的分析,留在 enact 那邊,不搬過來;這裡只放
通用、不綁論文的框架本體。
