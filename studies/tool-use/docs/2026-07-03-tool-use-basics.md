---
date: 2026-07-03
tags:
  - tool-use
  - basics
  - overview
---

# Tool Use 是什麼,又是怎麼運作的

官方一句話定義:「When Claude needs to use a tool, it will output a structured JSON object
specifying the tool to use and its arguments. The tool's output is then returned to Claude in a
structured format for further processing.」——重點是**結構化**:模型不是用一段文字暗示它想做
什麼,是吐出一個格式保證正確、可以直接被程式執行的物件。

## 沒有這個機制之前,LLM 怎麼「假裝」能做事

打個比方:一個關在房間裡的聰明人,只能從門縫遞紙條出來。他想叫外面的人幫他查股價,只能在紙條上
寫「幫我查一下蘋果的股價」——寫法每次可能不一樣(有時寫代號 AAPL,有時寫「蘋果公司」,有時
順便問了兩件事),房間外的人得**自己讀懂**這張紙條、猜他到底要什麼欄位、用什麼格式回覆。這件事
交給人做沒問題,交給程式做就很脆弱——程式沒辦法「讀懂」自然語言裡藏的意圖,只能用正規表達式去
賭格式長什麼樣。

Tool use 做的事,是把這張手寫紙條換成**一張固定欄位的表單**:房間裡的人只能填表單(工具名稱 +
參數),不能自己亂寫格式;房間外的人收到表單,直接照欄位執行,結果也用固定格式的表單送回去。
表單保證看得懂,不用再猜。

## 核心概念:agent 的「推理—行動」迴圈,tool use 補的是「行動」那一格

一個 agent 本質上是**在推理(reasoning)和行動(acting)之間反覆橫跳**的迴圈:看情況 → 想一下
要做什麼 → 真的去做 → 看結果 → 再想一下……重複到任務完成。這個迴圈本身不是新概念,新的是
「行動」這一步怎麼被可靠地做出來。

沒有 tool use 的世界,「行動」這一步只能靠模型在自由文字裡暗示意圖(例如自己約定一種格式:
「Thought: 使用者想查天氣。Action: get_weather(city="Paris")」),再靠外部程式碼用字串解析去
猜這段文字裡藏的到底是不是一個「動作」、動作是什麼、參數是什麼。格式漂移、參數亂填、意圖模糊
(模型只是在「討論」要不要打這通 API,還是真的要打)都是常態——這正是 tool use 正式上線前那個
「土法煉鋼時代」的真實樣貌,詳細時間軸見 `tool-use-origins.md`。

Tool use 把「行動」這一步從「自由文字 + 外部猜測」換成「模型原生吐出一個 schema 驗證過的決策
物件,外部直接執行」——迴圈本身沒變,只是「行動」這一格從不可靠變成可靠。這正是下面那個
`while (response.stop_reason === "tool_use")` 迴圈能夠穩定跑下去的原因:每一輪「行動」都是一個
保證格式正確的物件,不是要賭運氣的自由文字。

## 跟 structured output 的關係(概念上,不是時間先後)

Structured output 泛指「讓模型輸出符合某個 schema 的格式」這個技術本身——用途可以是**回答
使用者**(例如叫模型用固定 JSON 格式回一份履歷摘要)。Function calling / tool use 是這個技術
的一種**特定用法**:輸出的結構化物件不是拿來回答使用者的,是拿來**觸發外部系統執行一個動作**的
——多了一層「這是一個決策,不是一個答案」的語意。

這裡刻意只講**概念上**的關係(A 是 B 的一種特定用法),不牽涉「誰先誰後上線」——上線時間先後
反而跟直覺相反(是先有 function calling,14 個月後才長出通用的 structured output),這是一個
獨立的歷史事實,寫在 `tool-use-origins.md` 裡,這篇不重複。

## Anthropic 自己也有一個獨立的 Structured Outputs 功能

上面講的是「structured output」這個概念,這裡講的是 Anthropic 真的做出來的那個功能——兩件事
容易搞混,先講清楚差在哪:

- **`output_config`**——這個是新的。用途是回答使用者,讓 Claude 的一般文字回應直接符合你指定
  的 JSON Schema,不用再自己解析文字。
