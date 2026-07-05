# Progress: freely-start-auto-recovery-rootcause-governance

- issue_id: `I-20260414-0255-A`
- issue_path: `docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- title: `Freely start after-failure recovery handoff race root cause fix`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/freely-start-auto-recovery-rootcause-20260414`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260414-feature-freely-start-auto-recovery-rootcause`
- updated_at: `2026-04-14T18:28:01-07:00`
- session_refs:
  - {tool: codex, session_id: "019d8eb1-9e18-79b3-ade1-dcda6ca675eb", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T18-11-38-019d8eb1-9e18-79b3-ade1-dcda6ca675eb.jsonl", role: "continuation-author"}
  - {tool: codex, session_id: "019d8e74-3acf-7ca3-a2c4-a184a928c9f1", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T17-04-35-019d8e74-3acf-7ca3-a2c4-a184a928c9f1.jsonl", role: "continuation-author"}
  - {tool: codex, session_id: "019d8ca9-5ac6-74d1-858d-38f1a1937a69", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T08-43-22-019d8ca9-5ac6-74d1-858d-38f1a1937a69.jsonl", role: "author"}

## Summary

IBM 已完成 materialization。当前 issue 仍处于 feature lane 的 `dev-loop` closeout：主实现和一组 focused verification evidence 已落地，但 feature-lane verification / promote / post-merge tasks 仍未收口。本轮先按 `context compacted` 治理刷新 progress continuity，补齐 delegated continuation `healthcheck14/15` 的 run-dir 证据，再继续针对当前 runtime/test 脏改动执行最小 feature-local verification。

**Checkpoint 2026-04-14T18:28:01-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`当前输入同时命中项目级 AGENTS 首跳、fresh-session `context_compacted` handoff、delegated continuation `healthcheck15`，以及当前 milestone/progress 都把 `I-20260414-0255-A` 标成 `in_dev`；在 `MANAGER_MODE=false` 且当前仍位于 owner feature worktree 的前提下，优先级最高的需求池是 progress/recovery continuation，其次才是 milestone closeout、tests/reviews 与 promote 准备，因此保持 worker reentry scope，在当前会话直接继续 `freely-dev-loop-execution` 是最小正确动作`
- priority_pools:
  - `progress / recovery`
  - `human chat / session evidence`
  - `review / test / acceptance`
  - `docs/milestones.md`
  - `docs/PROJECT_INTENT.md`
  - `github issue` not currently authoritative for this round
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- next_prompt=`继续当前 issue 的 dev-loop：在本工位吸收 fresh-session continuity 与 delegated healthcheck14/15，随后对当前 runtime/watchdog/codex-after-failure 改动运行最小 feature-local 验证，并把结果回写到 progress；不要扩成 manager patrol、cleanup queue 或新的 doc-loop。`
- fresh handoff absorbed:
  - previous_tool_session_id=`019d8ebd-36ee-7a43-b4a4-507cc3025c24`
  - previous_cycle_log=`.freely/logs/cycle-20260414-182415.log`
  - previous_cycle_debug_log=`.freely/logs/cycle-20260414-182415.debug.log`
  - rotation_reason=`context_compacted`
  - summary_target_hint=`dev-loop: update progress first`
  - recent_output_excerpt=`fresh session after compacted handoff; progress refreshed before expanding verification scope`
- delegated continuation absorbed:
  - `.freely/run/healthcheck14.txt` created with `ok`
  - `.freely/run/healthcheck15.txt` created with `ok`
  - `preemption-state.env` points to intake `20260414-182550-issue-freely-run-healthcheck15-t`
  - note: `healthcheck14` had an existing delegated resolution artifact but missing run-dir file; this round restores the missing file evidence before continuing verification
- worktree hygiene snapshot:
  - current_project_dirty_entries=`7`
  - project_worktree_summary=`total=2; dirty=2`
  - checkpoint_judgement=`continuity updated first; dirty scope still maps to the active issue, so no split worktree or manager reroute is required before feature-local verification`

**Checkpoint 2026-04-14T18:12:53-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`当前输入先命中项目级 AGENTS 首跳治理、delegated continuation `healthcheck11/12/13`、以及 fresh-session `context_compacted` handoff；milestone 和 progress 都明确当前 owner issue 仍是 `in_dev`，因此最小正确动作是在当前 worktree 继续 dev-loop continuity，先补 recovery/run-dir 证据，再做与当前脏改动直接对应的 feature-local verification`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- fresh handoff absorbed:
  - previous_tool_session_id=`019d8eb1-9e18-79b3-ade1-dcda6ca675eb`
  - previous_cycle_log=`.freely/logs/cycle-20260414-181135.log`
  - previous_cycle_debug_log=`.freely/logs/cycle-20260414-181135.debug.log`
  - rotation_reason=`context_compacted`
  - summary_target_hint=`dev-loop: update progress first`
  - recent_output_excerpt=`Codex usage limit reached; reconnect attempts followed, so this round must refresh progress before expanding scope`
- delegated continuation absorbed:
  - `.freely/run/healthcheck11.txt` already present with `ok`
  - `.freely/run/healthcheck12.txt` already present with `ok`
  - `.freely/run/healthcheck13.txt` created with `ok`
  - `preemption-state.env` and `session-state.env` both point to intake `20260414-172942-issue-freely-run-healthcheck13-t`
- worktree hygiene snapshot:
  - current_project_dirty_entries=`7`
  - project_worktree_summary=`total=2; dirty=2`
  - checkpoint_judgement=`continuity update required before more implementation; dirty scope remains inside the active issue so no split worktree is needed yet`

**Checkpoint 2026-04-14T17:35:00-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`用户指出当前坏号已漂移到 worahe1000；真实重放后确认更深一层退化不是 failure label，而是 codex after-failure next-slot 仍会先看 availability cache，导致 1012 / a1018-1 这类 saved slot 被预跳过；当前最小正确动作是在现有 worktree 内把 after-failure contract 收紧为“严格按 saved-slot 顺序逐个运行”`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- latest real-env verdict:
  - manually verified bad slots: `account-worahe1000@outlook-com-1`, `account-worahe1012@outlook-com-1`, `apikey-codex-a1018-1`
  - saved codex inventory truth: `worahe1000 -> worahe1001 -> worahe1002 -> worahe1012 -> a1018-1 -> a1018-2`
  - pre-fix runtime replay skipped `worahe1012` and `a1018-1` because `select_next_codex_slot()` filtered through `codex_slot_is_available_now`
  - post-fix runtime replay now runs `worahe1000 -> worahe1001 -> worahe1002 -> worahe1012 -> a1018-1` in order before exhausting codex
  - note: this replay did not produce a new `healthcheck` artifact because every currently saved codex slot and downstream tools remained unavailable; runtime was stopped after the traversal proof to avoid token waste

**Checkpoint 2026-04-14T17:25:00-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`真实环境重复启动后确认，旧问题不是 failure label 分类，而是 codex 运行期 after-failure recovery 仍走了 hi-probe/saved-slot 特例，导致 slot 内循环可能回绕且拖慢跨工具外循环；当前最小正确动作是在现有 worktree 内把 codex after-failure 收回统一 next-slot contract，并用真实 freely start 回放验收`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- new root-cause verdict:
  - `codex` 在运行期失败后的 same-tool recovery 仍复用了旧的 saved-slot probe 语义，而不是统一的“切下一个 slot；没有下一个则交给跨工具外循环”
  - `select_next_codex_slot()` 旧实现允许从末尾回绕到前面 slot，和其他工具的 strictly-forward after-failure contract 不一致
- real replay verdict:
  - start slot: `account-worahe1000@outlook-com-1` (bad)
  - same-tool path: `account-worahe1000@outlook-com-1 -> account-worahe1001@outlook-com-1 -> account-worahe1002@outlook-com-1 -> apikey-codex-a1018-2`
  - cross-tool path: `codex -> cc -> iflow -> kiro-cli -> cc-use-codex-cli`
  - accepted task: `继续当前 issue：创建 .freely/run/healthcheck12.txt，内容仅为 ok。完成后继续保持运行。`
  - produced artifact: `.freely/run/healthcheck12.txt` with `ok`
  - final operator stop state: `desired_runtime_state=stopped`, `last_exit_reason=operator_stop`

**Checkpoint 2026-04-14T17:07:00-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`当前输入以 progress、delegated continuation 与 fresh handoff 为主；issue 边界和 IBM 产物稳定，且 AI_TOOL 仍为 codex，所以最小正确动作是在当前 worktree 内继续 dev-loop continuity，而不是切到新的 doc-loop 或 manager route`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- fresh handoff absorbed:
  - previous_tool_session_id=`019d8e74-3acf-7ca3-a2c4-a184a928c9f1`
  - previous_cycle_log=`.freely/logs/cycle-20260414-170432.log`
  - previous_cycle_debug_log=`.freely/logs/cycle-20260414-170432.debug.log`
  - rotation_reason=`context_compacted`
  - summary_target_hint=`dev-loop: update progress first`
  - recent_output_excerpt=`Codex usage limit reached; retry target Apr 16th, 2026 6:31 PM`
- delegated continuation absorbed:
  - `.freely/run/healthcheck10.txt` created with `ok`
  - `preemption-state.env` and `session-state.env` both point to intake `20260414-170442-issue-freely-run-healthcheck10-t`
  - note: control-plane truth had already marked the intake consumed; this round restores the missing file artifact so run-dir evidence and continuation bookkeeping agree again
- worktree hygiene snapshot:
  - current_project_dirty_entries=`0` before this writeback
  - project_worktree_summary=`total=2; dirty=1`
  - checkpoint_judgement=`continuity update first; current scope remains bounded to active issue continuity plus delegated healthcheck evidence`

**Checkpoint 2026-04-14T08:45:36-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`当前来源是 progress + delegated continuation；issue 边界和 docs 已完整，但 milestone/tasks 仍显示 feature-lane closeout 未完成，因此最小正确动作是继续当前 worktree 的 dev-loop continuity 与状态同步，而不是提前宣布 verification 结束`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- constitution_guard=`pass`
- laws_enforcer=`pass`
- fresh handoff absorbed:
  - previous_tool_session_id=`019d8ca9-5ac6-74d1-858d-38f1a1937a69`
  - previous_cycle_log=`.freely/logs/cycle-20260414-084319.log`
  - previous_cycle_debug_log=`.freely/logs/cycle-20260414-084319.debug.log`
  - rotation_reason=`context_compacted`
  - summary_target_hint=`dev-loop: update progress first`
- delegated continuation absorbed:
  - `.freely/run/healthcheck7.txt` present with `ok`
  - `.freely/run/healthcheck8.txt` present with `ok`
  - `.freely/run/healthcheck9.txt` created with `ok`
  - note: `session-state.env` already marked intake `20260414-084032-issue-freely-run-healthcheck9-tx` as consumed; this round reconciles the missing file artifact with that control-plane truth
- worktree hygiene snapshot:
  - current_project_dirty_entries=`1`
  - project_worktree_summary=`total=3; dirty=2`
  - checkpoint_judgement=`continuity update first; no unrelated diff splitting required yet because dirty scope remains focused to the active runtime file plus this continuity writeback`

**Checkpoint 2026-04-14T08:11:53-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`freely-dev-loop-execution`
- selected_tool=`codex`
- why_selected=`当前 issue 已有稳定边界且需要直接继续仓库内实现、测试和进度回写`
- workspace_action=`continue_current_worktree`
- execution_base=`develop`
- integration_target=`develop`
- depends_on=`none`
- fresh handoff absorbed:
  - previous_tool_session_id=`019d8c89-47e7-7bd0-b159-25f2be2e0452`
  - previous_cycle_log=`.freely/logs/cycle-20260414-080816.log`
  - rotation_reason=`context_compacted`
  - summary_target_hint=`dev-loop: update progress first`
- delegated continuation absorbed:
  - `.freely/run/healthcheck6.txt` present with `ok`
  - `.freely/run/healthcheck7.txt` present with `ok`
  - `.freely/run/healthcheck8.txt` created with `ok`
- real replay verdict:
  - start slot: `apikey-codex-a1018-1` (bad)
  - auto-recovery path: `apikey-codex-a1018-1 -> account-worahe1000@outlook-com-1 -> account-worahe1012@outlook-com-1`
  - accepted task: `继续当前 issue：创建 .freely/run/healthcheck8.txt，内容仅为 ok。完成后继续保持运行。`
  - final operator stop state: `desired_runtime_state=stopped`, `last_exit_reason=operator_stop`
- current dirty entries snapshot: runtime/monitor/interruption closeout plus focused regression tests

## Implementation Status

### 已完成

0. Fresh-with-handoff continuity refresh
   - 按 `context compacted` 治理先更新当前 progress，再继续本轮 issue
   - 吸收 delegated continuation `healthcheck9`
   - 记录本轮 Codex 显式 session evidence 与 dirty-budget judgement

0.1 Fresh-session continuation refresh
   - 吸收 `cycle-20260414-170432` 的 fresh handoff，并在当前 dev-loop continuity 中记录新的 compacted handoff 摘录
   - 创建 `.freely/run/healthcheck10.txt`
   - 对齐 run-dir 证据与 consumed delegated continuation bookkeeping，避免 `healthcheck10` 再次因为文件缺失而被误判为未落盘

0.2 Session-rotation continuity refresh
   - 吸收 `cycle-20260414-181135` 的 `fresh_with_handoff` 交接，并按 `summary_target_hint=dev-loop: update progress first` 先刷新当前 progress
   - 对齐 delegated continuation `healthcheck11/12/13` 与 run-dir 真相，其中 `healthcheck13` 于本轮补齐为 `ok`
   - 保持当前 route 为同 issue 的 `dev-loop` continuation，不把这轮 compacted handoff 误路由成新的 pre-brainstorm / IBM / manager patrol

1. IBM 文档 materialization
   - issue 文档：`docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
   - prd.md：已创建，描述核心合同和技术设计
   - pre-tests.md：已创建，包含 Unit/Integration/E2E/Real-Env 四层验收
   - tasks.md：已创建，包含实现、测试、验证、promote、post-merge 五类任务

