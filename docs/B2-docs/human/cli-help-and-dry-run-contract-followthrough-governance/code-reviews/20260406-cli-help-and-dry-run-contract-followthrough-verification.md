# Verification: cli-help-and-dry-run-contract-followthrough-governance

- issue_id: `I-20260405-2358-D`
- issue_path: `docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- verified_in_branch: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0408-feature-cli-help-dry-run-contract-followthrough`
- verified_at: `2026-04-06`
- verifier: `codex`

## Scope

验证本 owner 的三条 acceptance：

1. audited help commands 显式、无副作用、usage-only 返回成功
2. `ai switch codex --dry-run --format json` 输出稳定 machine-readable JSON，且不触发真实 probing
3. bounded owner 仍通过相邻回归和治理门

## Evidence

1. `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
   - 结果：通过
   - 说明：覆盖 `wt-create`、`wt-enter`、`wt-add`、`pr-merge-guarded`、`freely` 的 help surface；同时证明 `wt-create --help` 不创建 branch/worktree。
2. `freely wt-create --help`
   - 结果：通过
   - 说明：直接返回 usage，退出码 `0`。
3. `bash -lc 'source ./bin/wt-enter --help'`
   - 结果：通过
   - 说明：sourced helper help 直接返回 usage，退出码 `0`。
4. `freely pr-merge-guarded --help`
   - 结果：通过
   - 说明：usage-only invocation 退出码 `0`。
5. `./bin/freely --help`
   - 结果：通过
   - 说明：不再打印 `unknown command` 错误。
6. `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
   - 结果：通过
   - 说明：隔离 HOME 夹具确认 dry-run 直接输出 saved-slot inventory JSON，且不会调用 mock `codex` probing。
7. `python3 - <<'PY' ... json.loads(subprocess.check_output([... './bin/ai' '--quiet' '--format' 'json' '--dry-run' 'switch' 'codex' ...]))`
   - 结果：通过
   - 说明：真实 worktree 下 dry-run 输出可直接被 JSON parser 消费。
8. `./bin/ai --quiet --format json --dry-run switch codex`
   - 结果：通过
   - 说明：真实 HOME 下返回单个 inventory 摘要结果，不再长时间等待 probe timeout。
9. `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
   - 结果：通过
10. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
    - 结果：通过
11. `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
    - 结果：通过
12. `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
    - 结果：通过
13. `git diff --check`
    - 结果：通过
14. `./bin/governance-check`
    - 结果：通过

## Verdict

- 本 owner 当前修复已经满足 audited help contract 和 bounded dry-run JSON contract。
- 预集成前的 focused regressions 与治理门均通过；下一步可以进入 guarded promotion lane。
