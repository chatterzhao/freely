# PRD: protected-branch-hook-bypass-breakglass-governance

## Goal

为 Freely 的 protected-branch merge path 冻结第一版 break-glass governance，使 hook/gate bypass 只在少数白名单场景下可发生，并且可审计、可追溯、可补救。

## Why Now

本轮 dogfood 已真实发生两次 develop-bound `--no-verify` completion。问题不在于 hook 没开，而在于：

- Git client-side hook 天生可绕过
- Freely 没写 break-glass whitelist
- merge conflict completion path 缺受控 contract
- governance quality layer 不审计 bypass

## Product Surface

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `AGENTS.md`
- `docs/system/workspace/hooks/README.md`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/quality/governance-check`
- relevant governance skills

## Non-Goals

- 不解决所有宿主级不可绕过 enforcement
- 不重做整套 protected branch model
- 不回滚 ownership anti-stomp feature
- 不把 bypass 规则留在 skill 私有文本里

## Non-Negotiables

- protected-branch bypass 默认违规
- break-glass 只允许白名单 reason
- 合法 bypass 也必须留下 machine-readable receipt
- bypass 只能允许最小收尾动作
- break-glass 之后必须跟进修 gate，而不是把例外变常态

## Context Pack

- `pre-commit` 阻止 `develop/main/test-pre-merge-*` 上直接开发，但可被 `--no-verify` 跳过
- `pre-merge-commit` 会在 `develop` merge 时运行 governance merge gate 和 promotion gate，但同样属于可被跳过的 client-side hook
- `pr-merge-guarded` 当前只负责 merge 发起，没有封装冲突后的 completion path
- `governance-check` 目前不检查 develop merge 是否存在未授权 bypass

## Decomposition Tree

1. Freeze constitutional principle
2. Freeze law-level whitelist and forbidden examples
3. Freeze guarded merge completion contract
4. Freeze bypass receipt / audit contract
5. Decide the first implementation slice

## Phase-1 Canonical Contract

### Break-glass principle

- `main` / `develop` / `test-pre-merge-*` 上，hook/gate bypass 默认违规
- 只有显式 break-glass reason 命中白名单时，才允许最小化例外路径

### Reason taxonomy

- `tooling_unavailable`
- `verified_false_negative`

### Required fields

- `bypass_mode`
  - `forbidden | break_glass`
- `break_glass_reason`
  - `tooling_unavailable | verified_false_negative`
- `blocked_gate`
  - `pre-commit | pre-merge-commit | governance-merge-gate | governance-promotion-gate | pretests-gate | checkpoint-guard`
- `operation_scope`
  - `merge_completion_only | writeback_only | issue_closeout_only | other`
- `evidence_refs`
- `follow_on_owner`

### Frozen constraints

- bypass 不能用于继续开发，只能用于最小收尾动作
- 没有 `follow_on_owner` 的 bypass 不合法
- 单纯“人工确认没问题”不是 evidence
- 保护分支上的小改动、cleanup convenience、writeback convenience 都不能自动成为合法 break-glass

## Prototype Path

先冻结 contract，再实现最小 enforcement：

1. 文档真源冻结
2. `pr-merge-guarded` completion path 设计
3. `governance-check` bypass audit 设计

## Eval Plan

### Pre-merge focused regression

- environment: feature worktree
- evidence: issue-bound docs + `governance-check`
- failure signal: bypass contract 仍然分散在 skill/agent 文本里，没有 canonical whitelist

### Post-merge integration acceptance

- environment: `develop`
- evidence: future gate/audit 实现能发现未授权 bypass
- failure signal: 保护分支 merge 仍可无 receipt 地被跳过

### Post-merge application-native real-environment acceptance

- environment: `develop`
- evidence: merge conflict completion 不再默认依赖裸 `git commit`
- failure signal: guard path 断在冲突后收尾

## Execution Slices

1. principle + whitelist freeze
2. guarded completion contract
3. audit contract
4. follow-on implementation owner
