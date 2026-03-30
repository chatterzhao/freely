# Issue: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `project-command-semantics-and-restore-work-governance`
- issue-name: `project-command-semantics-and-restore-work-governance`
- source_candidate: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/candidates.md#c-20260327-2006-a`
- source_brainstorm: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/brainstorms.md`
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

- `2026-03-30 16:12 PDT` parent issue 的 canonical absorption 已发生在 `develop` commit `b93efd2`。本 issue 本轮不再承担新的 runtime change；它在当前 diff 中只保留 continuity writeback，用来证明 source candidate `C-20260327-2006-A` 的 parent owner 已先落主线，而 downstream split owner `I-20260327-2006-A-global-restart` 现在才进入 active dev-loop。
- 2026-03-30 15:47 PDT manager-side merge review确认本 issue 仍不应推进到 `I-20260327-2006-B`。原因不是 owner taxonomy 回退，而是 feature-lane verification harness 需要同 issue fixup：`test-freely-project-command-semantics` 已被收紧为 signal-aware cleanup，并去掉了会把 wall time 拖到约 `46s` 的 background pid probe fd inheritance；复跑后正常路径约 `13.76s` 通过，`ALRM` 打断时返回 `142` 且不再泄露 `/tmp/freely-project-command-semantics*` watcher residue。因此当前 lane 继续是 verification closeout，不 reopen IBM，也不把 downstream global restart 拉前。
- 2026-03-29 23:25 PDT fresh session 首跳再次复核 `live-status`、milestone、progress、verification artifact 与 worker continuity 后，当前 issue 的 active route 仍是 manager-owned `completion_verification`。这次新增的 runtime 事实只是本 worker lane 现已显示 `last_ai_state=down`、`last_exit_reason=ai_exit_rc_1`；它要求 runtime/manager 侧恢复和消费现有 evidence，但不构成 reopen IBM 或重开 worker dev-loop 的理由。
- 2026-03-29 22:47 PDT 首跳闭环再次复核 `live-status`、milestone、progress、verification artifact 与 worker continuity 后，当前 issue 的 active route 仍是 manager-owned `completion_verification`；当前 prompt 里残留的 IBM delegated continuation 继续只算 supervision history，不再触发回退到 `doc-ibm-execution`。
- next_action: 当前 feature lane 已完成 checkpoint `5bc3a86` 并补齐 feature-lane verification evidence，下一跳保持 manager-owned `completion_verification`；不在本 issue 内继续扩写 runtime patch，也不回退到 IBM/doc-loop。
- revisit_trigger: 若 manager merge review 指出 verification artifact、milestone state、或 runtime/test truth 之间仍有 contract 漏洞，再回到当前 worktree做定点修补；否则由 manager 决定 closeout、merge sequencing 与后续 `I-20260327-2006-B` 的启动时机。
- downstream_note: `I-20260327-2006-B` 继续保持 downstream `done_ibm` owner，等待本 issue 的 completion verification judgement，而不是被当前 worker提前拉进新的实现批次。
