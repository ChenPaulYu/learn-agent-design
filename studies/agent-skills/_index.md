---
date: 2026-07-02
tags:
  - agent-skills
  - index
---

# agent-skills — 導覽

> Anthropic 的 Agent Skills:把「怎麼做一件事」包成一個資料夾(`SKILL.md` + 附屬檔案),三層
> progressive disclosure 載入,需要時才讀。跟 MCP 太多工具問題那篇提過的 Tool Search Tool 是
> 同一個原理、不同粒度的內容;跟 Claude Code 的 Subagent/Hook 則是刻意設計成互斥的三個不同答案,
> 不同源。

## 文件

- [agent-skills-overview](docs/2026-07-02-agent-skills-overview.md) —
  三層載入模型、`SKILL.md` 結構、寫作準則(精簡是關鍵)、progressive disclosure 借自 1995
  年 Nielsen 的 UX 原則、沒有 Skills 之前的具體天花板(~10 個能力)、從哪裡來(2025-10 推出 →
  2025-12 開放成跨平台標準)、三個使用入口(claude.ai/API/Claude Code)、安全稽核(企業版
  風險分級)、跟 Tool Search Tool 的邊界(順序跟直覺相反,Skills 反而先推出)、跟 Subagent/Hook
  的邊界(不同源,三條獨立判斷軸)
- [pages/101](pages/101.html) —
  互動版 Agent Skills 101:圖 A 三層載入、圖 B 血緣(UX 1995 → 天花板 → 推出 → 開放標準)、
  圖 C 邊界(跟 Tool Search Tool、跟 Subagent/Hook)

## 出處

查證自 Anthropic 官方文檔(`platform.claude.com/docs/en/agents-and-tools/agent-skills/`,經
context7,2026-07-02)+ WebSearch(歷史時間線、Claude Code steering 生態的第三方/官方部落格)。
