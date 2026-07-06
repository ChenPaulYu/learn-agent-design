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
  - label: 核心機制(任意順序)
    note: 都只依賴 101,彼此互相獨立,讀完 101 之後想先看哪個都可以。
    parallel: true
    pages: [transformer-self-attention, next-token-prediction, in-context-learning, beyond-transformer-architectures]
  - label: 機制延伸(任意順序)
    note: 各自只延伸核心機制裡的某一篇,彼此不互相依賴。
    parallel: true
    pages: [positional-encoding, tokenizer-schemes-and-weight-tying, cross-entropy-teacher-forcing, decoding-strategies, scaling-laws]
  - label: 匯流
    note: 各自需要先讀過兩篇以上——autoregressive-vs-nonautoregressive 建議先讀完核心機制,in-context-learning-under-diffusion 再建議接著讀完 autoregressive-vs-nonautoregressive。
    pages: [autoregressive-vs-nonautoregressive, in-context-learning-under-diffusion]
  - label: 後訓練
    note: 下一個真實階段,不是更難——pretraining 到這裡結束,講的是 base model 怎麼變成會對話的助理。
    pages: [post-training-sft-rlhf]
---

從第一原理回頭問:為什麼 LLM 能這樣運作——Transformer、tokenizer、next-token prediction、
in-context learning,以及「這些是不是必須的」反事實測試。
