---
date: 2026-07-03
tags:
  - tool-use
  - built-in-tools
---

# Client Tools vs Server Tools:工具不是只有你自己定義的那一種

`tool-use-basics.md` 一路講的工具,都預設「你自己寫 schema、你自己執行」。官方文檔其實把
工具分成兩大類:「Tools are categorized as client tools or server tools. Client tools...
run within your application... Server tools... run on Anthropic's infrastructure, and you
receive the results directly without managing execution.」——這篇補的是這個缺口。

## 三種類型,不是兩種

官方分類其實是**兩個軸交叉出來的**:「schema 是誰定義的」跟「程式碼在哪裡執行」。組合出三種
實際存在的類型,第四種組合(Anthropic 執行你自己寫的程式碼)不存在:

| 類型 | Schema 誰定義 | 程式碼在哪執行 | 例子 |
|---|---|---|---|
| User-defined tools | 你自己 | 你自己的環境 | `tool-use-basics.md` 講的都是這種 |
| Anthropic-schema tools | Anthropic | 你自己的環境 | `bash`、`text_editor`、`computer`、`memory` |
| Server-executed tools | Anthropic | Anthropic 自己的伺服器 | `web_search`、`web_fetch`、`code_execution`、`advisor`、`tool_search` |

官方原句講中間這類的定位:「Anthropic-schema tools, such as bash, text_editor, computer, and
memory, are also client-executed, but Anthropic provides the schema, which Claude is optimized
to use reliably.」——Anthropic 把「怎麼設計 schema 讓模型用得順」這件最容易做錯的事先解決掉,
執行還是你的責任。

## User-defined tools:我們一路都在講的這種

工具定義、`tool_use`/`tool_result`、多輪迴圈——這些機制細節 `tool-use-basics.md` 已經完整
講過,這篇不重複。這一類的共同點是:**你決定這個工具存在、你決定它怎麼執行**,Anthropic 只
負責「模型判斷要不要呼叫、怎麼填參數」這一段。

## Anthropic-schema tools:說明書是 Anthropic 寫的,力氣是你自己出的

四個工具,都是「Anthropic 先把 schema 設計好、訓練模型可靠使用,但執行環境是你自己的」:

- **`bash`**(`bash_20250124`)——執行 shell 指令,指令在**你自己的機器/容器**裡跑。
- **`text_editor`**(`text_editor_20250728`,工具名 `str_replace_based_edit_tool`;更早的
  版本是 `text_editor_20250124`,工具名 `str_replace_editor`)——檔案讀寫,一樣你自己執行。
- **`computer`**(`computer_20251124`)——「Computer Use」的核心,操控螢幕/滑鼠/鍵盤,需要
  `computer-use-2025-11-24` 這個 beta header 才能用。
- **`memory`**(`memory_20250818`)——讓 Claude 讀寫檔案系統做長期記憶,能跟 context editing
  整合,用來維持長對話的狀態。這個概念其實跟 `agent-anatomy` 主題的記憶層是同一個問題,只是
  這裡是 Anthropic 官方給的一種具體實作,值得留意但這篇不展開。

三個工具(`bash`/`text_editor`/`computer`)常常一起出現在同一個請求裡——官方範例就是這樣
示範的,湊起來就是一個能操控整台電腦的 agent。

## Server-executed tools:你完全不用寫 tool_result

`web_search`、`web_fetch`、`code_execution`、`advisor`(還有前面已經講過的 `tool_search`)
——**你完全不用執行、不用組 `tool_result`**,官方原句:「For web_search, web_fetch,
code_execution, and tool_search, Anthropic runs the code... The server-side loop executes the
operation and feeds the output back to the model before the response reaches you.」

**回應格式本身也不一樣**——不是熟悉的 `tool_use` + 通用 `tool_result`,是 `server_tool_use`
+ 工具專屬的結果格式:

```json
[
  {
    "type": "server_tool_use",
    "id": "srvtoolu_01B3C4D5E6F7G8H9I0J1K2L3",
    "name": "bash_code_execution",
    "input": {"command": "ls -la | head -5"}
  },
  {
    "type": "bash_code_execution_tool_result",
    "tool_use_id": "srvtoolu_01B3C4D5E6F7G8H9I0J1K2L3",
    "content": {
      "type": "bash_code_execution_result",
      "stdout": "total 24\n...",
      "stderr": "",
      "return_code": 0
    }
  }
]
```

