# Verification: cli-wrapper-packaging-and-regression-surface-governance

- issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- verified_in_branch: `feature/cli-command-audit-20260406-0015`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0015-feature-cli-command-audit`
- verified_at: `2026-04-06`
- verifier: `codex`

## Scope

验证本 owner 的三条 acceptance：

1. audited runnable wrappers 可 direct-exec
2. `freely ai --help` 输出 clean
3. auth-change wake regression 在 primary / feature worktree 上 deterministic

## Evidence

1. `./bin/ai --help`
   - 结果：通过
   - 说明：help 直接输出 usage，不再出现 `mode` / `apikey` / `account` command-not-found 噪音。
2. `./bin/check-tauri-probe-host`
   - 结果：入口可 direct-exec；当前 feature worktree 因缺 `node_modules` 按预期失败在环境 preflight，而不是 permission denied。
3. `./bin/tauri-probe-dev`
   - 结果：入口可 direct-exec；当前 feature worktree 因缺 `node_modules` 停在 preflight，而不是 permission denied。
4. `./bin/test-freely-fleet-status`
   - 结果：通过
5. `./bin/test-rust-toolchain-preflight`
   - 结果：通过
6. `./bin/test-ai-cli-login-triggers-auth-change-wake`
   - 结果：通过
   - 说明：测试夹具改为同步 auth-change wake，消除了异步时序漂移。
7. `./bin/test-ai-cli-switch-triggers-auth-change-wake`
   - 结果：在 feature worktree 通过
8. `./bin/test-ai-cli-switch-triggers-auth-change-wake`
   - 结果：在 primary worktree `/Users/zhaoyu/Downloads/code/my-freely/freely` 通过
9. 隔离 HOME smoke:
   - 命令：`HOME=<tmp> ./bin/ai --yes login codex apikey --format json`
   - 结果：通过
   - 说明：基于当前用户 `.codex/auth.json` + `.codex/config.toml` 的 apikey/custom provider 真相，成功保存 `apikey-custom-1` 槽位，未污染真实 HOME。
10. 真实 HOME smoke:
   - 命令：`./bin/ai --yes login codex apikey --format json`
   - 结果：通过
   - 说明：确认用户当前 live auth 确实可走真实 `apikey` login 路径；后续不再重复触碰真实 HOME。
11. `git diff --check`
   - 结果：通过
12. `./bin/governance-check`
   - 结果：通过

## Verdict

- 本 owner 当前修复已经证明 runnable wrapper packaging、clean help surface、以及 auth-change wake regression determinism 三条 acceptance 都满足。
- 仍未进入 merge / canonical closeout；后续应在本 lane 收尾并走 guarded merge。
