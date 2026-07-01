---
date: 2026-07-01
tags:
  - agent-anatomy
  - orthogonal
---

# 五層是不是真的互相獨立?(orthogonal 分析)

> TL;DR — 五層本身乾淨、互相獨立,每一對都能找到「動一個、另一個沒動」的真實反例。但分析中發現
> 一個框架沒有格子裝的東西:一條連接 Pattern 和 Runtime 的**邊**(哪個 Runtime state 餵給哪個
> Pattern primitive)——這條邊,才是 Reflexion、Voyager 這類系統真正創新發生的位置。

## 逐對獨立性檢查

| 對照 | 動 A 不動 B 的反例 | 動 B 不動 A 的反例 | 結論 |
|---|---|---|---|
| Pattern vs Computation Model | 同一套 ReAct 文法,單一 trace(Linear)換成 ToT 的樹狀展開 | Reflexion 在文法裡加 Reflection primitive,整體仍是單一序列 | 通過,但措辭上「哪些可以接哪些」容易被讀成「序列/循環」而跟 topology 混在一起,要講清楚是「局部文法」vs「全域遍歷」 |
| Runtime(context builder)vs Environment(資源清單) | 同一套 load 政策接到兩個不同 repo/知識庫,結果因資源不同而不同 | 同一個環境,換一套 context builder 政策,行為大不同 | 通過,是「菜單」vs「今天點什麼」的關係 |
| Runtime(tool dispatch)vs Harness(介面設計) | 同一套 routing/retry 機制掛在不同 Harness 底下都能用 | 同一個 Harness,換一套 dispatch 策略(重試次數) | 通過,是「合約」vs「怎麼打這通電話」的介面/實作分離 |
| Harness vs Environment | 同一套 Harness 指向不同環境(本機/沙箱容器) | 同一個環境,換不同權限等級的 Harness | 通過,全框架最乾淨的一對 |
| Pattern vs Runtime(state schema) | 換一套 state 壓縮策略,primitive 完全不動 | (見下——這對藏了訊號) | 表面通過,但有隱藏耦合 |

## 真正的發現:Pattern-Runtime 之間藏著一條沒被畫出來的邊

三個範例系統裡(ReAct 樸素史/Reflexion/Voyager),**每次 Runtime 加新的 state 種類,Pattern
幾乎都同時多一個新 primitive 去讀寫它**(Reflexion 加 Reflection Memory 同時加 Reflection
primitive;Voyager 加 Skill Library 同時加 verify-and-store 步驟)。

這容易誤讀成「Pattern 創新」跟「Runtime 創新」其實是同一件事的兩張皮。但深挖後,這個「一起出現」
是**歷史上的設計慣例**(系統作者選擇在兩層都留痕跡),不是框架的必然——你可以只換 Runtime 的
state 壓縮策略、完全不碰 Pattern(見上表反例)。所以兩個軸仍然獨立;真正被漏掉的,是**「哪個
state 餵給哪個 primitive、在哪個時間點餵」這條邊**——它不是一個「層」(不回答「Agent 怎麼 X」),
是層與層之間的一條關係線,五層框架目前完全沒有位置放它。

**方向性**:這條邊是單向依賴——Pattern 的 primitive 要「吃」Runtime 的 state 才有料;但反過來,
Runtime 換一種 state 存法,不必然需要 Pattern 長出新 primitive。這個不對稱,是之後幫這條邊命名時
要抓住的核心特徵。

## Payload

五層框架結構上是乾淨的,可以放心當通用工具用。真正的空格不是某兩層要合併,是缺一條「edge」——
state 怎麼餵回 primitive 的路徑。這條邊解釋了為什麼 Pattern 和 Runtime 的創新在真實系統裡常常
綁在一起出現。
