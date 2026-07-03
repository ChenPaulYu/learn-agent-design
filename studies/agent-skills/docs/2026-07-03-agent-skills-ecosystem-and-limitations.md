---
date: 2026-07-03
tags:
  - agent-skills
  - ecosystem
  - limitations
---

# Agent Skills 的變形、進階應用、跟實測出來的缺陷

這篇跟 `agent-skills-overview` 性質不一樣——那篇查證對象是 Anthropic 官方文檔,這篇查證對象是
**第三方 arXiv 論文**(都還是 2026 年才發表的 preprint,不保證經過同行審查)。信任等級不同,
不該混在一起講得一樣篤定,所以分開一篇,結尾有完整的誠實聲明。

## 變形:一個 Skill 資料夾,不是只有一種形狀

Skill 目錄的官方規格是 `SKILL.md`(必要)+ `scripts/`(可選,可執行程式)+ `references/`
(可選,文件)+ `assets/`(可選,模板/資源)。實務上這產生兩種明顯不同的變形:

- **純指示型**——只有 `SKILL.md` 的自然語言指示,每次都靠 Claude 重新推一遍該怎麼做。
- **可執行型**——`scripts/` 裡放固定流程的腳本,Claude 直接跑,不用每次重新推導。好處是**更
  省 token、更確定性(同一件事每次做法一樣)、更容易審查**(一段腳本比一段自然語言指示更容易
  稽核出它到底做了什麼)。

社群另外還分出「task-level skill」(整套任務或一群相關任務的高層程序)跟「event-driven
skill」(針對重複出現的特定執行訊號給局部建議),但這個分類還沒查到官方或論文明確定義,標成
社群慣例,不是規格用語。

## 進階應用:會自己進化的 Skill

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

## 現況:生態規模,跟品質參差不齊同時發生

一份針對安全漏洞的大規模實測研究,從兩個主要 marketplace **收集了 42,447 個 skill,系統性
分析了其中 31,132 個**——這是目前查到最具體的生態規模數字。10 個月內長到這個量級,速度上
跟 MCP registry 的成長算同一個級別。

但規模不等於品質。另一份專門做效能評測的研究(SkillsBench,87 個任務、8 個領域、附精心策劃
的 skill + 確定性驗證器)發現:**生態系裡實際存在的 skill,平均品質分數只有 12 分裡的 6.2 分
(標準差 2.8),而這份研究自己精心策劃的 benchmark skill,平均分數是 10.1 分**——換句話說,
你隨手在 marketplace 上抓到的 skill,品質離「寫得好的 skill」有明顯落差。

## 缺陷 1:精簡是關鍵,這次有實測數字撐著,不只是官方建議

overview 那篇引用過官方建議「精簡是關鍵」,這次 SkillsBench 直接量出具體數字:

- 用精心策劃的 skill,平均通過率從 33.9% 提升到 50.5%(+16.6 個百分點)
- 拆解開來看:**「詳細」的 skill(+18.8pp)跟「精簡」的 skill(+17.1pp)效果最好,「什麼都
  塞」的 comprehensive skill 反而讓表現變差(-2.9pp)**
- 模組數量上限 3 個以內的聚焦型 skill,表現贏過更大、更包山包海的 skill 包;搭配 skill 的
  小模型甚至能追上沒有 skill 的大模型

官方建議「精簡」是原則性的話,這份研究把它變成一個**可以量測、可以反駁的具體主張**——這正是
論文型證據跟官方文檔的差別:前者能被複製驗證,後者是廠商自己的建議。

## 缺陷 2:安全漏洞是真的普遍存在,不是理論風險

專門做安全稽核的研究(從兩個 marketplace 收集 42,447 個、分析 31,132 個)用自建的偵測框架
SkillScan(精準率 86.7%、召回率 82.5%)量出:

> "26.1% of skills contain at least one vulnerability, spanning 14 distinct patterns across
> four categories: prompt injection, data exfiltration, privilege escalation, and supply chain
> risks."
> — [Agent Skills in the Wild(arXiv 2601.10338)](https://arxiv.org/abs/2601.10338)

拆開看:**資料外洩(13.3%)、權限提升(11.8%)最常見,5.2% 的 skill 有高嚴重度、強烈疑似
惡意的模式**。還有一個直接呼應「變形」那節的發現——**帶可執行腳本的 skill,漏洞機率是純指示型
的 2.12 倍**——腳本雖然更省 token、更確定,但也是更大的攻擊面,兩者是同一枚硬幣的兩面,不是
「腳本比較安全」或「腳本比較危險」這種單向結論。

## 出處

全部經 WebSearch 於 2026-07-03 查證,查證對象是 arXiv preprint(**未必經過同行審查,是
2026 年才發表的最新研究**),不是官方文檔:

- [CODESKILL: Learning Self-Evolving Skills for Coding Agents(arXiv 2605.25430)](https://arxiv.org/abs/2605.25430)
  ——self-evolving skill 的機制、EnvBench/SWE-Bench Verified/Terminal-Bench 2 的實測數字。
- [Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale(arXiv 2601.10338)](https://arxiv.org/abs/2601.10338)
  ——42,447 個收集、31,132 個分析、26.1% 漏洞率、四類漏洞分布、腳本型漏洞機率 2.12 倍。
- [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks(arXiv 2602.12670)](https://arxiv.org/abs/2602.12670)
  ——品質分數(6.2/12 生態平均 vs 10.1/12 benchmark 平均)、精簡 vs 全塞的效能差距
  (+18.8pp/+17.1pp vs -2.9pp)、curated skill 提升通過率(33.9%→50.5%)。
- 其他提及但未深入查證的 self-evolving 相關論文(SkillForge、EvoSkill)——只查了摘要層級,
  沒有像上面三篇一樣核對具體數字,標記為「同方向的佐證」,不是主要引用來源。

**誠實聲明**:這篇引用的三篇論文全部是 2026 年發表的 arXiv preprint,**沒有查證是否經過同行
審查**——這代表「有嚴謹方法論在研究這個題目」是可信的,但論文本身的結論不等於學界共識,數字
本身也可能在正式發表前的審稿過程中被修正。這篇跟 `agent-skills-overview.md` 不一樣的地方就在
這裡:那篇引用的是廠商官方文檔(相對穩定),這篇引用的是快速變動、還在被驗證中的學術研究。
