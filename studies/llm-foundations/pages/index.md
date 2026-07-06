---
title: LLM Foundations
topic: llm-foundations
permalink: /llm-foundations/
date: 2026-07-04
layout: default
groups:
  - label: 先讀這篇
    note: Level 1 核心迴圈——文字怎麼一步步變回文字。讀完就能完整回答「LLM 怎麼運作」。
    pages: ["101"]
  - label: 核心機制詳解(任意順序)
    note: 101 核心迴圈五站,各自的完整版本跟延伸細節——彼此獨立,讀完 101 之後想先看哪個都可以。
    parallel: true
    pages: [transformer-self-attention, positional-encoding, tokenizer-schemes-and-weight-tying, next-token-prediction, cross-entropy-teacher-forcing, decoding-strategies, in-context-learning]
  - label: 為什麼這樣就夠
    note: 規模、資料、算力怎麼換算成表現——emergent abilities mirage 的量化延伸。
    pages: [scaling-laws]
  - label: 是不是必須(任意順序)
    note: Transformer/autoregressive 是不是必須的反事實測試,以及對 agent 相關能力的影響。
    parallel: true
    pages: [beyond-transformer-architectures, autoregressive-vs-nonautoregressive, in-context-learning-under-diffusion]
  - label: 後訓練(獨立於核心迴圈)
    note: 接龍練完只是雜學高手,這篇講怎麼變成會對話的助理——假設核心迴圈已經存在,疊在上面的另一個階段。
    pages: [post-training-sft-rlhf]
---

從第一原理回頭問:為什麼 LLM 能這樣運作——Transformer、tokenizer、next-token prediction、
in-context learning,以及「這些是不是必須的」反事實測試。
