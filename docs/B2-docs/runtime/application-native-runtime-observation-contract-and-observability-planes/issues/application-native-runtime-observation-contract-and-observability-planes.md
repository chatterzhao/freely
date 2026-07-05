# Issue: application-native-runtime-observation-contract-and-observability-planes

- issue_id: `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `application-native-runtime-observation-contract-and-observability-planes`
- issue-name: `application-native-runtime-observation-contract-and-observability-planes`
- verification_artifact_dir: `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/code-reviews`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260324T041500Z/candidates.md#c-20260324-0415-a`
- source_brainstorm: `docs/B1-docs/raw-20260324T041500Z/brainstorms.md`
- source_candidates: `docs/B1-docs/raw-20260324T041500Z/candidates.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
  - `docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经具备多种观察面：

- `live-status`
- `fleet-status`
- session jsonl
- cycle log
- continuity / prompt / verification artifacts

但还没有统一 contract 去说明：

1. 真实环境测试时应该先看哪些 surface
2. 何种 signal 表示“仍在推进”或“已经空转”
3. 用户、manager、watchdog 应如何共享同一组状态卡片与 deep refs
4. 这套 contract 如何从 Freely self-host 泛化到未来任意应用

## Scope

1. 冻结应用无关的 `application-native runtime observation contract`
2. 冻结五个 observation planes：`current-state / session / stream / fleet / artifact`
3. 冻结 `plane identity block`、`progress signal schema`、`stall signal schema`、`acceptance evidence schema`
4. 冻结 CLI / TUI / GUI / API 共享的 `status card minimum fields` 与 `deep ref groups`
5. 明确 Freely self-host 只是第一份 concrete profile
6. 明确该 contract 如何同时服务 human interruption、manager/watchdog supervision、issue completion judgement 与 delete gate

## Acceptance

- artifact plane 是 `acceptance evidence` 的 canonical truth surface
- current-state / fleet / API surfaces 只镜像最小摘要与 `acceptance_ref`
- CLI / TUI / GUI / API 共享同一组最小 `deep ref groups`
- Freely self-host 对上述 contract 的 concrete profile 被写清：
  - `live-status`
  - `fleet-status`
  - session jsonl
  - cycle log
  - continuity / prompt / verification artifacts
- contract 明确区分：
  - progress signal 仅判断“仍在推进”
  - stall signal 仅判断“需要主管关注/重路由”
  - acceptance evidence 用于 issue completion 与 delete gate judgement

## Ready For Dev

当前 IBM 已冻结：

1. `acceptance evidence schema` 的 canonical truth 固定在 artifact plane
2. current-state / fleet / API 只镜像最小摘要与 `acceptance_ref`
3. CLI / TUI / GUI / API 共享同一组最小 `deep ref groups`
4. `live-status` / `fleet-status` 继续承接 Freely self-host day-1 current-state / fleet profile
5. 多 subagent day-1 继续聚合在 lane / worktree / session surfaces 下

## Implementation References

- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/brainstorms/b-application-native-runtime-observation-contract-and-observability-planes.md`
- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/prd.md`
- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/pre-tests.md`
- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/tasks.md`
- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/code-reviews/20260324-application-native-runtime-observation-contract-and-observability-planes-verification.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/README.md`

## Completion Evidence

- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/code-reviews/20260324-application-native-runtime-observation-contract-and-observability-planes-verification.md`
- `./bin/governance-check`
- `rg -n "current-state plane|fleet plane|artifact plane|acceptance evidence|acceptance_ref|deep ref|progress signal|stall signal" docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/skills/multi-worktree-supervision/SKILL.md docs/system/workspace/skills/watchdog-control-plane/SKILL.md docs/system/workspace/scripts/README.md docs/LAWS.md`

## Completion Note

本 issue 的最小 contract slice 已完成：`artifact plane` 固定为 acceptance evidence canonical truth，`current-state` / `fleet` surfaces 只镜像最小 acceptance 摘要与 shared `deep ref groups`，Freely self-host concrete profile 也已写清。更丰富的 CLI / TUI / GUI / API 产品化与多 subagent 一等可视化留作 follow-on scope，不阻塞本 issue 完成。
