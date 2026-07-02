---
date: 2026-07-02
tags:
  - mcp
  - json-rpc
  - transport
---

# MCP 的線路細節:LSP 怎麼實作、為什麼選 JSON-RPC、跟 gRPC / WebSocket 的關係

[mcp-architecture-and-primitives](2026-07-02-mcp-architecture-and-primitives.md) 講的是「MCP
長什麼樣子」;這篇是往下一層,挖「線路本身為什麼長這樣」。

## LSP 具體怎麼實作——MCP 抄的底

直覺會以為 LSP 是「一個 background server,所有編輯器共用」,官方規格寫的其實是反過來:

> "The lifecycle of a Language Server Protocol server is managed by the client. This means the
> client, such as VS Code or Emacs, is responsible for initiating the server process and
> determining when to shut it down."
> — [`specification.md` § Server lifecycle](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/specification.md)

**每個編輯器自己養一個專屬的 server process**,不是共用一個中央 server。VS Code 開一個
TypeScript 專案會自己啟動一個 `typescript-language-server` 子程序;Cursor 開同一個專案,會
自己啟動另一個獨立的 process。`initialize` 請求裡還帶了 client 自己的 `processId`,讓 server
能監控「養我的那個編輯器死掉了嗎」——這是 1:1 關係的直接證據。

**線路格式**,官方 base protocol 這樣定義,像 HTTP 一樣先有 header 再有內容:

```
Content-Length: 128\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"textDocument/completion","params":{...}}
```
— [`specification.md` § Base Protocol](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/specification.md)

`Content-Length` 告訴對方這則訊息有多長,後面才是 JSON-RPC 2.0 內容本體。傳輸管道可以是
stdio、pipe 或 socket。訊息分三種:**Request**(要回應)、**Response**(答案)、**Notification**
(單向,不用回應——例如 `textDocument/didChange` 這種「檔案改了」的事件)。

