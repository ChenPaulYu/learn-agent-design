---
date: 2026-07-02
tags:
  - agent-skills
  - overview
---

# Agent Skills:把「怎麼做一件事」包成一個資料夾,需要時才載入

官方一句話定義:「Agent Skills are modular capabilities that extend Claude's functionality by
packaging instructions, metadata, and resources that Claude uses automatically when relevant to
tasks.」——重點是**自動**:不是你每次都要重新解釋一遍怎麼做,是包成一個資料夾,Claude 自己判斷
什麼時候該去讀它。

## 三層載入,一層比一層晚讀

一個 Skill 的內容分三層,分三個時間點載入,這是整篇筆記最核心的機制:

1. **Metadata(永遠載入)**——`SKILL.md` 的 YAML frontmatter(`name` + `description`),開機時就
   載進 system prompt。這一層極輕量,所以可以裝很多 Skills 而不吃 context。
2. **Instructions(觸發時載入)**——`SKILL.md` 的主體內容,只有當 Claude 判斷這個 Skill 跟目前
   任務相關時,才透過 bash 從檔案系統讀進來。
3. **更深的參考資料(需要時才載入)**——如果 instructions 裡提到其他檔案或腳本,Claude 才進一步
   去讀或執行它們。

官方原句形容這個過程像「an onboarding guide」——資料夾裡有指示、可執行腳本、參考資料,結構上
就是一份新人手冊,不是一次性塞給你,是你翻到哪一頁才讀那一頁。

## `SKILL.md` 長什麼樣

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

`description` 這個欄位特別關鍵——**它是 Claude 唯一用來判斷「這個 Skill 現在該不該用」的依據**,
因為 metadata 階段只有這行文字被載入,instructions 主體還沒讀進來。寫得太抽象、太簡短,Claude
根本不知道什麼時候該觸發它。

官方對怎麼寫好這個欄位有具體準則:**一律用第三人稱**寫,保持一致的視角;**要包含具體的關鍵字
跟觸發情境**,不是只講「這個 skill 做什麼」,還要講「什麼時候該用」——上面的範例就是這樣寫的:
「Extract text and tables from PDF files... **Use when** working with PDF files or when the
user mentions PDFs, forms, or document extraction.」只講前半句(做什麼)沒有後半句(什麼時候
用),觸發準確度會明顯變差。

企業版文件甚至有維運層級的準則,把「觸發準不準」當一件要持續追蹤的事:**觸發準確度下降**→
回頭修 description 或 instructions;**兩個 skill 的觸發範圍重疊、互搶(coexistence
conflict)**→合併或收窄各自的 description;**持續輸出品質低落**→改寫 instructions 或加驗證
步驟;**改版後仍持續失敗**→考慮直接淘汰這個 skill。

## 官方寫作準則:「精簡是關鍵」

