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

## `advanced-tool-use`

- **Tool Search Tool 的三種實作對照** — regex / BM25 / custom,各自適合什麼場景,目前筆記只
  提過名字沒展開。

## 還沒開主題的候選

- **Claude Agent Skills 獨立成一篇** — 目前只在 advanced-tool-use 筆記裡當「同一個
  progressive disclosure 原理,不同粒度」的對照提了一句,沒有展開講 Skills 自己的完整設計
  (三層載入、怎麼寫一個 skill、跟 slash command/subagent 的邊界)。
