---
date: 2026-07-02
tags:
  - mcp
  - governance
---

# MCP 怎麼演化:SEP 跟治理結構

前面幾篇筆記引用了一堆 SEP(SEP-1319、SEP-2243、SEP-2575、SEP-2663……),但都只是引用「內容」,
沒看過「SEP 這個機制本身」怎麼運作。這篇補上——順便解釋為什麼有些機制(像 Tasks)明明查得到
文件,卻要特別標注「未定案」。

## SEP 是什麼:提案機制,抄的是 Python PEP / Rust RFC

> "Specification Enhancement Proposals (SEPs) serve as the primary mechanism for community
> members to propose changes to the Model Context Protocol. Inspired by established frameworks
> like Python PEPs and Rust RFCs, the process is designed to be straightforward and transparent."
> — [`2025-07-31-governance-for-mcp.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-07-31-governance-for-mcp.md)

任何人都能提案,但要有人「掛保證」才會真的往前走——流程是:先把提案寫成一份 markdown 檔案,
開一個 PR 到規格倉庫,找一個 sponsor(Core Maintainer 或 Maintainer)。Sponsor 同意後,狀態
改成 `draft`,先在 PR 留言區走一輪非正式討論,再進入 Core Maintainer 的正式審查(見
[`docs/community/sep-guidelines.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/community/sep-guidelines.mdx))。

## SEP 的狀態機——這解釋了為什麼有些東西要標「未定案」

```
Draft → In-Review → Accepted → Final
```

加上四個終止狀態:`Rejected`(否決)、`Withdrawn`(作者自己撤回)、`Superseded`(被別的
SEP 取代)、`Dormant`(六個月內找不到 sponsor,Core Maintainer 可以關掉,之後還能復活)——
見 [SEP-1850](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/1850-pr-based-sep-workflow.md)。

**這就是上次安全模型筆記裡,把 Tasks 機制特別標成「⚠ 提案中,未定案」的判斷依據**——一份
SEP 只要還沒走到 `Final`,即使文件寫得再詳細、範例再具體(甚至像 Tasks 那樣兩個範例的欄位
還互相不一致),都代表規格細節隨時可能改變,拿來當「MCP 現在的樣子」引用要小心。查一份 MCP
機制的成熟度,第一件事就是先看它掛的是哪份 SEP、那份 SEP 現在是什麼狀態。

## 治理結構:誰能拍板

```
Contributors → Maintainers → Core Maintainers → Lead Maintainers
```

四層階級,對應到實際做的事(見 [SEP-932](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/932-model-context-protocol-governance.md)、
[`2025-07-31-governance-for-mcp.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-07-31-governance-for-mcp.md)):

- **Maintainers**——負責特定元件(SDK、文件……)。
- **Core Maintainers**——引導整個專案方向、規格怎麼演化。
- **Lead Maintainers**——最終拍板的人,確保專案長期健康。

這四層人合起來組成 **MCP steering group**,每兩週開會審查 SEP,會議紀錄跟結論全部公開。

## Anthropic 現在的角色:不是唯一的守門人

> "The project has implemented a governance structure that facilitates collaboration between
> community leaders and Anthropic maintainers... designed to avoid gatekeeping, instead focusing
> on surfacing problems, aligning on solutions, and refining ideas into formal protocol updates."
> — [`2025-11-25-first-mcp-anniversary.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-11-25-first-mcp-anniversary.md)

不是「Anthropic 說了算」,也不是完全放給社群自治——Anthropic 的人是 maintainer 結構裡的一部分,
跟社群領袖一起坐進同一套治理層級,決策管道是共用的,不是分開兩條線。

## Working Groups / Interest Groups——不是每件事都要 Core Maintainer 親自審

大量的日常提案,如果每一份都要驚動 Core Maintainer,會變成瓶頸。SEP-1302 引入 Working Group
(WG)/Interest Group(IG)機制,讓有領域經驗的人先在自己的小組裡把想法磨過一輪:

> WG Lead / IG Facilitator 是「協調、不是合併權」的角色——他們能 sponsor SEP、能在自己小組
> 範圍內 triage(甚至關掉不合小組路線圖的提案,但可以上訴到 Core Maintainer),但沒有規格
> 核准權,merge 決定還是要跟 Maintainer 一起做。要當上這個角色,得先是 Member,還要兩位
> Core Maintainer(或一位 Lead Maintainer)背書。
> — [SEP-2148](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2148-contributor-ladder.mdx)

## 治理系統自己也在持續調整——目前正在解決的瓶頸

> "Currently, all SEPs require a full Core Maintainer review, which creates a bottleneck and
> slows down Working Groups with existing expertise... a delegation model allowing trusted
> Working Groups to approve SEPs within their domain without waiting for a core review."
> — [`2026-03-09-roadmap-update.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-03-09-roadmap-update.md)

現況是「每一份 SEP 都要 Core Maintainer 全程審過」,這正在被檢討——目標是讓有領域經驗的
Working Group 能在自己範圍內直接核准 SEP,不用每次等 Core Maintainer 排隊審查,Core
Maintainer 保留的是「策略層」的監督,不是每一條細節都要親自過一遍。**這套治理機制本身也是
用同一套 SEP 流程演化出來的**(SEP-932 定義治理結構、SEP-1850 定義 SEP 怎麼跑、SEP-2148
定義貢獻者怎麼升級)——治理規則跟協定規則走的是同一條路。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-02 抓取查證:

- [`blog/2025-07-31-governance-for-mcp.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-07-31-governance-for-mcp.md)
  ——治理模型的官方公告:SEP 定位、四層 leadership 結構、steering group 雙週會議。
- [`docs/community/sep-guidelines.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/community/sep-guidelines.mdx)
  ——SEP 提案的具體步驟(草稿 → PR → 找 sponsor → 非正式審查 → 正式審查)、狀態清單。
- [SEP-1850 `pr-based-sep-workflow.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/1850-pr-based-sep-workflow.md)
  ——狀態機 `Draft → In-Review → Accepted → Final` + 四個終止狀態的正式定義。
- [SEP-932 `model-context-protocol-governance.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/932-model-context-protocol-governance.md)
  ——選擇階層式治理結構的理由(Contributors → Maintainers → Core Maintainers → Lead Maintainers)。
- [`blog/2025-11-25-first-mcp-anniversary.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2025-11-25-first-mcp-anniversary.md)
  ——Anthropic maintainer 跟社群領袖共用治理層級的定位句。
- [SEP-2148 `contributor-ladder.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/seps/2148-contributor-ladder.mdx)
  ——Working Group / Interest Group 的角色定義、晉升條件。
- [`blog/2026-03-09-roadmap-update.md`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-03-09-roadmap-update.md)
  ——目前治理系統自己正在檢討的瓶頸(全案 Core Maintainer 審查)跟打算怎麼解(delegation model)。
