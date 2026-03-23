# Candidates - 20260323-0241--three-loop-lifecycle-dictionary-and-worktree-completion

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260323-0241-A
- title: Restore three-loop-capability-lifecycle as the full application event map
- problem: 当前 Freely 已经实现了大量 skill / agent / runtime / worktree 能力，但 `three-loop-capability-lifecycle` 没有继续把它们吸收成统一地图。结果是“按三层 loop 工作”还不能直接回答从哪里起、哪里循环、为什么不能停、下一跳是谁、terminal 在哪里；worktree 生命周期、promotion / cleanup 只是这个更大缺口下的一个子面。
- why_now: 本轮 Freely 自举里已经真实暴露出后果：agent 会停在 verification 或 merge-ready，不是因为能力不存在，而是因为三层 loop 地图没把这类事件和分支收进去。若不尽快修正，未来 Freely 开发自己和开发其他应用都会继续依赖人类解释下一跳，自治会退化为“人说一步动一步”。
- acceptance_hint:
  - 明确三层 loop 是 Freely 的全应用事件地图，而不是高层摘要
  - 明确所有主要事件、行为、分支、回流和 terminal state 都能落到三层 loop 的具体节点
  - 明确 worktree lifecycle、promotion、cleanup、recovery、checkpoint 等都属于三层 loop 组合，而不是例外流程
  - 明确 `signal -> lifecycle record -> worktree execution cell` 的联动模型，避免只画 issue 状态而丢掉 worktree 容器
  - 给出从 `human interruption` 到 `worktree retire/delete` 的最小事件链
  - 给出 worktree lifecycle 子状态机，至少覆盖 `planned / active / frozen / verification-ready / promotion-in-flight / merged-not-cleaned / retire-ready / retired`
  - 显式补出 `completion_verification` 回路，区分“继续实现”和“只剩 promote / cleanup”
  - 给出省周期 gate，说明何时复用旧树、何时跳过 IBM、何时直接 cleanup
  - 在地图中嵌入统一词典，例如 `active / merge-ready / merged-not-cleaned / retire-ready / completed`
  - 明确 agent / skill owner：哪些由 manager-agent 判断，哪些由 skill 作为模块执行
  - 落点优先放在 `three-loop-capability-lifecycle`、`LAWS`、`branch-management`、`worktree-maintenance-governance` 和项目级 `AGENTS.md`
- priority: P0
- status: proposed
- decision_reason: 这是 Freely 自治语义的根问题，不只是某一条 branch 的 completion 定义。只有把三层 loop 恢复成持续更新的总地图，未来 Freely 才能对自己和其他项目都稳定执行“从哪里起、哪里循环、何时终止”的自治闭环。
- next_action: 先把 pre-brainstorm 收敛为“全应用事件地图 + worktree-first execution map + completion / cleanup 回路 + cycle-saving gates”这一稳定边界，再 materialize 为治理 issue，不要提前缩成单一 worktree completion 词典。
- revisit_trigger: 当“按三层 loop 工作”已经足以单独驱动 agent 知道入口、循环、分支、回流与 terminal，而不再需要人类补解释时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
