# Progress: freely-start-auto-recovery-rootcause-governance

- issue_id: `I-20260414-0255-A`
- issue_path: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- title: `Freely start after-failure recovery handoff race root cause fix`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/freely-start-auto-recovery-rootcause-20260414`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260414-feature-freely-start-auto-recovery-rootcause`
- updated_at: `2026-04-14T08:45:36-07:00`
- session_refs:
  - {tool: codex, session_id: "019d8ca9-5ac6-74d1-858d-38f1a1937a69", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/04/14/rollout-2026-04-14T08-43-22-019d8ca9-5ac6-74d1-858d-38f1a1937a69.jsonl", role: "author"}

## Summary

IBM 已完成 materialization。当前 issue 仍处于 feature lane 的 `dev-loop` closeout：主实现和一组 focused verification evidence 已落地，但 feature-lane verification / promote / post-merge tasks 仍未收口，因此本轮先把 compacted handoff 与 delegated continuation `healthcheck9` 吸收到 continuity，再继续沿现有 dev-loop 推进。

**Checkpoint 2026-04-14T08:45:36-07:00**:
- source_class=`continuation`
- route_kind=`dev_loop`
- target_skill=`dev-loop-execution`
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
- target_skill=`dev-loop-execution`
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

1. IBM 文档 materialization
   - issue 文档：`docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
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
   - `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
   - `bash docs/system/workspace/scripts/tests/test-freely-interruption-timeout-falls-back-to-active-worker-continuation`
   - `git diff --check`
   - real-environment replay from bad slot `apikey-codex-a1018-1`

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

1. 提交当前 feature worktree 的最终补丁
2. 创建 test-pre-merge 批次做装配验证
3. 验证通过后 merge 到 `develop`
