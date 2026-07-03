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
  的邊界(不同源,三條獨立判斷軸)、跟 Workflow/MCP 的關係(推理整理,非官方比較——內部組織
  vs 碰外部世界,垂直不是同一排)
- [agent-skills-ecosystem-and-limitations](docs/2026-07-03-agent-skills-ecosystem-and-limitations.md) —
  查證對象是 arXiv preprint(2026 年最新研究,非官方文檔,信任等級不同):變形(純指示型 vs
  可執行型)、進階應用(CODESKILL 等 self-evolving skills)、現況(42,447 收集、31,132
  分析)、缺陷(品質分數 6.2/12 vs benchmark 10.1/12、精簡效果有實測數字、26.1% 至少一個
  安全漏洞)
- [pages/101](pages/101.html) —
  互動版 Agent Skills 101:圖 A 三層載入(手冊場景)、圖 B 血緣(UX 1995 → 天花板 → 推出 →
  開放標準)、圖 C 邊界(跟 Tool Search Tool、跟 Subagent/Hook,含委派場景比喻)
- [pages/ecosystem-and-limitations](pages/ecosystem-and-limitations.html) —
  互動版生態與缺陷:圖 A 變形(食譜卡比喻)、圖 B 進階應用(學徒筆記本比喻,CODESKILL 數字)、
  圖 C 現況與缺陷(品質分數長條圖、精簡效果、安全漏洞分布)

## 出處

查證自 Anthropic 官方文檔(`platform.claude.com/docs/en/agents-and-tools/agent-skills/`,經
context7,2026-07-02)+ WebSearch(歷史時間線、Claude Code steering 生態的第三方/官方部落格、
arXiv preprint 論文)。
