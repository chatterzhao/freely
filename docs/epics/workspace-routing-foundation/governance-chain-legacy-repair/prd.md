# PRD: governance-chain-legacy-repair

## Goal

恢复当前 legacy governance-chain repair 的 canonical owner 链，使 `develop` 的历史治理断裂能在不放宽 gate 的前提下被修复并推进回 lawful promotion path。

## Why Now

当前 `develop` 的 push / followthrough 被一组历史遗留治理断裂阻塞，而这组问题曾经裂变成多个 repair slices。如果不先 materialize 一个 umbrella owner，就会继续出现：

- parent lane 只有 candidate 没有 issue
- historical child slices 继续在 canonical docs 中伪装成 active lane
- 同一轮修补在不同时间点留下互相矛盾的 owner / fleet truth

## Product Surface

- `docs/milestones.md`
- `docs/pre-brainstorms/**`
- `docs/epics/**/issues/*.md`
- `docs/epics/**/code-reviews/*.md`
- `docs/progress/**`
- `docs/system/workspace/scripts/quality/governance-merge-gate`

## Non-Goals

- 不把 gate 降级成“允许 legacy drift 继续通过”
- 不把所有未来治理修补永久堆在一个 mega-owner
- 不把已完成 owner 重新改写为未完成

## Non-Negotiables

- promoted candidate 不能继续指向不存在的 issue
- historical child repair slices 不能继续以 active lane 形式污染 canonical docs
- umbrella owner 必须把 parent / child lane 边界写清
- develop-bound capability edits必须有 issue-bound decision note

## Decomposition Tree

1. materialize umbrella owner
2. normalize historical child repair slice status
3. repair legacy artifacts without weakening the gate
4. re-run governance checks and decide cleanup/promotion followthrough

## Current Repair Classes

1. missing `verification_artifact_dir`
2. missing implementation decision note fields
3. legacy review / issue key mismatches
4. candidate continuity field backfill
5. milestone / issue / progress chain gaps created by the current repair itself

## Eval Plan

### Canonical chain validation

- environment: feature worktree
- evidence: milestone + issue + progress + child-slice docs agree on ownership and current fleet reality
- failure signal: any promoted candidate still points to a nonexistent issue

### Governance gate validation

- environment: feature worktree
- evidence: `./bin/governance-check`
- failure signal: fix only passes by weakening scope or adding new exemptions

### Fleet hygiene validation

- environment: project fleet
- evidence: `./bin/wt-fleet-status`
- failure signal: absorbed/completed branches remain ambiguous or dirty without explicit handling
