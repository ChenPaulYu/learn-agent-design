---
date: 2026-07-03
tags:
  - tool-use
  - advanced
---

# Advanced Tool Use:基礎機制夠用,但三個地方會開始出問題

`tool-use-basics` 那篇的機制(定義工具、`tool_use`/`tool_result` 迴圈)在工具數量小、參數
簡單、每次只需要呼叫一兩個工具時,完全夠用。三個地方會開始出問題,Claude Developer Platform
在 2025 年 11-12 月推出三個對應的 beta 功能,一次解一個:

| 問題 | 功能 | 上線時間 |
|---|---|---|
| 工具定義太多,還沒開始做事 context 就被吃掉一大塊 | Tool Search Tool | 2025-11-19/20 |
| 多步驟工具鏈,每一步都要跑一次完整推論來回 | Programmatic Tool Calling | 同一批 beta |
| 參數結構複雜,模型單看 schema 常常填錯 | Tool Use Examples | 同一批 beta |

三個都要靠同一個 beta header 開啟:`advanced-tool-use-2025-11-20`。

## Tool Search Tool:先給搜尋工具,不要一次全塞

跟 `tool-use-basics` 的差別在:工具不是全部一次列進 `tools` 陣列裡讓模型看到,而是標記
`defer_loading: true`,只有真的需要時才被搜尋、載入完整定義:

```json
{
  "tools": [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {...},
      "defer_loading": true
    }
  ]
}
```

官方原句:「This approach can reduce total context consumption by **up to 95%**」。搜尋方式
有三種類型可選(`tool_search_tool_regex`、BM25、自訂),文檔沒有進一步比較三者的適用情境
差異,只列出這三個選項存在。

**什麼時候該用**:工具定義總長超過 1 萬 token、遇到模型選錯工具的準確度問題、用 MCP 接了
多個 server、或工具數量超過 10 個。代價是多一個搜尋步驟,要拿 context 節省跟延遲增加做
權衡,不是無腦開就一定好。

