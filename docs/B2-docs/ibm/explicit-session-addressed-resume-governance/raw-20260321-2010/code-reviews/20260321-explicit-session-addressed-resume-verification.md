# Code Review: explicit-session-addressed-resume-governance verification
- issue_id: `I-20260321-2010`

- date: `2026-03-21`
- scope:
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - `docs/system/workspace/scripts/monitor-ai-cli.sh`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
  - `docs/system/workspace/scripts/tests/test-freely-session-rotation`
  - `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- reviewer: `codex`
- status: `pass`

## Findings

- No blocking findings.

## Verification Notes

- 2026-03-21: `codex` 默认 runtime resume 已改成显式 `SESSION_ID`，缺失 target 会明确失败。
- 2026-03-21: `cc` / `cc-use-codex-cli` 继续使用 workcell-scoped `--session-id`，并通过共享 helper 参与同一 continuity contract。
- 2026-03-21: delegated continuation 现在会把当前 worker resume target 写回 intake `SESSION_REFS`。
- 2026-03-21: local continuation re-entry 现已优先 `TERM` 当前 AI，并把 fallback 模式写入 `preemption-state.env`。

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

## Residual Risks

- `iflow` / `kiro-cli` 仍属于弱 continuation contract；当前 issue 已如实标注，但并未把它们升级成与 `codex` / `cc` 同等级的显式 session-addressed surface。
- 当前 local re-entry 仍以 `TERM -> hard kill fallback` 为界；若后续需要更强 flush/checkpoint guarantee，应新开 lifecycle 承接。
