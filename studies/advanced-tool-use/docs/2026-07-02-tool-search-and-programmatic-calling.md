---
date: 2026-07-02
tags:
  - claude-api
  - tool-use
---

# Advanced Tool Use:Claude API 自己解「太多工具」問題的三個功能

這不是 MCP 的東西——Tool Search Tool、Programmatic Tool Calling、Tool Use Examples 是 Claude
Developer Platform 的 API 功能,管的是「Claude 拿到一堆工具時怎麼處理」,工具**不一定來自
MCP**,自己在 app 裡手刻的工具定義一樣適用。這篇筆記單獨開一個主題,不塞進 MCP 底下,理由見
[mcp-tool-scaling-problem](../../mcp/docs/2026-07-02-mcp-tool-scaling-problem.md) 的最後一段。

> "Advanced tool use on the Claude Developer Platform introduces three beta features: Tool
> Search Tool for discovering tools on-demand without consuming context, Programmatic Tool
> Calling for invoking tools within a code execution environment to reduce context window
> impact, and Tool Use Examples for demonstrating effective tool usage beyond schema
> definitions."
> — [`anthropic.com/engineering/advanced-tool-use`](https://www.anthropic.com/engineering/advanced-tool-use)

三個都還是 **beta**,呼叫時要另外帶 beta header(`betas=["advanced-tool-use-2025-11-20"]`)——
還不是穩定的正式功能。

## Tool Search Tool——工具標成「延後載入」,搜到才真的塞進 context

用法是把大部分工具標 `defer_loading: true`,只先放一個搜尋工具本身進去:

```json
{
  "tools": [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {},
      "defer_loading": true
    }
  ]
}
```

搜尋工具本身有三種實作可選:regex、BM25、或自己客製。行為是:「Tools marked with
`defer_loading: true` are not loaded initially but can be searched for and loaded on-demand
when Claude needs their specific capabilities」——官方數字是**最多省下 95% 的 context 消耗**,
而且連帶讓工具選擇的準確度也變好(選項少了,選錯的機率自然下降)。

## Programmatic Tool Calling——模型寫程式碼,在沙箱裡跑完才回報

工具要先加一個 `code_execution` 類型的工具,個別工具再用 `allowed_callers` 選擇性開放給它
呼叫:

```json
{
  "tools": [
    {"type": "code_execution_20250825", "name": "code_execution"},
    {
      "name": "get_team_members",
      "description": "...",
      "input_schema": {},
      "allowed_callers": ["code_execution_20250825"]
    }
  ]
}
```

官方講的問題是:「context pollution from intermediate results and inference overhead」——
一般呼叫每次都要把中間結果送回模型,模型再決定下一步,工具鏈越長,來回越多次。Programmatic
Tool Calling 讓模型一次寫出一段完整的程式碼,在沙箱裡依序執行、處理中間資料,**只有最終結果**
送回模型。官方給的實例(查團隊預算合規)把 token 從 43,588 壓到 27,297——不是靠少做事,是靠
少讓中間資料進模型的 context。

## Tool Use Examples——跟省 context 無關,解的是另一個問題

三個功能裡唯一跟「太多工具」沒關係的一個。用 `input_examples` 欄位放幾個具體的呼叫範例,幫
模型理解「這個工具實際上該怎麼填」:

```json
{
  "name": "create_ticket",
  "input_schema": {},
  "input_examples": [
    {"title": "Login page returns 500 error", "priority": "critical", "labels": ["bug"], ...}
  ]
}
```

解的是**格式跟巢狀結構容易填錯**的準確度問題——schema 只講「這個欄位是什麼型別」,沒講「實際
上大家怎麼填」;範例補上這個空隙。跟前兩個功能不是同一類問題,只是同一篇公告一起發的。

## 這三個功能跟 MCP 的關係

MCP 官方的 `client-best-practices.mdx` 講的是**通用模式**(Progressive Discovery、
Programmatic Tool Calling / Code Mode),這三個 Claude API 功能是**同一家公司把同樣的模式做
成具體可以直接開的產品功能**——名字幾乎沒改。差別是 API 層的這幾個功能不管工具從哪來,MCP 只
管「跟 server 之間怎麼講話」;可以把透過 MCP 拿到的工具,一樣餵進 Tool Search Tool / Code
Execution 裡用,兩者不衝突,是不同層。

## 跟 Skills 的關係——同一個原理,不同的單位

Claude 的 Agent Skills 用的是同一套「先放輕量的、貴的東西延後載入」原理(Progressive
Disclosure),只是套用的**單位**不一樣:

> "Metadata (always loaded)... This lightweight metadata is loaded at startup and included in
> the system prompt, allowing many Skills to be installed without context penalty. Instructions
> (loaded when triggered)..."
> — [`agent-skills/overview`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

Tool Search Tool 管的是「單個工具的 schema」;Skills 管的是「一整包程序性知識(SKILL.md +
參考檔案 + 腳本)」。同一個原理,兩個不同粒度的實作。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-02 抓取查證:

- [`anthropic.com/engineering/advanced-tool-use`](https://www.anthropic.com/engineering/advanced-tool-use)
  ——三個 beta 功能的官方公告、Tool Search Tool 的 `defer_loading` 用法跟 95% 數字、
  Programmatic Tool Calling 的 `allowed_callers` 用法跟 43,588→27,297 的實例、Tool Use
  Examples 的 `input_examples` 用法、beta header 用法。
- [`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
  ——Skills 的三層載入設計(metadata 永遠載入、指令觸發才載入)。