2. Milestone 更新
   - 已把候选提升为 committed_issue `I-20260414-0255-A`
   - `phase_state=done_ibm`（文档已备齐）

3. Pre-brainstorm 状态更新
   - candidate 已标记 promoted_issue_path
   - INDEX 已更新，指向新 issue

4. Runtime/monitor 根因修复
   - `monitor-ai-cli.sh` 现在会忽略 prompt/body 回显中的旧错误文本，避免把历史 429/ERROR 误判为本轮运行失败
   - `monitor-ai-cli.sh` 在 child fast-exit 后会执行 post-exit 日志扫描，确保快速 429/配额失败仍会写出统一 failure marker
   - `freely` handoff 只注入诊断摘录，不再把整段上一轮 cycle log 递归塞回下一轮 prompt，避免 `fresh_with_handoff` 自旋膨胀
   - after-failure auto-recovery 继续沿用统一切换方法，真实回放已确认坏号后会先扫同工具 slot，再稳定落到可用号
   - delegated continuation `healthcheck9` 已与当前 run-dir 真相对齐，避免 consumed signal 与文件证据失配

4.1 Codex after-failure recovery contract fix
   - `codex` 运行期 after-failure same-tool recovery 不再走 `hi` probe / saved-slot sweep；现在和其他工具一致，只顺序切到当前后的下一个 slot
   - `select_next_codex_slot()` 改为严格向后选择，不再从末尾回绕到前面的已失败 slot
   - `switch_to_next_codex_slot()` 的 after-failure 选择现在不再预先调用 `codex_slot_is_available_now` 跳过 saved slot；它会按保存顺序把下一个 slot 真正跑起来，失败后再继续切
   - 当 `codex` 已没有下一个 slot 时，worker runtime 会直接落到统一 cross-tool fallback，而不是继续在 `codex` 内部兜圈
   - 真实环境已确认从 `worahe1000` 出发会顺序切完 `codex` 候选，再按 `cc -> iflow -> kiro-cli -> cc-use-codex-cli` 外循环推进，并最终完成 `healthcheck12`

