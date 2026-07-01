---
date: 2026-07-01
tags:
  - agent-anatomy
  - reference
---

# OpenAI「harness engineering」是什麼(查證記錄)

> TL;DR — 這是查網路查到的外部定義,拿來解釋「為什麼我們把 Harness 這一層改名叫 Tool」的
> 出處記錄,不是我們自己的結論。

## 查到的定義

- **Harness engineering**:設計 environments、constraints、feedback loops,讓 AI agent
  在規模化下可靠的學科。formal 定義來自 OpenAI 2026-02-11 的一篇文章,標語是「Humans steer.
  Agents execute.」。核心組成:context architecture(分層漸進揭露)、agent specialization
  (限定 prompt + 限制工具)、persistent memory(檔案系統式的持久記憶)、structured execution
  (research→plan→execute→verify)。
- **Agent harness**(較廣義的業界用法):「圍繞在語言模型外面的整套軟體:tools、memory、
  state、execution、guardrails、observability」。核心是「決定 agent 什麼時候該停、錯誤怎麼
  處理、guardrails 怎麼設」。

## 對照我們的五層,OpenAI 的 harness 幾乎是三層的合體

| OpenAI harness 的組成 | 對到我們的哪一層 |
|---|---|
| structured execution、when to stop | Computation Model(控制流程、收斂判準) |
| persistent memory、context architecture、execution 的錯誤處理 | Runtime(state、context builder、tool dispatch) |
| tools、guardrails | Tool(我們原本叫 Harness 的那一層——工具集合 + 權限邊界) |

**結論**:OpenAI 的「harness」是工程實務上的統稱(幾乎等於「模型以外的所有工程」),不是一個
精確切開的架構層。我們的框架把這個大籠子拆成三個可以各自獨立驗證(orthogonal)、獨立定義
(first-principles)的小格子。因為同一個詞、範圍對不上會誤導讀者,所以把我們原本也叫「Harness」
的那一層改名叫 **Tool**(見
[five-layer-framework](2026-07-01-five-layer-framework.md) 的命名段落)。

## Sources

- [Harness engineering: leveraging Codex in an agent-first world | OpenAI](https://openai.com/index/harness-engineering/)
- [What Is Harness Engineering? Complete Guide for AI Agent Development (2026) | NxCode](https://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026)
- [What Is an Agent Harness? A Beginner's Guide | DataCamp](https://www.datacamp.com/blog/agent-harness)
- [Harness, Scaffold, and the AI Agent Terms Worth Getting Right](https://huggingface.co/blog/agent-glossary)
