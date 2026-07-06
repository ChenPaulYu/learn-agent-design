---
date: 2026-07-04
tags:
  - llm-foundations
  - index
---

# llm-foundations — 導覽

> 往下挖一層地基:`agent-anatomy` 的五層框架整個蓋在「LLM 已經能思考、能吐字」這個假設上,
> 這個主題回頭問**為什麼 LLM 能這樣運作**——從承載一切的架構(Transformer)、怎麼把文字餵給
> 它(tokenizer)、訓練目標(next-token prediction),到推論時最違反直覺的現象(in-context
> learning),再到「這些是不是必須的」反事實測試(Transformer/AR 是不是必須、diffusion 這種
> 替代範式對 tool use / ICL 這些 agent 相關能力的影響)。範圍先只做「LLM 原理」這一段(含它的
> 替代方案與邊界);「LLM 怎麼被組裝成 Agent」的橋接是下一步,先留在 `BACKLOG.md`。

## 文件

這份清單照**依賴關係**排(讀得懂這篇需要先讀過誰),不是照主題分類——用 `/frame:first-principles`
+ `/shape:elicit` 收斂過:大部分文件之間是「讀懂需要什麼」的引用依賴,但 `post-training` 是
例外,它留在最後不是因為比較難,是因為它描述的階段**在真實世界裡本來就發生在 pretraining 之後**
(時序依賴,不是理解依賴)。

先讀這篇:

- [llm-foundations 101](pages/101.html) ——
  Level 1 核心迴圈,文字怎麼一步步變回文字。讀完就能完整回答「LLM 怎麼運作」。

核心機制(任意順序,都只依賴 101):

- [transformer-self-attention](docs/2026-07-04-transformer-self-attention.md)([頁面](pages/transformer-self-attention.html)) ——
  RNN 的傳話遊戲問題、self-attention 的「整排一起看」解法、Transformer ≠ LLM(只是被選中的引擎)、
  為什麼特別適合套在 next-token prediction 上、multi-head 與疊層怎麼運作
- [next-token-prediction](docs/2026-07-04-next-token-prediction.md)([頁面](pages/next-token-prediction.html)) ——
  為什麼「猜下一個字」這個訓練目標,能練出理解文法/事實/邏輯的能力(壓縮論證 + GPT-2 案例
  校驗),「規模一到能力就忽然冒出來」這個敘事為什麼要打折扣(emergent abilities mirage),
  以及這個目標為什麼天生綁定 autoregressive 生成順序
- [in-context-learning](docs/2026-07-04-in-context-learning.md)([頁面](pages/in-context-learning.html)) ——
  為什麼塞幾個範例進 prompt,模型完全不改參數就「當場學會」——三套彼此不互斥、目前仍活躍研究
  中的解釋(induction heads 機制電路 / 隱式梯度下降 / 隱式貝氏推論)
- [tokenizer-bpe](docs/2026-07-04-tokenizer-bpe.md) ——
  為什麼要把文字切成積木、BPE 演算法怎麼造積木箱與套用、GPT-2 byte-level BPE 為什麼不會有
  「未知符號」(核心迴圈頁 `pages/101.html` 第 2 站已涵蓋這篇的精華)
- [beyond-transformer-architectures](docs/2026-07-04-beyond-transformer-architectures.md)([頁面](pages/beyond-transformer-architectures.html)) ——
  Transformer 是不是必須?Mamba/RWKV/RetNet 這些換引擎不換目的地的 rising star,diffusion
  language models 這個連目的地都換的更激進路線,以及為什麼 Transformer 現在還是預設選項

機制延伸(任意順序,各自只延伸上面某一篇,彼此不互相依賴):

- [positional-encoding](docs/2026-07-06-positional-encoding.md)([頁面](pages/positional-encoding.html)) ——
  「整排一起看」天生分不出順序這個副作用怎麼補:正弦波位置編碼(原始論文)vs RoPE(現代主流,
  關聯分數天生只跟相對距離掛勾)vs ALiBi
