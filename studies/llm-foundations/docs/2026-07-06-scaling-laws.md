---
date: 2026-07-06
tags:
  - llm-foundations
  - scaling-laws
  - chinchilla
---

# Scaling laws:規模、資料、算力怎麼換算

> TL;DR — 把模型變大、餵更多資料、砸更多算力,表現(loss)不是隨便亂漲,而是呈現平滑的
> **冪律關係(power law)**——量尺一路拉大,曲線不會忽然跳一階,是可以外推預測的。但「怎麼分配」
> 這件事業界一開始配錯了:Kaplan et al. 2020 的原始配方建議把預算大部分砸在**堆參數**上,資料量
> 相對少一點就好;DeepMind 的 Chinchilla 論文(Hoffmann et al., 2022)兩年後推翻這個配方,證明
> 同樣的算力預算下,**模型大小跟資料量應該接近等比例一起放大**——很多當紅大模型其實是「參數
> 撐得很大,資料餵得不夠」。

## 先講清楚在量什麼

這篇談的「表現」,量的是**訓練時的 loss**(對牌庫打分那一步,見
[`next-token-prediction.md`](2026-07-04-next-token-prediction.md)——模型對下一個字猜得準不準,
用一個連續的數字表示,猜得越準 loss 越低)。三個可以拉大的量尺:

- **N**——模型參數量(牌櫃收納位置的總數規模,大致對應模型「能裝多少東西」)
- **D**——訓練資料量(訓練時實際餵過幾次牌局、多少 token)
- **C**——訓練算力(FLOPs,把 N 跟 D 都跑起來要花多少計算資源)

## Kaplan et al. 2020:三條平滑的冪律曲線