`web_search` 是這批裡歷史最久的,`web_search_20250305` 之後陸續出過 `web_search_20260209`、
`web_search_20260318`(新版支援動態過濾跟回應內容控制);`web_fetch` 也有對應的
`web_fetch_20260209`/`web_fetch_20260318`。

**`advisor`(`advisor_20260301`)是這四個裡性質最特別的一個**——其他三個都是「幫你碰外部
世界」(查資料、抓網頁、跑程式碼),`advisor` 是反過來**幫你的 agent 自我審查**:官方描述它
的功能是「provide actionable insights into tool-use configurations」,抓工具描述寫得不清楚、
prompt 跟工具能力對不上這類問題。機制上主線程(官方文檔稱為 worker model)遇到不確定的
tool-use 決策時,可以呼叫這個獨立的顧問角色幫忙把關,不是查外部資料——它有自己獨立的
`max_tokens`(超過會在 `advisor_result`/`advisor_redacted_result` 裡標記 `max_tokens` 並附
截斷說明)、自己的 caching。

## 一個容易搞混的地方:`code_execution` 出現兩次,身分不一樣

`advanced-tool-use.md` 裡的 Programmatic Tool Calling,用的是 `code_execution_20250825`
當**開關**——讓模型寫的程式碼可以呼叫「其他」已宣告的工具。這篇講的 `code_execution` 是
它**自己作為一個獨立 server tool 的身分**——單純執行一段程式碼、拿 stdout/stderr 回來,不
牽涉呼叫其他工具。同一個底層工具類型,兩種不同的用法角色,寫的時候容易混在一起,要分清楚:
一個是「執行環境」本身,一個是「執行環境被拿去當跳板呼叫別的工具」。

## 跟 OpenAI 對照:沒有正式分類詞彙,但具體工具幾乎都對得上

**OpenAI 沒有像 Anthropic 這樣正式命名「client tools vs server tools」的分類**——最接近的是
他們的 **Agents SDK**(一個包裝函式庫,不是核心 API 本身)裡有類似分組(Hosted OpenAI tools /
本地執行工具 / Shell tool 雙模式),但那是 SDK 層的方便命名,不是 API 官方教義。不過**具體
工具幾乎都找得到平行案例**,只是分類方式不同:

| Anthropic | OpenAI 對應 | 上線時間 | 執行方式 |
|---|---|---|---|
| `web_search` | `web_search`(前身 `web_search_preview`) | 2025-03-11 | server-executed |
| `code_execution` | `code_interpreter`(OpenAI 管理容器,20 分鐘閒置到期) | 2025-03-11 | server-executed |
| —(Anthropic 沒有) | `file_search`(RAG 查向量資料庫) | 2025-03-11 | server-executed |
| `advisor` | **沒找到對應** | — | — |
| `tool_search` | `tool_search` + `defer_loading`(gpt-5.4+) | 已確認存在 | 兩種模式都有 |
| `computer` | `computer-use-preview` | 2025-03-11 | client-executed |
| `text_editor` | `apply_patch`(V4A diff 格式) | 隨 GPT-5.1 推出 | client-executed |
| `bash` | Shell tool | 未查到確切日期 | **雙模式**,代管或自己執行都支援 |
| `memory` | **沒找到對應** | — | — |

三個 server-executed 工具(`web_search`/`code_interpreter`/`file_search`)是**同一天**
(2025-03-11)隨 Responses API 一起上線的,不是分批推出——跟 Anthropic 這幾個工具各自不同
時間點推出的節奏不一樣。**`advisor` 這種「幫 agent 自我審查」的工具,查完確認業界找不到
對照**,目前看起來是 Anthropic 獨有。`memory` 也沒找到 OpenAI 官方的對應功能。

**一個意外發現**:OpenAI 的 `tool_search` 其實有**兩種模式**,不是只有代管一種——一種是
伺服器代管(跟 Anthropic 一樣,你完全不用管);另一種是**你自己執行搜尋**,模型吐一個
`tool_search_call`,你自己去查、自己回 `tool_search_output`。這是 Anthropic 版本沒有的
彈性,`tool_search` 在 OpenAI 那邊反而橫跨了 client-executed 跟 server-executed 兩種模式。

