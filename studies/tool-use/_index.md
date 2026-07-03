---
date: 2026-07-03
tags:
  - tool-use
  - index
---

# tool-use — 導覽

> Anthropic Claude API 的 Tool Use:LLM 怎麼決定要呼叫外部工具、怎麼把結果接回對話。從基礎
> 機制(定義工具、`tool_use`/`tool_result`、多輪迴圈)開始,再往上疊 advanced tool use 的
> 三個 beta 功能(Tool Search Tool、Programmatic Tool Calling、Tool Use Examples)。

## 文件

- [tool-use-basics](docs/2026-07-03-tool-use-basics.md) —
  工具定義(JSON Schema)、`tool_use`/`tool_result` content block、多輪對話的 `while` 迴圈、
  `is_error` 錯誤處理、`tool_choice`(auto/any/tool/none)+ 平行呼叫開關、跟 extended
  thinking 疊用時 thinking block 要一起傳回去的坑
- [advanced-tool-use](docs/2026-07-03-advanced-tool-use.md) —
  基礎機制會出問題的三個地方,各自對應一個 2025-11 推出的 beta 功能:Tool Search Tool
  (`defer_loading`,最多省 95% context)、Programmatic Tool Calling(`allowed_callers`,
  官方實例 43,588→27,297 token)、Tool Use Examples(`input_examples`,準確度 72%→90%)、
  三者疊在一起用各省不同的東西

## 出處

查證自 Anthropic 官方文檔,經 context7,2026-07-03:基礎機制查
`platform.claude.com/docs/en/agents-and-tools/tool-use/`,進階三功能查
`anthropic.com/engineering/advanced-tool-use`。
