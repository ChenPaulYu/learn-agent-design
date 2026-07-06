---
date: 2026-07-04
tags:
  - llm-foundations
  - autoregressive
  - diffusion
  - agent
---

# 如果換成 diffusion,tool use 這些 agent 技巧還撐得住嗎?

> TL;DR — 分層看差很多。Skills 這種「靠 context 內容驅動」的技巧,幾乎不受影響。Tool use
> 這種「需要中途暫停、等外部結果、再繼續」的迴圈,目前實測下來確實會出系統性的問題——不是
> 空想的架構摩擦,是有論文量到的真實現象。深挖下去,真正的分界線不是「是不是 diffusion」,
> 是更根本的 **autoregressive(AR)vs non-autoregressive(NAR)**:AR 的生成順序跟真實世界
> 資訊到達的順序是同構的,這是它天生適合 agent 的根本原因,不是巧合的工程優勢。

## 先分兩層:哪些技巧只是「靠 context 驅動」,哪些需要「中途暫停」

**Skills 大致不受影響。** Skill 的本質是「把一段程序性知識塞進 context,模型讀了就照著做」
——不管生成機制是接龍還是去噪,「context 裡放了什麼會影響輸出」是兩種架構共通的基礎能力。

**Tool use 是真正會出問題的地方。** 打個比方:自迴歸生成像一個人一句一句講話——講到一半剛好
可以停下來聽對方回答,再接著往下講。Diffusion(至少是最原始那種「一次對整段輸出反覆去噪」的
版本)比較像盯著一張模糊照片,對整張照片同時反覆調焦——沒有一個乾淨的「調到一半先暫停,拿新
資訊進來,再接著調」的節點,因為它做的不是「一格一格往後補」,是「整片一起慢慢變清楚」。

## 實測證據:不是空想的摩擦

