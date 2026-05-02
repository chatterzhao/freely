# Candidates - 20260319-1715--human-chat-intake-and-manager-delegation

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260319-1715-A
- title: CLI-first human chat intake and manager delegation loop
- problem: Freely 已定义 human chat 是 discovery source，也有 prompt 组装器与单测，但缺少可恢复的 intake 入口、主管监督面、worker 委派闭环和“已被 milestone 吸收”的完成信号，因此人类插话仍无法被系统稳定吸收。
- why_now: Freely 要真正“用 Freely 开发自己”，就不能继续依赖当前聊天线程上的人工解释；人的插话必须像 github issue、review/test 一样，成为可被主管监督和路由的正式输入面。
- acceptance_hint:
  - 先收敛一条 CLI-first intake 方案，明确命令面、artifact 落点和状态字段
  - 明确人类输入在 Freely 中的默认站位是“插话 side input”，不是阻塞主 loop 的同步 gate
  - 明确 AI 执行过程中的信息不足/分歧/澄清需求，默认应由主管再委派 AI 分析解决，而不是等待人类补充指令或意图
  - 明确主管“注意到插话”依赖 `durable intake + runtime signal + manager queue scan`，而不是依赖会话内 prompt 注入
  - 明确主管只负责 `notice + claim + choose reaction + delegate + choose absorption target`，不负责深度解释
  - 明确 specialized AI 负责深度解释与 skill 调用，并产出 `interruption resolution artifact`
  - 明确 `reaction plane` 与 `artifact plane` 分离：前者决定当前运行怎么响应，后者决定正式产物沉淀到哪里
  - 明确 `steer/followup/collect/interrupt/noise` 作为 reaction mode 的语义与链路，不替代 `source_class/route_kind`
  - 明确 manager 如何通过 runtime signal 发现 pending intake，并立即委派专门 AI 处理
  - 明确每种 reaction mode 的 runtime 落地：是否 kill 进程、是否 replacement worker、是否等待自然边界、是否继续收集
  - 明确 `.freely/intake/**` 是短期事件池，长期可发现事实仍需回到 canonical pools
  - 明确 discovery 类输入如何进入 dedicated worker 的 `doc-pre-brainstorm-execution`
  - 明确 continuation / control / noise 各自进入哪类 canonical artifact
  - 明确 worker 完成后如何把 intake、resolution artifact 与 canonical artifact 建立可追溯链接
  - 明确旧口径“chat / session evidence 是 discovery source”只对 absorption 为 discovery 的输入继续成立
  - UI 如需存在，只能复用同一 intake 能力，不新增绕过 CLI 的业务逻辑
- priority: P0
- status: promoted
- decision_reason: CLI-first intake、manager queue surfacing、`claim/resolve`、resolution artifact 与 `skill:human-interruption-handling` 的最小闭环已经落地；这条线已正式物化为 issue，后续从 issue / verification 继续收口，而不再停留在 pre-brainstorm。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`
- legacy_id_mapping: I-20260319-1715  # 历史遗留的 issue id
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
