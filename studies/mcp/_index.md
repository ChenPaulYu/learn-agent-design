---
date: 2026-07-02
tags:
  - mcp
  - index
---

# mcp — 導覽

> Anthropic 開的 Model Context Protocol:AI 應用跟外部工具/資料源之間的通用線路規格。這裡先讀
> 官方規格把架構跟六個 primitive 弄懂,再用官方 Python SDK 寫一個最小 server + client 實際跑一輪。

## 文件

- [mcp-architecture-and-primitives](docs/2026-07-02-mcp-architecture-and-primitives.md) —
  Host/Client/Server 三層架構、六個 primitive(server 端 Tools/Resources/Prompts,client 端
  Sampling/Elicitation/Roots)、Sampling/Elicitation/Roots 的人工審核鏈與「LLM 需要知道嗎」、
  initialize 握手與 capability 協商、stdio vs Streamable HTTP transport、MCP 從 LSP + Tool
  Use 衍生出來的脈絡(Fit/Adapt/New)
- [mcp-wire-protocol-deep-dive](docs/2026-07-02-mcp-wire-protocol-deep-dive.md) —
  往下一層的線路細節:LSP 具體怎麼實作(1:1 server、`Content-Length` 分幀)、為什麼選
  JSON-RPC、JSON-RPC 跟 gRPC 的關係、JSON-RPC 不等於 WebSocket(為什麼遠端 transport 不選
  WebSocket)、request/response 的 id 配對機制
- [pages/101](pages/101.html) —
  互動版 MCP 101(可長期回看的教學頁,內容以 docs/ 為真相來源):圖 A 架構、圖 B 脈絡、
  圖 C 傳輸協定怎麼選,點卡片看細節
- [code/](code/) — 官方 Python SDK 寫的最小 server(一個 tool + 一個 resource + 一個 prompt)
  + 一個 client 跑過一輪 `list_tools` / `call_tool` / `read_resource` / `get_prompt`

## 出處

架構與 primitive 定義查證自 Anthropic/MCP 官方規格倉庫(`modelcontextprotocol/
modelcontextprotocol`,經 context7,2026-07-02);hands-on 用官方 `mcp` Python SDK
(`mcp.server.fastmcp.FastMCP`)。
