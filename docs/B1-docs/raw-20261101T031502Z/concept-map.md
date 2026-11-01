# Super-agent 概念 → Freely 对应物全量对照

本文是 `brainstorms.md` 的附录，回答一个容易漏掉的问题：**Super-agent 提到的每一个面，在 Freely 里叫什么；如果没有，缺的是什么。**

对照原则：

- “等价”指解决同一个问题，不要求实现相同。
- “部分”指 Freely 有相近能力，但语义/粒度/时机不同。
- “缺口”指 Freely 当前没有对应机制，或只有提示词约定、没有代码落点。
- 同名不同义的词单独标出，避免把 `Worker`、`Session`、`Thread` 直接画等号。

## 1. 输入与事件

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Source | 一类事件流的可复用实现 + 一个实例配置 | platform adapter（GitHub/Gitee）、issue-sync、scan source、chat intake | 部分 | Freely 的“来源”分散在 adapter、scan、intake 三处，没有统一的 Source kind 协议 |
| Trigger | 一条不可变外部事件，带 actor 与来源元数据 | raw issue、chat intake、platform comment、scan item、human interruption | 部分 | Freely 没有“一条不可变 Trigger”的统一对象；同一件事可能在 scan 与 intake 各有一份 |
| Thread | 同一话题下按时间排列的 Trigger 集合 | raw issue 目录、PR/Issue 对话、session 延续、工位分支线 | 部分 | Freely 没有跨平台的 Thread 聚合；issue、PR、chat 是三条线 |
| Correlation | 多个 Thread 共享同一 Trigger 的关联，只加上下文不改路由 | scan 的 `cross_refs`、raw→C→M→I 链、PR/issue 链接 | 部分 | Freely 的关联是文档字段与人工维护，不是运行时对象 |
| Channel | Thread 的写侧：评论、回复、评审线程 | platform-adapter（GitHub/Gitee 评论/PR）、chat/discuss、CLI 输出 | 部分 | 没有统一 Channel 抽象；写侧能力由 adapter 与命令各自实现 |
| Disposition | 一条 Trigger 被过滤/评估/扇出的记录 | scan `stage`、`phase_state`、milestone 状态、review verdict、日志 | 部分 | 没有 per-trigger 账本；同一事件的处理结果散在文档与日志 |
| Input | 送给 Ticket 的上下文：扇出的 Trigger、Policy 变更、resume、文本 | scan JSON、A2A 状态、continuation handoff、docs、Manager 指令 | 部分 | 没有类型化 Input；上下文是拼接进 prompt 的文本 |
| Event / notice | 领域事件与给主 Session 的通知 | runtime 事件日志、SSE、issue-sync 通知、watchdog 信号 | 部分 | 没有统一的领域事件总线与去重 key |