[*The Bitter Lesson of Diffusion Language Models for Agentic Workflows: A Comprehensive Reality
Check*](https://arxiv.org/abs/2601.12979)(2026)直接測了這件事:目前的 diffusion LLM 拿去
當 agent 骨幹,在多輪互動場景會出現系統性失敗行為;tool-calling 場景會出現呼叫不精準、不
穩定,導致執行失敗;具身(embodied)agent 場景甚至會重複做同一個動作,而不是換個做法探索。
但也不是做不到——Google 的 [DiffusionGemma model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)
寫明「原生支援結構化工具呼叫」,代表有廠商在實際嘗試,只是自迴歸的 tool use 已經被業界磨了
三年(見 `tool-use` 主題的 `tool-use-origins.md`),diffusion 版本才剛起步。

## 更根本的分界線:AR vs NAR,不是「是不是 diffusion」

Diffusion 只是 NAR(non-autoregressive)陣營裡目前最紅的一種具體做法,問題的根源是 AR/NAR
這條軸,不是「是不是 diffusion」這個標籤。這件事有比 diffusion LM 早了快十年的歷史證據:
[Gu et al., 2018, *Non-Autoregressive Neural Machine Translation*](https://arxiv.org/abs/1711.02281)
(ICLR 2018)撞過一模一樣的牆,叫 **multimodality problem**——「Thank you very much.」翻成
德文,「Danke schön.」跟「Vielen Dank.」都對,但因為各個位置獨立平行決定,模型可能把兩種正確
答案的碎片混在一起,吐出「Danke Dank.」這種四不像。這跟「diffusion LLM tool-calling 不精準/
不穩定」是同一個病灶,只是換了個世代重新發作一次。

## 為什麼 AR 天生適合 agent:根因是跟真實世界因果結構同構

打個比方:你問朋友「猜蘋果現在股價多少」,他可以隨口猜;但如果他要「真的查一下」,查詢動作
必須先做、結果必須先出來,他才能根據真實數字繼續講——他不可能在結果出來前就把後面整段話定案。
這正是 AR 的結構:**每個字定案完,下一個字才輪到**,跟「每個動作做完才知道結果,才能決定下
一步」是同一種時間順序。AR 不是被設計出來特別適合 agent,是它天生的因果結構跟真實世界資訊
到達的順序**同構**——先發生的事才能決定後發生的事,不能反過來。

## 從這個根因,長出來的五個具體優勢

1. **乾淨的暫停/恢復點**——定案後的字不會再變,自然有明確邊界(stop token、完整的
   `tool_use` JSON)可以說「這裡先停,等結果,再繼續」。
2. **KV cache 可以重用**——已經定案的字,attention 計算結果可以直接快取,下一輪只需處理新
   內容,讓長迴圈的 agent 在計算上撐得住。如果前面的字隨時可能被後面收斂推翻(NAR 的情況),
   快取就沒有意義。
3. **單一個工具呼叫內部的一致性**——AR 先定案工具名稱,後面每個參數 token 都是看著這個已經
   定案的名稱在生成,保證決策物件內部連貫,不像獨立/平行決定容易出現「Danke Dank」式的自我
   矛盾。
4. **訓練資料的形狀天生就是這個順序**——工具呼叫訓練用的軌跡資料(問題 → 推理 → 呼叫 → 結果
   → 答案)本身就是一條時間軸,AR 的訓練目標套上去完全不用轉譯。
5. **出錯後可以整個重新決策**——下一步生成本來就是重新看著真實發生的結果從頭決定,沒有
   「之前已經定案、現在要推翻」的包袱,對 agent 常見的「試了不行、換個做法」是結構上天生支援。

## 修法:block-wise diffusion 借回 AR 的「定案」性質——但不是免費午餐

業界的答案不是放棄 diffusion,是把輸出切成一塊一塊(**block-wise / semi-autoregressive
diffusion**,BD3-LM、Fast-dLLM v2、LLaDA 2.0 是具體案例):block 跟 block 之間嚴格接龍(前
一個 block 定案了,後一個才開始,所以可以重用前面的計算、可以在兩塊中間插入工具結果),block
**內部**才做平行去噪。這正是在 block 的粒度上,把 AR 的「定案」性質借回來。

但這是一個真正的調校旋鈕,不是切一刀就搞定的開關:「block 切太小,保留局部條件依賴,但要跑
很多輪去噪;block 切太大,平行度看起來變高,但容易做出過早的決定、快取一致性也變差」——最新
的做法(AdaBlock-dLLM、CtrlDiff)已經把 block size 從訓練前定死的超參數,變成推論當下依樣本
動態決定的問題,代表「切多大、在哪裡切」仍是活躍在解的問題,不是已有標準答案。

## 一個容易混在一起、但其實獨立的軸

值得特別點出:**「Transformer vs Mamba/RWKV」跟「AR vs NAR」是兩條互相獨立的軸,不是同一件
事的兩種說法**(詳見 [`beyond-transformer-architectures.md`](2026-07-04-beyond-transformer-architectures.md))。
前者問「怎麼算出每個位置的表示」,後者問「輸出的各個位置,決定的順序/依賴關係長什麼樣」。實務
上兩兩都能組合:Mamba 語言模型其實也是 **AR** 的(一樣接龍生成,只是內部機制不是 attention);
多數 diffusion LM 內部其實也是拿 **Transformer** 的區塊在算,只是拿掉 causal mask、改成雙向
+ 迭代去噪。真正決定「tool use 好不好接」的是 AR/NAR 這條軸,不是 Transformer/Mamba 那條軸
——但下一篇 [`in-context-learning-under-diffusion.md`](2026-07-04-in-context-learning-under-diffusion.md)
會看到,**不是所有 agent 相關能力都掛在同一條軸上**,in-context learning 就是一個反例。

> **後續修正**:上面「拿掉 causal mask、改成雙向」這個細節,後來在
> [`llm-primitives.md`](2026-07-04-llm-primitives.md) 用第一原理重新檢驗時發現不能輕輕帶過
> ——causal mask 存不存在,其實是被解碼順序(AR/NAR)**決定**的,不是架構軸自己能選的自由度。
> 「混合機制(attention vs 狀態機)」才是真正獨立於 AR/NAR 的架構原子,細節見該篇。

## 出處

- [*The Bitter Lesson of Diffusion Language Models for Agentic Workflows*](https://arxiv.org/abs/2601.12979)(2026)——LIKELY(標題、核心論證經 WebSearch 交叉確認,未逐篇讀原文核對細節數字)。
- [DiffusionGemma model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)——LIKELY(來自 Google 官方文件站,經 WebSearch 摘要確認,未直接開啟原頁逐字核對)。
- [Gu, Bradbury, Xiong, Li & Socher, 2018, *Non-Autoregressive Neural Machine Translation*](https://arxiv.org/abs/1711.02281)(ICLR 2018)——VERIFIED(multimodality problem 定義、「Danke Dank./Vielen schön.」具體例子經 WebSearch 交叉確認多個獨立來源一致)。
- BD3-LM / Fast-dLLM v2 / SDLM / LLaDA 2.0(block-wise diffusion)、AdaBlock-dLLM / CtrlDiff(動態 block size)——LIKELY(多篇 2025-2026 arXiv 論文標題與核心機制經 WebSearch 交叉確認,未逐篇精讀;block size tradeoff 的具體措辭直接引用自搜尋摘要)。

**誠實聲明**:「AR 跟世界因果結構同構」這整套根因→分支的推導,是這篇筆記自己的重建,不是引用
某一篇論文的現成結論——上面列出的具體事實(multimodality problem、tool-use 訓練軌跡資料形狀、
block-wise 的機制與 tradeoff)都已查證,但把它們串成這個統一解釋,是這篇自己推出來的,沒有
對應到某篇論文的原句。
