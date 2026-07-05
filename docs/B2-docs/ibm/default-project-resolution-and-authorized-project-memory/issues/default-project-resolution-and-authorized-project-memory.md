# Issue: default-project-resolution-and-authorized-project-memory

- issue_id: `I-20260320-0018`
- title: Default project resolution and authorized project memory for CLI-first interruption entrypoints
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `default-project-resolution-and-authorized-project-memory`
- issue-name: `default-project-resolution-and-authorized-project-memory`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/default-project-resolution-and-authorized-project-memory/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260320/candidates.md`
- source_brainstorm: `docs/B1-docs/raw-20260320/brainstorms.md`
- execution_base: `feature/project-resolution-defaults-20260320-0005`
- integration_target: `develop`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 的 CLI-first 人类入口已经可用，但默认项目解析仍然需要被固定为：

- `--project` 是 override，不是日常默认必填。
- `chat` / `tui` / `intake status` / `status` 应优先解析当前项目。
- 只有一个已授权项目时，CLI 可以在外部目录回退到该项目。
- 解析逻辑不能把任意目录误判为项目。

## Scope

1. 把共享 resolver 的默认行为写进脚本级回归。
2. 覆盖当前 git root / 当前目录子路径 / 单一已授权项目回退。
3. 明确解析失败时仍要求显式 `--project` 或 `FREELY_PROJECT`。
4. 让 candidate / milestone / issue 的状态一致。

## Acceptance

- 在已初始化项目的任意子目录内，`freely baseline-status` / `freely chat` / `freely tui --once` 不需要显式 `--project`。
- 在当前目录之外、但 `FREELY_HOME` 中只有一个已注册项目时，`freely baseline-status` 可以自动回退到该项目。
- 当存在多个候选项目时，解析仍然失败并要求显式输入。
- 脚本回归覆盖上述行为。

## Verification

- `docs/system/workspace/scripts/tests/test-freely-project-resolution-defaults`

## Completion

- `docs/system/workspace/scripts/runtime/freely` already had the shared resolver for `--project`, `FREELY_PROJECT`, current git root, current directory, and single registered project fallback.
- `docs/system/workspace/scripts/tests/test-freely-project-resolution-defaults` now locks cwd auto-resolution and single authorized project fallback into regression coverage.
