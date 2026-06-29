# Brainstorm: develop-guarded-merge-entrypoint-enforcement-governance

## Narrow Boundary

这条 issue 只解决一件事：

- `develop` merge commit 进入 hook 时，必须已经证明自己来自 `freely pr-merge-guarded`

不解决：

- server-side enforcement
- receipt ledger 新语义
- break-glass whitelist 扩张

## Implementation Shape

最小实现优先放在 `pre-merge-commit`：

1. 若当前是 `develop` merge commit，则先要求 canonical guarded state + completion marker + target/source 与当前 merge 一致。
2. 若缺少上述 handshake，立即失败并提示改用 `freely pr-merge-guarded`。
3. 只有握手通过后，才继续执行 governance materialization gate 与 promotion ownership gate。

## Test Shape

至少需要三类证据：

1. raw merge 被挡住
2. guarded handshake 在 hook 下仍然触发 governance / promotion gate
3. canonical `pr-merge-guarded` 正常路径与 break-glass completion 仍然通过
