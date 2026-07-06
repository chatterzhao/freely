# Issue: governance-chain-legacy-repair

- issue_id: `I-20260403-1100-A`
- title: Governance chain legacy repair for develop push unblock
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `governance-chain-legacy-repair`
- issue-name: `governance-chain-legacy-repair`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260403T110000Z/candidates.md#c-20260403-1100-a`
- source_brainstorm: `docs/B1-docs/raw-20260403T110000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/gate/governance-chain-legacy-repair/raw-20260403-1100/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-chain-legacy-repair.md`
- verification_artifact_dir: docs/B2-docs/gate/governance-chain-legacy-repair/raw-20260403-1100/code-reviews
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`develop` 目前累积了一批在旧治理门禁放宽时期进入主线的 legacy governance drift。随着 `governance-merge-gate` 最近多轮收紧，这些历史断裂不再只是“文档有点旧”，而是直接阻塞 canonical `develop` 的 push 和后续 promotion followthrough。

当前问题不是一个单点 bug，而是一个链式 owner 缺口：

1. pre-brainstorm / candidate / issue / progress 真相面并不总是同时存在
2. 一部分旧 issue 缺少 `verification_artifact_dir`
3. 一部分旧 review 缺少 implementation decision note 必要字段
4. 一部分 review / candidate 仍使用旧 key 或缺少新的 continuity 字段
5. 历史上出现过的 `1200/1201/1202/1203` repair slices 已经退出当前文件系统，但 canonical docs 一度还把它们当作活跃 lane 消费；这同样属于 owner truth 缺口

如果继续让这些修补分散存在于多个 feature worktree，而没有一个 canonical umbrella owner，那么后续即使局部脚本被修好，也仍然无法证明整个治理链已经恢复。

## Scope

1. Materialize this repair as the canonical umbrella owner for the legacy governance-chain unblock effort that was completed on 2026-04-04.
2. Enumerate the concrete legacy drift classes that are currently blocking `governance-merge-gate`.
3. Normalize the historical repair-slice record for:
   - `20260403-1200--verification-artifact-dir-repair`
   - `20260403-1201--implementation-decision-note-repair`
   - `20260403-1202--candidate-touched-repair`
   - `20260403-1203--issue-id-key-repair`
4. Repair the governance artifacts and gate behavior without weakening the current standards just to get `develop` unstuck.
5. Produce enough canonical issue/progress evidence that later promotion or cleanup decisions can refer to one lawful historical owner.

## Non-Goals

1. Do not relax `governance-merge-gate` merely to pass legacy drift that should be repaired.
2. Do not silently reopen already completed owners whose canonical completion is already recorded on `develop`.
3. Do not treat stale or dirty sibling worktrees as canonical truth just because they contain related file edits.
4. Do not bypass worktree cleanup obligations for already absorbed branches.
5. Do not collapse all future governance drift into this owner once the current push-unblock batch is closed.

## Acceptance

1. `I-20260403-1100-A` must exist as the canonical owner of record for the completed legacy governance-chain unblock work.
2. Historical repair slices must not remain represented as active execution lanes without a current filesystem presence or a lawful issue/progress chain.
3. The parent lane must keep the current gate strictness and repair legacy truth instead of broadening exemptions.
4. `docs/milestones.md`, the issue, and the progress artifact must all agree that this owner is completed historical traceability, not current dev-loop authority.
5. The issue-bound decision note must explain why the current approach favors canonical repair and absorption over gate weakening.

## Current Artifact Set

- `docs/B1-docs/raw-20260403T110000Z/brainstorms.md`
- `docs/B1-docs/raw-20260403T110000Z/candidates.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/brainstorms/b-governance-chain-legacy-repair.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/child-slice-status.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/prd.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/pre-tests.md`
- `docs/B2-docs/gate/governance-chain-legacy-repair/tasks.md`
- `docs/progress/workspace-routing-foundation/p-governance-chain-legacy-repair.md`

## Current Evidence

- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/B2-docs/gate/governance-chain-legacy-repair/child-slice-status.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/milestones.md`

## Verification

- `git diff --check`
- `./bin/governance-check`
- `./bin/wt-fleet-status`

## Next

- `2026-04-04` closeout: canonical owner restoration, historical slice inventory, and dangling-reference cleanup are complete.
- Future governance-chain drift must open from current `develop` as a new lifecycle instead of reopening `1100`.