## 2. 授权与准入

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Policy | 版本化的准入规则 + 每个 Source 的白名单/机器人列表 | `CONSTITUTION.md`、`LAWS.md`、skills、gates、agent 角色定义 | 部分 | Freely 的规则是文档 + 代码门禁，没有运行时 Policy 版本对象 |
| Policy version | 一组规则/模式/Source 部分的标识，Mandate 记录它 | git commit、skill 版本、门禁版本 | 部分 | 没有“这次工作依据哪版规则批准”的结构化记录 |
| Gate | 确定性第一层：谁可以发起、什么强度 | 平台 issue 检查、branch/worktree 检查、IBM doc gate、pretests gate、pr gates、hooks | 等价（不同层） | Freely 的 gate 面向“流程阶段”，不是“单条事件准入” |
| Admission table | 按接收范围/发送者/是否点名决定 explicit/inferred/ignore | 无直接对应；由 Manager 判断 + 平台入口 | 缺口 | Freely 没有 per-message 的准入矩阵 |
| Bot list | 允许产生 inferred candidate 的机器人 | 无直接对应；外部 bot 评论作为数据 | 缺口 | Freely 没有“哪些 bot 可以触发工作”的配置 |
| accept mode（off/observe/auto） | 控制推断候选是否真的开工 | `task_mode`（wait/listen/auto） | 只同名不同义 | `task_mode` 控 runtime 是否巡逻/启动 AI，不控单条候选的授权强度 |
| Eval | 对一批 Trigger 的判断：gate + assessment | scan 阶段推导 + Manager 判断 + B1 brainstorm | 部分 | Freely 没有单一 Eval 对象；判断分散在 scan、Manager、B1 |
| Assessment | 模型对候选的语义判断（是否实现请求、规则匹配） | Manager 路由判断、B1 brainstorm、Reviewer verdict | 部分 | 没有结构化 assessment 输出与规则逐条判定 |
| Decision | accept/stop/ignore/unavailable | candidate 状态（promoted/absorbed/dropped）、review verdict、merge/close | 部分 | Freely 的 Decision 是流程动作，不是单条事件的结论对象 |
| Strength（explicit/inferred） | 这次请求的证据强度 | issue `kind`/`severity`、人工审批、review verdict | 缺口 | 没有“明确请求 vs 推断请求”的强度字段 |
| Mandate | 不可变授权凭证：范围、强度、规则、发送者、Policy 版本 | raw issue + candidate + worktree 所有权 + 分支保护 + 人工 approval | 部分 | 没有 per-work-item 的不可变凭证；授权依据散落 |
| Revalidation | 复活已结束 Ticket 前按当前 Policy 重校验 | 重新走 gate、review、merge | 部分 | 没有“原授权是否仍成立”的显式检查 |
| Person / identity | 人不是领域对象；身份随 Source | 平台账号、agent 身份、项目/工位身份 | 部分 | Freely 没有跨平台身份映射，也没有“人”的统一对象 |

## 3. 工作单元与执行

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Ticket | 一个被授权的工作单元 | raw issue → I-* issue + worktree lane | 部分 | Freely 的“工单”由 issue 文档 + 工位 + A2A task 三者共同表达 |
| Assignment | Ticket 与一个 Executor 实例的绑定 | A2A task、`agent_working` 绑定、worker session | 部分 | 没有明确的 Assignment 对象；绑定散在 DB 与工位 |
| Executor | 执行 Assignment 的端口：一个 Session + 一个目录 | AI CLI/ACP session（Claude/Codex/OpenCode/Cline） | 部分 | Freely 的 executor 是外部进程，不是内部端口；能力差异靠 adapter |
| Execution environment | 执行会话与 prepare 命令共享的变量/目录 | worktree + `.freely` 配置 + `sync-tooling` + env | 部分 | 没有类型化变量注册表；环境由脚本拼 |
| Worker slots | 并发执行槽位；人消息可多占一个 | worker pool、`agent_next_free`、worktree 容量 | 部分 | 没有“人优先”的额外槽位语义 |
| Prepare command | 首个 Assignment 前准备 Ticket 目录 | `wt-create` + `sync-tooling` + test-pre-merge 初始化 | 等价（不同阶段） | Freely 的 prepare 是命令封装，不是 Ticket 生命周期钩子 |
| Background work | 前台命令转后台，最多 30 分钟；subagent 可继续 | AI CLI 自身后台 job、watchdog、continuation | 部分 | 没有统一的 30 分钟上限与“交回给人时保留 shell job”语义 |
| Restart recovery | 重启后 Assignment 带恢复提示，先核对再重做 | continuation handoff、session resume、watchdog 重启 | 部分 | Freely 的恢复更偏“续接会话”，不是“恢复提示 + 幂等外部动作” |
| Auto-merge | 满足条件时由另一个账号开自动合并 | `pr-merge-guarded` | 等价（不同实现） | Freely 的门禁合并更重，但没有“200 行阈值”这类策略 |

