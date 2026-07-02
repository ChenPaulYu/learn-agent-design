---
date: 2026-07-02
tags:
  - mcp
  - architecture
  - gateway
---

# 多 Server 疊加:一個 MCP server 自己當另一個 server 的 client

問的是:一個 MCP server 自己可不可以當另一個 server 的 client,把好幾個下游 server 包成一個
統一入口?**這不是官方規格定義的東西**——查了規格倉庫,官方明確定義的「聚合」只在 registry
(discovery)這一層(subregistry 抓 MCP Registry 的 metadata,見
[`registry-aggregators.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/registry/registry-aggregators.mdx)),沒有在「執行期怎麼把多個 server 的工具呼叫代理起來」這一層定義任何東西——這篇的內容全部是社群/廠商做出來的架構模式,不是規格文字,查證方式也是網路搜尋,不是 context7。

## MCP Gateway 是什麼:一個 host 原本要接 N 條線,現在只接 1 條

> "An MCP gateway is an intermediary layer that simplifies how AI applications connect to
> multiple MCP servers, acting as a single point of entry for AI agents... Instead of agents
> connecting directly to dozens of different tool endpoints, they all connect to a single,
> unified gateway endpoint, which then securely routes requests to the appropriate upstream
> tools."

直覺上這正好打破了 101 筆記裡強調的「一個 server 一條專屬線」——但拆開看,規則沒被打破:
host 那端看到的還是「一條線接一個 server」,只是那個「server」自己背後又接了好幾條線去下游
真正的 server。從 host 的角度,gateway **看起來就是一個普通的 MCP server**,一對一連線的
規則完全沒變;變的是這個 server 自己身兼 client 的角色。

## 具體要做的三件事

- **工具聚合(Tool Aggregation)**——gateway 呼叫每個下游 server 的 `tools/list`,把結果全部
  合併成一份清單,再原樣提供給 host。
- **請求路由(name-prefixing)**——工具名字自動加上後端名稱當前綴(例如
  `github__issue_read`),host 呼叫這個名字時,gateway 才知道要轉給哪個下游 server。這是
  「一個統一入口」實際上怎麼避免工具名字互相撞名的具體做法。
- **Session 合併**——gateway 要把多個下游 server 各自的 session id 編碼成一個對 host 看起來
  統一的 session,還要處理多個下游 SSE 串流合併成一條、`Last-Event-ID` 斷線續傳要重新對應到
  正確的下游串流。這是上次 wire-protocol 筆記講的斷線續傳機制,疊了一層 gateway 之後複雜度
  直接乘上去——原本一條 client-server 連線的 session 管理,現在變成要幫每個下游各管一份、
  再合併成一份。

## 新的風險:不是重複安全模型那篇,是疊加一層之後才出現的東西

安全模型那篇已經講過 Confused Deputy(proxy 對第三方共用同一個 client_id)——這裡的
Confused Deputy 是同一個機制,只是換到 gateway 的情境:「MCP proxy servers can introduce
confused-deputy issues if they act with broad privileges instead of enforcing per-client and
per-user consent」,道理一樣,不重複講。

真正**新的**風險是這個:

> "Privilege concentration places all tool capabilities behind a single MCP server whose
> compromise yields the union of every tool's permissions... once an agent authenticates to an
> MCP server, it implicitly gains access to every tool that server exposes, with no per-tool
> credential check."

翻成白話:host 原本接 5 個各自獨立的 server,一個被攻破,損失只是那一個 server 的權限;疊上
一個 gateway 之後,**host 只認得 gateway 這一個 server**——gateway 這一個點如果被攻破,拿到
的是「後面 5 個下游 server 權限的總和」。這不是「多一個攻擊面」,是「把原本分散的風險,主動
集中到一個點上」——用一條線換方便,代價是那條線變成單點故障。

還有一個順帶發現的操作性問題:**稽核軌跡碎片化**(audit trail fragmentation)——沒有 gateway
時,每個下游 server 自己記自己的 log;疊了 gateway 之後,一次使用者請求可能觸發好幾個下游
呼叫,但這些呼叫散落在各自的 log 裡,沒有一條「這次使用者請求,實際觸發了哪些下游呼叫」的
統一軌跡——除非 gateway 自己額外做這件事。

## 真的有人在做這個——不是紙上談兵的架構圖

這個模式已經有多個獨立的實作,包括微軟自己的版本:

- **Microsoft `mcp-gateway`**——GitHub 上的開源專案,定位是「reverse proxy and management
  layer for MCP servers」,專門處理 Kubernetes 環境下的 session-aware 路由跟生命週期管理。
- **MetaMCP**——輕量的開源「meta gateway」,用 Docker 把好幾個 MCP server 代理起來,對外
  露出一個統一 endpoint。
- **Stacklok Virtual MCP Server**、**Envoy AI Gateway**、**Kong**、**TrueFoundry**——都是
  獨立廠商各自做的同一種架構,不是同一家公司的產品線。

多個互不相關的團隊獨立收斂到同一種架構,通常代表這是真的解決了一個真實痛點,不是某個廠商
硬造出來的需求。

## 出處

Sources(全部經 WebSearch 於 2026-07-02 查證,非規格文件,是廠商/社群技術文章):
- [Envoy AI Gateway — MCP capability 文件](https://aigateway.envoyproxy.io/docs/0.4/capabilities/mcp/)
- [Microsoft `mcp-gateway`(GitHub)](https://github.com/microsoft/mcp-gateway)
- [What is an MCP Gateway? — Kong](https://konghq.com/blog/learning-center/what-is-a-mcp-gateway)
- [What Is an MCP Gateway: Architecture and Use Cases — TrueFoundry](https://www.truefoundry.com/blog/what-is-mcp-gateway)
- [Introducing Virtual MCP Server — Stacklok](https://stacklok.com/blog/introducing-virtual-mcp-server-unified-gateway-for-multi-mcp-workflows/)
- [MCP Gateways: A Developer's Guide — Composio](https://composio.dev/content/mcp-gateways-guide)
- [Top 8 MCP Security Risks — Cequence](https://www.cequence.ai/learn/model-context-protocol/top-8-mcp-security-risks-and-how-to-prevent-them/)
  ——Privilege Concentration、單點故障、稽核軌跡碎片化。
- [The complete guide to MCP security — WorkOS](https://workos.com/blog/mcp-security-risks-best-practices)
  ——gateway 情境下的 Confused Deputy 重述。

官方規格對照:
- [`docs/registry/registry-aggregators.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/registry/registry-aggregators.mdx)
  ——證實官方定義的「聚合」只在 registry/discovery 層,不是這篇講的執行期 gateway。

**誠實聲明**:這篇跟其他 MCP 筆記不一樣的地方是——查證對象從頭到尾都是廠商部落格跟開源專案,
不是官方規格。這代表「這個模式存在、被多方獨立實作」是有查證的事實,但「這個模式該怎麼做才
正確」沒有一份官方規格背書,各家廠商的具體做法可能互相不一致,拿這篇當「MCP 官方推薦的做法」
引用是不準確的。