5. 已通过的 focused regressions / verification evidence
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-codex-429`
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-error-text-echoed-from-prompt`
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-error-text-in-echoed-user-prompt`
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-cc-on-missing-api-key`
   - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-iflow-on-concurrency-limit`
   - `bash docs/system/workspace/scripts/tests/test-freely-start-watchdog-recovers-when-fallback-tool-appears-late`
   - `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
   - `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-falls-through-to-cross-tool-after-failure`
   - `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`
   - `bash docs/system/workspace/scripts/tests/test-codex-after-failure-next-slot-ignores-availability-cache`
   - `bash docs/system/workspace/scripts/tests/test-codex-select-next-slot-does-not-wrap`
   - `bash docs/system/workspace/scripts/tests/test-freely-codex-after-failure-uses-next-slot-not-probe`
   - `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
   - `bash docs/system/workspace/scripts/tests/test-freely-interruption-timeout-falls-back-to-active-worker-continuation`
   - `git diff --check`
   - real-environment replay from bad slot `apikey-codex-a1018-1`
   - real-environment replay from bad slot `account-worahe1000@outlook-com-1`

### 待完成

1. 运行 test-pre-merge 装配验证
   - 创建 test-pre-merge 批次
   - merge feature 到 batch
   - 运行 premerge-integration tests
   - merge batch 到 develop

2. Post-merge dogfood
   - real bad account replay on develop
   - freely stop verification on develop

## Current Blockers

1. 无功能性 blocker
   - 当前仅剩 premerge 装配与 protected-branch promote 流程未执行
2. 无新的功能性 blocker
   - 当前剩余工作是 feature-lane verification / promotion closeout，而不是新的实现阻塞

## Session Evidence

- 当前会话已完成：真实坏号重放、统一切号修复、prompt/handoff 膨胀修复、interruption fallback 收口、focused regressions、real-env task completion
- tool: codex
- session_id: 019d8eb1-9e18-79b3-ade1-dcda6ca675eb
- jsonl_path: /Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T18-11-38-019d8eb1-9e18-79b3-ade1-dcda6ca675eb.jsonl
- role: continuation-author
- cycle_log:
  - `.freely/logs/cycle-20260414-181135.log` fresh handoff after context compaction
  - `.freely/logs/cycle-20260414-181135.debug.log` preserved the usage-limit / reconnect excerpt that triggered the refresh
- runtime-events:
  - latest delegated continuation intake: `20260414-172942-issue-freely-run-healthcheck13-t`
  - `preemption-state.env` records `local_continuation_reentry` for the same intake
- tool: codex
- session_id: 019d8e74-3acf-7ca3-a2c4-a184a928c9f1
- jsonl_path: /Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T17-04-35-019d8e74-3acf-7ca3-a2c4-a184a928c9f1.jsonl
- role: continuation-author
- cycle_log:
  - `.freely/logs/cycle-20260414-170432.log` fresh handoff rotated after `context_compacted`
  - `.freely/logs/cycle-20260414-170432.debug.log` captured the usage-limit excerpt that triggered the fresh session handoff
- runtime-events:
  - latest delegated continuation intake: `20260414-170442-issue-freely-run-healthcheck10-t`
  - `preemption-state.env` records `local_continuation_reentry` for the same intake
- tool: codex
- session_id: 019d8ca9-5ac6-74d1-858d-38f1a1937a69
- jsonl_path: /Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T08-43-22-019d8ca9-5ac6-74d1-858d-38f1a1937a69.jsonl
- cycle_log:
  - `.freely/logs/cycle-20260414-080744.log` bad slot fast-exit -> unified tool failure marker
  - `.freely/logs/cycle-20260414-080816.log` good slot stable run with `rc=0`
  - `.freely/logs/cycle-20260414-080928.log` delegated continuation absorption
  - `.freely/logs/cycle-20260414-084319.log` context-compacted handoff with 429 excerpt carried into fresh session
- runtime-events:
  - `event=tool_auto_switch_selected ... active_slot=account-worahe1012@outlook-com-1`
  - final stop truth: `desired_runtime_state=stopped`, `last_exit_reason=operator_stop`

## Next Action

1. 核对 tasks/pre-tests 中剩余 feature-lane verification 的真实状态，优先补齐可直接在当前 worktree 运行的 feature-local regressions 或把缺口如实写回
2. 在 feature lane 完成 closeout 后，再创建 test-pre-merge 批次做装配验证
3. 批次验证通过后按 canonical promote 路径进入 `develop`

## Closeout

- completed_at: `2026-04-28`
- merge_evidence: `merged via 277378ac`
