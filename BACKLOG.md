# Backlog

Living list of candidate topics — things worth studying next, not yet started. Not a history
log (git log / the docs themselves are that); this only tracks what's still open. Pull an item
out (and delete its line here) once its own topic/note exists.

## 還沒開的新主題(候選)

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

- **LLM → Agent 的橋接** —— `llm-foundations` 目前範圍只做「LLM 原理」本身(next-token
  prediction、in-context learning),刻意沒做「LLM 怎麼被組裝、包裝成一個 Agent」這段橋接。
  等 `llm-foundations` 的 LLM 原理部分做得夠完整,再回頭決定這段橋接要併進同一個主題,還是
  獨立開新主題——不要因為問題本來是連著問的就預設答案是「同一個主題」。

## 歸屬待重新檢視(不是候選主題,是既有內容的範圍疑慮)

- **`agent-skills-advanced-applications.md` 的兩塊,可能根本不屬於 Skills** ——
  self-evolving(CODESKILL)問的其實是「agent 怎麼從經驗裡自己學習」,更接近
  `agent-anatomy` 的 Runtime state/記憶層,只是這批論文剛好挑 skill 當載體;
  modular/hierarchical(AgentSkillOS、Graph-of-Skills)問的是「一大堆能力/知識怎麼組織、
  怎麼檢索」,根本跟 `mcp-tool-scaling-problem.md` 的 Progressive Tool Discovery 是同一個
  問題,只是多加了依賴關係這個維度。現在份量都還不到能獨立開主題(各自才 1-3 篇論文撐著),
  先留在 `agent-skills` 底下沒問題——但等哪天真的要擴充其中一塊,**先重新想一次歸屬,不要
  預設就是留在 Skills 底下**,免得因為「論文剛好研究的是 skill」就把一個更廣的問題釘死在
  一個過窄的主題裡,犯了跟「因為方便就照來源分類」一樣的錯,只是方向相反。
