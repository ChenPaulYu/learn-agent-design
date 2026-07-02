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
  真的動筆。跟 `agent-skills`(已開)共享同一個 progressive disclosure 原理、不同粒度,寫的
  時候可以互相連結,但不用合併成同一個主題。查證來源已知:
  `anthropic.com/engineering/advanced-tool-use`。
- **Claude Code 的客製化介面** — Subagent(2025-07)、Hook(2025-09)、Plugin(2025-10)、
  Workflow(含自行調節步調的 dynamic 模式)——跟 `agent-skills` 查證時發現這幾個刻意設計成
  互斥、佔據不同判斷軸(主線程可見 vs context 隔離 vs 不看 LLM 判斷的固定觸發 vs 多 agent
  怎麼編排),不同源,不是同一套機制的變體。份量夠大,值得單獨開一個主題,不要因為都跟 Skills
  同期出現就順手塞進 `agent-skills` 底下。官方來源已知:`claude.com/blog/steering-claude-code-...`、
  `code.claude.com/docs/en/sub-agents`、`code.claude.com/docs/en/hooks`。
  **開這篇時可以借用的比喻(已經在 `agent-skills-overview.md` 用過,效果不錯)**:把整個
  Claude Code 想成一個劇組——Workflow 是導演的分鏡腳本(決定誰先上場、要拍幾輪);Subagent
  是個別演員(丟去單獨拍一段,只回結果);Skill 是演員自己帶的劇本小抄(需要程序知識時翻);
  Hook 是片場固定規矩(觸發了就一定發生,不看導演當下怎麼想)。MCP 不屬於這個比喻的同一層——
  它是劇組跟外面廠商借道具的窗口,回答的是「碰外部世界」,不是「內部怎麼組織」,是垂直的
  另一個維度。
