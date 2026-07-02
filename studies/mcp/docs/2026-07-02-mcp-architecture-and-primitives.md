---
date: 2026-07-02
tags:
  - mcp
  - architecture
  - lineage
---

# MCP 架構、六個 primitive,以及它的脈絡

MCP(Model Context Protocol)是 Anthropic 開的一套「AI 應用怎麼接外部工具/資料」的通用線路規格——
不是某個工具的 API,而是工具跟 LLM 之間該講哪種語言的協定本身。目的是讓「一個 host 接 N 個
server」不用為每個 server 各自客製一條線,大家插同一種孔。

## 三個角色,不是兩個

MCP 不是單純的 client-server,是三層:

- **Host**——使用者實際在用的 AI 應用(例如 Claude Desktop、Claude Code)。
- **Client**——Host 內部,每個 server 各配一個的連線物件,負責跟一個 server 講 MCP。
- **Server**——真正擁有能力的一端(檔案系統、資料庫、Sentry……),可以是本機程序,也可以是遠端服務。

關鍵:**Client 跟 Server 是一對一的專屬連線**。Host 開了 4 個 client 就代表跟 4 個 server 各自
維持一條獨立連線,不是一條線多路復用。

```
Host (AI App)
 ├─ Client 1 ──dedicated── Server A (local, e.g. filesystem)
 ├─ Client 2 ──dedicated── Server B (local, e.g. database)
 └─ Client 3 ──dedicated── Server C (remote, e.g. Sentry)
```

## 六個 primitive,依「誰擁有」分成兩邊

MCP 的核心契約是六個 primitive,清楚分成 server 擁有 vs. client 擁有——這條線就是「誰對什麼有
權威」的邊界:

| 邊 | Primitive | 意思 |
|---|---|---|
| Server 擁有 | **Tools** | 可執行的函式(有 input schema,LLM 可以呼叫) |
| Server 擁有 | **Resources** | 可讀的資料源(檔案、DB 記錄……,唯讀情境資料) |
| Server 擁有 | **Prompts** | 可重用的 prompt 模板 |
| Client 擁有 | **Sampling** | Server 反過來請 client 幫它跑一次 LLM 生成 |
| Client 擁有 | **Elicitation** | Server 反過來向使用者要資訊(表單、確認) |
| Client 擁有 | **Roots** | Client 告訴 server 它能碰哪些檔案系統範圍 |

直覺會把 MCP 想成「server 給工具,client 只是接線」,但 Sampling/Elicitation/Roots 這三個
是反過來的——server 也可以對 client 發請求。這是雙向協定,不是單向的 RPC。

## Sampling/Elicitation/Roots:LLM 需要知道這件事嗎?

反直覺的答案:**大部分時候不需要。這三個不是寫進 prompt、也不是 post-training 灌進去的,是完全
由 client(host 應用程式的程式碼)在幫忙擋、幫忙跑腿**。

- **Sampling**——官方講的是「多層人工審核」,不是模型自己認得這個協定:「The sampling flow
  involves multiple human-in-the-loop checkpoints... The server initiates a sampling request,
  which the client presents to the user for approval or modification. The client then forwards
  the approved request to the AI model and presents the generated response back to the user for
  a final review before returning it to the server.」([`client-concepts.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/learn/client-concepts.mdx))
  模型收到的就是一段普通 messages,完全不知道這是 sampling 請求轉來的。
- **Elicitation**——更乾脆,不一定經過模型。Server 發 `elicitation/create`,client 直接跳表單
  (或轉 URL)給**使用者**填,填完直接回給 server(見 [`elicitation.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/elicitation.mdx))。