## 誠實的邊界:Managed Agents 不算進來

查證過程中還發現一個叫 **Managed Agents** 的東西(`Session`/`SessionThread`、streaming
events、`always_allow`/`always_ask` 權限政策、multiagent roster)——這**不是又一種工具類型**,
是包在 Messages API 外面、完全不同的一層**代管 agent 執行環境**。`bash`/`web_search` 這些
名字剛好也出現在它的工具清單裡,但那是「這個代管環境內部用到的工具」,不是「工具本身的新分類」
——把它塞進這篇會把「單一 API 呼叫裡工具怎麼分類」跟「一整個 agent session 怎麼被代管執行」
這兩個不同層次的問題混在一起。這篇不收,查過但刻意不寫,不是沒查到。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-03 查證,官方文檔:

- [`agents-and-tools/tool-use/how-tool-use-works`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
  ——client tools / server tools 的核心分類原句、三種類型的定義。
- [`agents-and-tools/tool-use/computer-use-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
  ——`computer`/`text_editor`/`bash` 的版本識別碼與官方範例、`computer-use-2025-11-24` beta。
- [`agents-and-tools/tool-use/memory-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  ——`memory_20250818`、跟 context editing 的整合。
- [`agents-and-tools/tool-use/code-execution-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
  ——`server_tool_use`/`bash_code_execution_tool_result` 的具體 JSON 範例。
- [`agents-and-tools/tool-use/web-search-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
  ——`web_search` 版本歷史(`20250305` → `20260209` → `20260318`)。
- [`agents-and-tools/tool-use/tool-reference`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)
  ——工具總覽,確認 Advisor 也在這份清單裡。
- [`agents-and-tools/tool-use/advisor-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)
  ——`advisor_20260301`、功能描述、`max_tokens`/caching 參數。

**跟 OpenAI 對照部分**經一次委派 subagent 的 WebSearch 深度查證,2026-07-03:

- [`developers.openai.com/api/docs/guides/tools-web-search`](https://developers.openai.com/api/docs/guides/tools-web-search)
  ——`web_search`,2025-03-11 隨 Responses API 上線。
- [`developers.openai.com/api/docs/guides/tools-code-interpreter`](https://developers.openai.com/api/docs/guides/tools-code-interpreter)
  ——`code_interpreter`,OpenAI 管理容器,20 分鐘閒置到期。
- [`developers.openai.com/api/docs/guides/tools-file-search`](https://developers.openai.com/api/docs/guides/tools-file-search)
  ——`file_search`,同日(2025-03-11)promoted 進 Responses API。
- [`developers.openai.com/api/docs/guides/tools-tool-search`](https://developers.openai.com/api/docs/guides/tools-tool-search)
  ——`tool_search` 的兩種模式(代管 / 你自己執行)。
- [`developers.openai.com/api/docs/guides/tools-computer-use`](https://developers.openai.com/api/docs/guides/tools-computer-use)
  ——`computer-use-preview`,官方原句確認 client-executed。
- [`developers.openai.com/api/docs/guides/tools-apply-patch`](https://developers.openai.com/api/docs/guides/tools-apply-patch)
  ——`apply_patch`,V4A diff 格式,隨 GPT-5.1 推出。
- [`developers.openai.com/api/docs/guides/tools`](https://developers.openai.com/api/docs/guides/tools)
  ——Shell tool 的雙模式框架(代管或本地執行都支援)。
- [`openai.github.io/openai-agents-python/tools/`](https://openai.github.io/openai-agents-python/tools/)
  ——Agents SDK(非核心 API)裡最接近的分類命名,確認核心 API 本身沒有正式分類詞彙。

**誠實聲明**:Managed Agents(`managed-agents/quickstart`、`api/beta/sessions`)確認查過,
判斷是不同抽象層級後刻意不收進這篇,理由寫在上面的邊界段落,不是沒注意到。OpenAI 對照部分是
WebSearch 查證,信心等級不如 Anthropic 官方文檔那部分(context7 直接讀一手文檔)——Shell
tool 的確切上線日期沒查到,標記為未查證到,不是省略。
