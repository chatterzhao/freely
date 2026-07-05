# Issue: chat-triggered-worker-runtime-reactivation-governance

- issue_id: `I-20260321-1706`
- title: Chat-triggered worker runtime reactivation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `chat-triggered-worker-runtime-reactivation-governance`
- issue-name: `chat-triggered-worker-runtime-reactivation-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/code-reviews`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260321-1706/candidates.md#c-20260321-1706-a`
- source_brainstorm: `docs/B1-docs/raw-20260321-1706/brainstorms.md`
- execution_base: `feature/codex-session-reentry-and-pty-input-20260321`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://manual-author-session", role: "author"}

## Why

真实狗粮表明：worker 工位在 `operator_stop` 后，`freely chat` 虽然能 durable 接住新 signal，并通过 interruption dispatcher 归类成 delegated continuation / verification handoff，但不会把 worker 主循环重新拉起，导致插话只堆积在 intake，没人真正接棒。

这会破坏 Freely 的产品语义：如果 `chat` 是正式入口，那么当 signal 明确要求当前 worker 继续做事时，runtime 必须在安全条件下重新激活正确的 worker loop。

## Scope

1. 明确 worker 工位的 chat-triggered runtime reactivation gate。
2. 区分：
   - `operator_stop`
   - `auth_failure`
   - `runtime-owned crash`
   - 当前已有 active AI
3. 明确哪些 delegated absorption target 会触发 worker re-entry：
   - `handoff://continuation`
   - `handoff://verification`
   - 其他 target 是否排除
4. 定义 reactivation 在 runtime 中的责任归属：
   - chat entrypoint preflight
   - dispatcher
   - watchdog
5. 补脚本级验证，覆盖 stopped worker + chat continuation/verification 的真实重入路径。

## Acceptance

- `freely chat` 在 worker 工位上，不再只会把 signal durable 写入 intake。
- 对需要本工位继续推进的 delegated continuation / verification handoff：
  - 若 worker runtime 未运行，runtime 会在安全条件下重激活主循环。
- 对不应自动重启的场景：
  - truth sources 明确写出 gate 与原因。
- 若当前已有 active AI，则不能重复拉起第二个主循环。
- review / progress / milestone 会记录真实狗粮验证结果。

## Verification Summary

- runtime 已 materialize chat-triggered worker runtime reactivation gate。
- gate 只对当前工位的 worker-owned `handoff://continuation` / `handoff://verification` 生效。
- 仅在 `operator_stop` 且无 active supervisor / ai 时自动重激活。
- `auth_failure` 与 active AI present 场景均保留为不自动重激活。
- 脚本级验证已覆盖 stopped worker re-entry 与 auth failure negative path。
- 真实狗粮验证已确认：`freely stop -> freely chat -> freely live-status` 会重新拉起本工位 worker supervisor / AI。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/progress/workspace-routing-foundation/p-chat-triggered-worker-runtime-reactivation-governance.md`
- `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/code-reviews/20260321-chat-triggered-worker-runtime-reactivation-verification.md`
