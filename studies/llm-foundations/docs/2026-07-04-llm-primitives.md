---
date: 2026-07-04
tags:
  - llm-foundations
  - first-principles
  - overview
---

# 理解 LLM 需要哪些 primitive?——第一原理重建

> TL;DR — 一開始隨口提的「四根柱子(架構/訓練目標/AR-NAR 解碼順序/tokenizer)+ 一陽台
> (in-context learning)」,經第一原理重新檢驗後,形狀不一樣了:真正互相獨立的只有**三根**
> (架構的混合機制、tokenizer、梯度優化——後者原本被漏掉),訓練目標跟解碼順序**不是平行的
> 兩根柱子,是一根柱子決定另一根有沒有得選**。這篇留下重建後的版本,也留下修正過程本身。

## 三根真正獨立的地基

1. **Tokenizer(必要性本身,不是某一種切法)**——神經網路只吃數字,文字必須先被離散化成有限
   詞彙。切法(BPE vs 其他)是設計選擇,但「要切」這件事本身不是。詳見
   [`tokenizer-bpe.md`](2026-07-04-tokenizer-bpe.md)。
2. **梯度優化(這幾篇筆記完全沒提過,是第一原理檢驗才發現漏掉的地基)**——參數是靠
   backpropagation + gradient descent 系找出來的。這幾輪查過的所有案例(Transformer/Mamba、
   next-token/masked)訓練參數的**方法本身**完全沒變過,是四根柱子共同站著的地基,不是柱子
   之一。
3. **架構的混合機制**——序列裡每個位置的表示,靠某個函式吸收其他位置的資訊算出來:attention
   (Transformer)或壓縮狀態機制(Mamba/RWKV/RetNet),兩者驗證過真的可以互換、在有意義的
   規模下打平(Falcon Mamba 7B,見
   [`beyond-transformer-architectures.md`](2026-07-04-beyond-transformer-architectures.md))。

## 一對不對等的關係,不是兩根平行的柱子

打個比方:做舒芙蕾——蛋白打發、拌入蛋黃糊、進烤箱——順序不是廚師「決定」的,是材料的化學性質
逼出來的,拌早了會消泡,順序被鎖死,沒得選。做沙拉——小黃瓜、番茄、生菜——先切哪個都行,菜本身
不要求任何順序;但廚師還是可以**自己選擇**先切不容易氧化的、再切香草,這個順序是廚師額外加上去
的,不是沙拉這道菜逼的。

**Next-token prediction 就是舒芙蕾**——「猜下一個字」這個目標的定義本身就已經寫死「只能照
順序、一個接一個生成」,選了這個目標,等於順便選了 AR 順序,不是另外多做一次選擇。**Masked/
denoising 目標就是沙拉**——蓋住哪個位置是隨機的,目標本身沒有要求任何生成順序;但你還是可以
自己選擇在 block 之間強加一個「先做完這塊才准做下一塊」的順序(block-wise diffusion 做的正是
這件事),這個選擇是為了品質(避免內部不連貫)、效率(能重用計算),不是目標逼你這樣做。

**這解釋了為什麼**
[`autoregressive-vs-nonautoregressive-for-agents.md`](2026-07-04-autoregressive-vs-nonautoregressive-for-agents.md)
裡,objective 跟 decoding order 看起來像兩個平行選項,實際上不是:選了 next-token 目標,AR
順序被鎖死;選了 masked 目標,才第一次真正打開「要不要另外選一個順序」這個問題——block size
那個調校旋鈕,就是在「完全不管順序」跟「照嚴格順序」之間,自己挑一個切多細的中間點。

**這個比喻會在哪裡失效**:沙拉的食材彼此真的互不影響,但 masked diffusion 裡同時猜的那些位置
不是這樣——它們雖然平行猜,彼此之間還是需要互相搭配、連貫(這正是 `autoregressive-vs-
nonautoregressive-for-agents.md` 提到的 multimodality problem,「Danke Dank.」那個四不像
案例)。沙拉比喻能說明「順序是不是被逼的」,不能拿來說明「平行生成的東西彼此需不需要互相
搭配」,不要把「食材完全獨立」誤推到 masked 位置上。

## 架構這根柱子,原本偷偷塞了兩件事

原本說「diffusion 內部也用 Transformer 的區塊」時含糊帶過一個事實:diffusion 用的是
attention 這個**混合機制**(真的獨立於解碼順序),但**拿掉了 causal mask**——而 causal mask
存不存在,其實是被解碼順序**決定**的,不是架構軸自己能選的東西(AR 需要 causal mask 讓訓練
時的 teacher forcing 成立;NAR 用雙向 attention,因為沒有「未來不能看」這回事)。「混合機制
(attention vs 狀態機)」才是真正獨立的架構原子,「causal mask 有沒有」是解碼順序的下游結果,
不是架構軸自己的自由度。

## 一個陽台:In-context learning

掛在架構(混合機制讀 context 的能力)+ 訓練目標(逼模型內化夠廣的模式),不特別掛在「目標
底下選了哪個解碼順序」——這件事在 next-token/AR 家族(GPT-3、induction heads)跟 masked/NAR
家族(LLaDA、Dream)都驗證成立,見
[`in-context-learning-under-diffusion.md`](2026-07-04-in-context-learning-under-diffusion.md)。

## 一個確認沒有 divergence的地方:規模不是第五根柱子

「規模」(資料/參數量/算力)原本就沒被算進四柱框架,重新檢驗後這個排除是對的——規模是架構軸
+ 目標軸上的「多寡」旋鈕,不是新增一個「有/沒有」的質變維度(`next-token-prediction.md` 裡
emergent abilities mirage 那段其實已經隱含支持這個判斷)。

## 一個沒收斂的邊界問題,留著不假裝有答案

這幾篇筆記完全沒處理「怎麼從一個只會接龍的 base model,變成會聽指令的助理」(SFT/RLHF 這類
後訓練)。這究竟該算 `llm-foundations`(LLM 為什麼能這樣運作)的一部分,還是該算
`BACKLOG.md` 裡留白的「LLM → Agent 橋接」的一部分,目前沒有答案——這是一個真正該決定、而不是
默默假設的範圍問題,先留在這裡等之後處理。

## 出處與方法

這篇整體是**推導性質**,不是新查證的外部事實——具體事實(Falcon Mamba 7B、causal mask 的
teacher forcing 原理、multimodality problem 案例)都已經在前面幾篇裡查證過並附上出處,這篇
做的是用 `/frame:first-principles` 重新檢驗自己先前口頭提出的「四柱一陽台」框架,找出裡面
「看起來獨立、實際上不對等」的地方。舒芙蕾/沙拉比喻經 `/frame:analogize` 生成並檢驗過映射
關係跟失效邊界,是這篇筆記自己的創作,不是引用來源。