## 4. 交接与人机

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Report | Assignment 向 Ticket 报告状态 | `a2a-exit --state` + summary + evidence、progress 文档、review verdict | 部分 | A2A 有状态，但没有 `ready/blocked/failed` 这类类型化报告字段 |
| Ticket stage | 由报告/输入推导“现在等谁” | scan stage + `phase_state`（B1_proposed…B2_verifying/completed） | 部分 | Freely 的阶段是生命周期阶段，不是“等人/等触发”的执行阶段 |
| Attention | 一个待人工回答的问题，路由回提问会话 | `input-required`、scan `needs_human`、chat/discuss、Manager 汇报 | 部分 | 没有结构化“问题 + 目标会话 + 所需动作”字段 |
| human_action | Worker 报告里的结构化提问字段 | `input-required` 的 `reason` + completion_summary | 缺口 | 人的问题混在 summary 里，容易丢 |
| followupOwners | 哪些 Ticket 仍拥有一条人 follow-up | 无直接对应；Manager 判断归属 | 缺口 | 后续消息归属靠人/Manager 记忆 |
| Subscription | Ticket 与 Thread 的多对多订阅 | A2A task SSE 订阅；平台线程无订阅 | 缺口（平台线程） | Freely 的 SSE 订阅对象是 task，不是 PR/Issue 对话 |
| Context-only subscription | 只给上下文、不授权、不复活 | Worker/Reviewer 读相关文档 | 缺口（运行时） | 没有“订阅但不授权”的运行时关系 |
| Handback | Worker 把越界消息交回，带理由，只一次 | Worker 上报 `input-required`，Manager 重派/新开 | 部分 | 没有消息级 one-shot handback |
| Stop | 人明确叫停，撤回 Mandate | 人工 stop、close、`wt-close` | 部分 | 没有 per-ticket 撤回凭证；停止靠流程动作 |
| Pause processing | 暂停派工/评估/投递/回复 | `task_mode wait/listen`、daemon 暂停 | 部分 | 没有统一“暂停所有外部效果”的语义 |

## 5. 上下文与模型

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Router / Main Session | 常驻全局路由与对外交互 | Manager | 部分 | Manager 还承担 scan、派工、纠偏、收口，职责比 Router 宽 |
| Worker Session | 上下文隔离的执行会话 | Worker（独立工位 + ACP session） | 等价（同名） | Freely 的 Worker 还要跑 B1/B2/RED/dev/test/PR 全流程 |
| Session | 一次 AI 工具调用的完整对话历史 | ACP session（JSONL + `session-state.env`） | 等价 | Freely 自己管 session 生命周期；DSH 由宿主管 |
| Session fork | 从父 session 派生独立会话 | ACP `session/fork`；Worker/Reviewer fork Manager | 等价 | 部分 CLI 不支持 fork，降级为 new |
| Session resume | 重启后续接同一会话 | `session/resume`、`session-state.env` | 等价 | 需要 JSONL 存在；丢失时硬错误或降级 |
| Inline & Spill | 近期信息内联，长文截断留续读入口 | prompt 拼接 scan/fleet/checkpoint；文档按需读 | 部分 | 没有显式 inline/spill 策略与字符预算 |
| Chained recall | 对象 ID 内联，按引用图逐跳召回 | scan `cross_refs`、issue/PR 链接、docs 引用 | 部分 | 没有类型化对象图与统一 `read` 入口 |
| Prompt parts | 分层拼装 + 覆盖 + base 版本 | agent 定义 + skills + runtime prompt 拼接 | 部分 | 没有版本化 part、base diff、Policy 置尾契约 |
| Prompt revision | 每次请求绑定 prompt 版本 | skill/agent 文件的 git 版本 | 部分 | 没有 per-request revision 记录 |
| Prompt cache | provider 前缀缓存；Policy 置尾保护 prefix | `[CACHE] cache_hit/miss` 日志、resume/fork | 部分 | 有度量，没有前缀契约与回归 |
| Tool surface | 角色专属工具清单 | AI CLI 工具面 + skills/hook 约束 | 部分 | 没有统一的工具白名单契约 |
| Skill | 按需加载的知识包 | `docs/system/workspace/skills/*` | 等价 | 加载机制不同：DSH skill 工具 vs Freely skill 文件 |

