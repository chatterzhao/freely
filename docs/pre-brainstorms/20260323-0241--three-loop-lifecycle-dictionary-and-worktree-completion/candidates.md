# Candidates - 20260323-0241--three-loop-lifecycle-dictionary-and-worktree-completion

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260323-0241-A
- title: Unify three-loop lifecycle dictionary and define worktree completion as cleanup-complete by default
- problem: 当前 Freely 已有三层 loop、worktree 技能和治理规则，但缺少一份统一词典与统一映射，明确“收口”“按 Freely 规范”“按 worktree 生命周期”“按三层 loop 工作”这些表述的唯一含义，导致 agent 容易把 `in_verification`、`merge-ready` 或 `merged-not-cleaned` 误当成“本轮已经做完”。
- why_now: 本轮在 Freely 自举时已经真实暴露这个问题。若不尽快固定，未来 Freely 开发自己和开发其他应用都会继续在 promote / cleanup 上停顿，自治会退化为“人说一步动一步”。
- acceptance_hint:
  - 明确 worktree lifecycle 不是第四层 loop，而是三层 loop 的组合表现
  - 明确“一个 worktree 开发完毕”的默认含义是 cleanup complete
  - 明确 `active / merge-ready / merged-not-cleaned / retire-ready / completed` 之类的统一词典
  - 明确用户说“按三层 loop 工作”时，默认等价于按 Freely 规范闭环到当前轮终点
  - 明确 agent / skill owner：哪些由 manager-agent 判断，哪些由 branch-management / worktree-maintenance-governance 执行
  - 落点优先放在 `three-loop-capability-lifecycle`、`LAWS`、`branch-management`、`worktree-maintenance-governance` 和项目级 `AGENTS.md`
- priority: P0
- status: proposed
- decision_reason: 这是 Freely 自治语义的根问题，不只是某一条 branch 的特例。只有把三层 loop 变成统一总词典和总映射，未来 Freely 才能对自己和其他项目都稳定执行“做到最后”的闭环。
- next_action: materialize 为治理 issue，先补三层 loop 词典和 worktree 完成态定义，再回收各 skill/入口里会导致歧义的表述。
- revisit_trigger: 当“按三层 loop 工作”已经足以单独驱动 promote + cleanup，不再需要额外的表述补丁时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