**業界對照**:這不是 Anthropic 獨創,**OpenAI 也有幾乎同名的功能**——`tool_search` +
`defer_loading`(gpt-5.4+ 限定),[官方文檔](https://developers.openai.com/api/docs/guides/tools-tool-search)
直接點名解決的是同一個問題(N 個工具定義即使只用 2 個也要付全部 token)。**Google Gemini
沒有這個功能**——查到一個開發者在 GitHub 上直接跟 Google 要「跟 Anthropic/OpenAI 一樣的
功能」([issue #2185](https://github.com/googleapis/python-genai/issues/2185)),抱怨 Gemini
工具數超過 30-50 個就會退化,這是一個確認過的缺口。這塊屬於**業界共識**,只是 Google 還沒跟上。

## Programmatic Tool Calling:讓模型寫程式碼一次跑完,不要每步都推論一次

`tool-use-basics` 那個 `while` 迴圈的問題:工具鏈越長,來回次數越多,每一次都要付一次完整
推論的成本。Programmatic Tool Calling 讓模型改成寫一段 Python 程式碼,在沙箱裡一次跑完整條
邏輯,中間結果不進 context,只有最終結果回傳:

```json
{
  "tools": [
    {"type": "code_execution_20250825", "name": "code_execution"},
    {
      "name": "get_team_members",
      "description": "Get all members of a department...",
      "input_schema": {...},
      "allowed_callers": ["code_execution_20250825"]
    }
  ]
}
```

`allowed_callers` 是每個工具自己選擇要不要「開放給程式碼呼叫」——不是全域開關,是逐個工具
opt-in。開啟後,API 會把工具定義轉成 Python function,模型寫的程式碼可以直接呼叫這些
function,執行到需要工具結果時才暫停、等 API 把結果餵回這段程式碼,程式碼接著往下跑。

官方給的具體案例(預算合規檢查,要串好幾個工具查詢再判斷):用 Programmatic Tool Calling
把一個任務從 **43,588 token 壓到 27,297 token**——省的不是工具定義本身(那是 Tool Search
Tool 的事),是**中間結果不用來回搬進模型的 context**,靠減少推論次數同時省 token 跟延遲。

**業界對照**:這塊是三個功能裡最豐富的一塊——**OpenAI 的 Code Interpreter 不算同一件事**,
它能跑 Python,但沒辦法從程式碼裡直接呼叫使用者定義的其他工具,查到的是社群工作繞道,不是
官方內建橋接;**Google Gemini 也是分開的兩個工具**,程式碼執行歸程式碼執行,function call
還是得回傳給用戶端執行,不是從沙箱程式碼裡直接呼叫。**最接近的業界平行案例是 Cloudflare 的
「[Code Mode](https://blog.cloudflare.com/code-mode/)」**(2025-09-26)——讓 agent 寫
TypeScript 呼叫 MCP 工具(當成有型別的 API 函式),在沙箱裡執行,官方數字最多省 81%
token,這剛好是 `mcp/tool-scaling` 那篇筆記已經畫過的同一個概念。開源界則有
**Hugging Face smolagents 的 `CodeAgent`**,學術根源是 **CodeAct**(2024 論文)。**「Code
Mode」現在正變成業界通用叫法**,不只是 Cloudflare 自家用語;Anthropic 的「Programmatic Tool
Calling」是同一個概念的自家品牌名稱。這塊屬於**平行案例**——概念上大家都在做同一件事,但
Anthropic 走「原生 API 功能」路線,Cloudflare/smolagents 走「框架層實作」路線,不是同一種
產品形態。

## Tool Use Examples:不只給 schema,還給具體填法

`input_schema` 只講「這個參數是什麼型別」,沒講「實際上通常怎麼填」——遇到巢狀結構、可選
參數之間互相關聯時,模型單看 schema 常常猜錯。`input_examples` 直接給幾組具體範例:

```json
{
  "name": "create_ticket",
  "input_schema": { /* 跟平常一樣 */ },
  "input_examples": [
    {
      "title": "Login page returns 500 error",
      "priority": "critical",
      "labels": ["bug", "authentication", "production"],
      "reporter": {"id": "USR-12345", "name": "Jane Smith", "contact": {"email": "jane@acme.com"}},
      "escalation": {"level": 2, "notify_manager": true, "sla_hours": 4}
    },
    {"title": "Add dark mode support", "labels": ["feature-request", "ui"], "reporter": {"id": "USR-67890", "name": "Alex Chen"}},
    {"title": "Update API documentation"}
  ]
}
```

刻意給的三個範例,欄位完整度不一樣(第一個填滿巢狀結構跟可選欄位,第三個只填必要欄位)——
目的是讓模型看到「哪些欄位是真的常一起出現、哪些是可有可無」的實際搭配模式,不是只靠 schema
猜。官方內部測試數字:**準確度從 72% 提升到 90%**。

**業界對照**:查了 OpenAI、Google、Mistral、Meta,**都沒有找到對應功能**——OpenAI 的官方
指引是把範例寫進 `description` 自由文字裡,沒有獨立的 `examples` 欄位;Google Vertex AI 的
`FunctionDeclaration` schema 明講支援的屬性清單裡沒有 `example` 這個關鍵字,官方建議也是
塞進 `description`。這塊目前是**獨創**——沒有業界共識,也沒有平行案例,是三個功能裡唯一
一個「目前只有 Anthropic 有」的。

**跟 Agent Skills 的邊界**:同一主題底下沒有平行案例,不代表這個「給範例」的手法在 Anthropic
自己的產品線裡是孤例——`agent-skills-overview.md` 裡 `SKILL.md` 的「## Examples」段落 +
可以再拆的 `examples.md` 附屬檔案,解決的是同一種精神的問題(抽象規格講不清楚,靠具體案例
補上)。差別是顆粒度差一個量級:這裡的 `input_examples` 只到「一次函式呼叫的參數」,而且是
工具定義的一部分,只要工具出現在 `tools` 陣列就跟著送進去,每次都在;Skills 的 `examples.md`
範圍是「一整個任務/流程」,而且是 progressive disclosure 的最後一層,判斷需要才會去讀,不是
自動跟著送。詳細比較寫在 `agent-skills-overview.md`,這篇不重複。

## 業界對照總表:同一個問題,三種不同的普及程度

三個功能面對的都是同一個 context 預算問題,但放到整個產業去看,普及程度差很多,不是「Anthropic
出的功能都一樣新」:

| 功能 | 普及程度 | 證據 |
|---|---|---|
| Tool Search Tool | **業界共識** | OpenAI 幾乎同名功能已上線;Google 缺席但被開發者公開要求跟進 |
| Programmatic Tool Calling | **平行案例** | 概念上 Cloudflare(Code Mode)、Hugging Face smolagents 都在做同一件事,但走框架層而非原生 API 路線 |
| Tool Use Examples | **獨創** | OpenAI/Google/Mistral/Meta 都沒有對應功能,沒有查到業界通用叫法 |

## 三個功能不是互斥,是疊在一起用

`tool-use-basics` 已經完整解釋過三個功能各自解的是同一個 context 預算問題的不同切面——
不衝突,可以同時開:先用 Tool Search Tool 把工具清單縮小到真正需要的幾個、載入它們的完整
定義,再用 Programmatic Tool Calling 把邏輯寫成一段程式碼一次跑完,個別工具再用
`input_examples` 提高填參數的準確度。三層省的是三種不同的東西——定義、來回次數、填錯率。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-03 查證,官方來源(`anthropic.com/
engineering/advanced-tool-use`):

- **Tool Search Tool**——`defer_loading`、`tool_search_tool_regex_20251119` 版本識別碼、
  「up to 95%」context 節省原句、適用情境判準(>10K token、準確度問題、多 MCP server、
  ≥10 個工具)。
- **Programmatic Tool Calling**——`allowed_callers`、`code_execution_20250825`、預算合規
  檢查案例的具體數字(43,588 → 27,297 token)。
- **Tool Use Examples**——`input_examples` 欄位格式、官方內部測試準確度數字(72% → 90%)。

**業界對照部分**經一次委派 subagent 的 WebSearch 深度查證,2026-07-03:

- [`developers.openai.com/api/docs/guides/tools-tool-search`](https://developers.openai.com/api/docs/guides/tools-tool-search)
  ——OpenAI 的 `tool_search` + `defer_loading`。
- [`github.com/googleapis/python-genai/issues/2185`](https://github.com/googleapis/python-genai/issues/2185)
  ——開發者要求 Google 跟進的 issue,證明 Gemini 缺席。
- [`ai.google.dev/gemini-api/docs/file-search`](https://ai.google.dev/gemini-api/docs/file-search)
  ——Gemini 唯一相鄰功能(RAG 查文件,不是查工具定義)。
- [`developers.openai.com/api/docs/guides/tools-code-interpreter`](https://developers.openai.com/api/docs/guides/tools-code-interpreter)
  ——OpenAI Code Interpreter,確認不能從程式碼裡呼叫其他工具。
- [`ai.google.dev/gemini-api/docs/code-execution`](https://ai.google.dev/gemini-api/docs/code-execution)
  ——Gemini Code Execution 跟 function calling 是分開協調的兩個工具。
- [`blog.cloudflare.com/code-mode`](https://blog.cloudflare.com/code-mode/)
  ——Cloudflare Code Mode,2025-09-26,以及[後續擴展到任意 MCP portal 的文章](https://blog.cloudflare.com/code-mode-mcp/)(2026-04-23)。
- [`huggingface.co/docs/smolagents`](https://huggingface.co/docs/smolagents)
  ——smolagents `CodeAgent`。
- [`developers.openai.com/api/docs/guides/function-calling`](https://developers.openai.com/api/docs/guides/function-calling)
  ——OpenAI Function Calling 官方指引,確認無獨立 examples 欄位。
- [`cloud.google.com/vertex-ai/.../Schema`](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/Schema)
  ——Vertex AI FunctionDeclaration schema 支援屬性清單,確認沒有 `example` 欄位。
- [`docs.mistral.ai/capabilities/function_calling`](https://docs.mistral.ai/capabilities/function_calling)
  ——Mistral function calling 文檔,確認無對應功能。
- [`llama.developer.meta.com/docs/features/tool-calling`](https://llama.developer.meta.com/docs/features/tool-calling)
  ——Meta Llama tool calling 文檔,確認無對應功能。

**誠實聲明**:regex/BM25/自訂三種 Tool Search Tool 實作的具體差異,官方 engineering blog
沒有進一步比較,只列出三個選項存在——這篇沒有查證到更細的選用判準,標記為留待以後有需要再
深入查證的缺口,不是查過但省略。業界對照部分是 WebSearch 查證,信心等級不如 Anthropic 官方
文檔那部分(context7 直接讀一手文檔)——沒有找到某功能不代表確定不存在,只代表查證當下沒
查到公開文檔佐證。
