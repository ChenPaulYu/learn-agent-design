---
date: 2026-07-03
tags:
  - tool-use
  - basics
---

# Tool Use 基礎:LLM 怎麼決定要呼叫一個工具

這個機制在 MCP 血緣那篇筆記裡當過配角(「Tool Use / Function Calling」是 MCP 借用的兩個
既有能力之一),但從沒被當成主角講過——這篇補上這個缺口:**不透過 MCP,LLM API 本身怎麼讓
模型呼叫外部工具**。

## 三個部分:定義、呼叫、回結果

一輪工具呼叫,分三段:

**1. 你定義工具長什麼樣**——`name` + `description` + `input_schema`(標準 JSON Schema):

```json
{
  "name": "get_stock_price",
  "description": "Get the current stock price for a given ticker symbol.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {"type": "string", "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."}
    },
    "required": ["ticker"]
  }
}
```

**2. 模型決定要呼叫,回一個 `tool_use` content block**:

```json
{"type": "tool_use", "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV", "name": "get_stock_price", "input": {"ticker": "^GSPC"}}
```

**3. 你執行完,把結果包成 `tool_result` 送回去**,靠 `tool_use_id` 對應到剛剛那次呼叫:

```json
{"type": "tool_result", "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV", "content": "259.75 USD"}
```

response 的 `stop_reason` 會是 `"tool_use"`,回應的 `content` 陣列**不保證 `tool_use` block
排在第一個**——官方範例特別提醒:文字說明可能先出現(「我先幫你查一下股價」這種),再接
`tool_use`,所以程式要**掃描整個 content 陣列**去找 `tool_use` block,不能假設它的位置。

## 多輪對話怎麼接——一個 while 迴圈

一次任務裡模型可能連續呼叫好幾次工具,官方範例的核心邏輯就是一個迴圈:只要
`stop_reason === "tool_use"`,就把這輪的 `tool_use` block 全部執行完、包成 `tool_result`
陣列送回去,直到模型不再要求呼叫工具為止:

```typescript
while (response.stop_reason === "tool_use") {
  const toolResults = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      const result = runTool(block.name, block.input);
      toolResults.push({ type: "tool_result", tool_use_id: block.id, content: JSON.stringify(result) });
    }
  }
  messages.push({ role: "assistant", content: response.content });
  messages.push({ role: "user", content: toolResults });
  response = await client.messages.create({ model, max_tokens, tools, messages });
}
```

注意 `assistant` 那輪(模型的回應)跟 `user` 那輪(工具結果)是**兩個獨立的訊息**,不是塞進
同一則——這是 Messages API 本身角色輪替的規則,工具結果永遠是用 `user` 角色送回去的,即使
邏輯上是「系統執行完回報」,不是使用者真的講話。

## 工具執行失敗怎麼辦——`is_error: true`

工具執行出錯不代表整輪對話中斷,把錯誤訊息包進 `content`、加一個 `"is_error": true`,模型
會把這個錯誤納入它接下來的判斷(可能重試、可能換個做法、可能直接告訴使用者失敗了):

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
  "content": "ConnectionError: the weather service API is not available (HTTP 500)",
  "is_error": true
}
```

## `tool_choice`——要不要用工具,你也能插手

預設是 `auto`(模型自己決定要不要用、用哪個),但可以強制:

- `{"type": "any"}`——一定要用某個工具,不限定是哪個
- `{"type": "tool", "name": "get_weather"}`——一定要用這個指定的工具
- `{"type": "none"}`——這輪完全不准用工具

另外有個容易漏掉的旗標 `disable_parallel_tool_use`——預設模型可以一次回傳好幾個 `tool_use`
block(平行呼叫多個工具),設成 `true` 會限制模型**一次最多只能呼叫一個**。

## 跟 Extended Thinking 疊在一起用時,有一個容易踩的坑

如果同時開了 extended thinking,模型的回應會多一個 `thinking` block(帶一個 `signature`)。
**下一輪把 `tool_use` 的結果送回去時,`thinking` block 必須原封不動一起傳回去**,不能只傳
`tool_use` block——官方明講,漏了會直接噴錯:

```typescript
messages: [
  { role: "user", content: "What's the weather in Paris?" },
  // 注意:thinkingBlock 一定要跟 toolUseBlock 一起傳回去,漏了會噴錯
  { role: "assistant", content: [thinkingBlock, toolUseBlock] },
  { role: "user", content: [{ type: "tool_result", tool_use_id: toolUseBlock.id, content: "..." }] }
]
```

這個坑不算顯眼,因為單純只用 tool use(沒開 thinking)時不會遇到,一旦兩個功能疊在一起用才會
突然冒出來。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-03 查證,官方文檔:

- [`agents-and-tools/tool-use/define-tools`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  ——工具定義格式、`tool_choice` 四種模式、`disable_parallel_tool_use`。
- [`agents-and-tools/tool-use/build-a-tool-using-agent`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent)
  ——完整的 `while` 迴圈範例(TypeScript + Bash 兩種語言)、掃描 content 陣列找 `tool_use`
  的提醒。
- [`agents-and-tools/tool-use/handle-tool-calls`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
  ——`is_error: true` 的錯誤處理格式。
- [`build-with-claude/extended-thinking`](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
  ——thinking block 必須跟 tool_use block 一起傳回去的規則(Java/TypeScript 範例)。
- [`api/messages`](https://platform.claude.com/docs/en/api/messages)
  ——Messages API 的角色輪替規則(工具結果用 `user` 角色送回)。
