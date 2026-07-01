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
| **Pattern** | 認知原語(Cognitive Primitive)+ 局部文法(哪個 primitive 可以接哪個) | Agent 怎麼思考? | Primitive 列表 + 接續關係 | ReAct 的 Thought/Action/Observation |
| **Computation Model** | 一個「計算預算怎麼分配去探索候選延續」的政策——見
[computation-model-first-principles](2026-07-01-computation-model-first-principles.md) | Agent 如何展開思考? | 分岔幾條/什麼結構/怎麼比較/何時收斂 | Linear、Self-Consistency、Beam Search、ToT、MCTS/LATS、Graph of Thoughts |
| **Runtime** | 執行迴圈 + 維護 Agent State | Agent 如何活著? | Loop/scheduler + state schema + context builder + tool dispatch + caching | Reflexion 的 Reflection Memory、Voyager 的 Skill Library |
| **Tool** | 與世界溝通的抽象介面(工具集合 + 權限邊界) | Agent 如何接觸世界? | 介面規格 + 工具抽象 + 權限邊界 | Coding Tool 層的 read_file()/run_bash() |
| **Environment** | Agent 真正作用的世界 | Agent 在哪裡? | 資源清單 + 觀測/行動限制 + 世界動態 | Coding Agent 的 Git Repository + Filesystem |

明確排除:**Prompt 不是一層**——它是 primitive 的 instantiation(具體內容),不是 primitive 本身。
**Multi-Agent 不是 Computation Model 的一個取值**——它是好幾個各自完整的 agent 堆疊怎麼組合,單位
跟「一個決策者怎麼探索候選延續」不同,見
[computation-model-first-principles](2026-07-01-computation-model-first-principles.md) 的
Divergence 第 1 點。

## 命名:這一層原本叫 Harness,改叫 Tool

原本用「Harness」這個字,但 OpenAI 2026 年的「harness engineering」把這個詞的意思泛用成「模型以外
的整套軟體(memory/execution/tools/guardrails/observability)」,範圍比我們這裡窄很多的定義
(只管工具集合+權限邊界)寬得多——同一個詞、範圍對不上,容易誤導讀者。討論過 World Interface、
Affordance、Action Space 等候補,最後選 **Tool**:業界(Anthropic/OpenAI API)本來就用這個字
指同一件事,最直覺、不用另外造詞;單數是配合其他四層(Pattern/Computation Model/Runtime/
Environment)都是類別詞的命名習慣。

## 待決定:五句「回答的問題」太像,容易混淆

上面那五句(怎麼思考/如何展開思考/如何活著/如何接觸世界/在哪裡)對仗工整但語感重疊(尤其「思考」
vs「展開思考」),讀者容易靠語感腦補,而不是靠這句話真的分辨出五層的界線。討論中提過的替代版本
(未拍板,列在這裡當候補):

| 層 | 候補問法 |
|---|---|
| Pattern | 有哪些思考的「動作單位」,誰能接誰? |
| Computation Model | 這些動作展開成什麼形狀? |
| Runtime | 狀態怎麼被存住、跨步驟續住? |
| Tool | 對外能做哪些具體動作? |
| Environment | 外面的世界本身長怎樣、有什麼限制? |

## 出處

框架是 Paul 的原創分層(見 `enact` repo 的
`research/raws/2026-06-12-layer-taxonomy-and-gap-framing.md`),當初是為了 Paper 1(Actor-Based
Agent Runtime)的 Gap section 推導出來的——那份文件裡把 Enact 逐層對照(哪層創新、哪層故意不動)
是論文專屬的分析,留在 enact repo;這裡只留通用框架本體。
