# Candidates

## C-20260319-0500-A: legacy issue

- status: `proposed`
- problem: Freely 已有方法论与治理规则，但运行器层的可移植、可验证、可实现规范还不如 Symphony 的 `SPEC.md` 那样集中。
- change:
  - 为 Freely 的 auto-loop / worker execution / recovery / supervision 形成更系统的 executable spec
  - 区分 required core 与 optional extensions
  - 让实现、测试、治理文档之间的映射更直接
- acceptance_hint:
  - 能明确 Freely 运行器最小必选能力和推荐扩展能力
  - 后续实现不再主要靠散落的脚本说明和 prompt 注入对齐
- decision_reason: 这是 Symphony 对 Freely 最值得吸收的部分之一，而且不会破坏三层循环本身。
- next_action: 继续 pre-brainstorm，先确认 Freely 是否真的缺一份更集中、可执行的 orchestrator spec；若边界继续稳定，再 materialize 为独立 issue。
- revisit_trigger: 当 auto-loop / worker execution / recovery / supervision 的最小执行规范缺口被明确证明，且不再只是文档表述偏好时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0500-A: legacy issue

- status: `needs_research`
- problem: Symphony 用单 persistent workpad comment 维持单 issue 执行态，降低了执行记录碎片；Freely 当前的 continuity 仍分散在 issue / progress / recovery / brainstorm 等层。
- change:
  - 研究 Freely 是否需要一个更统一的 issue-level continuity 抽象
  - 明确它与 pre-brainstorm / IBM / dev-loop / recovery 各自文档边界的关系
  - 避免为了“统一”而破坏分层治理
- acceptance_hint:
  - 能说明哪些信息必须跨环持续存在，哪些仍应按 loop 分层存放
  - 设计结果不会把 Freely 退化成单文档系统
- decision_reason: 有启发，但风险也高；如果处理不好，会冲掉 Freely 已建立的分层模型。
- next_action: 保持在 pre-brainstorm，先确认哪些 continuity 信息必须跨环持续存在、哪些仍应按 loop 分层存放；未稳定前不要 materialize。
- revisit_trigger: 当能明确写出跨环 continuity 的最小抽象且不破坏 pre-brainstorm / IBM / dev-loop 分层时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0500-A: legacy issue

- status: `needs_research`
- problem: Symphony 已把 SSH worker 作为可选扩展建模，Freely 后续也可能需要 manager/worker 跨主机执行。
- change:
  - 评估 Freely 当前 worktree / auth / recovery / observability 设计是否适合远程 worker
  - 识别远程执行对 workspace ownership、cleanup、resume、host health 的新增要求
- acceptance_hint:
  - 明确远程 worker 是否只是扩展，还是会反过来要求重写当前本地执行模型
  - 若推进，能列出最小必要前置条件
- decision_reason: 方向成立，但与当前“自治开发应用”主线相比优先级明显更低。
- next_action: 保持在 pre-brainstorm，优先只收集远程 worker 对 workspace ownership、cleanup、resume、host health 的新增要求。
- revisit_trigger: 当远程执行不再只是扩展设想，而是已经出现明确的前置条件或主线压力时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0500-A: legacy issue

- status: `dropped`
- problem: Symphony 具备较强执行器形态，容易让后续讨论误把它当成 Freely 的直接蓝图。
- change:
  - 在相关研究和后续 issue 中明确：仅吸收局部机制，不整体照搬
  - 保持 Freely 的三层循环、治理分层、多来源发现为主轴
- acceptance_hint:
  - 后续设计不再把 Freely 简化成 Linear-first issue runner
  - 不出现“为了对齐 Symphony 而回退 pre-brainstorm / IBM / recovery 分层”的方案
- decision_reason: 这是研究排除项，不是功能交付项。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
