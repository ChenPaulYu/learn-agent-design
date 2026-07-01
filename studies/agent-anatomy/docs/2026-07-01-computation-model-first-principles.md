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

1. **Multi-Agent 根本不屬於這一層,不是拆分問題,是單位不對。** 慣例把 Linear/Tree/Graph/
   Multi-Agent 當平行選項,但公理 1-4 講的都是「**一個**決策者面對 Pattern 打開的候選延續空間,
   怎麼分配運算去探索」——Multi-Agent 講的是「**好幾個各自完整**的 agent(各自有自己的
   Pattern+Computation Model+Runtime+Harness+Environment 整套堆疊)怎麼組合」,層級不同,不是
   同一個維度上的一個取值。**結論:把 Multi-Agent 從這一層的例子清單整個移除**,跟「Prompt 不是
   一層」性質一樣,是明確排除,不是子維度。
2. **「execution topology」這個名字在誤導。** 它暗示產出是「形狀」(靜態、事後才看得到),但真正
   決定的是「政策」(動態、事前的決策規則)——形狀只是政策的痕跡。這解釋了這一層一開始為什麼讓人
   覺得模糊:用一個描述結果的詞,指稱一個決定過程的東西。
3. **對「這層不宣稱創新」這種立場更有利。** 若核心概念是「topology」,「不宣稱這層創新」讀起來
   像「沒發明新形狀」,偏弱、有迴避感。換成「探索政策」,同一句話會變成「不改變計算預算怎麼分配
   去探索候選延續的策略——分岔數、深度、收斂判準,一律用系統預設」——更精準,也排除了「是不是
   偷偷改了搜尋策略」的潛在誤解。

## 具體怎麼實作:跟 Runtime、跟 prompt 的關係

- **跟 Runtime**:不是合作,是引擎跟演算法的關係。Runtime 的「loop/scheduler」是通用執行引擎
  (能跑迴圈、能保留呼叫間的狀態);Computation Model 是塞進這個引擎的具體演算法(分岔幾條、探
  多深、何時收斂)。同一個引擎可以換不同演算法——這就是為什麼兩層獨立(見 orthogonal 分析)。
- **跟 prompt(Pattern)**:Computation Model 自己不含任何文字內容,只決定「呼叫幾次、怎麼組織
  這些呼叫」;每次呼叫要送什麼內容進去,是 Pattern 的事。兩者運作時一定同時出現(沒有 prompt,
  Computation Model 無事可做),但彼此不知道對方的細節——政策不管內容寫什麼,內容也不管自己會
  被呼叫幾次。**具體來說 Computation Model 是 code(控制流程),不是 prompt。**
  - 陷阱:可以寫一個 prompt 叫模型「自己在心裡想三種做法、評估、選一個」,全部在同一次生成裡
    完成——這是 Pattern 的內容在裝成 Computation Model 的樣子,不是真的 Computation Model(沒
    有真的多分配運算資源去探索,只是文字上看起來像探索)。
  - 可以「更智慧」的分岔決策:插一個專門的 LLM 節點問「這裡值得分岔嗎?分幾條?」,但那個節點
    本身仍是 Pattern(一次 primitive 呼叫);Computation Model 永遠是「讀這個節點輸出、據此調
    整分岔參數」的那段 code——它是消費 Pattern 智慧的地方,不是產生智慧的地方。

## 具體案例校驗

- **ToT(Tree of Thoughts)屬於這一層,而且是最乾淨的範例**:同一個 Thought primitive 的多個
  候選內容實例(分岔幾條)、候選互相看得到可以比較(結構)、用評分決定探哪條剪哪條(依賴結構)、
  深度到了或找到夠好的就停(收斂判準)——四要素全部具體對應得上,而且全程只有一個決策者。
- **LangGraph 是這個框架的具體實作對照**:StateGraph 的 nodes/edges(含 conditional edges、
  `Command` 路由)= Computation Model;State 物件(跨 node 累積、持久化)= Runtime;node 函式
  內部呼叫 LLM 用的實際文字 = Pattern。LangGraph 把 Computation Model 跟 Runtime 包在同一個
  框架裡,但概念上仍是兩層。
- **Claude Code 的 hooks 是 Runtime,不是 Computation Model**:28 種 hook 事件全部是「攔截/
  擋掉/修改/塞 context」單一次工具呼叫,沒有分岔機制——對應 Runtime 的 tool dispatch,不是
  Computation Model。例外是 Stop hook 可以擋住 agent 停下來、強迫繼續,這剛好對應「收斂判準」
  這一個要素;但因為 Claude Code 的 Computation Model 本身寫死是 Linear(分岔數恆為 1),
  分岔/結構/深度三個要素都是常數不用管,只剩收斂判準這一個變數還活著,Stop hook 剛好落在這裡。
  想要真的分岔探索(像 ToT),hooks 給不了,要另外寫調度 code(例如平行呼叫多個 subagent、比較
  結果、選一個)。

## 常見的 Computation Model 一覽(除了 ToT)

| 名稱 | 分岔幾條 | 結構 | 怎麼比較 | 收斂判準 |
|---|---|---|---|---|
| Linear | 恆為 1 | 單一序列 | 不用比 | 到達終止條件 |
| Self-Consistency(取樣投票) | N 條**完全獨立**的完整解法 | 平行、互不知道彼此 | 全部跑完才比 | 多數決選最常見答案 |
| Beam Search | 每步固定留 K 條 | 樹狀但**限制寬度** | 每步用分數排序剪枝 | 固定深度或終止符 |
| ToT(Tree of Thoughts) | 某些節點分 N 條 | 樹狀,候選互相看得到 | 評分後剪枝 | 深度/分數判準 |
| MCTS / LATS | 動態(探索/利用權衡決定) | 樹,但用模擬(rollout)估分 | 模擬到底,回推更新節點分數 | 模擬預算用完或分數夠好 |
| Graph of Thoughts(GoT) | 跟 Tree 類似會分岔 | 允許把分岔結果**合併回同一節點**(DAG) | 合併時聚合候選精華 | 同 Tree |
| 迭代修正迴圈(Reflexion 式) | 恆為 1(不是真分岔) | 線性但允許回頭重跑 | 用自我批評結果決定要不要重跑 | 批評通過或到最大重試次數 |
| 遞迴分解(RLM 式) | 不是探索候選解,是**拆子問題** | 遞迴樹(節點是子問題) | 子問題各自解完後合併 | 遞迴到底層可直接解決 |

陷阱提醒:Debate(辯論)類技巧要看實作——同一個決策迴路生兩個候選角色互相比較,還算 Computation
Model;若是兩個各自獨立、各自完整的 agent 在對話,就跟 Multi-Agent 一樣單位不對,不屬於這一層。

## 出處

從 `enact` repo 對「Paper 1: Actor-Based Agent Runtime」的 Computation Model 立場(topology-
invariant,不宣稱這層創新)回頭挖出來的——這裡只留通用結論,論文專屬的應用留在 enact 那邊。
