---
date: 2026-07-02
tags:
  - mcp
  - index
---

# mcp — 導覽

> Anthropic 開的 Model Context Protocol:AI 應用跟外部工具/資料源之間的通用線路規格。這裡先讀
> 官方規格把架構跟六個 primitive 弄懂,再用官方 Python SDK 寫一個最小 server + client 實際跑一輪。

## Pages(讀這裡——互動教學頁,是實際會回頭看的東西)

- [pages/101](pages/101.html) —
  架構、六個 primitive(含 Logging/Completion、五種 Content Type、Resources 訂閱)、脈絡
  (M×N/LSP/A2A)、線路層(JSON-RPC/gRPC/WebSocket)、長時間任務與斷線續傳
- [pages/security](pages/security.html) —
  責任分工(Client 大樓/Server 工廠場景)、Lethal Trifecta(Venn 圖)、OAuth 2.1 流程
  (音樂節戴手環場景,含 server 怎麼驗 token)、四個具體攻擊
- [pages/tool-scaling](pages/tool-scaling.html) —
  太多工具問題三個壞處、Progressive Tool Discovery(context window 填滿比例切換)、
  Programmatic Tool Calling / Code Mode(多輪來回 vs 一次跑完)
- [pages/ecosystem](pages/ecosystem.html) —
  採用時間線、Agentic AI Foundation Platinum 會員、三個 registry 是誰在營運/收書規則、
  信任缺口切換
- [pages/inspector](pages/inspector.html) —
  瀏覽器/Proxy/Server 架構場景(Proxy 雙重角色)、四個分頁對應哪些 primitive、三層安全機制
- [code/](code/) — 官方 Python SDK 寫的最小 server(一個 tool + 一個 resource + 一個 prompt)
  + 一個 client 跑過一輪 `list_tools` / `call_tool` / `read_resource` / `get_prompt`

## Docs(查證筆記——只留還沒被 page 吸收的)

大部分主題寫完 page 後,doc 已經刪掉(內容被吸收進對應 page,doc 的工作就結束了——跟
`/shape` 的 thought 被 canon 吸收後可以清掉是同一個邏輯)。目前留著的,是**還沒有對應
page** 的:

- [mcp-gateway-pattern](docs/2026-07-02-mcp-gateway-pattern.md) —
  進階主題(社群/廠商模式,非官方規格):一個 MCP server 自己當另一個 server 的 client——
  工具聚合、name-prefixing 路由、多下游 session 合併,新風險(privilege concentration:
  gateway 被攻破 = 拿到所有下游權限總和、稽核軌跡碎片化),微軟/MetaMCP/Stacklok 等多方
  獨立實作

## 出處

架構與 primitive 定義查證自 Anthropic/MCP 官方規格倉庫(`modelcontextprotocol/
modelcontextprotocol`,經 context7,2026-07-02);hands-on 用官方 `mcp` Python SDK
(`mcp.server.fastmcp.FastMCP`)。
