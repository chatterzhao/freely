# Brainstorm: test-pre-merge-family-promotion-gate-enforcement-governance

## Decision

这条 follow-on owner 同时包含 truth-source update 与 promotion gate enforcement，不再拆成两个独立 owner。

## Why This

1. 当前冲突点是同一个语义面：谁能 merge 到 `develop`。
2. `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` 和 `pr-merge-guarded` / tests 都在表达同一套 source-branch 规则。
3. 分拆成两个 owner 只会产生临时双真相，而不会减少复杂度。

## Frozen Boundary

本 owner 解决：

1. source-branch semantics
2. protected-branch gate enforcement
3. regression tests alignment

本 owner 不解决：

1. family lifecycle automation
2. manifest generation automation
3. batch create UX
4. runtime stale/status surfaces

## Expected Follow-On

本 owner 完成后，下一个 owner 才应进入：

- `test-pre-merge family lifecycle automation`
