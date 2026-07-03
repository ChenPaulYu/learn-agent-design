---
date: 2026-07-03
tags:
  - agent-skills
  - advanced
  - research
---

# Agent Skills 的研究前沿:會進化的 Skill,跟一堆 Skill 該怎麼組織

跟 `agent-skills-ecosystem-and-limitations` 同一個查證等級——查證對象是**第三方 arXiv
preprint**(2026 年才發表,未必經過同行審查),不是官方文檔。但這篇問的是不同的問題:那篇
問「Skills 現在真實部署出來是什麼樣子」,這篇問**「研究前沿在往哪個方向走」**——兩條軸線,
不是同一件事:

- **時間軸**——同一個 skill 用久了,會不會自己變聰明(self-evolving)
- **結構軸**——一堆 skill 之間,該怎麼組織彼此的關係(modular / hierarchical)

## 時間軸:會自己進化的 Skill

最讓人意外的發現不是某個功能,是**已經有正式學術研究在追這個只上線 9 個月的功能**。其中一個
方向是「self-evolving skills」——agent 自己隨著使用不斷改寫、優化自己的 skill:

> CODESKILL 是一個從 coding agent 的執行軌跡裡,自動萃取多粒度程序性技能、隨新經驗持續演化、
> 並維護一份精簡技能庫的框架。用強化學習訓練,結合密集的規則式技能品質回饋跟稀疏的可驗證執行
> 回饋。
> — [CODESKILL(arXiv 2605.25430)](https://arxiv.org/abs/2605.25430)

具體數字:在 EnvBench、SWE-Bench Verified、Terminal-Bench 2 三個測試集上,CODESKILL 比
「完全不用 skill」的基準線平均通過率高 **9.69** 個百分點,比「最強的 prompt-based 或記憶型
基準線」高 **4.01** 個百分點,而且技能庫大小維持穩定(不會無限膨脹)。

同一個方向還有 SkillForge(雲端技術支援場景的領域專用 self-evolving skill)、EvoSkill(透過
分析執行失敗、自動提出新 skill 或修改既有 skill)——一個功能上線不到一年,已經有好幾個獨立
團隊在做「skill 自己學會變更好」這件事,是個訊號,不是單一個案。

## 結構軸:一堆 Skill 該怎麼組織——官方故意保持扁平,學術界已經在解決規模問題

先講官方立場:`container.skills` 是一個平的清單,可以同時掛好幾個 skill,但彼此獨立、沒有誰
依賴誰。官方最佳實踐甚至**明確建議不要做太深的巢狀參考結構**——「Avoid deeply nested
references」,超過一層,Claude 可能只讀到部分內容,反而資訊不完整。這是故意的簡化,不是漏做。

但學術界已經看到扁平設計在大規模下會出問題,提前在做解法:

**問題本身,查得很具體**——不是憑空擔心,是實際指出扁平語意檢索的一個結構性漏洞:

> "Semantic retrieval surfaces topically relevant skills but misses their prerequisite chain of
> upstream and downstream skills, creating a prerequisite gap that leaves the retrieved bundle
> execution-incomplete."
> — [Graph-of-Skills(arXiv 2604.05333)](https://arxiv.org/abs/2604.05333)

翻成白話:單純用語意搜尋(就是 Tool Search Tool 那種 regex/BM25 找法)去一大堆 skill 裡挑,
可能挑到「主題上相關」的那個 skill,但**漏掉它偷偷依賴的其他 skill**——結果你拿到手上的那包
東西,執行到一半才發現少了一塊,跑不完整。這是純粹靠語意相似度檢索,天生會漏掉的問題,跟
「有沒有仔細設計 description」沒關係,是**結構性**的問題。

Graph-of-Skills 的做法:離線先從 skill 套件建出一個「可執行的 skill 圖」,推論時用「混合
語意-字面 seeding + 反向感知的 Personalized PageRank + 依 context 預算裁切」,一次撈出一包
「有邊界、有考慮依賴關係」的 skill 組合。實測結果:在 SkillsBench(87 個 dockerized coding
任務)跟 ALFWorld(134 個家務情境遊戲)兩個 benchmark、三個模型家族上,**每個模型的表現都是
最高分,輸入 token 數比基準做法最多省到 56 倍**。

另一篇 AgentSkillOS 從另一個角度處理同一個規模問題——不是修檢索,是重新組織整個 skill 生態:

> AgentSkillOS 分兩階段:(1)**Manage Skills**——用節點層級的遞迴分類法,把 skill 組織成一棵
> capability tree,方便有效率地發現;(2)**Solve Tasks**——透過 DAG-based pipeline 檢索、
> 編排、執行多個 skill。
> — [AgentSkillOS(arXiv 2603.02176)](https://arxiv.org/abs/2603.02176)

實驗橫跨三個生態規模(200 個到 200,000 個 skill)測試,發現**樹狀檢索在 200,000 個規模下依然
逼近理論最佳的 skill 選擇**,而且**就算給的是完全一樣的一組 skill,DAG-based 編排的表現也
明顯贏過原生的扁平呼叫**——換句話說,同樣的積木,有沒有結構化組織起來,結果差很多,不是
「skill 本身寫得好不好」的問題。

《The Hitchhiker's Guide to Agentic AI》把這個方向講得最直接:「Skills can depend on other
skills, forming a DAG, where a high-level skill may invoke sub-skills with explicitly declared
dependencies resolved before execution」——一個高層 skill 呼叫子 skill,依賴關係要先解完才能
執行,是正式把「skill 之間的依賴」變成一個顯式宣告的機制,不是靠猜。

## 合起來看:規模一上去,原本簡單的設計會被迫長出更複雜的結構

官方現在的立場是「先保持扁平、簡單」,理由大概是大部分使用者手上的 skill 數量還沒到需要
階層的規模。但學術界已經用「200,000 個 skill」這種數字提前示範了扁平設計的極限——這跟
`agent-skills-ecosystem-and-limitations` 那篇提到 MCP registry「10 個月內長到 4 萬多個」是
同一種節奏:規模一旦上去,原本簡單的設計就會被迫長出更複雜的結構,不是設計者想把事情搞複雜,
是規模逼出來的。

## 出處

全部經 WebSearch 於 2026-07-03 查證,查證對象是 arXiv preprint(**未必經過同行審查,是
2026 年才發表的最新研究**),不是官方文檔:

- [CODESKILL: Learning Self-Evolving Skills for Coding Agents(arXiv 2605.25430)](https://arxiv.org/abs/2605.25430)
  ——self-evolving skill 的機制、EnvBench/SWE-Bench Verified/Terminal-Bench 2 的實測數字。
- [AgentSkillOS: Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale
  (arXiv 2603.02176)](https://arxiv.org/abs/2603.02176)
  ——capability tree + DAG-based pipeline 兩階段架構、200 到 200,000 個 skill 的規模測試、
  「同樣 skill、有無結構化編排表現差很多」的實測結論。
- [Graph-of-Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills
  (arXiv 2604.05333)](https://arxiv.org/abs/2604.05333)
  ——語意檢索漏掉依賴鏈的「prerequisite gap」問題、離線建圖 + 線上檢索的機制、SkillsBench/
  ALFWorld 上省最多 56 倍 token 的實測數字。
- [The Hitchhiker's Guide to Agentic AI: From Foundations to Systems](https://arxiv.org/pdf/2606.24937)
  ——「skill 依賴 skill,形成 DAG」的正式描述,子 skill 依賴要先解完才能執行。
- 其他提及但未深入查證的同方向論文(SkillForge、EvoSkill、SkillPyramid、「From Skills to
  Talent」)——只查了摘要層級,沒有像上面四篇一樣核對具體數字,標記為「同方向的佐證」,不是
  主要引用來源。

**誠實聲明**:這篇引用的四篇主要論文全部是 2026 年發表的 arXiv preprint,**沒有查證是否經過
同行審查**——這代表「有嚴謹方法論在研究這個題目」是可信的,但論文本身的結論不等於學界共識,
數字本身也可能在正式發表前的審稿過程中被修正。跟 `agent-skills-ecosystem-and-limitations`
一樣,這篇引用的是快速變動、還在被驗證中的學術研究,不是廠商官方文檔。
