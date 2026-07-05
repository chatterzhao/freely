# Brainstorm: protected-branch-merge-receipt-hardening

## Boundary

这条 owner 不是第二次 break-glass policy freeze，而是 canonical phase-1 absorbed 之后的 runtime/gate residual hardening。

要回答的不是“允不允许 bypass”，而是：

1. 哪些 hardening 缺口确实还在
2. 哪些 root staged changes 只是 regression
3. 第一刀应该接到哪个 runtime / quality hook 点

## Root Staged Patch Classification

### keep-as-signal

- `pr-merge-guarded` 的 initial merge / completion boundary 仍值得单独 harden
- `governance-check` 的 receipt / ledger parity audit 仍值得增强
- `governance-merge-gate` staged/touched relevance 仍需要更明确 regression coverage

### already-absorbed

- `availability-watchdog` repo-root resolution 已经由 `e506982` 吸收进 canonical `develop`
- `test-availability-watchdog-path-resolution` 当前在 canonical `develop` 中存在且有效

### drop-as-regression

- 把 `pr-merge-guarded` 初始 merge 改回 `git merge --no-ff -m ...`
  - 这会绕开当前通过 `--no-commit` + controlled continue 写 receipt 的路径
- 删除 `test-pr-merge-guarded-hooked-initial-merge-receipt`
  - 这是直接删除当前 canonical safety net
- 删除 `governance-merge-gate` staged-view parsing与对应测试
  - 这会把 “staged merge 之前 owner artifact 只在 index 中存在” 的边界退化掉
- 把 candidate relevance 改成整文件 touched 即整候选相关
  - 这会重新把 sibling candidate context 误判成直接 touched candidate

## First Implementation Slice Candidates

### Option A: receipt/ledger parity audit first

优点：
- scope 最窄
- 与当前 root staged regression 无关，不会引入 accidental simplification
- 可以直接建立 follow-on truth，不必先动 merge semantics

缺点：
- 不能直接回答 handshake 是否够硬

### Option B: merge completion handshake hardening first

优点：
- 直接解决“环境变量握手仍偏软”的 residual concern

缺点：
- 需要仔细避免碰坏 current completion path
- 比 parity audit 更容易误触发 develop merge 流程

### Option C: governance-merge-gate staged regression coverage first

优点：
- 直接封死这次 root staged patch 想回退的边界

缺点：
- 更像 guardrail / test-first，不一定是用户最关心的第一刀

## Current Leaning

第一刀更适合 `receipt_ledger_parity_audit`，然后再接 `merge_completion_only` / handshake hardening：

- parity audit 更容易 issue-bound 实现
- 它不会误导成“删测试换稳定”
- 它还能作为后续 merge-completion hardening 的审计底座

但在进入 dev-loop 前，仍应在 PRD / pre-tests 中把 staged regression boundary 冻结住，避免下一位执行者再次参考 root staged patch 做回退式修改
