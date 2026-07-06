---
date: 2026-07-04
tags:
  - llm-foundations
  - in-context-learning
  - diffusion
---

# Diffusion 怎麼做 in-context learning?

> TL;DR — 意外的是,non-autoregressive(NAR)的 diffusion 語言模型,少樣本(few-shot)ICL
> 表現追平甚至打贏同量級的自迴歸(AR)模型。回頭看並不意外:ICL 靠的是 attention 怎麼讀
> context,是「Transformer vs Mamba」那條**架構軸**在管的事,幾乎跟「AR vs NAR」那條**生成
> 順序軸**無關。具體機制是:few-shot 範例被當成一塊從頭到尾不變、雙向 attention 全程可見的
> 「凍結鷹架」,答案的每個位置從第一步去噪就能直接看到全部範例。

## 意外的實證結果

[Nie et al., 2025, *Large Language Diffusion Models*](https://arxiv.org/abs/2502.09992)
(LLaDA,8B)在 15 項標準 zero/few-shot 評測上大多打贏 LLaMA2 7B、追平 LLaMA3 8B——TriviaQA
5-shot 拿到 62% 準確率,跟 LLaMA3 8B 打平。[Ye & Xie et al., 2025, *Dream 7B*](https://arxiv.org/pdf/2508.15487)
在 few-shot 設定下,同樣贏過同量級的 AR 模型。**LLaDA 這篇論文自己的結論很直接:non-
autoregressive 模型可以擁有 in-context learning、instruction-following 這些核心 LLM 能力,
挑戰了「語言智能必須靠自迴歸建模」這個常見假設。**

## 為什麼這個結果其實不意外——ICL 掛在另一條軸上

[`in-context-learning.md`](2026-07-04-in-context-learning.md)講的三套理論(induction
heads / 隱式梯度下降 / 隱式貝氏推論),講的都是「模型怎麼看 prompt 裡的範例」——這是
attention 怎麼處理輸入 context 的能力,是架構軸在管的事,不是生成順序軸在管的事。Diffusion
模型生成輸出時,一樣要對整個輸入 context(包含 few-shot 範例)做 attention——只是輸出的解碼
順序換了,讀入 context 的方式沒有變。ICL 成不成立,問的是「context 裡的範例有沒有被有效利用」,
跟「輸出是接龍生成還是平行去噪」是兩個不同的問題。

## 具體機制:凍結的鷹架 + 雙向 attention

**訓練階段(forward process)**:拿一段乾淨文字,用隨機比例 `t ~ U[0,1]` 去蓋住其中一部分
token,練模型「看剩下沒被蓋住的,猜被蓋住的原本是什麼」——這是 BERT 填空題的廣義版:BERT 固定
蓋 15%,這裡蓋的比例每次不一樣,從蓋一點點到蓋到全部都可能。

**使用階段(reverse process)**,分兩塊處理:

- **Prompt(含 few-shot 範例)整段從頭到尾原封不動,完全不蓋。**
- **真正要生成的答案部分一開始整段蓋起來**,然後重複:模型同時對所有還蓋著的位置猜答案 →
  挑信心最高的幾個位置「定案」(拿掉遮罩)→ 剩下沒信心的繼續蓋著 → 重複直到全部定案。

因為 attention 是雙向的(沒有 causal mask),答案裡的每一個位置,在**第一輪去噪**就已經可以
直接看到整個 prompt——結構上甚至比 AR(只能往回看)對 context 的存取更直接、更平等。

## 機制研究的細節:AR 式的偏向還在,但來源不是訓練目標

[Piskorz et al., *In-Context Learning in Diffusion Language Models*](https://transformerstheory.github.io/pdf/14_piskorz_et_al.pdf)
直接做了控制實驗,發現兩件事:DLM 在 ICL 評測上追平 AR;但 DLM 還是帶有「偏近、偏左」的傾向
(recency bias、left-directedness),跟 AR 模型類似,只是比較弱。更關鍵的是,**這個傾向追根
究底來自訓練資料本身的統計特性**(人類正常寫的文字本來就有「越靠近越相關、由左到右鋪陳」的
結構),**不是來自 AR 這個訓練目標本身**——證據是:把一個已經訓練好的 AR 模型拿 diffusion
loss 重新微調,這個偏向不會完全消失;但從頭就用 diffusion 目標訓練出來的模型,偏向反而比較弱。

## 澄清:單次 ICL 是靜態的,「凍結區增長」是多輪 agent 才有的事

容易搞混的一點:**單次 few-shot ICL,凍結區在生成過程中不會變大**——你一次決定好放幾個範例,
一次凍結,然後對答案去噪,是「一次到位、凍結後重複讀很多次」,不是「邊生成邊長大」。

「凍結區一直長大」真正發生的地方,是
[`autoregressive-vs-nonautoregressive-for-agents.md`](2026-07-04-autoregressive-vs-nonautoregressive-for-agents.md)
講的**多輪 agent 迴圈**:每完成一個 block(一輪對話、一次工具呼叫的結果),這個 block 就併入
凍結區,下一個 block 站在變大後的凍結區上繼續生成——這正是 block-wise diffusion(BD3-LM、
Fast-dLLM v2)的實際做法,跟 AR 的 KV cache 隨對話輪數增加是同一個精神,只是單位從「一個
token」換成「一個 block」。兩者疊在一起看:多輪 agent 場景其實是很多次「單次 ICL」疊起來——
每一輪內部都是靜態的一次性讀取,但輪與輪之間,凍結區確實在累積長大。

## 出處

- [Nie et al., 2025, *Large Language Diffusion Models*](https://arxiv.org/abs/2502.09992)(LLaDA)——VERIFIED(TriviaQA 5-shot 62%、追平 LLaMA3 8B、「non-autoregressive 也能做 ICL」的核心結論經 WebSearch 交叉確認)。
- [Ye & Xie et al., 2025, *Dream 7B: Diffusion Large Language Models*](https://arxiv.org/pdf/2508.15487)——LIKELY(核心比較結論經 WebSearch 摘要確認,未逐篇精讀原始評測表格)。
- Masked diffusion 的 forward/reverse process、prompt 永遠不被遮罩、雙向 attention 全程可見——LIKELY(經 WebSearch 交叉確認多個 2025-2026 來源一致描述,未逐篇精讀原始論文的公式推導)。
- [Piskorz et al., *In-Context Learning in Diffusion Language Models*](https://transformerstheory.github.io/pdf/14_piskorz_et_al.pdf)——LIKELY(標題與核心發現經 WebSearch 摘要確認,這是一篇 workshop 論文,未取得完整內文逐段核對)。

**誠實聲明**:「ICL 掛在架構軸、幾乎跟 AR/NAR 無關」這個區分,以及「單次 ICL 靜態 vs 多輪
agent 凍結區增長是同一機制的不同尺度」這個整合,是這篇筆記自己的推導——建立在上面已查證的
事實上,但不是某篇論文的現成結論。