**MCP 沿用了同一套 JSON-RPC 內容,但分幀方式不一樣**:MCP 的 stdio transport 官方規格寫的是
**換行分隔**——一行一個完整 JSON 訊息,不能有內嵌換行,沒有 `Content-Length` header
(見 [`transports.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx))。內容語言一樣,分句子的標點規則不同。

## 為什麼選 JSON-RPC

官方 JSON-RPC 規格自己講的定位:

> "JSON-RPC is a stateless, light-weight remote procedure call (RPC) protocol... It is transport
> agnostic... It uses JSON... It is designed to be simple!"
> — [jsonrpc.org 規格 § Overview](https://www.jsonrpc.org/specification/index)

對 LSP/MCP 這種場景,三個特性剛好都用得到:

- **transport-agnostic**——同一套訊息語意,可以走 stdio、socket、HTTP,不用為每種傳輸重寫語意。
- **Notification(不用回應的單向訊息)**——請求不帶 `id` 就變成「不用等回應」的通知,適合「一直有
  小事件要推」的場景(檔案存檔、工具清單變了),不用每次都走一輪完整來回。
- **simple + 人可讀**——普通 JSON,debug 時直接印出來就看懂,不用額外的 binary 編碼工具。

## JSON-RPC 跟 gRPC 的關係——不是新舊版本,是兩個不同的設計點

都是「RPC」家族(把呼叫遠端方法包裝成像呼叫本地函式),但選了不同的取捨:

| 維度 | JSON-RPC 2.0 | gRPC |
|---|---|---|
| 訊息格式 | JSON 文字,人眼可讀 | Protocol Buffers 二進位(預設) |
| 傳輸方式 | 跟傳輸脫鉤 | 綁在 HTTP/2 上 |
| 型別 | 鬆散,不強制檢查 | 強型別,`.proto` 定義 + 編譯器產生程式碼 |
| Streaming | 沒有原生串流,只有請求/回應跟單向通知 | 原生四種:unary、server-stream、client-stream、bidirectional |

gRPC 官方部落格的定位:

> "gRPC is a modern RPC protocol implemented on top of HTTP/2. It offers advantages over
> traditional HTTP/REST/JSON mechanisms such as a binary protocol, multiplexing requests on one
> connection, header compression, and strongly typed service/message definitions."
> — [`grpc-load-balancing.md`](https://github.com/grpc/grpc.io/blob/main/content/en/blog/grpc-load-balancing.md)

`.proto` 定義完服務後,四種 RPC 方法是明文寫死的:

```protobuf
rpc GetFeature(Point) returns (Feature) {}                    // 一問一答
rpc ListFeatures(Rectangle) returns (stream Feature) {}        // server 連續推
rpc RecordRoute(stream Point) returns (RouteSummary) {}        // client 連續推
rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}  // 雙向同時推
```
— [`core-concepts.md`](https://github.com/grpc/grpc.io/blob/main/content/en/docs/what-is-grpc/core-concepts.md)

**MCP 現在跟 gRPC 的關係是「鋪路,還沒真的做」**。[SEP-1319](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/1319-decouple-request-payload-from-rpc-methods-definiti.mdx)
把「資料長什麼樣」(`CallToolRequestParams` 這種 payload)跟「用 JSON-RPC 包裝它」拆成兩層,
動機寫得很直接:「to support transports like gRPC (which is currently a popular ask from the
community), a transport-agnostic definition of its request and response messages [is needed].
The current structure makes this practically impossible.」——先拆開,以後才有機會加 gRPC binding
而不用整份規格重寫,不是現在就要把 JSON-RPC 換掉。

## JSON-RPC 不等於 WebSocket——這是兩個不同層的東西

JSON-RPC 是**說什麼語言**(`method`/`params`/`id` 這種訊息結構),WebSocket 是**用什麼管道講話**
(一種持續開著的雙向傳輸)。兩者不衝突,你可以「JSON-RPC 內容 + WebSocket 傳輸」一起用——只是
MCP 的官方 transport 選的不是這條路,是本機 stdio + 遠端 **Streamable HTTP**(普通 HTTP
POST 送、可選的 GET+SSE 收)。

**為什麼遠端場景不選 WebSocket**,兩個官方理由:

1. **MCP 正在往「協定本身無狀態」的方向走**,WebSocket 恰恰是「持續佔用一條管道」的極致代表:

   > "MCP was originally designed as a stateful protocol. Clients and servers maintain mutual
   > awareness through a persistent, bidirectional channel that begins with a handshake...
   > Because this state remains fixed throughout the connection, scaling requires techniques
   > like sticky sessions or distributed session storage."
   > — [`2025-12-19-mcp-transport-future.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-12-19-mcp-transport-future.md)

   一條 WebSocket 連線會把 client 綁死在某一台特定的 server 機器上,雲端多機器場景下逼你搞
   sticky session 或分散式 session 同步。方向反過來,是想讓每個請求可以隨便丟給任何一台機器
   處理。

2. **留在普通 HTTP 語意上,現有基礎設施不用改**:

   > "By mirroring key fields from the JSON-RPC payload into HTTP headers, network intermediaries
   > such as load balancers, proxies, and observability tools can route and process MCP traffic
   > without deep packet inspection."
   > — [SEP-2243](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2243-http-standardization.mdx)

   WebSocket 需要先用 HTTP Upgrade 換協定,有些防火牆/舊代理伺服器對這個換協定動作不友善。
   Streamable HTTP 靠「POST 送、GET+SSE 收」湊出雙向能力,兩個都是大家都懂的 HTTP 老招,不用
   換協定。

