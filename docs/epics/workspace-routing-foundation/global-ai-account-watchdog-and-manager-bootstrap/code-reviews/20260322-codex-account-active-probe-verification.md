# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

## Result

- pre-merge verification passed

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `./bin/governance-check`

## What Changed

1. `freely ai switch codex` 在未显式指定账号时，会主动 probe 所有已保存账号，并切到可用账号或最早恢复账号。
2. availability watchdog 的 probe contract 从“空输出/非空输出”收紧为显式 `usable` / `rate_limited:<reset_at>`，避免把解析失败误判为可用。
3. 自动切号路径改为复用显式 `cmd_switch` 主路径，保留现有校验与 `--dry-run` 语义。
4. 新增脚本级回归，覆盖：
   - 主动 probe 找到可用账号
   - 全部限流时切到最早恢复账号
   - 本地 runtime 仍把 rate-limit 恢复交给 watchdog，而不是在本地长睡眠

## Remaining Acceptance

- merge 到 `develop` 后，在受保护工位再跑一次目标 issue 的 completion verification，然后再进入 cleanup 决策。
