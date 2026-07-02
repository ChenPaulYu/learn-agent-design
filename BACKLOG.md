# Backlog

Living list of candidate topics — things worth studying next, not yet started. Not a history
log (git log / the docs themselves are that); this only tracks what's still open. Pull an item
out (and delete its line here) once its own topic/note exists.

## `mcp`

- **生態現況** — MCP 有沒有真的解決 M×N 問題,還是又長出新的 registry/分發問題;OpenAI 後來
  跟進採用這件事本身說明了什麼。查證方式跟其他 MCP 筆記不同——要查部落格/新聞/採用公告,不是
  規格文件。
- **多 server 疊加(Gateway 架構)** — 一個 MCP server 自己可不可以當另一個 server 的
  client(proxy/aggregate 多個下游 server)。跟安全模型那篇的 Confused Deputy 有重疊(那篇談
  的就是「MCP server 當代理」的情境),這篇是從架構模式角度重新看,不是安全視角。MCP 規格本身
  沒定義這個模式,查證對象是社群實作範例。

## 還沒開的新主題(候選)

- **advanced-tool-use** — Claude Developer Platform 自己的三個 beta 功能:Tool Search Tool
  (`defer_loading`,最多省 95% context)、Programmatic Tool Calling(`allowed_callers`,官方
  實例把一個任務從 43,588 token 壓到 27,297)、Tool Use Examples(`input_examples`,跟省
  context 無關,解的是參數填錯的準確度問題)。跟 mcp 的太多工具問題是「同一個模式,Claude API
  做成產品」的關係,但這是 API 能力不是 MCP 協定,不屬於 mcp 這個主題——獨立開一個新主題,還沒
  真的動筆。查證來源已知:`anthropic.com/engineering/advanced-tool-use`。
- **Claude Agent Skills** — 三層載入設計(metadata 永遠在、指令觸發才載入)跟上面 Tool
  Search Tool 是同一個 progressive disclosure 原理、不同粒度,值得展開講 Skills 自己的完整
  設計(怎麼寫一個 skill、跟 slash command/subagent 的邊界)。
