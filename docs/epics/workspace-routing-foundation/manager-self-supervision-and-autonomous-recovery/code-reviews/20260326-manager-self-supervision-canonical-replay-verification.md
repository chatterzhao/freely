# Code Review: manager-self-supervision-and-autonomous-recovery canonical replay
- issue_id: `I-20260318-1408`

- verdict: pass
- date: `2026-03-26`

## Why

本 issue 先前只差 verification closeout，没有新的实现缺口。当前需要确认 canonical `develop` 是否仍保留 manager self-supervision、runtime recovery、PID ownership 和 account-boundary contract，避免把已经被同族实现吸收的工作重复推进。

## Checks

- `bash docs/system/workspace/scripts/tests/test-freely-supervisor-loop`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-does-not-switch-accounts`
- `bash docs/system/workspace/scripts/tests/test-freely-status-pid-ownership`
- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `./bin/governance-check`

## Findings

1. manager prompt 仍会自动暴露 `expected-running` worker 掉线，说明 self-supervision alert contract 仍成立。
2. manager runtime 仍会优先做脚本级 worker supervisor 恢复，说明 runtime-owned recovery 没有退回人工插话依赖。
3. worker runtime 命中 auth failure 时继续把全局账号恢复交给外层 watchdog / account controller，角色边界没有回退。
4. stale supervisor pid ownership 继续被正确忽略，fleet desired runtime / issue hints 也仍可见。
5. 更外层 “主管 supervisor 自己消失时如何复活” 已由 global watchdog family 承接，不再是本 issue 的未完成项。

## Conclusion

manager self-supervision and autonomous recovery 已在 canonical `develop` 稳定存在并通过 focused replay；本 issue 可以从 `in_verification` 收口为 `completed`。