- [tokenizer-schemes-and-weight-tying](docs/2026-07-06-tokenizer-schemes-and-weight-tying.md)([頁面](pages/tokenizer-schemes-and-weight-tying.html)) ——
  造牌庫的兩種哲學(BPE 合併 vs SentencePiece/Unigram 篩選)、輸入 embedding 表跟輸出打分表
  常常是同一份參數(weight tying)
- [cross-entropy-teacher-forcing](docs/2026-07-06-cross-entropy-teacher-forcing.md)([頁面](pages/cross-entropy-teacher-forcing.html)) ——
  訓練時怎麼打分(teacher forcing 讓整排一起算、cross-entropy loss 怎麼算)、訓練跟推論之間
  的落差(exposure bias)
- [decoding-strategies](docs/2026-07-06-decoding-strategies.md)([頁面](pages/decoding-strategies.html)) ——
  從機率分佈到一個字:貪婪解碼、beam search、溫度、top-k、top-p——沒有絕對最好,是穩定 vs
  多樣的設計取捨
- [scaling-laws](docs/2026-07-06-scaling-laws.md)([頁面](pages/scaling-laws.html)) ——
  規模、資料、算力怎麼換算成表現(Kaplan et al. 冪律關係),以及 Chinchilla 對「一味堆參數」
  的修正——emergent abilities mirage 的量化延伸

匯流(各自需要先讀過兩篇以上):

- [autoregressive-vs-nonautoregressive-for-agents](docs/2026-07-04-autoregressive-vs-nonautoregressive-for-agents.md)([頁面](pages/autoregressive-vs-nonautoregressive.html)) ——
  需要先讀過 `next-token-prediction`(AR 從哪來)+ `transformer-self-attention`(架構軸 vs
  解碼軸的區分)。換成 diffusion,tool use 還撐得住嗎?真正的分界線是 AR vs NAR(不是「是不是
  diffusion」),為什麼 AR 天生跟真實世界因果結構同構,以及 block-wise diffusion 怎麼借回這個
  性質(但不是免費午餐)
- [in-context-learning-under-diffusion](docs/2026-07-04-in-context-learning-under-diffusion.md)([頁面](pages/in-context-learning-under-diffusion.html)) ——
  需要先讀過 `in-context-learning` + `autoregressive-vs-nonautoregressive-for-agents`,是
  兩者的交集。反例:non-autoregressive 的 diffusion 模型 ICL 表現不輸 AR,因為 ICL 掛在
  「架構軸」,幾乎跟「AR/NAR 軸」無關——具體機制是凍結的 prompt 鷹架 + 雙向 attention

全域收斂(建議讀過上面全部再看):

- [llm-primitives](docs/2026-07-04-llm-primitives.md) ——
  理解 LLM 最少需要哪幾個互相獨立的 primitive?用 `/frame:first-principles` 重新檢驗一次
  隨口提出的框架,找出「看起來獨立、實際上不對等」的地方(訓練目標決定解碼順序的開放度,不是
  平行選項;架構軸原本偷塞了 causal mask 這個其實不獨立的細節)

後訓練(下一個真實階段,不是更難——pretraining 到這裡結束):

- [post-training-sft-rlhf](docs/2026-07-06-post-training-sft-rlhf.md)([頁面](pages/post-training-sft-rlhf.html)) ——
  接龍練完只是一個什麼都能接、但不一定有幫助的雜學高手;SFT 照抄範例、RLHF/DPO 靠人類偏好
  比較調整——base model 怎麼變成會對話的助理

## 跟 `agent-anatomy` 的關係

`agent-anatomy` 研究「怎麼把一個 agent 系統拆成五層」,五層框架裡的 Pattern 層(prompt 設計)
預設了一件事:LLM 收到 prompt 之後,「知道」怎麼回應。這個主題往下一層,問的正是**這個「知道」
從哪裡來**——訓練階段內化的通用能力(`next-token-prediction.md`)+ 推論時怎麼被 prompt 裡的
內容「指認」出該用哪一種(`in-context-learning.md`)。這裡的結論是 `agent-anatomy` Pattern
層的前提知識,不是它的一部分。
