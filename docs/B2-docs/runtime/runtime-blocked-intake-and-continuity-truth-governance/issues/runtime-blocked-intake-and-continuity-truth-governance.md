# Issue: runtime-blocked-intake-and-continuity-truth-governance

- issue_id: `I-20260404-1545-A`
- title: Runtime blocked intake and continuity truth governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-blocked-intake-and-continuity-truth-governance`
- issue-name: `runtime-blocked-intake-and-continuity-truth-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260404-1545/candidates.md#c-20260404-1545-a`
- source_brainstorm: `docs/B1-docs/raw-20260404-1545/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-blocked-intake-and-continuity-truth-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 现在已经分别具备：

1. execution-time network failure 的 bounded taxonomy
2. manager bootstrap prompt publication 与 continuity materialization 的启动路径
3. delegated intake absorption closure
4. latest manager continuity / worker prompt consumption truth

但 `2026-04-04` 的 canonical `develop` 现场仍暴露出一个没有 owner 的组合性缺口：

- runtime 能把新的 human intake durable 写入 `.freely/intake/*`
- prompt assembly 也能继续把这些 intake 带进新的 manager prompt
- 但 manager 无法完成 intake claim、continuity materialization、或 blocked handoff truth 写回

于是系统呈现出一种 false-active state：

- prompt 持续刷新
- intake `meta.env` 仍停在 `STATUS="new"` 或未收敛到 machine-readable blocked truth
- 没有新的 manager continuity 或等价 blocked artifact

这已经不是单纯“再识别一种 network reason”或“继续修 prompt parser”的问题，而是 runtime supervision 在 blocked execution surface 下如何维持 intake/continuity truth 的 narrow follow-on owner。

## Scope

1. 冻结 runtime blocked supervision 的最小 machine-readable truth surface：
   - prompt 已生成
   - intake 尚未 claim / absorb
   - continuity 尚未 materialize
   - 当前 recovery gate 为何阻塞
2. 冻结哪些 execution surfaces 可以进入这个 blocked state family：
   - websocket `Operation not permitted` / permission-denied execution failures
   - active shared slot-switch busy that prevents launch progress
   - local process-capacity / fork exhaustion that blocks manager execution before continuity advances
3. 冻结 blocked state 与现有 network taxonomy、semantic-loop signal、delegated intake closure 的边界。
4. 冻结 runtime 在 blocked state 下应如何收束 truth，而不是继续无限制地重发 prompt：
   - intake 不得无限停留在 misleading `new`
   - manager continuity 或等价 blocked artifact 必须说明 why + next recovery gate
   - status surface 必须能区分 “prompt assembly 正常但 claim/continuity blocked”
5. 为 follow-on dev-loop 冻结最小验证面，确保后续实现不会误把 GitHub issue automation、generic watchdog redesign 或 broader orchestration 混入本 lane。

## Non-Goals

1. 不重开 `I-20260330-2358-A` 的 generic network taxonomy、retry window 或 fallback policy。
2. 不重开 `I-20260404-1405-A` 的 bootstrap prompt publication / worker dispatch parser。
3. 不在本 owner 内重写 interruption dispatcher 或所有 intake lifecycle。
4. 不把 semantic-loop monitoring、auto-recovery orchestration、或 worker-side stalled continuation 修复吸收到本 lane。
5. 不把 GitHub issue create/sync 误写成当前 runtime 已具备的能力。

## Acceptance

1. 文档明确说明：当 prompt assembly 成功但 manager 无法 claim intake 或写 continuity 时，runtime 需要一个新的 blocked supervision truth，而不是继续表现为 generic active loop。
2. 文档明确区分：
   - execution-time network taxonomy 负责 classify + bounded retry
   - 本 owner 负责 blocked intake / continuity truth and handoff
3. 文档明确列出当前进入 blocked family 的候选触发面：
   - websocket permission denied
   - active shared slot-switch busy
   - local fork/resource exhaustion
4. follow-on implementation owner 不需要重新研究 blocked truth 应写到哪里：
   - intake status / claim reaction
   - manager continuity or equivalent blocked handoff artifact
   - live-status / fleet-status machine-readable surface
5. 文档明确禁止把本 owner 扩写为 generic watchdog redesign、broad dependency-health orchestration、或 unrelated issue automation。

## Completion

- `docs/B1-docs/raw-20260404-1545/brainstorms.md`
- `docs/B1-docs/raw-20260404-1545/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/brainstorms/b-runtime-blocked-intake-and-continuity-truth-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/prd.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-canonical-closeout-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-blocked-intake-and-continuity-truth-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-blocked-supervision-status-surface`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- milestone / candidate writeback showing this is the canonical owner for blocked intake/continuity truth under runtime supervision

## IBM Handoff

- implementation_scope_summary:
  - `I-20260404-1545-A` 负责冻结 runtime blocked supervision truth：当 prompt 可见但 intake claim / continuity materialization 没有前进时，系统应该如何 machine-readably 表达 blocked state。
  - follow-on implementation 允许同步更新 runtime status surface、blocked artifact writeback、以及 focused regressions。
  - generic network retry/cooldown policy、semantic-loop automation、worker stall recovery、GitHub issue automation 仍留在各自 owner。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/brainstorms/b-runtime-blocked-intake-and-continuity-truth-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/tasks.md`
  - `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`

## Next

- Completed on canonical `develop` via guarded merge `fd1907b`.
- This closeout also backfills the previously missing `progress` plus issue-bound verification artifacts so the governance chain is explicitly closed instead of relying on the merge alone.
- Post-merge closeout verification is recorded in `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` again leaves prompt-visible intake stuck without claim/continuity writeback, or if future work tries to widen this owner back into generic watchdog redesign or network taxonomy.

## Verification

- `git diff --check`
- `./bin/governance-check`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-test-lane`
- `bash docs/system/workspace/scripts/tests/test-freely-blocked-supervision-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- review `docs/B1-docs/raw-20260404-1545/brainstorms.md`
- review `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- review `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- confirm the resulting docs do not claim broader watchdog redesign or GitHub issue automation
