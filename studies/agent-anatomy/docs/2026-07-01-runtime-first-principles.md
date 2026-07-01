---
date: 2026-07-01
tags:
  - agent-anatomy
  - first-principles
---

# Runtime 到底是什麼?(first-principles 分析)

> TL;DR — 慣例把 Runtime 講成「執行迴圈 + 維護 Agent State」,底下籠統塞了 loop/scheduler、
> state schema、context builder、tool dispatch、caching 五樣東西。重建後,Runtime 的核心是
> **在無狀態的 primitive 呼叫之間製造連續性的機制**——具體拆開後,這五樣東西可能其實是兩種不同的
> 連續性(記憶連續性 vs 執行可靠性連續性)被同一個籠統標籤蓋住,值得後續驗證。

## 公理

1. *(物理事實)* 單次 LLM 呼叫是無狀態的——那次呼叫只知道餵給它的輸入,呼叫結束後什麼都不會
   自動留下。
2. *(定義性需求)* 但 agent 要表現得像連續的一個東西,得跨很多次呼叫維持記憶、維持進度。
3. *(物理事實推論)* 所以一定要有外部機制,負責:(a) 留住什麼、(b) 決定下一次呼叫要餵回哪些
   留住的東西、(c) 確保每一步的機械執行(含呼叫外部工具)真的成功。

## 重建結論

Runtime = **在無狀態的 primitive 呼叫之間製造連續性的機制**——不只是籠統的「維護 State」,是
具體回答「什麼會被留住、下一次要餵回哪些、每一步怎麼確保機械上真的執行成功」。

## 懷疑:Runtime 現在的五樣東西,可能是兩種連續性被混在一起講(未驗證,留待後續)

- **記憶連續性**:state schema + context builder——記得什麼、餵回什麼。
- **執行可靠性連續性**:loop/scheduler + tool dispatch + caching——確保每一步機械上真的跑成功
  (重試、不重複算)。

直覺上這兩者可以獨立變動(換一套重試策略不需要換 state schema),如果成立,Runtime 這個標籤
可能跟 Computation Model 一樣,籠統地把兩件事捆在一起——值得之後正式跑一次 orthogonal 分析驗證。

## Runtime 跟 tool 的關係:誰定義 vs 誰執行

比喻:Tool 是菜單(有哪些工具、規格、權限邊界——靜態合約),Runtime 是服務生(真的去下單、
出包要不要重試、結果怎麼處理、要不要快取——動態機制)。

- **Tool 層定義 tool 是什麼**:工具存在、介面規格、權限邊界。
- **Runtime 執行對 tool 的呼叫**:路由到對的處理程式、失敗重試、結果後處理、caching。

Claude Code 的 PreToolUse/PostToolUse hooks 就是 Runtime 對 tool 做的事——攔截、擋掉、修改、
重試一次已經被 Tool 定義好的工具呼叫,不會定義新工具本身(細節見
[computation-model-first-principles](2026-07-01-computation-model-first-principles.md) 的
hooks 段落)。

工具呼叫回來的結果,常常會變成 Runtime state 的一部分(例如 read_file 讀到的內容存進 context),
下一步又被某個 Pattern primitive 吃進去——這是 conditioning edge 的其中一種具體餵法(見
[orthogonal-analysis](2026-07-01-orthogonal-analysis.md))。

## 具體來說,Runtime state 是什麼

任何活得比單次 primitive 呼叫還久的資料都算,但結構上永遠由三件事組成:

1. **Schema**——這筆資料長什麼形狀(逐字歷史?帶 embedding/時間戳/重要性分數的記憶條目?固定
   維度的身分向量?)
2. **Write-back 規則**——什麼時候、怎麼寫進去(每次 Action 後存 Observation?每次 Reflection
   後新增一條記憶?)
3. **Read/篩選規則(= context builder)**——下次呼叫時怎麼從存著的資料裡挑要餵回去的東西(取
   最後 N 筆?按相似度檢索 top-K?整包塞回去?)

**但更重要的是,這些狀態依「誰讀」分兩種**:

- **(A) 餵給 Pattern 的記憶型狀態**——目的是變成某個 primitive 的內容(conditioning edge)。
  例如記憶庫、對話歷史、身分向量。memory + retrieve 系統(Generative Agents、MemGPT)幾乎全部
  創新都集中在這一種:state schema(怎麼存記憶)+ context builder(怎麼檢索)。
- **(B) 只給 Runtime/Computation Model 自己用的機制型狀態**——完全不會被塞進任何 prompt,單純
  內部記帳。例如工具呼叫重試了幾次、結果有沒有被快取過、迴圈跑到第幾輪、預算還剩多少。這種狀態
  只影響「要不要再打一次、要不要停」的控制決策,模型自己看不到它。

**範例對照**:ReAct 的 Interaction History、Reflexion 的 Reflection Memory、Voyager 的 Skill
Library + Experience Store,都是 (A) 型;Enact 自己的設計(`enact` repo 的 Internal Given / 
per-act residue write-back / rolling Preparation window,見
`research/raws/2026-06-12-layer-taxonomy-and-gap-framing.md`)也是 (A) 型,只是存的不是事實
記憶,是身分狀態。

## 出處

從跟 Paul 的對話逐步深挖出來的:先重建定義,再用「Runtime -> tool」「memory+retrieve 算不算
Runtime」兩個具體案例校驗,最後收斂出 (A)/(B) 兩種 state 的分法。