舊版規格(2024-11-05)其實是兩個獨立 endpoint(一個 SSE 收、一個 POST 送),新版
Streamable HTTP 把它們合併成一個 endpoint 同時支援 POST/GET(見
[`transports.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx))。

## 斷線怎麼辦——Resumability 跟 Session

選了 Streamable HTTP 不選 WebSocket,省了協定升級的麻煩,但代價是:那條 SSE 串流一樣可能斷
(網路抖動、代理逾時)。MCP 用兩個獨立機制分別處理「斷線後怎麼接回來」跟「怎麼認得是同一次對話」。

**斷線續傳**——server 可以幫每個 SSE 事件掛一個 `id`,斷線後 client 用 HTTP GET 重新連,帶著
`Last-Event-ID` header,server 就從那個點之後重播:

> "If the client wishes to resume after a disconnection, it SHOULD issue an HTTP GET to the MCP
> endpoint and include the `Last-Event-ID` header. The server MAY use this header to replay
> messages that would have been sent after the last event ID on the stream that was
> disconnected... The server MUST NOT replay messages that would have been delivered on a
> different stream."
> — [`transports.mdx` § Resumability and Redelivery](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx)

重點是最後一句:重播只認**同一條串流**,不會把 A 串流斷線的補償訊息塞進 B 串流——這條邊界是
避免訊息送錯管道。

**Session 管理**——跟斷線續傳是分開的另一層:server 在 `initialize` 回應時可以發一個
`MCP-Session-Id`,之後 client 每個請求都要帶著它。Session 被 server 終止後,帶著舊 id 的請求
會收到 404,client 必須重新 `initialize` 拿新的 session(見同一份 `transports.mdx`)。斷線續傳
解決「這條串流斷了,接得回來嗎」;session 解決「這整段對話還算不算數」——兩個問題,不是同一件事。

## Request/Response 怎麼配對 id

JSON-RPC 本身就定義好的機制,MCP 直接照用:

```typescript
// RequestId 的型別
type RequestId = string | number;
```
— [`schema.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/schema.mdx)

規則:

1. **發請求的一方自己決定 id**——字串或數字,自己挑。
2. **回應必須原封不動帶回同一個 id**——官方規格:「id 必須符合原 Request 的 id,連 id 都認不出來
   的錯誤(如 parse error)才給 `null`」([jsonrpc.org](https://www.jsonrpc.org/specification/index))。
3. **發送方自己維護一張「還在等誰回應」的表**——送出請求時把 id 對應到「我在等這個結果」記下來;
   收到回應時拿 id 查表配對。這張表不是協定規定的存法,是每個實作自己該做的事。
4. **id 只要求「同一個發送方,還沒收到回應前別重複用」**,不是全域唯一——MCP 把這規則寫得更
   精確:「a sender MUST NOT issue a request whose `id` matches that of another request it has
   sent and not yet received a response for」([SEP-2567](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2567-sessionless-mcp.md))。因為 MCP 是雙向的,
   **client 跟 server 各自維護自己的 id 序列**——server 發 `sampling/createMessage` 時是自己
   挑一個 id、自己等回應,跟 client 平常發請求用的序列互不相關。
5. **Notification 完全跳過這套機制**——沒有 `id` 欄位,天生不用等回應,也就沒有配對這回事。

官方 Python/TypeScript SDK 都內建幫你管這張表——這也是為什麼
[`../code/client.py`](../code/client.py) 完全沒出現手動比對 id 的程式碼。

## 長時間任務怎麼處理——Progress 跟 Tasks

一問一答的 request/response 模型,碰到「這個工具要跑五分鐘」就卡住——client 只能乾等,也不知道
到底跑到哪了。MCP 有兩個機制處理這件事,一個穩定、一個還在提案階段。

**Progress notifications(穩定,已在正式規格裡)**——發請求時在 `_meta.progressToken` 帶一個
自己選的 token,server 就可以在結果送回來之前,先推幾則進度通知:

```json
// 請求時附上 token
{"jsonrpc": "2.0", "id": 1, "method": "some_method", "params": {"_meta": {"progressToken": "abc123"}}}
// server 跑到一半推進度(可以推多次)
{"jsonrpc": "2.0", "method": "notifications/progress",
 "params": {"progressToken": "abc123", "progress": 50, "total": 100, "message": "Reticulating splines..."}}
```

規則很直白:progress 數值只能往上走,`total` 可以留空(代表不知道總量,但至少讓 client 知道
「還在動」),收到終態(完成/失敗/取消)之後就不能再推進度了(見
[`progress.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/utilities/progress.mdx))。

**Tasks(SEP,提案階段,還沒定案)**——比進度通知更進一步:整個請求變成一個有 id、有狀態機的
物件,client 可以隨時 `tasks/get` 去問「現在跑到哪」,不用一直掛著等:

```json
// 問任務現在的狀態
{"jsonrpc": "2.0", "method": "tasks/get", "params": {"taskId": "786512e2-..."}}
// server 答:還在跑,建議 5 秒後再問一次
{"jsonrpc": "2.0", "id": 1,
 "result": {"resultType": "task", "taskId": "786512e2-...", "status": "working",
            "createdAt": "2025-11-25T10:30:00Z", "pollIntervalMs": 5000}}
```

狀態機是 `working` → `completed`/`failed`/`cancelled`/`input_required`。這個機制目前是
[SEP-2663](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2663-tasks-extension.mdx)
的提案內容,**還沒進正式規格**,官方文件裡看到的兩個回應範例格式甚至互相有點不一致(`resultType`
一個寫 `"task"`、一個寫 `"complete"`)——這正是提案階段常見的樣子,細節還在收斂,不是穩定
API,拿來當「這是 MCP 現在的樣子」引用要小心。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-02 抓取查證。

**LSP 實作**
- [`specification.md`(LSP 3.17)](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/specification.md)
  ——Server lifecycle 由 client 管理、Base Protocol(`Content-Length` header + JSON-RPC 內容)。
- [`workspace/configuration.md`](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/workspace/configuration.md)、
  [`showMessageRequest.md`](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_includes/messages/3.17/showMessageRequest.md)、
  [`registerCapability.md`](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_includes/messages/3.17/registerCapability.md)、
  [`applyEdit.md`](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/workspace/applyEdit.md)
  ——四個 server→client 反向請求的官方範例,證明「反向呼叫」不是 MCP 發明的。

**JSON-RPC 本身**
- [jsonrpc.org 規格](https://www.jsonrpc.org/specification/index)——Overview 定位句、
  Notification 定義、Request/Response object 結構、id 配對規則、錯誤碼表。

**gRPC**
- [`core-concepts.md`](https://github.com/grpc/grpc.io/blob/main/content/en/docs/what-is-grpc/core-concepts.md)、
  [`introduction.md`](https://github.com/grpc/grpc.io/blob/main/content/en/docs/what-is-grpc/introduction.md)
  ——service 定義、四種 RPC 方法、Protocol Buffers 預設序列化。
- [`grpc-on-http2.md`](https://github.com/grpc/grpc.io/blob/main/content/en/blog/grpc-on-http2.md)、
  [`grpc-load-balancing.md`](https://github.com/grpc/grpc.io/blob/main/content/en/blog/grpc-load-balancing.md)
  ——HTTP/2 特性、gRPC 對 HTTP/REST/JSON 的定位句。

**MCP transport / SEP**
- [`specification/2025-11-25/basic/transports.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx)
  ——stdio 換行分隔規則、Streamable HTTP 的 POST/GET+SSE 設計。
- [`specification/2024-11-05/basic/transports.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2024-11-05/basic/transports.mdx)
  ——舊版 HTTP+SSE 雙 endpoint 設計,對照新版差異。
- [SEP-2243](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2243-http-standardization.mdx)
  ——HTTP header 標準化,讓中間設備不用 deep packet inspection 就能路由。
- [SEP-2575 `stateless-mcp`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2575-stateless-mcp.mdx)
  ——目前 stateful handshake 的爭議、「optional handshake」替代方案為何被否決。
- [`2025-12-19-mcp-transport-future.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-12-19-mcp-transport-future.md)
  ——stateful 協定現況、sticky session 問題、無狀態路線圖。
- [SEP-1319](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/1319-decouple-request-payload-from-rpc-methods-definiti.mdx)
  ——拆開 payload 跟 RPC method 的動機,為未來 gRPC binding 鋪路。
- [SEP-2567 `sessionless-mcp`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2567-sessionless-mcp.md)
  ——request id 唯一性從「per-session」重新定義為「per-sender、回應前不可重複」。
- [`specification/2025-11-25/schema.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/schema.mdx)
  ——`RequestId` 型別定義。
- [`specification/2025-11-25/basic/utilities/progress.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/utilities/progress.mdx)
  ——progressToken、progress notification 的行為規則(穩定規格)。
- [SEP-2663 `tasks-extension`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2663-tasks-extension.mdx)
  ——Tasks 機制的提案內容(未定案),`tasks/get` 輪詢範例。

**FastAPI(對照用)**
- [`websockets.md`](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md)
  ——`@app.websocket` 的 full-duplex 單一 TCP 連線,對照一般 REST route 天生單向。
