---
date: 2026-07-02
tags:
  - mcp
  - ecosystem
---

# MCP 生態現況:M×N 問題解決了,換來一個新問題

前面幾篇筆記查的都是規格文件,這篇不是——查證方式是部落格、新聞、採用公告,不是官方規格,
因為問的問題本身就是「規格之外實際發生了什麼」。**注意這篇比其他幾篇更容易過期**:採用數字、
生態規模這種東西,查證當下(2026-07-02)是準的,幾個月後這些數字大概就舊了。

## 規模:一年內從內部實驗變成產業標準

Anthropic 自己的說法:「In one year, MCP became one of the fastest-growing and widely-adopted
open-source projects in AI with over **97 million monthly SDK downloads**, **10,000 active
servers** and first-class client support across major AI platforms like ChatGPT, Claude,
Cursor, Gemini, Microsoft Copilot, Visual Studio Code and many more.」
([`linuxfoundation.org` 公告](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation))

**OpenAI 的採用時間線**——這是最直接的「競爭對手都在用」訊號:2025 年 3 月官方採用 MCP、
整合進 ChatGPT desktop app;2025 年 9 月 ChatGPT apps 加入 MCP 支援。Google、Microsoft、
GitHub、Vercel、VS Code、Cursor 全部都有官方文件或公告顯示支援 MCP 或提供 MCP server 基礎
設施。

## 最大的事:MCP 已經不是「Anthropic 的協定」了

2025 年 12 月,Anthropic 把 MCP **捐給了一個新成立的基金會**——不是捐給既有的 Linux
Foundation 本體,是捐給 Linux Foundation 底下新設的一個 directed fund,叫 **Agentic AI
Foundation(AAIF)**:

> "Anthropic donated the Model Context Protocol (MCP) to the Agentic AI Foundation (AAIF), a
> directed fund under the Linux Foundation, with the foundation co-founded by Anthropic, Block
> and OpenAI, and with support from Google, Microsoft, Amazon Web Services (AWS), Cloudflare,
> and Bloomberg."
> — [`linuxfoundation.org` 公告](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)

Platinum 會員名單:AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、
OpenAI——**包含了 Anthropic 最直接的競爭對手**。同一輪捐贈裡,Block 捐了 `goose`(他們自己的
agent 框架),OpenAI 捐了 `AGENTS.md`(給 agent 讀的專案說明檔案格式標準)——三個公司同時把
各自的東西捐進同一個中立基金會,不是只有 MCP 單獨的動作。

治理機制本身官方說沒有大改:「The Model Context Protocol's governance model remained
unchanged: the project's maintainers continue to prioritize community input and transparent
decision-making」——換的是**掛在哪個組織底下**,不是換一套新的決策流程。

## Registry 是什麼——先講最基本的