> "Conciseness is essential because Skills share the context window with system prompts,
> conversation history, and other metadata... Authors should assume Claude possesses general
> knowledge and only include information that is strictly necessary for the task."
> — [`best-practices`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

具體做法:`SKILL.md` 本身當目錄用,細節拆到附屬檔案(`FORMS.md`、`reference.md`、
`examples.md`)——這幾個檔案只有 instructions 主體真的提到、Claude 真的需要時才會去讀,不會
因為存在就自動被載入。這正是三層模型的第三層在實務上怎麼運作。

## Progressive Disclosure 本身不是 AI 圈發明的——借了 30 年前的 UX 原則

整篇筆記最核心的機制(三層載入)有自己的血緣,不是 Anthropic 憑空想出來的。**Jakob Nielsen**
(Nielsen Norman Group 共同創辦人)**1995 年**就提出「progressive disclosure」這個互動設計
原則,2006 年補上具體可用性準則,講法是「defers advanced or rarely used features to a
secondary screen, making applications easier to learn and less error-prone」。原本是拿來解決
「人類使用者的認知負擔」——介面上不要一次塞滿所有選項,先給常用的,進階功能延後顯示。

Anthropic 做的事,是把「認知負擔」換成「LLM 的 context 預算」,原則完全沒變,對象換了——跟
MCP 借 LSP 的 client-server 概念是同一種「借用既有設計原則」的故事,只是這次借用的來源不是
另一個技術協定,是一條 30 年前的 UX 智慧。

## 沒有 Skills 之前——不是空白,是一個查得到數字的天花板

「為什麼被發明」的真正答案,不是取代了某個特定的舊工具,是**system prompt 本身有一個具體的
天花板**:在 Skills 之前,可重用的操作指示只能全部塞進一個巨大的 system prompt——查到的具體
說法是塞得下大概 **10 種能力左右**,prompt 就會長到不能再長,改一個功能要重寫整份 prompt,
不同 agent 之間也無法共用。Skills 靠「需要才載入」把這個天花板推高到「幾百個」。

官方部落格講的推出動機,讀起來也更貼近「新能力被新模型解鎖」,不是「填補一個急迫的缺口」:

> "As model capabilities improve, we can now build general-purpose agents that interact with
> full-fledged computing environments. As these agents become more powerful, we need more
> composable, scalable, and portable ways to equip them with domain-specific expertise."
> — [Anthropic Engineering, "Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## 2025 年 10 月推出,兩個月後開放成跨平台標準

Skills 是 2025 年 10 月 16 日正式推出的新功能,一開始只是 Claude 自己的能力。2025 年 12 月
18 日,Anthropic 把它開放成跨平台/跨產品可重用的**開放標準**——同一個月,Block 的 `goose`、
OpenAI 的 `AGENTS.md` 也各自捐進新成立的 Agentic AI Foundation(見 `mcp-ecosystem-reality`
那篇筆記),時間點高度重疊,但這是另一條獨立的公開/標準化動作,不是同一次公告。**這條「先當
自家功能推出,幾個月後開放成跨廠商標準」的軌跡,跟 MCP 當初的路徑很像**,只是 MCP 走了一年多
才到那一步,Skills 兩個月就走到了。

## 怎麼用——三個不同的入口面

Skills 可以在三個地方被用,呼叫方式不一樣:

- **`claude.ai`**——內建 Skills 自動在背景跑(用在文件產生這類場景);custom Skills 要透過
  Settings → Features 上傳 zip 檔,Pro/Max/Team/Enterprise 方案才有,且是「使用者個人的」,
  管理員不能集中管理。
- **Claude API**——需要三個 beta header:`code-execution-2025-08-25`、`skills-2025-10-02`、
  `files-api-2025-04-14`。可以用 `skill_id` 引用官方內建的 Skill,也可以自己上傳 custom
  skill——custom skill 是**整個 workspace 共用**,跟 claude.ai 的「個人專屬」不一樣。
- **Claude Code**——可以直接在專案裡建立 Skill(檔案系統裡放一個資料夾),不用透過 API 上傳。

## 安全:跟裝一個新軟體是同一個等級的謹慎

> "Exercise caution when using Skills, especially from untrusted sources, as they can grant
> Claude new capabilities, including tool invocation and code execution. Malicious Skills could
> potentially lead to data exfiltration, unauthorized access, or misuse of tools... treat Skill
> integration with the same care as installing new software."
> — [`overview` § Security considerations](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

官方甚至有一份專門給企業用的稽核指南(`enterprise` 頁),列出風險分級的具體判準:

- **高風險指標**——腳本有環境變數存取權限、指示裡包含「繞過安全規則」的內容、參照外部 MCP
  server、有網路存取行為、寫死的憑證(hardcoded credentials)。
- **中風險指標**——單純的檔案系統存取、特定工具呼叫。

這個風險形狀跟 MCP 安全模型那篇講的東西高度重疊——**未經審查的內容(這裡是 Skill 的
instructions/腳本) + 能力(程式碼執行) + 對外接觸面(網路/檔案系統)**,本質上是同一組
Lethal-Trifecta-style 的風險組合,只是包裝方式不同(一個是資料夾,一個是網路協定)。

## 跟 Tool Search Tool 的邊界——同一個原理,不同粒度的內容,而且順序跟直覺相反

Skills 延遲載入的是**整套操作程序**(procedural knowledge);Tool Search Tool 延遲載入的是
**工具定義**(tool schema)。兩者共享的是同一個 progressive disclosure 原理,套用在兩種不同的
內容類型上——這不是巧合,是 Anthropic 自己在多個場合用類似語言描述兩者。

**容易誤會 Tool Search Tool 是 Skills 的前身,但查證後順序是反的**:Skills 是 2025 年 10 月
16 日推出;Tool Search Tool 從官方原始資料裡的版本識別碼(`tool_search_tool_regex_20251119`)
跟 beta header(`advanced-tool-use-2025-11-20`)確認是 **2025 年 11 月 19-20 日**才上線,比
Skills 晚了超過一個月。Tool Search Tool 不是 Skills 的前身——如果真要說方向,頂多是「Skills
先把這個原理套在操作程序上,一個半月後同一個團隊把同一個原理套到工具定義上」,但這個「A 啟發
了 B」的因果關係本身也還沒有查到官方明確承認,更保守的講法是:**同一個 context 預算問題,被
分兩次、套在兩種不同內容上解決,不是一個線性演變的故事。**

## 跟 Tool Use Examples 的邊界——同樣是「給範例」,但顆粒度差一個量級

`SKILL.md` 裡固定有一個「## Examples」段落,細節還能再拆到獨立的 `examples.md` 附屬檔案——
這解決的問題,跟 tool-use 主題裡 `advanced-tool-use.md` 的 **Tool Use Examples**
(`input_examples`)其實是同一種精神:**光看抽象規格,不知道實際上怎麼用,靠具體範例補上這個
缺口**。Tool Use Examples 補的是「schema 只講型別,沒講怎麼填」;Skills 的 Examples 補的是
「instructions 只講步驟,沒講做起來長什麼樣」——都是「抽象規格 + 具體案例」這個組合。

但**顆粒度差一個量級,載入方式也不一樣**:Tool Use Examples 範圍只到「一次函式呼叫的參數」,
而且是**工具定義的一部分**,只要這個工具出現在 `tools` 陣列裡,範例就跟著送進去,每次都在;
Skills 的 `examples.md` 範圍是「一整個任務/流程怎麼跑」,而且**不是自動跟著送**,是三層
progressive disclosure 裡的最後一層——判斷這個 Skill 相關、讀了 instructions 之後,才會視
需要再去讀。這條邊界線跟上面「跟 Tool Search Tool 的邊界」比的是不同的軸:那條比的是
「延遲載入」這個機制本身,這條比的是「給範例」這個手法本身,兩條線都存在,不要混在一起。

## 跟 Subagent/Hook 的邊界——不同源,是刻意設計成互斥的三個答案

容易誤會成「Skills、Subagent、Hook 都是 Claude Code 的擴充機制,應該是同一套底層東西」——查證
後發現**不是**。三者是**分開、依序**上線的:

| 功能 | 上線時間 |
|---|---|
| Subagents | 2025 年 7 月 |
| Hooks | 2025 年 9 月 |
| Skills | 2025 年 10 月 |

Anthropic 自己的部落格〈Steering Claude Code〉把這些歸為「七種指揮 Claude Code 的方法」之一,
選哪個看的是三條互相獨立的判斷軸,不是三個變體:

- **要不要在主線程裡看得到、能介入每一步**——選 Skill(延遲載入,但觸發後在你看得到的主對話
  裡跑)
- **會不會產生一堆不想留在主對話裡的中間雜訊**——選 Subagent(整個丟到全新、乾淨的 context
  裡跑,只有最後結果回來)
- **要不要不看 LLM 判斷、每次都固定執行**——選 Hook(在特定生命週期事件上觸發,可以是純 shell
  指令,完全不需要 LLM 決定要不要做)

三者可以互相組合(Skill 跟 Subagent 的 frontmatter 都能直接定義自己的 hooks,只在該元件執行期
間生效),但組合得起來不代表同源——它們是刻意設計成互補、佔據不同位置的三個答案。

**Plugin 不屬於這三個判斷軸,是更高一層的打包單位,容易被誤放進同一排。** 官方原句:
「Plugins are reusable packages that add skills, agents, hooks, MCP servers, and LSP
configurations to Claude Code」——一個 Plugin 可以同時裝 Skill、agent、hook、MCP server
設定,是**容器**,不是跟 Skill 並列的第四個候選。透過 `claude plugin marketplace add` 註冊
一個目錄(`marketplace.json`),再用 `claude plugin install` 把整包裝進來,自動寫進
`.claude/settings.json`。值得注意的是 npx 不是 plugin install 的替代方案,是不同層次——
官方範例裡,一個 Plugin 內部設定 MCP server 時,`command` 欄位本身就是寫 `npx
@company/mcp-server`。Plugin 負責打包/發布/自動註冊,npx 是 Plugin 內部拿來啟動某個元件的
手段之一,兩者疊在一起用,不是二選一。

## 跟 Workflow、跟 MCP 的關係——垂直,不是同一排(這節是推理整理,不是查到的官方比較)

**這節跟上面幾節不一樣,沒有官方明文比較當依據,是根據 Workflow/MCP 兩者已知的文件行為推理
整理出來的**,標成這樣是因為信任等級跟前面查證過的內容不同,不該混在一起講得一樣篤定。

把整個 Claude Code 想成一個劇組:

- **Workflow**(包括自行調節步調的 dynamic 模式)是**導演的分鏡腳本**——決定誰先上場、誰
  同時上場、要重複拍幾輪、拍到什麼程度才收(dynamic 模式甚至是「不先寫死要拍幾次,邊拍邊決定
  夠了沒」)。
- **Subagent** 是分鏡腳本裡**個別演員**——一個腳本節點可能就是丟給一個 subagent 去單獨處理
  一段戲,只回一句「這段拍完了,結果是這樣」。
- **Skill** 是演員**自己帶的劇本小抄**——不管是主線程還是被分鏡腳本叫出來的某個演員,需要
  「這件事該怎麼做」的程序知識時,翻自己的小抄。
- **Hook** 是**片場的固定規矩**——不管拍哪一段、誰在演,某個動作發生(比如喊卡)就一定觸發
  某件事,不看導演當下怎麼想。

這四個回答的是同一個問題的四個面——「劇組內部的工作怎麼組織」。

**MCP 是完全不同的另一個層次——是劇組跟外面廠商借道具的窗口**。不管是導演本人、還是被分鏡
腳本叫出來的某個演員,只要它需要外部的東西(道具、場地),都得透過 MCP 這條線去借,跟「劇組
內部怎麼分戲」沒關係。一個 Workflow 腳本裡的某個 `agent()` 呼叫,執行過程中完全可能去呼叫
一個 MCP server——這時候兩者疊在一起用,但疊在一起不代表同一層,跟 Skill 跟 Hook 可以互相
組合但不同源是同一個道理。

## 出處

全部經 [context7](https://context7.com)(官方文檔)+ WebSearch(歷史時間線、第三方部落格)於
2026-07-02 查證:

- [`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
  ——三層載入模型、`SKILL.md` 結構、API beta header、Security considerations 原句。
- [`platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  ——「精簡是關鍵」原句、progressive disclosure 的實務切法、Writing effective descriptions
  (第三人稱、關鍵字+觸發情境)。
- [`code.claude.com/docs/en/plugin-marketplaces`](https://code.claude.com/docs/en/plugin-marketplaces)、
  [`code.claude.com/docs/en/plugins-reference`](https://code.claude.com/docs/en/plugins-reference)、
  [`code.claude.com/docs/en/discover-plugins`](https://code.claude.com/docs/en/discover-plugins)
  ——Plugin 是打包單位(裝 skills/agents/hooks/MCP servers/LSP 設定)、`marketplace.json`
  格式、`claude plugin install` 指令、Plugin 內部設定 MCP server 時用 `npx` 啟動的範例。
- [Nielsen Norman Group, "Progressive Disclosure"](https://www.nngroup.com/articles/progressive-disclosure/)、
  [IxDF Glossary](https://ixdf.org/literature/book/the-glossary-of-human-computer-interaction/progressive-disclosure)
  ——Jakob Nielsen 1995 年提出、2006 年補上可用性準則,progressive disclosure 的原始 UX 出處。
- [`anthropic.com/engineering/advanced-tool-use`](https://www.anthropic.com/engineering/advanced-tool-use)
  ——Tool Search Tool 的官方原始碼範例,版本識別碼(`tool_search_tool_regex_20251119`)、beta
  header(`advanced-tool-use-2025-11-20`)直接標示上線日期,比 WebSearch 轉述更可靠的一手來源。
- [`platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
  ——企業版風險分級判準(高/中風險指標)。
- [Anthropic Engineering, "Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  ——官方推出動機原句。
- [Claude by Anthropic, "Steering Claude Code: skills, hooks, subagents and more"](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)
  ——七種指揮方法的官方分類、Skill/Subagent/Hook 的選用判準原句。
- 上線時間線(Subagents 2025-07、Hooks 2025-09、Plugins/Skills 2025-10、開放成開放標準
  2025-12-18)——經 WebSearch 多篇第三方報導交叉確認(The New Stack、VentureBeat、
  SiliconANGLE 等),非官方逐字公告,時間點本身容易隨時間被更完整的官方回顧文章取代,查證時間
  2026-07-02。

**誠實聲明**:上線時間線那幾個日期是第三方報導交叉比對出來的,不是直接來自 Anthropic 官方的
單一權威公告頁——如果之後查到官方自己的完整功能時間軸,應該用那份取代這裡的日期。「跟
Workflow、跟 MCP 的關係」那節整段是根據已知行為推理整理的,沒有查到官方逐字比較這幾個東西的
文件,信任等級比其他節低,拿去引用時要標明是推論,不是官方立場。
