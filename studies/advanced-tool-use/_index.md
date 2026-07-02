---
date: 2026-07-02
tags:
  - advanced-tool-use
  - index
---

# advanced-tool-use — 導覽

> Claude Developer Platform 自己出的三個 beta 功能(Tool Search Tool、Programmatic Tool
> Calling、Tool Use Examples),管的是「Claude 拿到一堆工具時怎麼處理」——工具不一定來自
> MCP,是 Claude API 層的能力,不是 MCP 協定本身的東西,所以獨立開一個主題,不掛在 mcp 底下。

## 文件

- [tool-search-and-programmatic-calling](docs/2026-07-02-tool-search-and-programmatic-calling.md) —
  Tool Search Tool(`defer_loading`,省最多 95% context)、Programmatic Tool Calling
  (`allowed_callers`,沙箱裡跑完才回報)、Tool Use Examples(`input_examples`,跟省 context
  無關,解的是準確度問題)、跟 MCP 的關係、跟 Skills 的關係(同一個 progressive disclosure
  原理,不同粒度)

## 出處

查證自 Anthropic 官方 engineering 部落格與 Claude Platform 文件,經 context7,2026-07-02。

## 起於

從 [mcp](../mcp/_index.md) 主題的太多工具問題筆記聊出來的,但範圍不屬於 MCP(這是 Claude API
本身的功能,不是協定),所以另開主題——理由見
[mcp-tool-scaling-problem](../mcp/docs/2026-07-02-mcp-tool-scaling-problem.md) 最後一段。
