---
date: 2026-07-02
tags:
  - mcp
  - tooling
---

# MCP Inspector:官方自己的除錯/測試工具

官方定義:「an interactive developer tool designed for testing and debugging Model Context
Protocol (MCP) servers... allows developers to connect to MCP servers, inspect their resources,
test prompts, and monitor notifications」——一句話:**寫 server 的人自己先戳一遍看有沒有做對,
不用等到接上真正的 AI host 才發現東西壞了**。

## 架構:為什麼要拆成兩個東西

Inspector 不是一個單一程式,是**兩個元件**:

- **MCP Inspector Client(MCPI)**——一個 React 網頁 UI,瀏覽器裡看到的介面。
- **MCP Proxy(MCPP)**——一個 Node.js server,身兼兩個角色:對 MCP server 來說它是**client**
  (真的去連線、真的送 JSON-RPC),對瀏覽器來說它是**HTTP server**(把網頁 UI 端出來)。

拆成兩個的原因是**瀏覽器沒辦法自己開一個 stdio 子行程**——你的 server 可能是用 stdio 跑的一個
本機程式,瀏覽器 JavaScript 沒有權限直接 spawn 一個行程去接它。Proxy 存在的意義就是幫瀏覽器
「代打」這件事:它自己去連 server(不管是 stdio、SSE、還是 Streamable HTTP),再把結果轉譯成
瀏覽器聽得懂的介面——同一份 UI,不用管你的 server 用哪種 transport。

## 四個分頁,對應四個 primitive + 通知

- **Server connection pane**——選 transport、本機 server 的話可以自訂指令參數跟環境變數。
- **Tools tab**——列出所有工具、看 schema、帶自訂輸入去測試呼叫、看執行結果。
- **Resources tab**——列出所有 resource、看 metadata、檢視內容,也能測試訂閱(上次筆記補的
  `resources/subscribe` 機制,這裡就是拿來實測的地方)。
- **Prompts tab**——列出 prompt template、看參數、測試、預覽組出來的訊息長什麼樣。
- **Notifications pane**——把 server 送過來的所有 log/通知全部匯總在一個地方看。

四個分頁剛好對上 Tools/Resources/Prompts 三個 server 端 primitive,加一個看 Logging 通知的
地方——沒有專門測 Sampling/Elicitation/Roots 的分頁,因為那三個是**反過來**的方向(server 找
client 要東西),Inspector 本身扮演的是 client 角色,天生就在「被 server 呼叫」的那一端,不需要
額外分頁去模擬它。

## 怎麼指到你的 server——三種情境

```bash
# 本機開發中的 server(Node.js)
npx @modelcontextprotocol/inspector node path/to/server/index.js args...

# 本機開發中的 server(Python,用 uv)
npx @modelcontextprotocol/inspector uv --directory path/to/server run package-name args...

# 已發布在 npm 上的 server
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /Users/username/Desktop

# 已發布在 PyPI 上的 server
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code/mcp/servers.git
```

不用先安裝,`npx @modelcontextprotocol/inspector <command>` 直接跑;也有純 CLI 模式(不開瀏覽器
UI,直接在終端機跑指令、適合寫腳本自動化測試),跟開網頁 UI 的模式是同一個入口,差在給的指令
不同。

## 安全:預設只綁 localhost,而且要驗證身分

Inspector 開起來會佔兩個 port:UI 在 `6274`,proxy 在 `6277`,**兩個都預設只綁定
localhost**——不是隨便誰在同一個網路上都連得到。Proxy server 預設要求身分驗證:啟動時會生成
一個隨機的 session token,印在終端機裡。還特別防了一種攻擊:**DNS rebinding**——驗證進來的
請求的 `Origin` header,預設只准來自 `CLIENT_PORT`(預設 6274)的請求通過,擋掉惡意網頁想偷偷
從瀏覽器裡打你本機的 Inspector proxy。

這幾個安全設計跟前面安全模型筆記講的「本機 server 的風險」是同一個精神——Inspector 自己也是
一個在你機器上跑、能執行任意工具呼叫的東西,官方沒有因為它只是「開發工具」就放寬警惕。

## 出處

全部經 [context7](https://context7.com) + WebSearch 於 2026-07-02 查證:

- [`docs/tools/inspector.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/tools/inspector.mdx)
  ——官方定義、四個分頁的 Feature overview、CLI 指令範例(本機/npm/PyPI 三種情境)。
- [`github.com/modelcontextprotocol/inspector`](https://github.com/modelcontextprotocol/inspector)
  ——README 裡的架構說明(MCPI/MCPP 兩元件拆分、proxy 身兼 client+HTTP server 雙重角色)、
  port 配置(6274/6277)、安全機制(session token、Origin header 驗證防 DNS rebinding)。

**誠實聲明**:架構跟安全機制那兩節,官方規格倉庫(`docs/tools/inspector.mdx`)本身沒有寫到
這麼細,是另外去查 Inspector 自己的 GitHub repo README 補上的——這篇引用了兩個不同倉庫的內容,
不是單一來源。