## 6. 状态、持久化与可靠性

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Engine | 领域唯一写者，事务化命令 | runtime 脚本 + freely-db daemon（单 SQLite writer） | 部分 | Freely 没有统一领域 Engine；写入分散在脚本 |
| Store | 单 SQLite，单写者 | `freely.db` + `freely_db_manager.py` 单连接 | 等价（存储层） | 领域表不同；没有 Trigger/Ticket 表 |
| Effects | 持久化副作用队列，带重试/退避 | `a2a_tasks`、`chats`、watchdog、runtime retry | 部分 | 没有通用 effect 队列与 kind/key 合并 |
| Outbox | 消息回执与按序发送 | platform-adapter、issue-sync、retry 日志 | 部分 | 没有 per-message receipt 与“同一工单同一会话按序” |
| Health board | 每个部件一个健康项，唯一写者 | `live-status`、`fleet-status`、`doctor`、runtime 日志 | 部分 | 没有 per-component health entry |
| Single writer | 每类状态一个写者 | DB daemon 单写者 + 文档所有权 + gate | 部分 | 文档状态没有强制单写者 |
| Idempotence | trigger ID / effect key / receipt | `a2a_task list --raw-key`、scan 去重、wt-create 幂等 | 部分 | 没有事件级幂等账本 |
| Atomic transaction | 命令内多聚合一次事务 | DB 单写 + 脚本步骤 | 部分 | 跨文档/DB/平台没有统一事务 |
| Migrations | schema 版本只增 | config/DB migrations、脚本兼容 | 部分 | 没有统一 schema 版本与迁移契约 |

## 7. 运行时、扩展与观测

| Super-agent 概念 | 它真正解决的问题 | Freely 对应叫法 | 等价度 | 差异/缺口 |
| --- | --- | --- | --- | --- |
| Source kind plugin | 新事件源的扩展点 | platform adapter（github/gitee）、issue-sync | 部分 | 没有统一 kind 协议；新增来源要改 runtime |
| Bundle | 一次性打包插件、preset、客户端 | `bin/` + `docs/system/workspace/` + skills | 部分 | 没有宿主插件清单与装载协议 |
| Cordis plugin API | DSH 宿主扩展面 | 无对应 | 缺口 | Freely 没有 host plugin API |
| ACP | runtime ↔ AI CLI 的会话协议 | `run-acp-prompt.py` / `acp-bridge.py` | 等价 | 已是 Freely 的 harness 连接层 |
| A2A | agent ↔ agent 的任务协调 | `a2a_server.py` / `a2a_task.py` / `watchdog_sse.py` | 等价 | 已有，但偏 task 状态，不是事件总线 |
| MCP | agent ↔ 工具/资源 | AI CLI 自带 / MCP 支持 | 等价（外部） | 不是编排层 |
| Watchdog | 主系统外的独立控制回路，判断任务是否有进展 | supervisor heartbeat、`watchdog_sse.py`、continuation watchdog、Loop Guard L0–L3 | 部分 | Freely 的 watchdog 偏进程/任务状态，不是 agentic 进展判断 |
| Speculative execution | 后台提前尝试，有价值才交付 | 无直接对应；B1 预研是“先研究再承诺”，不是投机执行 | 缺口 | 没有后台投机与丢弃机制 |
| Async ReAct（start/stop） | 工具异步执行，前台不阻塞 | AI CLI 自身后台 job / ACP prompt | 部分 | Freely runtime 的 cycle 仍是同步 prompt |
| Panel | 值班人“现在要不要我”的界面 | `live-status`、`fleet-status`、scan、milestones、progress | 部分 | 没有 Web 面板；以 CLI/文档为主 |
| Overview | 需人处理 + 系统问题 + 活动量 | `live-status` 摘要、scan `needs_human`、fleet 快照 | 部分 | 没有统一的“现在需要我”视图 |
| Glossary / locale | 领域词表 + 双语 | 文档术语表（分散） | 部分 | 没有统一 glossary 与 UI 本地化 |

## 8. 同名不同义（最容易被误判）

