---
date: 2026-07-04
tags:
  - llm-foundations
  - transformer
  - alternative-architectures
---

# Transformer 是必須的嗎?——Mamba、RWKV、RetNet、Diffusion 這些 rising star

> TL;DR — 不是必須,是目前最有效,而且「有效」裡面混了一部分基礎建設慣性。至少有兩層挑戰
> 正在鬆動「Transformer 必須」這個假設:一層是換掉 self-attention 這個引擎、但目的地(接龍
> 生成)不變(Mamba/RWKV/RetNet);另一層更激進,連「一個字一個字接龍」這件事本身都不是
> 必須的(diffusion language models)。目前公開已知最頂尖的旗艦模型,骨幹仍以 Transformer
> 或 Transformer 混血為主——這條假設正在被鬆動,還沒被推翻。

## 兩層不同的「不一定要」

`transformer-self-attention.md` 建立起來的整套東西像一台車:next-token prediction 是「目的
地」(每次都往正確答案開一步),Transformer 是「引擎」(「整排一起看」這個具體做法)。「一定要
Transformer 嗎」這個問題藏著兩層:引擎能不能換(還是朝著同一個目的地開)、連目的地開法都能不
能換。

## 第一層:換引擎,目的地不變——State Space Models(Mamba)最亮眼

[Gu & Dao, 2023, *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*](https://arxiv.org/abs/2312.00752)
不用「整排一起看」(成本隨句子長度**平方**成長),改用一種可以「選擇性記住/忘記」的狀態機制,成本隨
句子長度**線性**成長、推論時記憶體用量固定。**Falcon Mamba 7B**(純 Mamba 架構,5.8 兆 token
訓練)是一個具體的「存在證明」——真的訓練出來,在多項評測上贏過同量級的 Transformer 模型
(如 Mistral 7B)。後續 Mamba-2 用一種叫 SSD(state space duality)的技巧讓訓練效率再提升
2-8 倍。

同一個方向還有 **RWKV**(「把 RNN 為 Transformer 時代重新發明」)跟 **RetNet**(微軟提出,靠
retention 機制做到推論時每步固定成本、精度跟 Transformer 打平),都在追同一個目標:保留
Transformer 訓練時能平行運算的優點,甩掉它推論成本隨長度爆炸的缺點。

**現狀是混血,不是全面換血。** 目前業界最主流的做法,不是整台車全部換引擎,是換成混血引擎——
多數新架構拿 SSM/線性注意力當骨幹,但每隔幾層還是保留幾層真正的 self-attention(例如 AI21
的 Jamba)。純 SSM 在中小規模已經證明能打平甚至贏過同量級 Transformer,但公開已知的最頂尖
旗艦模型,骨幹仍然是 Transformer 或這種混血版本,還沒有純 SSM 站上最前沿。

## 第二層:連「接龍」本身都能換——Diffusion Language Models

這層更激進,直接挑戰 [`next-token-prediction.md`](2026-07-04-next-token-prediction.md) 裡
「一個字一個字往後猜」這個前提本身。Diffusion 語言模型不接龍——從一整片雜訊開始,**同時對所有
位置**反覆去噪,一輪一輪把雜訊修正成合理的文字,跟 Stable Diffusion 生圖片是同一種數學框架,
只是套用到文字上。好處是生成可以平行,不用等前一個字生完才生下一個字。LLaDA、Dream、
DiffuLLaMA 是這條線幾個十億參數級的具體案例,Google 的 **Gemini Diffusion**(2025 年 5 月)
是目前查到第一個「商用等級品質追平自迴歸模型」的案例。

這層跟 tool use / in-context learning 這些 agent 相關能力具體怎麼互動,留給
[`autoregressive-vs-nonautoregressive-for-agents.md`](2026-07-04-autoregressive-vs-nonautoregressive-for-agents.md)
跟
[`in-context-learning-under-diffusion.md`](2026-07-04-in-context-learning-under-diffusion.md)
兩篇處理,這篇只講架構本身。

## 為什麼 Transformer 現在還是「預設選項」——不完全是技術原因

除了引擎/目的地本身的技術權衡,還有一個容易被忽略的因素:整個業界過去八年的訓練框架、硬體
co-design、除錯工具、人才經驗,全部是圍著 Transformer 這個特定架構堆出來的。換一種架構,不只
是架構本身要打平甚至打贏,還要打贏這整套已經堆了八年的基礎建設慣性——這是「已經有更好的引擎」
跟「大家真的換過去用」中間,還隔著一段真實距離的原因。

## 出處

- [Gu & Dao, 2023, *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*](https://arxiv.org/abs/2312.00752)
  ——VERIFIED(標題、arXiv 編號經 WebSearch 確認;Falcon Mamba 7B、Mamba-2 SSD 效率提升倍數
  來自搜尋摘要,未逐篇原文核對細節數字,LIKELY)。
- RWKV(*Reinventing RNNs for the Transformer Era*)、RetNet——LIKELY(標題、機制描述經
  WebSearch 交叉確認多個來源,未逐篇讀原文)。
- Diffusion language models(LLaDA、Dream、DiffuLLaMA、Gemini Diffusion)——LIKELY(經
  WebSearch 交叉確認多個 2025-2026 來源一致,「Gemini Diffusion 2025 年 5 月首次商用等級追平」
  這個具體說法沒有找到 Google 官方一手公告核對,是第三方摘要)。

**誠實聲明**:「基礎建設慣性」這個解釋是這篇筆記自己的推論,不是引用某篇論文的結論,但邏輯上
站得住——換架構不只是架構本身要贏,還要贏過已經堆了八年的生態系統慣性。