- **工具呼叫的 `input_schema`**——這個是舊的,`tool-use-basics.md` 前面一路都在講這個。用途
  是觸發工具,格式是 Claude 決定要呼叫工具時,參數要長成什麼樣。

兩者用的是**同一套底層技術**(schema 驗證生成的內容),差別只在「這段輸出是要給誰看」——回答
使用者用前者,觸發工具用後者。

**用法長這樣**(注意欄位名稱是 `output_config`,不是 `tools`):

```yaml
output_config:
  format:
    type: json_schema
    schema:
      type: object
      properties:
        name: {type: string}
        email: {type: string}
      required: [name, email]
      additionalProperties: false
```

**目前只支援一種格式:`json_schema`。** 查遍官方文檔,`format.type` 這個欄位沒有第二個選項
——沒有 XML、沒有 YAML、也沒有其他自訂格式。

**還有兩個容易漏掉的地方**:

1. **不是所有模型都支援這個功能。** 用不支援的模型時,Anthropic 不會報錯——schema 會被**直接
   忽略**,回應照樣送出去,只是不會被結構化。你得自己確認模型有沒有支援,不能靠錯誤訊息提醒你。
2. **可以跟工具呼叫的 `strict: true` 一起用。** 在工具定義裡加 `strict: true`,可以讓工具
   呼叫的參數也套用同一套「完全保證符合 schema」的保證——這樣一次 API 呼叫裡,一般回答跟工具
   參數兩邊都能拿到格式保證。

## 什麼時候該用工具,什麼時候不該

官方對這件事有明確判準:「Tools are best for structured data retrieval, performing
calculations, or interacting with external systems. Prose is more suitable for creative
writing, summarization, or general conversation where direct tool interaction is not
required.」——換句話說,不是所有任務都該塞進 tool use,自由文字在很多場景(創意寫作、摘要、
一般對話)反而是更自然、成本更低的做法。

## 機制細節:一輪工具呼叫,分三段

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

## 這篇跟同主題其他文件的分工

- **這篇**——tool use 是什麼、為什麼需要它、跟 structured output 的概念關係,以及 API 層面的
  機制細節(工具定義、`tool_use`/`tool_result`、多輪迴圈、`tool_choice`)。
- [`tool-use-origins`](2026-07-03-tool-use-origins.md)——這個機制的歷史:學術先驅期、三家
  廠商官方上線時間對照、structured output 實際上線順序的反轉。
- [`advanced-tool-use`](2026-07-03-advanced-tool-use.md)——基礎機制不夠用時的三個 beta 功能。

## 出處

全部經 [context7](https://context7.com) 於 2026-07-03 查證,官方文檔:

- [`agents-and-tools/tool-use/tool-search-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
  ——「structured JSON object」這句核心定義的原句出處。
- [`agents-and-tools/tool-use/how-tool-use-works`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
  ——「When to use tools (and when not to)」判準原句。
- [`agents-and-tools/tool-use/define-tools`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  ——工具定義格式、`tool_choice` 四種模式、`disable_parallel_tool_use`。
- [`agents-and-tools/tool-use/build-a-tool-using-agent`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent)
  ——agentic loop 的官方描述、完整的 `while` 迴圈範例(TypeScript + Bash 兩種語言)、掃描
  content 陣列找 `tool_use` 的提醒。
- [`agents-and-tools/tool-use/handle-tool-calls`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
  ——`is_error: true` 的錯誤處理格式。
- [`build-with-claude/extended-thinking`](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
  ——thinking block 必須跟 tool_use block 一起傳回去的規則(Java/TypeScript 範例)。
- [`api/messages`](https://platform.claude.com/docs/en/api/messages)
  ——Messages API 的角色輪替規則(工具結果用 `user` 角色送回)。
- [`build-with-claude/structured-outputs`](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  ——`output_config.format.type: json_schema` 的用法、目前只支援這一種格式、不是所有模型都
  支援(不支援時 schema 被靜默忽略,不報錯)、跟工具呼叫 `strict: true` 可以一起用。

**誠實聲明**:「關在房間遞紙條 / 填表單」的比喻跟「行動這一格從不可靠變可靠」的敘事框架是這篇
筆記自己的推導,不是官方原句——官方只講機制本身,沒有用這套比喻描述「為什麼這個機制重要」。
