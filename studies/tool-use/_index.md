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

## 出處

查證自 Anthropic 官方 Claude Platform 文檔(`platform.claude.com/docs/en/agents-and-tools/
tool-use/`,經 context7,2026-07-03)。
