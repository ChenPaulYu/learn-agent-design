---
date: 2026-07-01
tags:
  - agent-anatomy
---

# 五層框架:Pattern → Computation Model → Runtime → Tool → Environment

> TL;DR — 拆解任何 agent 系統的五個維度,各自回答一個問題、產出一個 deliverable。已驗過五層本身
> 互相獨立(見 [orthogonal-analysis](2026-07-01-orthogonal-analysis.md)),但其中一層
> (Computation Model)的定義本身還不夠精準(見
> [computation-model-first-principles](2026-07-01-computation-model-first-principles.md))。

## 五層

| 層 | 定義 | 回答的問題 | Deliverable | 例子 |
|---|---|---|---|---|
| **Pattern** | 認知原語(Cognitive Primitive)+ 局部文法(哪個 primitive 可以接哪個) | 腦中的念頭,哪些自然接著哪些? | Primitive 列表 + 接續關係 | ReAct 的 Thought/Action/Observation |
| **Computation Model** | 一個「計算預算怎麼分配去探索候選延續」的政策——見
[computation-model-first-principles](2026-07-01-computation-model-first-principles.md) | 面對決定,是直覺反應,還是要多想幾種、比較後才選? | 分岔幾條/什麼結構/怎麼比較/何時收斂 | Linear、Self-Consistency、Beam Search、ToT、MCTS/LATS、Graph of Thoughts |
| **Runtime** | 執行迴圈 + 維護 Agent State | 身體怎麼讓你維持是你、又怎麼確實把決定做出來? | Loop/scheduler + state schema + context builder + tool dispatch + caching | Reflexion 的 Reflection Memory、Voyager 的 Skill Library |
| **Tool** | 與世界溝通的抽象介面(工具集合 + 權限邊界) | 能拿起哪些外部工具去擴充原本做不到的事,哪些被允許用、哪些不行? | 介面規格 + 工具抽象 + 權限邊界 | Coding Tool 層的 read_file()/run_bash()、MCP |
| **Environment** | Agent 真正作用的世界 | 所在的這個世界長什麼樣,有什麼是控制不了的? | 資源清單 + 觀測/行動限制 + 世界動態 | Coding Agent 的 Git Repository + Filesystem |

## 對應人類的什麼

| 層 | 對應人類的什麼 |
|---|---|
| Pattern | 長期學會的能力(skills / cognitive repertoire) |
| Computation Model | 當下採用的思考策略 |
| Runtime | 當下整個人(身體狀態 + 工作記憶 + 注意力 + 目標) |
| Tool | 身體以外借用的東西(手機、筆、電腦、扳手) |
| Environment | 世界 |

身體被 Runtime 吸收(狀態 + 記憶 + 注意力 + 目標,全部是「當下這個人」的一部分),Tool 因此
重新變回單純的「外部工具」,不用再糾結身體器官算不算 Tool——這樣分反而更自然。詳細推導過程見
[human-analogy-elicit](2026-07-01-human-analogy-elicit.md)。

明確排除:**Prompt 不是一層**——它是 primitive 的 instantiation(具體內容),不是 primitive 本身。
**Multi-Agent 不是 Computation Model 的一個取值**——它是好幾個各自完整的 agent 堆疊怎麼組合,單位
跟「一個決策者怎麼探索候選延續」不同,見
[computation-model-first-principles](2026-07-01-computation-model-first-principles.md) 的
Divergence 第 1 點。

## 兩軸 + 五層:更高一層的分組

五層可以再分成兩個正交的軸——五層本身不變,只是多一層更粗的分組:

```
Decision 軸(決定「做什麼」)
├── Pattern
└── Computation Model

Execution 軸(決定「怎麼做」)
├── Runtime
├── Tool
└── Environment
```

兩軸之間靠 **Runtime 持續回頭問 Computation Model「下一步呢」形成一個迴圈**:Runtime 執行完一步、
更新 state,拿新 state 問 Computation Model 要不要繼續、怎麼繼續(`while not done: op =
policy.choose(state); result = execute(op); state = update(state, result)`)。

**這件事不會推翻五層**,因為要分清楚兩件不同的事:
- **設計時的可分離性**——五層各自能不能獨立換掉,已經用 orthogonal 分析驗過(見
  [orthogonal-analysis](2026-07-01-orthogonal-analysis.md))。
- **執行時的呼叫關係**——誰跑起來的時候呼叫誰、資料怎麼流動,是上面那個迴圈在講的事。

兩個模組執行時互相呼叫、形成迴圈,是完全正常的架構現象,不代表它們不是獨立模組(就像 scheduler
跟 policy 常常互相呼叫成迴圈,沒有人因此說它們是同一層)。Decision 軸 vs Execution 軸,是五層之上
再加的一層粗分組,兩種描述可以同時成立:先看兩軸抓大方向,再往下鑽進五層抓細節。

## 命名:這一層原本叫 Harness,改叫 Tool

原本用「Harness」這個字,但 OpenAI 2026 年的「harness engineering」把這個詞的意思泛用成「模型以外
的整套軟體(memory/execution/tools/guardrails/observability)」,範圍比我們這裡窄很多的定義
(只管工具集合+權限邊界)寬得多——同一個詞、範圍對不上,容易誤導讀者。討論過 World Interface、
Affordance、Action Space 等候補,最後選 **Tool**:業界(Anthropic/OpenAI API)本來就用這個字
指同一件事,最直覺、不用另外造詞;單數是配合其他四層(Pattern/Computation Model/Runtime/
Environment)都是類別詞的命名習慣。

## 已定案:五句「回答的問題」原本太像,已換掉

原本五句(怎麼思考/如何展開思考/如何活著/如何接觸世界/在哪裡)對仗工整但語感重疊(尤其「思考」
vs「展開思考」),讀者容易靠語感腦補,而不是靠這句話真的分辨出五層的界線。第一輪改成工程術語
(動作單位)、第二輪改成臨時比喻(思考步驟、遇到岔路),都還是覺得彆扭;第三輪改成直接從人類
經驗重建(如果 agent 是一個人,這句話問的是人的哪個面向),才真正定案——過程 + 三個額外發現
(身體=Runtime、Tool 層名重新確認不用換、Enact P1 證明 Tool 是真正獨立的第五層)見
[human-analogy-elicit](2026-07-01-human-analogy-elicit.md)。兩份 Notion 頁面(hub 完整版 +
獨立教學版)已同步套用。

## 出處

框架是 Paul 的原創分層(見 `enact` repo 的
`research/raws/2026-06-12-layer-taxonomy-and-gap-framing.md`),當初是為了 Paper 1(Actor-Based
Agent Runtime)的 Gap section 推導出來的——那份文件裡把 Enact 逐層對照(哪層創新、哪層故意不動)
是論文專屬的分析,留在 enact repo;這裡只留通用框架本體。
