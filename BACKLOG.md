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
  `code.claude.com/docs/en/sub-agents`、`code.claude.com/docs/en/hooks`。額外參考(使用者提供,
  還沒查證內容品質):[hardness1020/awesome-agent-architecture](https://github.com/hardness1020/awesome-agent-architecture)
  ——本質上是在整理 Claude Code 的架構,開這篇時可以拿來對照,但要自己驗證內容,不要照單全收。
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

- **Advanced LLM 現在到底怎麼訓練?有什麼新招?** —— `llm-foundations` 現有的機制篇(BPE、
  位置編碼、weight tying、cross-entropy/teacher forcing、decoding strategies、scaling laws、
  SFT/RLHF/DPO)講的都是相對成熟、定案的做法,還沒碰「這一兩年前沿模型實際在用的新招」這塊。
  候選角度(先列下來,還沒查證,開這篇時要重新確認每個角度是不是還是最新):
  - DeepSeek 這類模型對 attention/residual 機制的重新設計(例如壓縮 KV cache 的做法)
  - 更省的 attention 機制(FlashAttention、分組查詢注意力 GQA、滑動視窗這類)
  - Speculative decoding(小模型先猜、大模型驗證,加速生成)
  - 現代 optimizer 是不是還是 Adam 系,有沒有新的替代方案開始普及
  - Pretrain/post-train 是不是已經收斂出新的固定範式,還是每家仍各自摸索
  範圍待決定:併進 `llm-foundations` 當更深一層的 Level(前面已經打過折扣過「機制篇/替代方案篇」
  都是相對穩定的知識),還是獨立開一個「前沿/currently-changing」性質的新主題,因為這塊的
  查證有效期會比其他機制篇短很多,可能需要不同的「誠實聲明」寫法(標明查證日期、預期會過時)。

- **Coding Agent 這個範式本身(Claude Code / Codex / Cursor 跨系統比較)** —— 這幾個系統已經
  收斂出一種可以辨認的「範式」,不是各自獨立的產品特性。**跟上面「Claude Code 的客製化介面」
  那個候選不同**——那個是深挖 Claude Code 一家的內部機制(Subagent/Hook/Plugin/Workflow),
  這個是問「跨這幾個系統看,coding agent 這個類別共同長成的樣子是什麼」,層級不一樣,不要因為
  都跟 Claude Code 有關就合併成一篇。候選角度:
  - 共同的骨架:agentic loop + tool use(讀寫檔案、跑 bash、搜尋程式碼)+ 怎麼管理大型
    codebase 的 context(全塞進 context vs 檢索式 vs 摘要式)
  - 怎麼驗證自己做對了(跑測試、type check、linter,這些回饋怎麼被塞回迴圈)
  - 各家實際做法的差異(Cursor 偏 IDE 內嵌 + 行內 diff、Claude Code 偏 CLI + 明確的 agentic
    loop、Codex 偏雲端/自主執行)——這些差異背後是同一個範式的不同取捨,還是根本不同的設計哲學
  - 是不是已經有業界公認的「coding agent 架構」名詞或論文,類似 ReAct 之於 tool use 的地位

- **Computer use** —— 模型直接看螢幕截圖、操作滑鼠鍵盤,跟 `tool-use` 主題現有的「結構化 API
  呼叫」是不同的介面風格(同一層——Tool——的不同做法,不是全新的一層)。**注意跟 `tool-use-origins.md`
  的關聯**:WebGPT(微調 GPT-3 操作固定指令集的瀏覽器)已經是這條線最早的前身之一,開這篇時要
  先確認是要併進 `tool-use` 當一個新的子篇,還是份量夠大獨立開主題——不要預設答案。候選角度:
  - 模型怎麼「看」螢幕(截圖 + 視覺定位座標)、怎麼決定要點哪裡
  - 實際的工具schema長什麼樣(screenshot/click/type/scroll/key 這類動作原語)
  - 跟結構化 tool use 的介面風格對比:一個是明確 schema 的 API 呼叫,一個是像素座標層級的操作
  - 這種介面特有的風險(動作不可逆、沒有 undo、出錯的代價可能是真實世界的操作)
  - 跟這個 repo 自己在用的 `agent-browser`(瀏覽器驗證 agent 用的工具)是不是同一類機制,還是
    網頁自動化跟通用電腦操作根本是兩回事

- **Personal agent(例如 OpenClaw、Hermes 這類)** —— 跟上面「coding agent 範式」「computer
  use」都不同層級:這個問的是「服務個人、跨多種日常任務」這種 agent 的設計,不是特定領域
  (寫程式)或特定介面(操作電腦)。這兩個名字(OpenClaw、Hermes)是使用者當下提到的例子,
  開這篇之前要先查證這兩個具體是什麼、現在還活不活躍,不能預設。候選角度:
  - Personal agent 跟 coding agent 的差異到底是什麼:是「領域窄 vs 領域廣」,還是「單次任務
    vs 長期記憶/個人化」這種更根本的軸
  - 長期記憶/個人偏好怎麼被保存跟利用(這跟 `agent-anatomy` 的 Runtime state 概念直接相關)
  - 自主程度:被動等指令,還是主動幫使用者做決定/採取行動
  - 現在是不是已經有一個公認的「personal agent」架構範式,還是各家做法差異很大,仍在摸索期

- **怎麼 evaluate / 測試 agent 的能力(evaluation、benchmark 都算)** —— 上面幾個候選主題都在問
  「agent 怎麼設計」,這個問的是「怎麼知道一個 agent 做得好不好」,是完全不同的問題。**已經有一個
  相關的具體案例**:`tool-use-origins.md` 提過 BFCL(Berkeley Function-Calling Leaderboard),
  只評測「工具呼叫」這一個窄能力——這篇如果要開,範圍要擴大到「評測 agent 整體表現」,不是只評測
  單一能力。候選角度:
  - 評測 agent 為什麼比評測單次 LLM 輸出難:多步驟軌跡、要跟環境互動、環境本身可能不確定/會變
  - 現有的具體 benchmark:SWE-bench(coding)、WebArena/OSWorld(computer use)、GAIA(通用助理
    任務)、BFCL(工具呼叫,已查證過)——這些各自在測什麼、彼此覆蓋得到的範圍有沒有重疊或空隙
  - 評測方法論:LLM-as-judge、人工評測、自動化成功條件判定,各自的可信度跟成本
  - 已知的問題:benchmark 污染(訓練資料混進測試題)、針對 benchmark 過度優化、大規模跑 agent
    評測的成本、跟真實環境互動時的可重現性問題

- **Prompt optimization / self-evolving agent,以及 agent 架構的 modular primitive 化** ——
  使用者提出時就注意到這可能是兩個 facet,不一定是同一個主題,**開這篇時要重新確認要不要分開,
  不要預設**:
  - Facet A(靠回饋迭代變好):Reflection/Reflexion、TextGrad(用文字當「梯度」反向傳播去優化
    prompt)、這類「feedback descent」風格的技巧——問的是「agent 怎麼靠回饋自己變強」
  - Facet B(架構模組化):DSPy(把 prompt 當可優化參數、LLM 呼叫當可組合模組,類似 PyTorch
    layer 的設計)、LangGraph(圖狀態機式的多步驟編排)——問的是「agent 怎麼被拆成可重用的積木
    來建構」
  - **DSPy 剛好橫跨兩個 facet**(模組化設計 + 自動 prompt 優化是同一套系統的兩面)——這可能
    代表兩個 facet 其實是同一件事的兩個切面,也可能只是巧合,不要預設答案。
  - **注意跟既有內容重疊,開這篇前要先讀過**:`agent-anatomy` 的
    `computation-model-first-principles.md` 已經把 Reflexion 式迭代修正列為一種 Computation
    Model 政策,`five-layer-framework.md`/`human-analogy-elicit.md` 也提過 LangGraph 當
    Computation Model vs Runtime 的實作對照——確認新內容補的是「沒講過的東西」,不是重講一次。

- **Agent 的 Memory design** —— **跟上面「Personal agent」那個候選重疊**(裡面已經列了「長期
  記憶/個人偏好怎麼被保存跟利用」當候選角度),開任一篇之前要先確認這兩個要合併還是分開。
  **跟 RAG 的關係已經討論過,結論是分開,但 Memory 依賴 RAG**——檢索只是 Memory 要解決的其中
  一個子問題,RAG 剛好是專門解這個子問題的技術,但 RAG 自己的地盤(查文件、查網頁、查
  codebase)比「幫 Memory 做檢索」大得多;Memory 除了檢索,還要處理寫入/整理壓縮/遺忘這幾塊
  RAG 完全不碰的東西。合併會讓 RAG 被窄化、或讓 Memory 真正核心的部分被稀釋——兩篇獨立開,
  但 Memory 那篇該直接引用 RAG 那篇的檢索機制,不要重新推導一次。
  **也跟既有內容重疊,開這篇前要先讀過**:`agent-anatomy` 的 `orthogonal-analysis.md` /
  `runtime-first-principles.md` 已經把 memory 定位成 Runtime state 的一種(「(A) 記憶型」,
  跟只給內部記帳用的「(B) 機制型」對照),並點名 Generative Agents、MemGPT 當案例——但只停在
  「這是 Runtime state 的一種」這個第一原理層級,沒有深入這些系統實際怎麼設計 memory。候選角度:
  - 具體的記憶架構:短期/工作記憶 vs 長期記憶、情節記憶(episodic)vs 語意記憶(semantic)
  - 檢索式(向量資料庫)vs 結構化儲存,各自的取捨
  - 記憶怎麼被寫入、整理/壓縮(consolidation)、遺忘——不是只有「存」跟「查」兩個動作
  - 具體系統案例:MemGPT、Generative Agents 的 reflection + retrieval、其他近期的 memory 框架

- **把 `agent-anatomy` 完整化** —— 這幾輪開的其他主題,事後看其實都在幫 `agent-anatomy` 的
  某一層打地基:`tool-use` 整個就是在深挖 Tool 這一層,`llm-foundations` 是在補 Pattern 層
  背後「LLM 為什麼知道怎麼接」這個前提知識——但 `agent-anatomy` 自己現在還停在第一原理層級的
  骨架,沒有跟著這些深挖回頭補完。候選角度(哪幾層目前最薄,開這篇前要重新確認,不要預設):
  - Pattern 層目前只有「認知原語 + 局部文法」這個定義,沒有具體案例集或分類法
  - Environment 層目前份量最少,只有「資源清單 + 觀測/行動限制 + 世界動態」三個名詞,沒有深入
  - 上面新加的幾個候選(Memory 屬於 Runtime 的具體深化、Computer use/Personal agent 是 Tool
    或 Environment 的具體案例)完成後,要不要回頭補進 `agent-anatomy` 對應的層,還是讓
    `agent-anatomy` 保持通用框架、細節都留在各自主題裡——這是範圍決定,不要預設答案。

- **RAG(完整版本,範圍要廣,不要只窄化成一個對比)—— 跟 Memory design 要不要合併待定** ——
  一開始想窄化成「傳統向量 RAG vs 檔案系統式迭代檢索」這一個對比,但那只是候選角度之一,完整的
  RAG 地圖至少要包含:
  - 核心管線本身:切塊策略、embedding 模型怎麼選、檢索方式(dense/向量 vs sparse/BM25 vs
    混合)、重排序(re-ranking)、檢索結果怎麼餵進生成的 prompt
  - 近幾年的進階做法:GraphRAG(先建知識圖譜再檢索,不只靠向量相似度)、Self-RAG/CRAG(模型
    自己判斷要不要檢索、檢索到的東西夠不夠用)、HyDE(先生成一個假設性答案再拿去搜,不是直接
    拿問題搜)
  - Agentic/迭代式檢索(邊搜邊想,查一次不夠就換個關鍵字再查,`file system is all you need`
    這個方向屬於這裡)vs 一次性 embedding 檢索——這是完整地圖裡的一塊,不是全部
  - RAG vs 長 context(乾脆全塞)vs fine-tuning(把知識直接練進權重)——三種「怎麼把外部知識
    餵給模型」的手段各自的取捨,這條線直接連回 `llm-foundations` 的 `post-training-sft-rlhf.md`
  - RAG 本身怎麼評測(RAGAS 這類框架,測檢索品質 + 生成內容忠實度兩件事)
  使用者提到一個叫 **OKF(Google)** 的東西,名稱本身還沒查證,不確定具體所指,開這篇時要先查
  清楚再引用,不要憑印象寫。
  **跟 Memory design 的關係,結論是分開,Memory 依賴 RAG**(討論見上面「Agent 的 Memory
  design」那條)——RAG 自己的地盤(查文件、查網頁、查 codebase)比「幫 Memory 做檢索」大得多,
  合併會窄化 RAG、或稀釋 Memory 真正核心(寫入/整理/遺忘)的部分。兩篇獨立開,Memory 那篇直接
  引用這篇的檢索機制,不重新推導。

- **Multi-agent 協作/編排** —— 這個其實已經被這個 repo 自己標記過是個洞:`agent-anatomy` 的
  `computation-model-first-principles.md` 明講「Multi-Agent 根本不屬於 Computation Model
  這一層,是單位不對」(它是好幾個各自完整的 agent 怎麼組合,不是一個決策者怎麼探索候選延續),
  `mcp` 的文件也提過 A2A(Agent-to-Agent)協定當邊界對照——但「好幾個各自完整的 agent 怎麼
  組合」這個問題本身,從來沒有被真正展開過。候選角度:
  - Orchestrator-worker(一個主管派工)vs 對等協商(沒有主管,agent 之間互相溝通決定)
  - Agent 之間怎麼溝通:共享同一份 context,還是各自獨立、靠訊息傳遞交換資訊
  - 辯論/共識機制:多個 agent 各自產生答案,怎麼收斂成一個最終決定
  - 跟上面「Prompt optimization / modular primitive」候選裡的 LangGraph 有沒有重疊(LangGraph
    的多節點編排,有一部分可能就是在做 multi-agent 這件事)——開這篇前要先確認分工

- **Long-horizon agent / context 生命週期管理** —— 跟「Memory design」不一樣:Memory 是跨
  session 的長期知識怎麼存,這個是**單一個長任務進行中**,當下的 context window 該放什麼、
  怎麼精簡——這條線 2026 上半年查到具體、可查證的研究成果,不是空泛的方向:
  - **35 分鐘退化問題**:任務時長超過約 35 分鐘(以人類完成同等任務的時間換算),agent 成功率
    開始下滑,而且任務時長翻倍,**失敗率是四倍**而不是兩倍——LIKELY(來自 EPAM 的工程分析,
    未查到原始論文,開這篇時要重新確認有沒有更硬的出處)。
  - 具體技術方向(2026 上半年 arXiv 論文,查得到連結,開篇時要重新驗證):Context Window
    Lifecycle(CWL,依類型/依賴關係做漸進式淘汰,不是單純砍舊的)、
    [Beyond Compaction: Structured Context Eviction for Long-Horizon Agents](https://arxiv.org/pdf/2606.11213)、
    MAGMA(多重圖譜記憶架構,用語意/時間等多個正交圖譜各自代表一個記憶項目)
  - 候選角度:摘要/壓縮策略、什麼時候該把工作丟給 subagent 保護主線 context、檢索式 vs 全塞
    進 context 的取捨、「強規格勝過模糊目標」這類工程原則(目標含糊的 agent drift 得更快)
  - 這個議題現在業界討論得很熱,而且這個 repo 自己每天用 Claude Code 就在經歷這件事——開篇時
    可以拿這個 repo 自己的實際使用經驗當案例

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
