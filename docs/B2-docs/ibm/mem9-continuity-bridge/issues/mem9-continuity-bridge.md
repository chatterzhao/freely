# Issue: mem9-continuity-bridge

- issue_id: `I-20260318-1222`
- title: Mem9 shared memory evaluation for Freely continuity plane
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `mem9-continuity-bridge`
- issue-name: `mem9-continuity-bridge`
- source_candidate: `docs/B1-docs/raw-20260318-1222/candidates.md#c-20260318-1222-01`
- source_brainstorm: `docs/B1-docs/raw-20260318-1222/brainstorms.md`
- execution_base: `feature/mem9-research-20260318`
- integration_target: `develop`
- depends_on: `none`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经拥有本地 continuity / recovery / session rotation / multi-worktree supervision，但还没有一个正式的外部共享记忆边界来回答：

- 什么可以写入外部 memory backend
- 什么必须继续由本地治理事实源裁决
- 外部 memory 是否只作为 continuity enhancement，而不是 authority

## Scope

1. 把 `mem9` 定义为可选连续性增强层，而不是治理真源。
2. 形成 `local-only` 与 `local + mem9` 的边界说明。
3. 把可外部化内容限定为 session summary、handoff hint 和 cross-tool recall 线索。
4. 把受保护分支、worktree 生命周期、checkpoint commit 和 merge gate 明确留在本地治理链路。
5. 将该边界 materialize 为一个可复用的 `skill:mem9-continuity-bridge`。

## Acceptance

- `mem9` 不会被描述为 Freely 的正式治理事实源。
- 本地治理事实源的优先级保持不变。
- `skill:mem9-continuity-bridge` 已存在并被技能索引收录。
- `docs/B1-docs/raw-.../candidates.md` 已回写到正式 issue 路径。
- 这条研究不再停留在“只有 brainstorm，没有承接”的状态。

## Completion

- `docs/B1-docs/raw-20260318-1222/brainstorms.md`
- `docs/B1-docs/raw-20260318-1222/candidates.md`
- `docs/system/workspace/skills/mem9-continuity-bridge/SKILL.md`
- `docs/system/workspace/skills/README.md`

## Verification

- `./bin/governance-check`

