---
date: 2026-07-03
tags:
  - tool-use
  - index
---

# tool-use — 導覽

> Anthropic Claude API 的 Tool Use:LLM 怎麼決定要呼叫外部工具、怎麼把結果接回對話。先懂
> 概念(是什麼、為什麼、跟 structured output 的關係),再看 API 機制細節(定義工具、
> `tool_use`/`tool_result`、多輪迴圈)——這兩塊原本拆成兩篇,後來發現比既有慣例(MCP
> 101、agent-skills-overview 都是概念 + 機制放同一份)切得更細,合併回一篇。接著先看這個
> 機制的身世(學術先驅期 + 廠商官方搶跑時間軸)——身世那篇拆開是因為證據類型不同(有日期、
> 有信心分級),跟合併的理由不衝突;再往上疊 advanced tool use 的三個 beta 功能;最後補
> client/server tools 這塊之前完全沒寫過的缺口。

## 文件

- [tool-use-basics](docs/2026-07-03-tool-use-basics.md) —
  tool use 是什麼、為什麼需要它(agent 推理-行動迴圈裡「行動」這一格)、跟 structured
  output 的概念關係、什麼時候該用工具,加上 API 機制細節:工具定義(JSON Schema)、
  `tool_use`/`tool_result` content block、多輪對話的 `while` 迴圈、`is_error` 錯誤處理、
  `tool_choice`(auto/any/tool/none)+ 平行呼叫開關、跟 extended thinking 疊用時 thinking
  block 要一起傳回去的坑
- [tool-use-origins](docs/2026-07-03-tool-use-origins.md) —
  學術先驅期時間軸(WebGPT → SayCan → MRKL → ReAct → Toolformer → Gorilla/ToolLLM)、是
  OpenAI 的 Function Calling 讓這個「土法煉鋼時代」收斂成官方機制、三家廠商搶跑對照、
  function calling 先於 structured output 上線的方向反轉、Perplexity 不等官方機制自己
  上線的案例、現在(2026)原生訓練(SFT+RL 餵工具呼叫軌跡)取代了 prompt 教格式,但宣告
  工具清單這件事還是要做
- [advanced-tool-use](docs/2026-07-03-advanced-tool-use.md) —
  基礎機制會出問題的三個地方,各自對應一個 2025-11 推出的 beta 功能:Tool Search Tool
  (`defer_loading`,最多省 95% context)、Programmatic Tool Calling(`allowed_callers`,
  官方實例 43,588→27,297 token)、Tool Use Examples(`input_examples`,準確度 72%→90%)、
  三者疊在一起用各省不同的東西,加上業界對照總表:三個功能放到整個產業去看,普及程度差很多
  (Tool Search Tool 是業界共識、Programmatic Tool Calling 有平行案例如 Cloudflare Code
  Mode、Tool Use Examples 目前是 Anthropic 獨創)
- [pages/101](pages/101.html) —
  互動版 Tool Use 101,六張圖:圖 A 沒有 tool use 會怎樣、圖 B agent 推理-行動迴圈、圖 C
  跟 structured output 的關係 + 何時該用工具、圖 D 三段式流程(定義/呼叫/回結果)、圖 E
  多輪迴圈(成功 vs is_error 兩條路徑)、圖 F tool_choice 四種模式(含一排隨模式切換
  可拿/鎖住的工具卡片)+ extended thinking 的坑
- [pages/origins](pages/origins.html) —
  互動版「Tool Use 的身世」:圖 A 學術先驅期時間軸、圖 B 廠商搶跑對照(含終結土法煉鋼時代
  的那一天)、圖 C 反轉洞察、圖 D Perplexity 案例、圖 E 模型怎麼學會格式的三段式弧線
  (WebGPT 窄且訓練 → ReAct 廣但要教 → 現在廣且訓練,含 BFCL)
- [pages/advanced-tool-use](pages/advanced-tool-use.html) —
  互動版「Advanced Tool Use」:圖 A Tool Search Tool 的 context 節省對照(含 OpenAI/
  Google 業界對照)、圖 B Programmatic Tool Calling 的來回次數對照(含 Cloudflare Code
  Mode/smolagents 平行案例)、圖 C Tool Use Examples 的準確度對照(獨創,無業界對照,
  跟 Agent Skills 的 Examples/examples.md 邊界)、圖 D 三個功能的業界普及程度總表
- [tool-use-client-server-tools](docs/2026-07-03-tool-use-client-server-tools.md) —
  工具不是只有你自己定義的那一種:兩軸(schema 誰定義 × 程式碼在哪執行)交叉出三種類型
  (User-defined / Anthropic-schema / Server-executed)、Anthropic-schema tools
  (`bash`/`text_editor`/`computer`/`memory`)在你的環境裡跑、server-executed tools
  (`web_search`/`web_fetch`/`code_execution`/`advisor`)完全不用你動手、wire-format
  差異(`server_tool_use` + 工具專屬結果格式)、`code_execution` 兩種身分辨析、Managed
  Agents 為什麼刻意不收,加上跟 OpenAI 對照(9 組工具幾乎都有平行案例,但 `advisor`/`memory`
  查無對應,OpenAI 沒有正式的 client/server 分類詞彙、`tool_search` 反而橫跨兩種執行模式)
- [pages/client-server-tools](pages/client-server-tools.html) —
  互動版「Client Tools vs Server Tools」:圖 A 三種類型矩陣(含一格不存在的組合)、圖 B
  Anthropic-schema tools 場景圖、圖 C server-executed tools 場景圖(advisor 性質特別標
  出來)、圖 D 兩個誠實澄清(各配一張小 SVG)、圖 E 跟 OpenAI 的對照表

## 出處

查證自 Anthropic 官方文檔,經 context7,2026-07-03:概念與基礎機制查
`platform.claude.com/docs/en/agents-and-tools/tool-use/`,進階三功能查
`anthropic.com/engineering/advanced-tool-use`。身世那篇、以及進階三功能的業界對照部分,
查證自 WebSearch(arXiv preprint + 廠商官方 blog + 開發者社群)+ 兩次委派 subagent 的深度
查證,信心等級(VERIFIED/LIKELY/UNCERTAIN)標示在文件跟頁面裡,不是官方一手文檔的等級。
