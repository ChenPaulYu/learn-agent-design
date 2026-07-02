---
date: 2026-07-02
tags:
  - mcp
  - scaling
---

# 太多工具問題:一個 host 接多個 server 之後,工具清單怎麼辦

MCP 解決了「接一個 server」該怎麼講話的問題,但沒解決「接十個 server」之後會發生什麼事——
每個 server 的工具清單、input schema 全部要塞進同一個 context,LLM 得從裡面挑對的呼叫。官方
文件對這件事講得很直接。

## 問題本身:笨拙的做法會讓模型變笨、變慢、變貴

> "Naive approaches to tool management in MCP host applications can lead to issues like wasted
> tokens, increased latency, and degraded model performance when connecting to numerous servers
> and tools."
> — [`client-best-practices.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/clients/client-best-practices.mdx)

拆開看是三個獨立的壞處,不是同一件事的三種說法:

1. **浪費 token**——每個工具的 name/description/input schema 都要塞進 context,工具一多,
   還沒開始做事,prompt 就先被工具定義吃掉一大塊。
2. **延遲增加**——context 變大,單次生成的時間跟著變長。
3. **模型表現變差**——選項太多,LLM 從一堆長得差不多的工具裡挑錯的機率上升,這不是「模型變笨」,
   是「攤在它面前的選擇太雜」。

## Progressive Tool Discovery——先給搜尋工具,不要一次全塞

> "Progressive discovery defers injecting tool definitions into the model's context. Instead of
> loading all definitions upfront, the host provides a lightweight `search_tools` meta-tool and
> only loads full definitions as needed. This is particularly beneficial when tool definitions
> consume a significant portion of the context window."
> — [`client-best-practices.mdx` § Progressive Tool Discovery](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/clients/client-best-practices.mdx)

具體做法:host 不把十個 server 的所有工具定義一次性塞進 system prompt,而是先只給模型一個
輕量的 `search_tools`(或類似名字)meta-tool——模型想找工具時,先呼叫這個 meta-tool 描述
需求,host 才把符合的少數幾個工具的完整 schema 載進 context。**先搜尋、後載入**,不是
**先載入全部、後選擇**。

## Programmatic Tool Calling(Code Mode)——讓模型寫程式碼呼叫工具,不要一次一輪來回

一般的工具呼叫是「模型生成一次呼叫 → client 執行 → 結果送回模型」,每次呼叫都要走一輪完整的
來回——工具鏈越長,來回越多次,每次都要付 token 跟延遲的代價:

> "Direct tool calling involves a round trip for each tool invocation... Programmatic tool
> calling, or 'code mode', allows the model to write code that calls tools, which then executes
> in a sandboxed environment, returning only the final result to the model."
> — [`client-best-practices.mdx` § Programmatic Tool Calling / Code Mode](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/clients/client-best-practices.mdx)

也就是模型不再「一次呼叫一個工具、等結果、再決定下一步」,而是一次寫出一段完整的程式碼(裡面
可能呼叫好幾個工具、串起邏輯),丟進一個沙箱裡執行,**只有最終結果**送回模型——中間步驟的
資料完全不會進到模型的 context。代價是 client 端要多做一件事:**自己實作一個沙箱環境**來跑
這段程式碼,不是白吃的午餐。

## 兩個手法疊起來用

> "The model first uses discovery tools to determine the necessary tools, loads their schemas,
> and then generates a single script to execute multiple tools in one pass. This approach
> reduces token costs for both tool definitions and results, allowing the model to focus on
> reasoning rather than data transfer."
> — [`client-best-practices.mdx` § Combining Both Patterns](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/clients/client-best-practices.mdx)

流程是:先用 Progressive Discovery 找出真正需要的那幾個工具、只載入它們的 schema(省下工具
定義的 token)→ 再用 Programmatic Tool Calling 把整條邏輯寫成一段程式碼一次跑完、只把最終
結果送回模型(省下中間結果的 token)。兩層省的是不同的東西——一個省「定義」,一個省「資料
搬運」——疊起來才蓋住兩種浪費。

## 跟 tools/list 的 pagination 不是同一件事,別搞混

`tools/list` 本身支援 `cursor`/`nextCursor` 分頁:

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {"cursor": "optional-cursor-value"}}
```

這是**單一 server** 工具清單太長時,線路層的分頁機制,防的是「一次回應塞爆」這種傳輸層問題。
跟 Progressive Discovery 防的不是同一種浪費——分頁只是把同一份清單切成幾批傳,清單裡的東西
**最終還是會全部進到 client 手上**;Progressive Discovery 防的是「host 決定要不要把某個工具
的完整定義塞進**模型的 context**」,這是模型能看到多少的問題,跟「傳輸怎麼分批」是兩層不同的
關注點。

## Anthropic 自己把這套模式做成產品功能了

Claude Developer Platform 有三個對應的 beta 功能(Tool Search Tool、Programmatic Tool
Calling、Tool Use Examples),名字幾乎沒改。但這是 Claude API 本身的能力,不是 MCP 協定的
東西,工具不一定來自 MCP——歸屬不屬於這篇,獨立開一個主題的候選項記在 repo 根目錄的
`BACKLOG.md`,還沒真的動筆。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-02 抓取查證:

- [`docs/develop/clients/client-best-practices.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/develop/clients/client-best-practices.mdx)
  ——這篇筆記幾乎全部內容的來源:問題描述、Progressive Discovery、Programmatic Tool Calling
  / Code Mode、兩者疊加的做法。
- [`specification/2025-11-25/server/tools.mdx`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx)
  ——`tools/list` 的 `cursor`/`nextCursor` 分頁機制。
