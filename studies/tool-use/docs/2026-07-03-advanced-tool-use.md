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

**誠實聲明**:regex/BM25/自訂三種 Tool Search Tool 實作的具體差異,官方 engineering blog
沒有進一步比較,只列出三個選項存在——這篇沒有查證到更細的選用判準,標記為留待以後有需要再
深入查證的缺口,不是查過但省略。
