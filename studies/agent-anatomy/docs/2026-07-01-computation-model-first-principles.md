---
date: 2026-07-01
tags:
  - agent-anatomy
  - first-principles
---

# Computation Model 到底是什麼?(first-principles 分析)

> TL;DR — 慣例把 Computation Model 講成「execution topology(線/樹/圖)」,但這只是**結果的
> 幾何描述**,不是這一層真正在決定的東西。重建後,它其實是**一個「計算預算怎麼分配去探索候選
> 延續」的政策**——topology 只是這個政策跑出來的痕跡。

## 慣例答案 + 藏著的假設

慣例:Computation Model = execution topology(線性/遞迴/樹/圖/多代理)+ 遍歷規則,回答「Agent
如何展開思考?」。

藏著的假設:
- *(analogy)* 借用圖論/資料結構的現成詞彙描述,因為畫圖方便、分類好教。
- *(convention)* 把「形狀」本身當作這一層的產出,而不是「決定形狀的那個政策」。
- *(analogy)* Linear/Tree/Graph/Multi-Agent 常被並列展示,看起來像同一維度上的四個平行選項。

## 公理(剝到不能再剝)

1. *(definitional)* Pattern 的文法在某個節點可能開放不只一種合法延續——這個選擇空間是 Pattern
   打開的,Computation Model 不是製造它的人,是面對它的人。
2. *(物理事實)* 把候選具體算出來要花真實運算(LLM 呼叫、token、時間)——資源有限。
3. *(可驗證)* Linear = 每節點只算 1 條;Tree(ToT)= 某些節點算 N 條、比較後剪枝;Graph = 允許
   重訪已算過的節點;Multi-Agent = 把「誰在探索」變成一個變數。四者共同回答:面對 Pattern 打開的
   選擇空間,實際花多少運算探索、什麼結構探、什麼時候收斂。
4. *(跟 orthogonal 分析一致)* 這一層的決定不改 Pattern 的合法文法,也不決定 Runtime 存什麼。

## 重建結論

Computation Model = **一個「計算預算怎麼分配去探索 Pattern 打開的候選延續空間」的政策**:在每個
分岔點決定要不要展開、展開幾條、用什麼依賴結構讓候選互相看不看得到彼此(序列互斥/平行獨立/樹狀
分裂/多代理各自維護但偶爾同步),以及什麼判準觸發收斂(選一個變成真正執行的下一步)。

## Divergence

1. **Multi-Agent 混了兩件事,值得拆開。** 慣例把 Linear/Tree/Graph/Multi-Agent 當平行選項,但
   Multi-Agent 其實回答的是不同的次問題——不是「分岔幾條」(branching),是「誰去維護這些候選」
   (agency)。這是被慣例的並列展示掩蓋的一條次維度。
2. **「execution topology」這個名字在誤導。** 它暗示產出是「形狀」(靜態、事後才看得到),但真正
   決定的是「政策」(動態、事前的決策規則)——形狀只是政策的痕跡。這解釋了這一層一開始為什麼讓人
   覺得模糊:用一個描述結果的詞,指稱一個決定過程的東西。
3. **對「這層不宣稱創新」這種立場更有利。** 若核心概念是「topology」,「不宣稱這層創新」讀起來
   像「沒發明新形狀」,偏弱、有迴避感。換成「探索政策」,同一句話會變成「不改變計算預算怎麼分配
   去探索候選延續的策略——分岔數、深度、收斂判準,一律用系統預設」——更精準,也排除了「是不是
   偷偷改了搜尋策略」的潛在誤解。

## 出處

從 `enact` repo 對「Paper 1: Actor-Based Agent Runtime」的 Computation Model 立場(topology-
invariant,不宣稱這層創新)回頭挖出來的——這裡只留通用結論,論文專屬的應用留在 enact 那邊。