- **Roots**——最單純,就是 server 問 `roots/list`,client 直接回答能碰的資料夾清單,純 client
  端靜態設定查詢,跟 LLM 完全沒關係(見 [`roots.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/roots.mdx))。

真正需要 LLM「懂」的只有 **Tools**——但那也不是靠 MCP 專屬訓練,是借用早就存在的 function
calling / tool use 能力,MCP 只是把工具清單包裝成標準格式,每次請求塞進去當參數。

**這條「server 反過來呼叫 client」的機制,是 MCP 獨有的嗎?不是**——LSP 早就有一堆這種反向
請求:`window/showMessageRequest`(server 請 client 跳訊息框)、`workspace/configuration`
(server 反過來問 client 設定)、`workspace/applyEdit`(server 請 client 改檔案)、
`client/registerCapability`(server 動態註冊新功能)。MCP 是把這個既有機制,專門拿來開一條
「server 借用 client 手上的 LLM」的門,新的是**用途**,不是**機制**。

如果自己拿 FastAPI 搭一個後端要做到同樣的事,技術上做得到,但要換工具:一般 REST route
(`@app.get`/`@app.post`)天生單向,server 沒有反向管道,得換成
[`@app.websocket`](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md)
(full-duplex 單一 TCP 連線)。麻煩不在開一條雙向管道本身,是管道之上那層協定要自己重新發明:
請求跟回應怎麼配對 id、client 到底支不支援這個能力(能力協商)、審核這件事是規範還是自己記得寫。
MCP 存在的理由,就是讓這幾件事變成大家共用的一份規格,不用每對 client/server 各自重談一次
(細節見 [mcp-wire-protocol-deep-dive](2026-07-02-mcp-wire-protocol-deep-dive.md) 的 id 配對段落)。

## Lifecycle:先握手,再談能力

每條 client-server 連線開始都要先做 `initialize`:

1. Client 送 `protocolVersion` + 自己支援的 `capabilities`(如 `roots`、`sampling`、`elicitation`)
2. Server 回自己的 `protocolVersion` + `capabilities`(如 `tools`、`resources`、`prompts`)
3. 雙方都用「有沒有宣告某個 capability」來決定接下來能不能用某個 primitive——沒宣告
   `sampling` 的 client,server 就不能對它發 `sampling/createMessage`。

Capability 底下還有子欄位,例如 `tools: { listChanged: true }` 表示「這個 server 支援工具
清單變動時發通知」,`resources` 則多一個 `subscribe`,可以訂閱單一項目的變化。這一層設計的
用意是漸進式披露(progressive disclosure):協定本身很大,但每條連線只需要協商出雙方都用得到
的子集。

## Transport:兩種送 JSON-RPC 的方式

MCP 的訊息格式是 JSON-RPC 2.0,傳輸方式分兩種:

- **stdio**——host 直接把 server 當子程序啟動,用 stdin/stdout 傳訊息。用在本機 server(檔案
  系統、本機腳本),沒有網路開銷,但只能跑在同一台機器。
- **Streamable HTTP**——server 是獨立跑著的 HTTP 服務,client 用 HTTP POST 送請求,用一條可
  串流的回應通道收訊息(取代了舊版規格裡的 HTTP+SSE 雙通道設計)。用在遠端 server。

兩種 transport 之下的訊息語意完全一樣——這是刻意的分層:protocol semantics(JSON-RPC 方法、
primitive)跟 transport(訊息怎麼送)是兩個獨立關注點,新增一種 transport 不需要改 primitive
的定義。

JSON-RPC 跟 WebSocket 常被搞混,但它們不是同一層(一個是「說什麼語言」,一個是「用什麼管道
講話」),也不是互斥選項。MCP 為什麼遠端場景選 Streamable HTTP 不選 WebSocket、LSP 的線路
細節長什麼樣、gRPC 跟 JSON-RPC 的關係——這幾件事拉得比較深,整理進
[mcp-wire-protocol-deep-dive](2026-07-02-mcp-wire-protocol-deep-dive.md)。

## 脈絡:MCP 站在誰的肩膀上

MCP 不是憑空出現的協定,往前推可以看到三塊既有的東西:

1. **M×N 整合問題(MCP 之前的困境)**——如果每個 AI 應用都要各自客製「怎麼接檔案系統、怎麼接
   資料庫、怎麼接這個那個 API」,M 個應用 × N 個工具,就要寫 M×N 條各自不同的線。換一個 AI
   應用,前面所有工具整合等於重寫一遍。
2. **Language Server Protocol(LSP,2016,Microsoft)**——IDE 世界先遇過同一種形狀的問題:M 個
   編輯器 × N 種程式語言。LSP 讓每種語言只要寫一個 language server,任何編輯器裝上對應的
   client 就能用,把 M×N 條線變成 M+N 條。MCP 官方規格明文寫「取材自 LSP」(見下方出處)。
3. **Tool Use / Function Calling(2023,OpenAI function calling、Anthropic tool use 等
   LLM API)**——LLM 這邊已經先有「模型自己決定要呼叫哪個函式、帶什麼參數」的能力,解決的是
   另一半問題:讓模型知道「有工具可以叫」跟「怎麼叫」。

MCP(2024,Anthropic)把這三塊接在一起,可以拆成三種借用方式:

| 借用方式 | 內容 |
|---|---|
| **Fit(原樣借用)** | JSON-RPC 2.0 當線路格式,以及「client/server 一對一專屬連線」的接法——LSP 怎麼接,MCP 幾乎照抄。 |
| **Adapt(借了但放大形狀)** | LSP 標準化的是「語言功能」(補全、跳轉定義);MCP 把這個概念放大成「情境 primitive」——不只工具,還有可讀資料(Resources)跟模板(Prompts)。 |
| **New(LSP 沒有的)** | Server 反過來呼叫 client 的三個 primitive(Sampling / Elicitation / Roots)。LSP 的溝通基本上單向;MCP 因為要服務「會自主決策」的 LLM,才需要這條反向的門。 |

這條「Fit / Adapt / New」的拆法是這次對話自己的推導,不是官方逐字這樣講的分類——但「MCP 取材自
LSP」這件事本身,是官方規格 Overview 明文寫的。

互動版可以點著看:[mcp-101 互動圖解](../pages/101.html)。

## 跟 agent-anatomy 五層框架的對應

Tools/Resources/Prompts 這三個 server-side primitive,對應到
[agent-anatomy](../../agent-anatomy/_index.md) 五層框架裡的 **Tool** 層——MCP 是那一層目前
最主流的具體協定實作之一。Sampling/Elicitation 則有點特殊,是「Tool 層反過來要用 Runtime/
Pattern 層能力」的洞——值得之後回去對照 orthogonal-analysis 那篇找到的隱藏邊。

## 出處

以下都是這篇筆記實際查過的來源,全部經 [context7](https://context7.com) 於 2026-07-02 抓取
查證,可以照連結回去對——不是憑印象寫的:

**架構 / 三個角色 / 六個 primitive**
- [`docs/learn/architecture.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/learn/architecture.mdx)
  ——Host/Client/Server 圖、六個 primitive 的官方分類(server 端 Tools/Resources/Prompts,
  client 端 Sampling/Elicitation/Logging)。
- [`specification/2025-11-25/server/tools.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx)
  ——Tools capability 宣告(`listChanged`)。
- [`specification/2025-11-25/server/prompts.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/prompts.mdx)
  ——Prompts capability 宣告。
- [`specification/2025-11-25/client/sampling.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/sampling.mdx)
  ——`sampling/createMessage` 的請求格式範例。
- [SEP-1577 `sampling-with-tools.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/1577--sampling-with-tools.md)
  ——SamplingMessage 的 schema(user/assistant message、tool_use/tool_result content)。
- [`docs/learn/client-concepts.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/learn/client-concepts.mdx)
  ——Sampling 的多層人工審核流程(這篇筆記「LLM 需要知道這件事嗎」段落的主要來源)。
- [`specification/2025-11-25/client/elicitation.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/elicitation.mdx)、
  [`specification/2025-11-25/client/roots.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/roots.mdx)
  ——Elicitation 的表單/URL 兩種模式、Roots 的 `roots/list` 查詢。
- [`websockets.md`(FastAPI)](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md)
  ——自己搭後端要做到「反向呼叫」得換 `@app.websocket` 的對照依據。

**Lifecycle / capability 協商 / transport**
- [`specification/2025-11-25/basic/lifecycle.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/lifecycle.mdx)
  ——`initialize` 請求/回應範例、capability negotiation 的完整說明(這篇筆記的 lifecycle 段落
  主要來源)。
- [SEP-2575 `stateless-mcp`](https://modelcontextprotocol.io/seps/2575-stateless-mcp)
  ——目前 stateful handshake 設計在雲端場景下的爭議,補充 transport 演化的背景。

**脈絡 / LSP 取材**
- [`specification/2025-11-25`(Overview)](https://modelcontextprotocol.io/specification/2025-11-25)
  ——官方原句:「MCP takes inspiration from the Language Server Protocol」,是「脈絡」那節
  唯一直接引用官方文字的地方。**M×N 整合問題的比喻、以及 Fit/Adapt/New 三欄拆法,是這次對話
  自己的推導跟整理,官方文件沒有逐字這樣分類**——查證時請把這條線分開看待。

**動手做(`../code/`)**
- 官方 Python SDK:PyPI 套件 [`mcp`](https://pypi.org/project/mcp/)(這篇筆記寫時裝的是
  1.28.1),原始碼在 [`modelcontextprotocol/python-sdk`](https://github.com/modelcontextprotocol/python-sdk)。
  `code/server.py`、`code/client.py` 裡的 decorator 用法(`@mcp.tool()` 要帶括號)是直接讀
  裝好的套件 `inspect.signature()` 對出來的,不是查文件猜的——因為 context7 上查到的
  [gofastmcp](https://gofastmcp.com) 文件是另一個獨立套件(`fastmcp`,支援不帶括號的
  `@mcp.tool`),跟官方 SDK 內建的 `mcp.server.fastmcp` 語法有落差,兩者別搞混。
