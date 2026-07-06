---
date: 2026-07-04
tags:
  - llm-foundations
  - in-context-learning
---

# 為什麼塞幾個範例進 prompt,模型就「當場學會」了——而且完全沒改任何參數

> TL;DR — In-context learning(ICL)是指:在 prompt 裡塞幾個「範例輸入 → 範例輸出」,模型
> 接下來就會照著這個模式做新的輸入,**而且中間完全沒有任何梯度更新、沒有任何參數被改動**。這
> 件事乍看違反直覺(不改參數哪來的「學」?),目前業界**沒有單一定論**,存在三種各自有實證
> 支持、彼此不互斥的解釋:一個電路層級的機制發現(induction heads),兩個「這其實等價於某種
> 學習算法」的理論框架(隱式梯度下降、隱式貝氏推論)。這篇筆記的立場是誠實列出三者,不假裝
> 已經有共識答案。

## 先講清楚在講什麼現象

[Brown et al., 2020, *Language Models are Few-Shot Learners*](https://arxiv.org/abs/2005.14165)
(GPT-3 論文)把這個現象講得很白:給模型看幾個「示範」(demonstration),不做任何 fine-tuning、
不改任何權重,純粹靠 prompt 裡的文字,模型接下來的輸出就會照著示範的模式走——而且**模型越大,
這個「靠示範就上手」的能力進步得越快**(比起完全不給示範的 zero-shot,few-shot 隨規模拉大進步
更陡)。

這件事奇怪在哪:傳統機器學習的「學習」,定義就是「看到資料 → 調整參數 → 表現變好」。ICL 完全
沒有中間那一步——**推論當下權重是凍結的**。模型卻表現得「好像學會了」。這不是量變(記憶體
更大所以背得更多能查),是質變(它在利用範例的方式,看起來像真的在跑一套學習算法,只是這套
算法不改權重)。

## 打個比方:不是重新學樂器,是認出你要哪種風格

想像一個資歷很深的即興爵士樂手,几乎把所有常見的曲式、和聲進行、各種樂風的「套路」都內化在
身體裡了(這對應**訓練階段**,見 [`next-token-prediction.md`](2026-07-04-next-token-prediction.md)
裡「網路文字已經藏著各種任務示範」那個論證,只是這裡藏的是「各種音樂套路」)。你現場哼兩小節
給他聽,他不需要「重新學一種新樂器」或「重新練一種新技巧」——他只是從內化的龐大曲庫裡,**認出**
你哼的接近哪一種調性/風格/套路,然後順著那個套路接下去彈。範例做的事是「指認」,不是「教學」:
它沒有塞進一個樂手原本不會的新技能,它做的是從樂手已經會的海量技能裡,**挑出**這次該用哪一種。

這正是下面幾套理論想解釋的東西:「指認」這個動作,在模型內部具體是怎麼發生的?

## 解釋一:電路層級的機制發現——Induction Heads

[Olsson et al., 2022, *In-context Learning and Induction Heads*](https://arxiv.org/abs/2209.11895)
(Anthropic)是第一篇直接**打開模型內部**去找機制的研究,不是靠外部行為推測。他們找到一組具體
的注意力頭組合(稱為 induction head):由兩層注意力頭合作完成一個「複製-補全」的動作——前一層
的頭負責定位「上一次看到類似 pattern 時,後面接的是什麼」,後一層的頭把那個「後面接的東西」
複製過來、接在當下位置後面。簡化講:**模型內部長出了一個專門做「找相似片段、抄它後面接什麼」
的迴路。** 這個迴路在 GPT-2、GPT-Neo、以及用不同隨機種子從頭訓練的模型上都獨立長出來過,說明
這不是巧合,是訓練這個目標下**收斂出來的通用解法**。

## 解釋二:等價於一次隱式的梯度下降

[von Oswald et al., 2023, *Transformers Learn In-Context by Gradient Descent*](https://arxiv.org/abs/2212.07677)
(ICML 2023)從理論構造角度證明:一層 linear self-attention,對範例做的資料轉換,在數學上可以
**構造出跟對一個回歸問題跑一步梯度下降,完全等價**的權重組合。換句話說:模型不是真的在推論時
「動了參數」,但它的**前向運算過程**,在效果上等同於「用 prompt 裡的範例當訓練資料,臨時跑了
一次學習算法」——只是這個「學習算法」是被寫死在模型的前向計算路徑裡,不是外部真的在更新權重。
[Dai et al., 2022, *Why Can GPT Learn In-Context? Language Models Implicitly Perform Gradient
Descent as Meta-Optimizers*](https://arxiv.org/abs/2212.10559)是同一時期獨立提出的相近框架,
把 attention 直接類比成一種「meta-gradient」的更新規則。**這一派理論回答的問題是:「指認」這
個動作,在計算上等價於哪一種已知的學習算法?**

## 解釋三:隱式貝氏推論

[Xie et al., 2022, *An Explanation of In-context Learning as Implicit Bayesian Inference*](https://arxiv.org/abs/2111.02080)
(Stanford,ICLR 2022)走的是不同角度:如果訓練語料裡本來就存在大量「長距離主題一致」的文件
(同一篇文章前後文風格、主題、語氣是連貫的),模型要把「猜下一個字」做好,某種程度上必須先
在心裡「猜這篇文章現在是哪個主題/哪種情境」,再根據這個猜測去預測下一個字。範例塞進 prompt,
在這個框架下做的事是:**提供證據,讓模型收斂到「現在是哪個情境」這個內部猜測上**——跟貝氏
推論「看到證據,更新對隱藏變數的信念」是同一個數學形狀。**這一派理論回答的問題是:「指認」
這個動作,在統計上對應哪一種已知的推論框架?**

## 三者不互斥,而且沒有定論——誠實聲明

這三套解釋回答的不是同一個問題:Induction heads 講的是「內部長了什麼具體電路」(機制層級),
隱式梯度下降講的是「這個計算過程數學上等價於哪種學習算法」(功能層級),隱式貝氏推論講的是
「這個計算過程統計上對應哪種推論框架」(另一種功能層級的刻畫)。**三者可以同時成立**——一個
具體電路,做出來的效果剛好同時可以被兩種不同的數學語言描述。**目前沒有一篇論文一統這三者**,
業界對「ICL 為什麼有效」仍是活躍研究題目,不是已解決的問題。這篇筆記刻意不挑一個「最終答案」
講,是因為現有材料本身就沒有收斂到單一答案。

## 出處

- [Brown et al., 2020, *Language Models are Few-Shot Learners*](https://arxiv.org/abs/2005.14165)
  ——ICL 這個現象的原始命名與定義出處(GPT-3 論文)。VERIFIED(經 WebSearch 交叉確認標題、
  核心定義、規模與 few-shot 表現的關係)。
- [Olsson et al., 2022, *In-context Learning and Induction Heads*](https://arxiv.org/abs/2209.11895)
  ——induction head 機制發現。VERIFIED(經 WebSearch 交叉確認標題、機構 Anthropic、arXiv 編號、
  跨模型/跨種子普遍出現的主張)。
- [von Oswald et al., 2023, *Transformers Learn In-Context by Gradient Descent*](https://arxiv.org/abs/2212.07677)
  (ICML 2023)——隱式梯度下降的等價性證明。VERIFIED(經 WebSearch 交叉確認標題、作者、發表
  會議、核心構造性證明的主張)。
- [Dai et al., 2022, *Why Can GPT Learn In-Context? Language Models Implicitly Perform Gradient
  Descent as Meta-Optimizers*](https://arxiv.org/abs/2212.10559)——同期相近框架,補充引用,
  沒有另外展開細節查證。LIKELY(標題/arXiv 編號在搜尋結果中直接出現,但沒有針對這篇單獨做
  第二輪確認)。
- [Xie et al., 2022, *An Explanation of In-context Learning as Implicit Bayesian Inference*](https://arxiv.org/abs/2111.02080)
  (Stanford,ICLR 2022)——隱式貝氏推論框架。VERIFIED(經 WebSearch 交叉確認標題、機構、
  發表會議、核心論證)。

**誠實聲明**:「即興爵士樂手認曲風」的比喻是這篇筆記自己的推導,不是任何一篇論文的原句或官方
說法——三篇論文都沒有用這套比喻描述自己的結論,只是這篇筆記拿來把三套理論放進同一個直覺畫面裡
的橋接工具。
