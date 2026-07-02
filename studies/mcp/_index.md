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
- [mcp-security-model](docs/2026-07-02-mcp-security-model.md) —
  進階主題(101 之外):誰該防誰的責任分工、遠端授權怎麼跑(OAuth 2.1、PKCE、resource
  indicator)、本機 server 淪陷風險、Confused Deputy Problem、Session Hijacking 兩種變體、
  Lethal Trifecta(私密資料 + 不信任內容 + 對外通訊三者疊加)、tool description 本身是攻擊面
- [mcp-tool-scaling-problem](docs/2026-07-02-mcp-tool-scaling-problem.md) —
  進階主題:一個 host 接多個 server 之後,工具清單塞爆 context 怎麼辦——Progressive Tool
  Discovery(先搜尋、後載入)、Programmatic Tool Calling / Code Mode(模型寫程式碼在沙箱裡
  跑,只把最終結果送回)、兩者疊加,以及跟 `tools/list` pagination 的區別
- [mcp-gateway-pattern](docs/2026-07-02-mcp-gateway-pattern.md) —
  進階主題(社群/廠商模式,非官方規格):一個 MCP server 自己當另一個 server 的 client——
  工具聚合、name-prefixing 路由、多下游 session 合併,新風險(privilege concentration:
  gateway 被攻破 = 拿到所有下游權限總和、稽核軌跡碎片化),微軟/MetaMCP/Stacklok 等多方
  獨立實作
- [mcp-ecosystem-reality](docs/2026-07-02-mcp-ecosystem-reality.md) —
  進階主題(查證方式是新聞/公告,不是規格):採用規模、OpenAI 的採用時間線、MCP 被捐給新成立的
  Agentic AI Foundation(不再是「Anthropic 的協定」)、registry 數字互相打架、registry 不做
  安全審查換來的新信任問題——M×N 問題解決了一半,換了個形狀重新出現
- [mcp-inspector](docs/2026-07-02-mcp-inspector.md) —
  官方的除錯/測試工具:MCPI(React 網頁 UI)+ MCPP(Node.js proxy,身兼 client 跟 HTTP server
  雙重角色,幫瀏覽器代打 stdio 連線)兩元件架構、四個分頁對應 Tools/Resources/Prompts/
  Notifications、三種指到 server 的情境(本機/npm/PyPI)、安全機制(localhost-only、session
  token、防 DNS rebinding)
- [pages/101](pages/101.html) —
  互動版 MCP 101(可長期回看的教學頁,內容以 docs/ 為真相來源):圖 A 架構、圖 B 脈絡、
  圖 C 傳輸協定怎麼選,點卡片看細節
- [pages/security](pages/security.html) —
  互動版安全模型:圖 A 責任分工、圖 B Lethal Trifecta(Venn 圖)、圖 C OAuth 2.1 流程、
  圖 D 四個具體攻擊
- [pages/tool-scaling](pages/tool-scaling.html) —
  互動版太多工具問題:圖 A 三個壞處、圖 B context window 填滿比例(笨拙 vs Progressive
  Discovery 切換)、圖 C 多輪來回 vs Code Mode 一次跑完
- [pages/ecosystem](pages/ecosystem.html) —
  互動版生態現況:圖 A 採用時間線、圖 B Platinum 會員(競爭對手同桌)、圖 C 三個 registry
  數字打架、圖 D 信任缺口切換
- [code/](code/) — 官方 Python SDK 寫的最小 server(一個 tool + 一個 resource + 一個 prompt)
  + 一個 client 跑過一輪 `list_tools` / `call_tool` / `read_resource` / `get_prompt`

## 出處

架構與 primitive 定義查證自 Anthropic/MCP 官方規格倉庫(`modelcontextprotocol/
modelcontextprotocol`,經 context7,2026-07-02);hands-on 用官方 `mcp` Python SDK
(`mcp.server.fastmcp.FastMCP`)。
