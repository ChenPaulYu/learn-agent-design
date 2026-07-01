---
date: 2026-07-01
tags:
  - agent-anatomy
  - elicit
---

# 五層「回答的問題」:從人類經驗重建(elicit 收斂記錄)

> TL;DR — 工程術語(動作單位、primitive)跟臨時比喻(思考步驟、遇到岔路)都讀起來彆扭,原因是
> 「先有系統概念、再包裝成中文」,讀者要拆包裝才懂。改成直接問「如果 agent 是一個人,這句話問的
> 是人的哪個面向」,秒懂,因為這是人自己每天在做的事。過程中意外驗證了 Runtime state 的
> (A)/(B) 兩種分法,也重新確認了 Tool 這個層名不用換。

## 最終定案:五句「回答的問題」

| 層 | 問法 |
|---|---|
| Pattern | 腦中的念頭,哪些自然接著哪些? |
| Computation Model | 面對決定,是直覺反應,還是要多想幾種、比較後才選?(對應 Kahneman System 1/2) |
| Runtime | 身體怎麼讓你維持是你、又怎麼確實把決定做出來? |
| Tool | 能拿起哪些外部工具去擴充原本做不到的事,哪些被允許用、哪些不行? |
| Environment | 所在的這個世界長什麼樣,有什麼是控制不了的? |

不直接稱呼「你」(避免總表語氣太像人格測驗,跟旁邊工程語氣的 Deliverable 欄不搭),但保留人類
經驗的具體感。

## 過程中的三個發現

### 1. 身體 = Runtime(兩條路徑獨立收斂到同一個答案)

「Runtime」這個詞本身的意思就是「讓一個東西持續跑下去的機制」——人類經驗裡最符合的不是記憶
(那只是其中一部分),是身體:心跳、呼吸、代謝讓你「持續活著、持續是你」,不用刻意去想。用足球
的例子最明顯:「腳很重」「體力下降」「左腳不穩」都不是 Pattern 或 Computation Model,是
**Runtime state**。

身體同時解釋了 Runtime 兩個子功能(呼應 [runtime-first-principles](2026-07-01-runtime-first-principles.md)
的 (A)/(B) 猜測):
- **自動維持**(心跳、呼吸)→ 對應 state schema/context builder(記憶連續性)
- **確實執行**(決定伸手拿東西,神經肌肉系統確保動作真的做出來,沒抓到會自動調整重試)→ 對應
  loop/scheduler、tool dispatch(執行可靠性)

### 2. 身體的「感知/動作器官」屬於 Tool,不是 Runtime——同一個部位,兩個面向都碰得到

嘴巴、耳朵、手、腳這些**真正跨出去碰世界、或讓世界進來的器官**,屬於 Tool,不是 Runtime——
判準是「跨不跨越 Agent–Environment 邊界」:
- 腳現在累不累、平衡穩不穩(**狀態**,不跨邊界)→ Runtime
- 腳實際去踢球那個動作(**跨出去、碰到世界**)→ Tool

Tool 因此分兩種來源:**內建**(身體自帶的眼睛/耳朵/手腳)vs **外部撿起來的**(扳手、手機)——
兩者都算 Tool,只是來源不同。

**對應到實際 agentic 場景的判準**:不是「文字輸出 vs 呼叫工具」這種表面區分,而是**這個能力
需不需要一份外部 schema/定義才能用,還是模型天生(post-training 練進去的)就會**。不需要 schema
的(輸出文字、讀懂 context 裡的東西,或像 Anthropic computer use 這種端到端練進權重的操作)是
內建工具;需要 schema 才會用的(`read_file()`、`search()`、`click()`)是外部工具。這個判準比
「文字 vs 工具呼叫」更本質,也更能一般化到未來新出現的能力上。

### 3. Tool 這個層名重新檢查過一輪,確認不用換

有人質疑 Tool 太窄(嘴巴、耳朵都不算 Tool)、跟 Environment 混淆(扳手本身算 Environment 的
東西,不是 Tool)、感覺是 object 不是 relation——一度考慮換成 Interface。但深挖後發現:**這些
反對意見全部來自「硬把 Tool 套進人類身體比喻」時才冒出來的**,不是這一層在它真正服務的領域
(LLM agent)裡有問題。Anthropic/OpenAI 的 tool calling、MCP,業界從來沒把 Tool 跟「扳手」搞混過。

Interface 也不是更好的答案——它「太薄、太被動」的疑慮,只有在一個框架把「介面定義」跟「執行
機制」混在一起時才成立;我們的框架已經把兩者切開(Tool = 靜態合約,Runtime = 動態執行,見
[runtime-first-principles](2026-07-01-runtime-first-principles.md)的「跟 tool 的關係」段落),
所以 Interface 太薄這個問題對我們不成立。

**結論:Tool 維持不變。** 「介面規格」是 Tool 底下的一個子概念(不是要取代 Tool 整層的名字),
MCP 是這個子概念的具體產業標準案例,補進 Tool 的例子清單。

## 額外驗證:Tool 是不是真正獨立的第五層?

有人提出更根本的質疑:如果 Runtime 已經吸收了「身體」,那 Tool 會不會其實只是 Runtime 管理的
一種資源,不是並列的第五層?檢驗判準:**拿掉 Tool,Runtime 還能完整描述一個 agent 嗎?**

答案已經有現成的實驗:**Enact P1 論文本身明確排除 Tool/Harness 這一層**(純對話 agent,不碰
工具),但它的 Runtime(身分狀態、記憶、迴圈)完全站得住、邏輯自洽,不需要 Tool 存在才成立。
這證明 Tool 是真正獨立的第五層,不是 Runtime 的附屬資源——五層維持並列結構。

## 出處

跟 Paul 的一輪 `/think:first-principles` + `/shape:elicit` 收斂出來的,過程中一部分推導是 Paul
自己在別處平行想的,拿回來對照後跟這裡的結論一致(見「身體 = Runtime」)。