MCP 這個協定本身,沒有內建一個「幫你找 server」的搜尋引擎——你想用一個 server,得自己先知道
它在哪、怎麼裝。**Registry 就是一個網站,把「有哪些人做了什麼 MCP server、這些 server 是做
什麼的、怎麼裝」整理成一份可以搜尋的名單**,概念上很像電話簿,或 App Store 的目錄。一份社群
分析直接點出這件事存在的動機:「Fragmented approaches led to duplicated effort, inconsistent
metadata views, and discovery friction, which motivated the creation of a centralized MCP
registry to serve as a single source of truth」(見
[safedep.io](https://safedep.io/the-state-of-mcp-registries/))。

## 三個 registry,分別是誰在營運

- **官方 MCP Registry**(`registry.modelcontextprotocol.io`)——連「官方」這個詞背後也是跨
  公司協作:2025 年 2 月由 MCP 原創者發起,找 **PulseMCP** 跟 **Block(Goose 團隊)**幫忙建,
  後續 **GitHub**、**Anthropic** 的人也加入當維護者(見
  [`blog.modelcontextprotocol.io` 公告](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/))。
- **Glama**(`glama.ai`)——**一間獨立公司/產品**,創辦人 Frank Fiegel 一個人做的,2024 年
  11 月 25 日上線,就在 Anthropic 剛發布 MCP 沒幾天。自稱是官方 registry 的「superset」——
  自己主動去多方掃描、收錄範圍故意比官方寬。
- **MCP.so**——**社群維護的目錄專案**,由 ChatMCP 團隊做的開源專案(`github.com/chatmcp/mcpso`),
  比較像一份「精選清單」,不是公司產品,也不是官方的一部分。

## 為什麼數字打架——不是算錯,是「圖書館的收書規則不一樣」

三邊實際規模數字完全不一樣:

| 來源 | 數字 | 查證時間 |
|---|---|---|
| 官方 MCP Registry API | 9,652 個最新版 server 記錄、28,959 個 server/版本記錄 | 2026-05-24 |
| Glama registry | 19,831+(同一天直接查 glama.ai 首頁,數字已經是 **50,777**) | 2026-03 / 2026-07-02 |
| MCP.so | 16,000+ | 未標明具體日期 |

用圖書館比喻更準確:**不是同一批書、三個館員數出不同答案,是三座圖書館的「收書規則」本來就
不一樣,書架上放的書不完全相同**。官方那座只收「有人正式送書來登記」的書(靠上面那四方
maintainer 一起審核);Glama 那座主動派人到處掃、收書範圍故意比官方寬;MCP.so 那座是社群自己
挑的精選書單,不是來者不拒。三座圖書館的書架本來就不會放一樣的書,所以**「世界上到底有多少個
MCP server」沒有一個唯一正確答案,取決於你問的是哪座圖書館、那座圖書館的收書規則是什麼**。

這也順便給了「容易過期」這件事一個更具體的例子:上面表格裡 Glama 的「19,831+」是查證當時
(2026-03)另一份分析引用的數字,但**同一天**直接去 glama.ai 首頁查,寫的已經是「50,777」——
不是幾個月後才舊,是**幾天內就已經舊了**。

這正是「M×N 問題有沒有真的解決」這個問題的一半答案:找 server 這件事確實比以前容易(不用每個
AI 應用各自維護一份清單),但「哪個 registry 的數字才是真的」本身變成一個新的小 M×N。

## 換來的新問題:能收錄,不代表被審查過

這是最值得記住的一句:「Registry admission requires only proof of GitHub repository or domain
ownership and **does not require code review, security audit, or malware scanning**, yet users
may incorrectly assume registry presence implies vetting.」
(見 [safedep.io](https://safedep.io/the-state-of-mcp-registries/))

拆開看是兩層問題:

1. **假冒**——攻擊者可以把惡意 server 包裝成大公司的 icon/品牌上傳,registry 本身的收錄門檻
   只檢查「你證明擁有這個 GitHub repo/網域」,不檢查程式碼內容。這跟上次安全模型筆記裡的
   Lethal Trifecta 是同一條線——**registry 沒有把關,把關的責任又回到 client 端自己判斷**。
2. **同一個服務,多個互相競爭的非官方實作**——像 Slack 沒有官方 MCP server,PyPI 上就冒出
   好幾個非官方的 Python 套件,安裝指令看起來都像官方的,但provenance(誰寫的、誰維護)完全
   不透明。這正好是 M×N 問題「換了個形狀重新出現」的具體案例:以前是「每個 AI 應用各自兜工具」,
   現在是「同一個工具,冒出一堆互相競爭、可信度不明的實作」。

目前官方 registry 的應對方式是開源 + 社群共管(hybrid human + automated moderation)——使用者
可以在 GitHub issue 上舉報,maintainer 可以拉黑或移除,但這是**事後**機制,不是**事前**審查。

## 回到問題本身:解決了嗎?

分兩半看比較準確:

- **「找 server 難」這一半的 M×N 問題,確實比以前好——有 registry 就是有進展,即使數字打架。**
- **「這個 server 值不值得信任」這一半,沒有真的解決,只是把 M×N 換成了另一種形狀**(誰的
  registry、誰的 unofficial package、哪個才是真的)——這也是為什麼安全模型那篇特別花力氣講
  「Server 不歸你管、不能假設它是善意的」,不是多餘的謹慎。

## 出處

Sources:
- [Linux Foundation Announces the Formation of the Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
  ——AAIF 成立公告,platinum 會員名單,97M 下載/10,000 server 的官方數字。
- [Donating the Model Context Protocol and establishing the Agentic AI Foundation — Anthropic](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
  ——Anthropic 自己的捐贈公告。
- [MCP joins the Agentic AI Foundation — MCP 官方部落格](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)
  ——2025-12-09,官方視角的同一則新聞。
- [The State of MCP Registries — safedep.io](https://safedep.io/the-state-of-mcp-registries/)
  ——Registry 收錄門檻不含安全審查、假冒品牌風險、社群共管的應對機制。
- [MCP Registry Architecture: A Technical Overview — WorkOS](https://workos.com/blog/mcp-registry-architecture-technical-overview)
  ——分散式做法造成的重複/metadata 不一致/發現困難,官方 registry 的動機。
- [MCP Adoption Statistics 2026 — Digital Applied](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol)
  ——官方 registry API、Glama、MCP.so 三個來源的數字對照。
- [Introducing the MCP Registry — MCP 官方部落格](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
  ——官方 registry 的起源(PulseMCP、Block、GitHub、Anthropic 跨公司協作)。
- [`glama.ai/mcp`](https://glama.ai/mcp)、[`glama.ai/mcp/servers`](https://glama.ai/mcp/servers)
  ——Glama 自己的定位(創辦人 Frank Fiegel、2024-11-25 上線、自稱是官方 registry 的 superset)、
  即時查到的最新收錄數字(50,777,查證時間跟官方數字不同天,差距本身就是重點)。
- [`github.com/chatmcp/mcpso`](https://github.com/chatmcp/mcpso)
  ——MCP.so 的營運方(ChatMCP 團隊的開源社群目錄專案)。

**誠實聲明**:這篇的數字全部是這次對話用 WebSearch 查的當下(2026-07-02)結果,不是查證過長期
穩定的規格文字——採用數字、生態規模這類東西會持續變動,過一段時間回來看這篇筆記,數字部分
應該假設已經過期,結構性的觀察(registry 不做安全審查、governance 換了主辦方)相對穩定。
