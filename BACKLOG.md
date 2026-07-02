# Backlog

Living list of candidate topics — things worth studying next, not yet started. Not a history
log (git log / the docs themselves are that); this only tracks what's still open. Pull an item
out (and delete its line here) once its own topic/note exists.

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
