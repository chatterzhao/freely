# Verification: bash32-daemon-compat-fix

- issue_id: `I-20260429-1745-A`
- issue_path: `docs/B2-docs/runtime/bash32-daemon-compat-fix/raw-20260429T174500Zissues/I-20260429-1745-A.md`
- verification_date: `2026-04-29`
- verifier: `human`

## Scope Verdict

- `PASS`: `resolve_active_supervisor_pid_for_start` 显式排除 `$$`，不再自检测自杀
- `PASS`: `select_launch_kind` 用 nullglob 数组代替裸 ls，不再因空 glob 崩溃
- `PASS`: 两处改动均为防御性代码，不改变核心逻辑
- `PASS`: `bash -n` 语法检查通过

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
3. `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Implementation Decision Note

- decision: `Minimal defensive fixes for bash 3.2 compatibility.`
- why_this: `macOS ships bash 3.2 by default. Without these fixes, freely daemon cannot start on the default system shell.`
- alternatives_considered: `Require bash 4.0+ (impractical for macOS users); switch shebang to zsh (too invasive, risks Linux regressions).`
- boundary_non_goals: `Not auditing all glob uses; not changing shebang; not making the entire runtime bash 4.0+ compatible.`
- residual_risk: `Other ls/glob patterns may have similar bash 3.2 issues; the nullglob guard pattern is reusable if discovered.`