[Kaplan et al., 2020, *Scaling Laws for Neural Language Models*](https://arxiv.org/abs/2001.08361)
(OpenAI)訓練了兩百多個 Transformer 模型,橫跨算力七個數量級、參數量四個數量級、資料量三個
數量級,量出一件事:只要另外兩個量尺不是瓶頸,loss 跟 N、D、C 各自呈現乾淨的冪律關係——
`L ∝ N^(-α)`、`L ∝ D^(-β)`、`L ∝ C^(-γ)`。畫在 log-log 座標上,這些關係是接近直線的——這正是
[`next-token-prediction.md`](2026-07-04-next-token-prediction.md) 提過的「規模一大能力忽然冒出來
(emergent abilities)可能是量尺選擇的錯覺」的量化版本:如果連續指標(loss)本身就是平滑外推的
冪律,那「忽然開竅」的觀感,很可能真的是換了不連續的評測量尺才看到的假象,不是 loss 這條底層
曲線本身在某個點忽然轉彎。

**這篇論文更關鍵、影響更大的地方,是它給出的「配方」**:在固定算力預算 C 下,怎麼分配給 N
(模型大小)跟 D(資料量)才最划算?Kaplan et al. 的結論是 **N 該吃掉大部分預算,D 只要跟著吃一小
部分**——量化下來大致是 `N_optimal ∝ C^0.73`、`D_optimal ∝ C^0.27`,換句話說「算力每增加十倍,
模型大小該漲得比資料量快得多」。背後的論證是**大模型比小模型「樣本效率」更高**——同樣一批訓練
資料,大模型能榨出更多東西,所以最划算的做法是把模型盡量做大、訓練資料相對少一點、甚至**訓練
還沒收斂到底就提早停**,而不是把小模型的訓練資料塞好塞滿。

這個配方在當時被業界奉為圭臬,直接影響了 GPT-3 這類模型的設計——[Brown et al., 2020,
*Language Models are Few-Shot Learners*](https://arxiv.org/abs/2005.14165) 裡的 GPT-3 有 175B
參數,訓練資料大約 300B token。

## Chinchilla / Hoffmann et al. 2022:配方配錯了,資料餵太少

兩年後,DeepMind 的 [Hoffmann et al., 2022, *Training Compute-Optimal Large Language
Models*](https://arxiv.org/abs/2203.15556)(NeurIPS 2022)重新做了一次規模更大的實驗——訓練
超過四百個模型,參數量從 70M 到 16B、資料量從 5B 到 500B token,重新去擬合「同樣算力下,N 跟 D
該怎麼配」這個問題。結論跟 Kaplan et al. 明顯不同:**最划算的配比是 N 跟 D 接近等比例一起放大
——模型大小每翻倍,訓練資料量也該跟著翻倍**,不是像 Kaplan 配方那樣讓 N 遠遠跑在 D 前面。順著
這個結論反推回去看,像 GPT-3(175B 參數、300B token)這類照 Kaplan 配方訓練出來的模型,其實是
**「模型撐得很大、資料相對餵不夠」**——同樣的算力,如果把資料量拉高、模型做小一點,理論上可以
換到更低的 loss。

論文用一個直接的對照組驗證這個結論:**Chinchilla**(70B 參數,餵了 1.4 兆 token)跟
**Gopher**(280B 參數,餵了約 300B token)用掉差不多的訓練算力——Gopher 的參數量是 Chinchilla
的四倍,但 Chinchilla 用等比例放大資料量的配方,在幾乎相同的算力預算下,表現**全面優於**
Gopher(以及 GPT-3、Jurassic-1、Megatron-Turing NLG 這些同期的大模型),在 MMLU 這個綜合測驗
上拿到 67.5% 的平均正確率,比 Gopher 高超過 7 個百分點。換句話說:**同樣的算力,配方對了,可以
用四分之一大小的模型打贏四倍大的模型**。

## 誠實提醒:這是經驗擬合,不是理論證明,係數也不是永久不變

- 這些冪律關係是**觀察到的經驗規律**,不是從第一性原理推導出「必然如此」的數學定理——擬合出來
  的指數(`α`、`β`、`γ`,以及 Chinchilla 的等比例配方)是對特定一批實驗數據做迴歸的結果,換一種
  架構、換一種資料組成、換一種評測方式,係數會不一樣,曲線也可能不再是乾淨的直線。
- Chinchilla 論文本身的具體係數,後來受到過方法學上的質疑:[Besiroglu, Erdil et al., 2024,
  *Chinchilla Scaling: A replication attempt*](https://arxiv.org/abs/2404.10102) 嘗試重建
  Hoffmann et al. 論文圖表背後的數據,指出原論文報的信心區間窄得不合理(那麼窄的區間需要遠超過
  原論文實際跑的實驗數量才撐得起來),懷疑是擬合過程中優化器提早停止導致的統計瑕疵——但這篇
  重建文章本身也承認,修正過後重新擬合,「模型大小跟資料量該接近等比例放大」這個**方向性結論**
  站得住腳,受質疑的是原論文報告的精確係數跟信心區間,不是 Chinchilla 配方整體的方向。LIKELY
  (經 WebSearch 確認論文標題、核心質疑與其自陳的結論,未逐篇精讀原文的統計細節)。
- 這些規律是在特定任務(語言模型的 next-token loss)、特定資料分佈(網路爬蟲文字為主)下量出來
  的,換到程式碼、多模態、或資料品質差異很大的語料,實際擬合出來的係數會不一樣——不能直接把
  「70B 配 1.4 兆 token」當成放諸四海皆準的公式硬套。

## 出處

- [Kaplan, McCandlish, Henighan et al., 2020, *Scaling Laws for Neural Language Models*](https://arxiv.org/abs/2001.08361)
  ——原始 scaling laws 論文,N/D/C 三條冪律關係、`N_optimal ∝ C^0.73`、`D_optimal ∝ C^0.27` 的
  配方出處。VERIFIED(經 WebSearch 交叉確認論文標題、作者、實驗規模、核心冪律公式與配方指數)。
- [Hoffmann, Borgeaud, Mensch et al., 2022, *Training Compute-Optimal Large Language
  Models*](https://arxiv.org/abs/2203.15556)(NeurIPS 2022)——Chinchilla 論文,「模型與資料
  該等比例放大」的修正結論、Chinchilla(70B/1.4T token)對照 Gopher(280B)、MMLU 67.5% 的具體
  數字出處。VERIFIED(經 WebSearch 交叉確認論文標題、發表會議、實驗規模、Chinchilla vs Gopher
  的參數量/資料量/MMLU 分數)。
- [Brown et al., 2020, *Language Models are Few-Shot Learners*](https://arxiv.org/abs/2005.14165)
  ——GPT-3 論文,175B 參數、約 300B token 訓練資料量的出處。VERIFIED(經 WebSearch 交叉確認)。
- [Besiroglu, Erdil et al., 2024, *Chinchilla Scaling: A replication attempt*](https://arxiv.org/abs/2404.10102)
  ——對 Hoffmann et al. 原始係數的方法學質疑與重新擬合。LIKELY(經 WebSearch 確認論文標題與核心
  論點摘要,未逐篇精讀原文統計方法)。

**誠實聲明**:「跟 [`next-token-prediction.md`](2026-07-04-next-token-prediction.md) 的 emergent
abilities 錯覺互相呼應」這一段連結,是這篇筆記自己做的推論串接,不是 Kaplan et al. 或
Schaeffer et al. 論文裡明講的對照——兩篇論文談的分別是「loss 這個連續指標本身是否平滑」跟「下游
任務表現在不連續量尺下是否平滑」,是相關但不是同一件事,這裡只是指出兩者共同指向「平滑漸進、
沒有魔法門檻」這個方向。除此之外,本篇所有具體數字(冪律指數、Chinchilla/Gopher/GPT-3 的參數量
與資料量、MMLU 分數)均經 WebSearch 查證,並在上方出處逐條標記信心等級。