| 词 | Super-agent 含义 | Freely 含义 | 影响 |
| --- | --- | --- | --- |
| Router | 常驻、只路由、不实现 | Manager：巡逻、派工、纠偏、收口，职责更宽 | 不能直接说“Freely 有 Router” |
| Worker | 只执行一个 Ticket，上下文隔离 | 执行整个 B1→B2→RED→dev→test→PR 生命周期 | Freely 的 Worker 负载更重、上下文更长 |
| Session | 宿主管理的会话 | ACP session + `session-state.env` + JSONL | 生命周期归属不同 |
| Thread | 领域对象，事件按时间排列 | 通常指 PR/Issue 对话或工位分支线 | Freely 没有统一 Thread 对象 |
| Ticket | 授权 + 执行 + 报告的核心对象 | issue + worktree + A2A task 的组合 | 没有单一 Ticket 聚合 |
| Policy | 版本化运行时规则 | 宪法/法律/skill/门禁的集合 | 没有运行时版本对象 |
| Report | 类型化报告（六态 + attention） | A2A state + summary + evidence | 粒度更粗 |
| Gate | 单条事件准入 | 流程阶段门禁 | 防守点不同 |
| Assignment | Ticket 与 Executor 的绑定 | `agent_working` + A2A task + worker session | 没有单一绑定对象 |

## 9. Freely 有、Super-agent 没有

| Freely 能力 | 作用 | Super-agent 对应 |
| --- | --- | --- |
| three-loop（auto/doc/dev） | 调度、设计、实现的分离与回环 | 无；Ticket 直接进入 Worker |
| B1/B2 IBM | 预研、候选、PRD、pre-tests、任务分解 | 无 |
| 独立 Reviewer | 四层/六维审查、pass/fail、打回 | 无；Worker 自审 + 外部 bot |
| worktree + test-pre-merge | 隔离、可丢弃验证、dev↔test 一致性 | 每 Ticket 一个目录，但没有 test lane |
| PR 门禁链 | create/review/merge/closeout | 有 PR 规则，但没有等价门禁链 |
| 多项目 fleet | 跨项目监督与并行 | 单仓库 |
| scan 生命周期定位 | stage + next_action 一次给出 | 有 Ticket stage，但没有“从问题到合并”的阶段 |
| 文档证据链 | brainstorms/candidates/PRD/pre-tests/review | 有 Decision/Report，但不以文档为治理证据 |
| 角色化 harness 适配 | Claude/Codex/OpenCode/Cline 可切换 | 绑定 DSH 宿主 |

## 10. Super-agent 有、Freely 没有（或只有提示词约定）

| Super-agent 能力 | 作用 | Freely 现状 |
| --- | --- | --- |
| Mandate | 不可变授权凭证 | 无；授权靠流程 |
| Admission table / bot list | 确定性事件准入 | 无；靠 Manager 判断 |
| Subscription / direct pass | 线程事件直达 Worker | 无；靠 Manager/A2A/intake |
| followupOwners / handback | 消息归属与一次性交回 | 无；靠 Manager 判断 |
| Typed Report / Attention | 六态报告 + 结构化提问 | 无；A2A state + 自由文本 |
| Disposition | 每条 Trigger 的去向账本 | 无；散在文档/日志 |
| Effects / Outbox | 持久副作用队列 + 消息回执 | 无通用实现；靠脚本/DB/重试 |
| Policy version / revalidation | 规则版本与复活校验 | 无运行时对象 |
| Health board | 每部件健康项 | 无；CLI/日志 |
| Capability probe | 统一 harness 能力探测 | 无；adapter 分支兜底 |
| Agentic watchdog | 判断任务是否有实质进展 | 无；偏进程/状态 |
| Speculative execution | 后台提前尝试 | 无 |

## 11. 结论

- **Freely 不是“缺一半”**：输入、执行、评审、门禁、多项目这些面都有，只是叫法与聚合方式不同。
- **Freely 真正缺的是“运行时协作对象”**：Trigger、Thread、Ticket、Mandate、Report、Attention、Disposition、Subscription 这一组，在 Freely 里被拆成 issue 文档、A2A task、工位、日志和提示词。
- **Freely 的强项不在这些对象上**：它的强项是生命周期与治理证据。用 Super-agent 的对象模型替换 Freely 的文档模型，会丢掉可审计性；反过来，只补对象而不补文档，会丢掉治理。
- **最值得补的映射**：把“消息归属/交接/注意力”做成轻量运行时对象（C-A/B），把“harness 能力”做成显式端口（C-C），而不是复制整套 Trigger/Ticket/Mandate。
