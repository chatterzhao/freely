# Issue: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `project-command-semantics-and-restore-work-governance`
- issue-name: `project-command-semantics-and-restore-work-governance`
- source_candidate: `docs/B1-docs/raw-20260327/candidates.md#c-20260327-2006-a`
- source_brainstorm: `docs/B1-docs/raw-20260327/brainstorms.md`
- pre_tests_path: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "019d3752-80a1-7773-808d-081375e06aa7", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-00-47-019d3752-80a1-7773-808d-081375e06aa7.jsonl", role: "dev-loop-and-verification-writeback"}
  - {tool: codex, session_id: "019d377f-37b7-7cf2-8b76-d6a4a36a4a7f", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-49-37-019d377f-37b7-7cf2-8b76-d6a4a36a4a7f.jsonl", role: "completion-verification-continuity-refresh"}
  - {tool: codex, session_id: "019d3d46-4e39-7020-afdc-cd2f6822ae30", jsonl_path: "unavailable://live-status-deep-ref-only", role: "fresh-session-first-hop-recheck"}

## Why

Freely 已经有 project-scoped pid ownership 与 `cmd_stop()` 的底层 blast radius，但还没有冻结 `start` / `stop` / `restart` / `start --force` / `restore-work` 这组单项目命令的 operator contract。若继续缺这层 contract，project restart 很容易误触 global reset，或把 interrupted AI work 的恢复策略混成隐式副作用。

## Scope

1. 冻结单项目 command family 的 blast radius：`freely start`、`freely stop`、`freely restart`、`freely start --force`、`freely restore-work`。
2. 冻结 project-scoped 默认优先序：`attach/reuse -> local repair -> fresh bootstrap -> explicit global escalation`。
3. 定义 project force 的 safe repair set，以及它不能触碰的 shared/global assets。
4. 冻结 interrupted local AI work 的默认行为：`restart` 不静默恢复，显式恢复走 dedicated `restore-work` surface。
5. 维持 process discovery / kill scope 继续锚定 Freely-owned project identity，而不是 generic process-name matching。

## Non-Goals

1. 不在本 issue 定义 all-project global restart manifest schema。
2. 不把 slot/account watchdog、shared lock、cooldown/cache inventory 重新吸回 project command owner。
3. 不在本 issue 直接写 runtime patch 或 completion verification。
4. 不重新打开 `I-20260318-1630`。

## Completion Contract

- `start`：确保当前 project control-plane/runtime 处于 up；优先 attach/reuse healthy project-scoped components。
- `stop`：只停止当前 `--project` 归属下的 runtime/control-plane，不触碰 shared/global control-plane。
- `restart`：作为 project-scoped 一级 command surface，重建当前 project runtime/control-plane，但默认不静默恢复 interrupted AI work。
- `start --force`：强制重建当前 project runtime chain，只允许处理 project-local stale pid、idle supervisor、partial readiness 与同 project child process；不得隐式执行 global reset。
- `restore-work`：explicit project-scoped AI-work restore surface；任何 `--restore-work` 仅可作为 secondary alias，不取代 dedicated surface。

## Acceptance

- 单项目 command family 与 future global action 的 owner taxonomy 清晰分离。
- `restart` 成为显式一级 command surface，而不是长期隐藏在 `stop + start` 的 operator 口头语义里。
- `start` 与 `start --force` 不再新增第三个 repair-only 用户态 surface。
- project force 的 safe repair set 与 global-only touch list 被冻结到足以驱动实现。
- interrupted local AI work 的默认行为稳定为：project restart 不静默恢复，恢复必须显式进入 `restore-work`。
- `global restart restore memory` 只作为 downstream owner 继承本 issue 已冻结的 taxonomy，不重新定义 project blast radius。

## Next

- `2026-03-30 17:34 PDT` parent owner closeout is complete. The canonical absorption happened at `develop` merge `b93efd2`, and the verification closeout is anchored by `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md`.
- Downstream work now belongs to its own owner lifecycle. Any future change to project command semantics must open a new lifecycle instead of reopening this completed parent.
