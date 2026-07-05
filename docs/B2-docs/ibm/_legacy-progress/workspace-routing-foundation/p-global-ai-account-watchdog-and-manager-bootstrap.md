# Progress: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `completed`
- runtime_state: `stopped`
- branch: `feature/upstream-governance-merge-prep-20260327`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-feature-upstream-governance-merge-prep`
- issue_path: `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "019d29a9-5895-74b0-aee5-b3d44d9f2390", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-20-57-019d29a9-5895-74b0-aee5-b3d44d9f2390.jsonl", role: "manager-closeout-audit"}
  - {tool: codex, session_id: "019d29b2-d89b-7393-9704-c7ea6cd0b526", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-31-19-019d29b2-d89b-7393-9704-c7ea6cd0b526.jsonl", role: "manager-closeout-audit-refresh"}
  - {tool: codex, session_id: "019d29b7-4cf6-7f23-a8d0-39f1176fad36", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-36-11-019d29b7-4cf6-7f23-a8d0-39f1176fad36.jsonl", role: "manager-closeout-audit-current"}
  - {tool: codex, session_id: "019d29bb-9572-74f0-99dd-3b066647ea6a", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-40-52-019d29bb-9572-74f0-99dd-3b066647ea6a.jsonl", role: "manager-closeout-audit-fresh-recheck"}
  - {tool: codex, session_id: "019d29c0-a278-7833-be12-65efef7889cd", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-46-23-019d29c0-a278-7833-be12-65efef7889cd.jsonl", role: "manager-closeout-audit-current-fresh-session"}
  - {tool: codex, session_id: "019d29f2-3953-75f2-9be9-34822f55f374", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T04-40-33-019d29f2-3953-75f2-9be9-34822f55f374.jsonl", role: "manager-closeout-audit-fleet-refresh"}
  - {tool: codex, session_id: "019d29f6-6f39-71e1-ae7a-1676f191b63c", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T04-45-09-019d29f6-6f39-71e1-ae7a-1676f191b63c.jsonl", role: "manager-closeout-audit-authoritative-refresh"}
  - {tool: codex, session_id: "019d2a17-0762-7720-80f2-03ea4786077b", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T05-20-45-019d2a17-0762-7720-80f2-03ea4786077b.jsonl", role: "manager-closeout-audit-first-jump-refresh"}
  - {tool: codex, session_id: "019d2a66-1e0b-7563-a4b7-e38b2d5d971b", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T06-47-08-019d2a66-1e0b-7563-a4b7-e38b2d5d971b.jsonl", role: "manager-closeout-audit-current-refresh"}
  - {tool: codex, session_id: "019d2c8b-59c1-7713-9f67-8ff2a6455a8c", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T16-47-03-019d2c8b-59c1-7713-9f67-8ff2a6455a8c.jsonl", role: "manager-closeout-audit-continuity-stabilization"}
  - {tool: codex, session_id: "019d2c94-db34-7012-b942-129dc5dfa98e", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T16-57-26-019d2c94-db34-7012-b942-129dc5dfa98e.jsonl", role: "manager-closeout-audit-authoritative-fleet-refresh"}

## Summary

- 2026-03-27 canonical scheduler recheck confirmed `C-20260323-2045-A` is no longer an open retained research owner. Current `develop` already requires dispatch metadata in manager/lead/lifecycle truth, `runtime/freely` now uses `unbounded` launch slots with lane-local queue guards, and both `test-freely-manager-worker-launch-capacity-queue` plus `test-freely-manager-worker-launch-busy-worker-queue` pass on canonical `develop`. Treat the older `needs_research / retained-with-reason` wording below as historical context only; this candidate is now absorbed supporting evidence and no longer part of this issue's open tail.
- 2026-03-26 22:58 PDT canonical closeout writeback rechecked `20260326-global-ai-account-watchdog-canonical-replay-verification`, `./bin/wt-status-all`, `./bin/wt-fleet-status`, and current branch ancestry. The closeout judgement is now frozen as `completed`: canonical replay already passed on `develop`, the authoritative fleet truth is now 4 worktrees / dirty=0 / all stopped, and the previous `review-ready but not promote-closed` wording is now stale. `C-20260323-2045-A` remains an independent retained research owner, but it no longer blocks this issue's completion.
- 2026-03-26 upstream absorption followthrough re-ran `./bin/wt-fleet-status`, `git merge-base --is-ancestor feature/develop-merge-prep-fleet-closure-20260325 HEAD`, `git rev-list --left-right --count feature/develop-merge-prep-fleet-closure-20260325...HEAD`, and `git rev-list --left-right --count feature/manager-scheduler-capacity-candidate-replay-20260324...HEAD`, then retired the absorbed closeout owner by deleting both its worktree and local branch. The current route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`, but the active owner has moved for good: authoritative retained fleet is now 4 worktrees, every remaining worktree is explicitly `stopped`, `feature/develop-merge-prep-fleet-closure-20260325` is no longer part of current inventory, and the only retained non-protected sibling is `feature/manager-scheduler-capacity-candidate-replay-20260324`, which still carries unresolved local-only history (`... = 24/266`) and therefore remains `needs_research / retained-with-reason`. Current closeout judgement stays `review-ready but not promote-closed`: canonical `develop` replay and develop-side completion verification still remain outstanding, but old closeout-owner cleanup has finished and no longer blocks current truth.
- 2026-03-26 current authoritative patrol re-ran `freely live-status --project ...`, `git worktree list --porcelain`, `./bin/wt-status-all`, `git status --short --branch`, and `git rev-list --left-right --count develop...HEAD`. The route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`, but the current truth now supersedes every older 7-tree / 10-tree / 12-tree snapshot: `live-status` reports `activity_state=stalled_without_runtime`, `desired_runtime_state=stopped`, `last_exit_reason=operator_stop`, and non-empty `pending_delegated_continuation_ids`; `git worktree list --porcelain` plus `./bin/wt-status-all` show 5 worktrees with `Summary: total=5, dirty=1`; the only dirty owner remains `feature/develop-merge-prep-fleet-closure-20260325`; and this branch now sits `ahead 167 / behind 1` relative to current `develop`.
- 2026-03-26 same-family continuation absorbed additional watchdog/control-plane evidence without opening a new issue: slot-only identity with `auth_email` as metadata, detached manager/watchdog/dispatcher survival after manager `auth_failure`, watchdog-only `live-status` surfacing plus dispatcher-ready start gate, and slot probe timeout / `deactivated_workspace` partial-output artifacts in `.freely/run`.
- `C-20260323-2045-A` remains frozen as `needs_research / retained-with-reason`; its blocker is still canonical `develop` proof writeback for direct dispatch, queued-lane retention, and busy-worker no-duplicate-launch behavior, not replay-owner-local evidence.
- Current closeout judgement: the lane is review-ready enough for manager-owned continuity writeback, but not promote-closed and not cleanup-admissible. Protected manager merge judgement, canonical `develop` replay, develop-side completion verification, and explicit delegated-continuation absorption/closure still remain outstanding.
- 2026-03-26 16:53 PDT current continuity stabilization rechecked the delegated continuation handoff, current `live-status`, and the six-file dirty set, and confirmed no new scope drift: all remaining edits are still same-family closeout evidence for `I-20260318-1630` plus the explicit `C-20260323-2045-A` blocker carry-forward. No additional fleet truth changed after the 16:38 PDT refresh; the closeout lane therefore stays `review-ready but not promote-closed`, and the writeback is now coherent enough for protected manager merge judgement. This worktree still cannot claim cleanup, because latest-`develop` absorption, canonical replay, and develop-side completion verification remain outstanding.
- 2026-03-26 16:38 PDT current refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. The authoritative fleet truth still remains a 10-worktree inventory with `Summary: total=10, dirty=2`; only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are dirty, and the clean sibling dispositions remain unchanged. The only new truth drift is branch divergence: this replay owner now sits `ahead 162 / behind 12` relative to latest `develop`, so manager merge judgement, latest-develop absorption, canonical replay, and develop-side completion verification remain mandatory before cleanup. The scheduler candidate blocker also stays unchanged: it is still blocked on canonical `develop` proof writeback from `I-20260318-1630`, not on replay-owner-local evidence.
- 2026-03-26 05:26 PDT current first-jump refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. The authoritative fleet truth remains a 10-worktree inventory with `Summary: total=10, dirty=2`; only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are dirty. The clean sibling dispositions remain unchanged: intake stays `supervision-needed`, latest-manager-continuity stays unresolved verification/cleanup followthrough, watchdog auth-failure stays `ownership-followthrough-needed`, watchdog live-status stays `cleanup-followthrough-needed`, and the two slot-gating trees stay `supervision-needed`. This branch still sits `ahead 162 / behind 10` relative to latest `develop`, so manager merge judgement, latest-develop absorption, canonical replay, and develop-side completion verification remain mandatory before cleanup. The scheduler candidate blocker also stays unchanged: it is still blocked on canonical `develop` proof writeback from `I-20260318-1630`, not on replay-owner-local evidence.
- 2026-03-26 04:57 PDT current authoritative refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. The authoritative fleet truth remains a 10-worktree inventory, but the latest stable recheck has moved from `Summary: total=10, dirty=3` to `Summary: total=10, dirty=2`: only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are still dirty. `feature/intake-absorption-closure-governance-20260326` is now clean and sits `develop...HEAD = 1/0`, so it no longer qualifies as a dirty unpublished lane or this issue's cleanup blocker; because canonical docs still lack explicit owner/phase absorption for that branch, it stays `supervision-needed`. This branch now sits `ahead 162 / behind 10` relative to latest `develop`, so manager merge judgement plus latest-develop absorption remain mandatory before any canonical replay or cleanup claim.
- 2026-03-26 04:47 PDT current fleet-refresh session re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、`git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. The authoritative truth has moved again: fleet inventory is now 10 worktrees with `Summary: total=10, dirty=3`; dirty owners are `feature/manager-scheduler-capacity-candidate-replay-20260324`, `feature/develop-merge-prep-fleet-closure-20260325`, and `feature/intake-absorption-closure-governance-20260326`. The scheduler lane remains `needs_research / retained-with-reason` but is no longer clean, while the intake lane is currently a stopped dirty unpublished lane whose candidate / issue / milestone materialization exists only in its local uncommitted docs. This branch now sits `ahead 162 / behind 8` relative to latest `develop`, so manager merge judgement plus latest-develop absorption remain mandatory before any canonical replay or cleanup claim.
- 2026-03-26 03:53 PDT current fresh session re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、`git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. The current truth is unchanged: authoritative fleet inventory remains 7 worktrees, `Summary: total=7, dirty=1`, the only dirty owner remains `feature/develop-merge-prep-fleet-closure-20260325`, and this branch still sits `ahead 162 / behind 6` relative to latest `develop`. A fresh manager continuity / prompt pair is therefore required, but no new worker prompt is admissible.
- 2026-03-26 03:49 PDT current live recheck re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `freely live-status --project ...`、`freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance`. `live-status` remains `last_launch_kind=fresh`, `last_rotation_reason=initial_start`, and `pending_delegated_continuation_ids=none`, so the current lane continues manager-owned closeout writeback instead of reopening doc/dev-loop or emitting a new worker prompt.
- 2026-03-26 03:43 PDT current continuation re-ran `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD` after absorbing the latest manager continuity, and the route still stays `continuation -> completion_verification -> freely-worktree-maintenance-governance` with no new worker lane.
- 2026-03-26 03:33 PDT current fresh session re-ran `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD`，确认 closeout judgement 仍与 03:28 manager continuity 一致：route 继续保持 `continuation -> completion_verification -> freely-worktree-maintenance-governance`，当前 lane 不释放新 worker prompt，也不降级回新的 doc/dev-loop。
- 2026-03-26 当前 manager-owned closeout audit 已切到 authoritative active fleet 中唯一 dirty owner `feature/develop-merge-prep-fleet-closure-20260325` 继续写回；旧的 `feature/watchdog-family-replay-20260325` 已不在当前 7-tree inventory 中，因此不再作为本轮 continuation 的 branch/worktree truth。
- 2026-03-25 新 pre-brainstorm `C-20260325-0921-A` 已完成首跳判断，并作为 supporting evidence 被本 issue 吸收：
  - 当前恢复 contract 的主问题不再只是“slot-sweep-first 是否建立”，而是 probe 窗口是否真正独占、是否仍残留 cooldown 逻辑、以及 all-unavailable 时是否还会错误拉起 AI
  - 当前判断：`cooldown` 应彻底退出恢复逻辑；slot sweep / reprobe 期间必须阻塞 AI launch；all-unavailable 时 watchdog 保持活着，但 manager / worker 保持 down，直到 inventory 变化或低频 probe 找到 usable slot
  - 这意味着本 issue 当前不进入 merge judgement，而是先回到 doc-loop + dev-loop 完成 strict probe-gating rewrite
- 2026-03-25 当前 worktree 正在做这一轮 stricter rewrite：
  - 已先更新 pre-brainstorm、issue、pre-tests、tasks、progress、milestones，把 no-launch probe-gating 和 wake-only recovery 固定为 acceptance contract
  - 已完成 `availability-watchdog.sh`、`runtime/freely`、`ai-cli` 和 focused regressions 的收口，去掉 cooldown 逻辑残留并补上 all-unavailable / inventory-change wake 验证
- 2026-03-25 live 调查又暴露出一条更底层的 identity 漂移，当前已吸收到同一 issue：
  - `./bin/ai switch` / `whoami` 现场出现 `Current slot = worahe3977@outlook-com-2`，但 `Current account = worahe3976@outlook.com`
  - 逐个解码 `~/.ai-auth/codex-*/auth.json` 后确认，这不是 runtime 读错 active slot，而是 slot 目录本身可以承载与目录名不同的授权邮箱；同一个邮箱/`account_id` 也可出现在多个 slot
  - 结论是 slot 仍然正确，错的是 CLI 把授权邮箱元数据冒充成“当前身份”；当前批次已把 `ai-cli` 的 `whoami`/`switch`/`status`/`save`/`login` contract 改回 slot-first，邮箱仅保留为 `auth_email` 元数据
- 本轮 continuation 吸收过 delegated handoff 中一组较早的恢复 contract，并确认这些旧语义已落在当前分支祖先、随后又被更严格的 slot-sweep-first rewrite 吸收：
  - 较早版本曾在 all accounts unusable 时回到 earliest-reset 语义
  - 较早版本曾使用 `reset_at + 60s` buffer 与 cooldown elapsed 后 reprobe/reselect 的等待逻辑
  - wait 期间周期性真实 reprobe，任一已保存账号恢复可用即可提前唤醒
  - `ensure-manager.pid` 只代表 live watchdog，stale pid 会被覆盖并在退出时清理
  - 当前 canonical contract 不再把 earliest-reset / cooldown wait 当作主恢复决策；它们仅保留为被 strict probe-gating rewrite 吸收的历史背景
- 当前轮次已经补齐 canonical writeback，纠正 issue / milestone / code-review 与实际 continuation 状态之间的漂移。
- 2026-03-24 fresh session 因上一轮 `context_compacted` 交接被重新拉起后，先按 continuity guard 重跑聚焦验证，再继续保持当前批次 `in_verification` / manager merge review 待处理结论。
- 本轮继续吸收 fresh-session verification 新暴露出的收口缺口：
  - `test-freely-rate-limit-defers-to-watchdog` 的整秒计时断言存在秒边界抖动，已改成 monotonic 毫秒阈值
  - `ensure-manager` 与 earliest-reset 回归已补 manager bootstrap handoff artifact 断言，锁住 `trigger/account/reason/next_action` 契约
  - 手工或自动账号切换 sweep 期间，watchdog/ensure-manager 之前仍可能并发触发 `whoami/list/switch/codex exec`；当前已补 shared switch lock，让 watchdog 在 sweep 结束前延迟 probe/bootstrap，避免误把切号中间态当成新的限流/授权恢复信号
  - 当前 continuation 又补了一轮锁边界：
    - `whoami/list` 读路径也受 shared switch lock 保护，不再只靠 `switch`/bootstrap 本身等待
    - watchdog `codex exec` probe 现在会持有 shared lock 直到 probe 结束，避免 manual sweep 在 wait-return 后立刻插入
    - focused tests 已覆盖 `ensure-manager` defer 期间不触发 `whoami/list`，以及 probe 自身的 defer + serialization
  - 2026-03-24 slot-only cooldown writeback：
    - `ensure_codex_slot_ready_for_manager` 现在只认 `whoami.slot` 作为 cooldown identity；授权邮箱只允许作为 `auth_email` 元数据存在
    - `select_any_available_codex_slot` 只排除当前精确 slot，不再做同 family exclusion，避免把同邮箱的 `-x` 兄弟 slot 误伤
    - 已验证 `ai-cli` 的 `login`/`switch` 入口遵守显式 suffixed slot contract，不再生成或消费无后缀目录
    - 新的 focused regression `docs/system/workspace/scripts/tests/test-freely-ensure-manager-slot-alias-cooldown` 覆盖了 slot selector / manager bootstrap 路径以及 slot-only cooldown identity
  - 2026-03-25 develop live investigation 追加了新的生产现场证据；这一段解释了为什么后续要做 slot-sweep-first rewrite，但它不再代表当前 closeout blocker：
    - canonical `whoami.slot` 当前为 `worahe3976@outlook-com`
    - canonical `ai list` 共返回 15 个保存 slot
    - canonical `.freely/run/codex-slot-cooldowns.tsv` 中有 6 个保存 slot 缺失 cooldown entry：`worahe3976@outlook-com`、`worahe3976@outlook-com-3`、`worahe3977@outlook-com-1`、`worahe3978@outlook-com-1`、`worahe3978@outlook-com-2`、`worahe3978@outlook-com-4`
    - 同时还残留 7 条不再对应保存 slot 的旧 identity entry，均为无后缀旧命名
    - 当时的现场判断是 cooldown truth 与 `.ai-auth` slot reality 漂移会阻止旧恢复路径稳定收敛；该判断后来被 strict probe-gating rewrite 吸收，现在已退为历史成因，而非当前 closeout blocker
  - 同轮还补了一条测试 tightening：
    - `test-freely-rate-limit-defers-to-watchdog` 与 `test-freely-rate-limit-log-defers-to-watchdog` 现在都直接断言 cooldown ledger 写入的是 suffixed slot key `limited@example-com-1`
    - 这把 `runtime/freely` supervisor 在 rate-limit 退出后的 slot-first 写回契约也锁住了，不再只依赖 `ensure-manager` focused regression 间接覆盖
  - 当前 continuation 继续补齐了两个 review 暴露出的缺口：
    - `ensure_manager_once()` 的 idle-manager unavailable 检查现也改成走 slot-first cooldown identity，不再用 `codex_current_account`
    - 当 `whoami.slot` 临时缺失时，cooldown identity 会回退到 `~/.codex/active-slot`，避免 rate-limit 记录直接丢失

## Verification

- `git status --short --branch`
- `git rev-list --left-right --count develop...HEAD`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-freely-watchdog-control-plane-skills`
- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch`
- `./bin/ai --quiet --format json whoami codex`
- `./bin/ai --quiet --format json list`
- compare canonical `.freely/run/codex-slot-cooldowns.tsv` entries against saved slot inventory
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-whoami-prefers-slot-identity`
- `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-watchdog-live-during-active-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact`

### Latest rerun

- 2026-03-24 02:25:39 PDT fresh session rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-watchdog-control-plane-skills` pass
  - `./bin/governance-check` pass with legacy pre-brainstorm naming warnings only
- 2026-03-24 current continuation rerun:
  - 首轮 `test-freely-rate-limit-defers-to-watchdog` 曾再次命中一次 `4s` 秒边界误报，确认问题出在测试计时口径而非 runtime 回退到本地睡眠
  - 修复后重复验证：
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass，且同时验证 wait/reprobe、stale pid cleanup、manager bootstrap handoff
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass，且同时验证可用账号切换与 manager bootstrap handoff
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` 连跑 5 次全部 pass，使用 monotonic 毫秒阈值避免秒边界抖动
  - `./bin/governance-check` pass with legacy pre-brainstorm naming warnings only
- 2026-03-25 canonical develop live check:
  - `wait_for_codex_slot_switch_idle()` 与 shared switch lock 仍在真源里，说明“切号前等待旧切号/旧 probe 结束” contract 还在
  - 但 live cooldown 账本与保存 slot 清单发生漂移，slot-first continuation 仍未完全反映到 canonical state truth
  - 当前判断：同族 continuation 需要继续围绕 slot inventory / cooldown ledger reconcile 收口，而不是新开独立 process-lifecycle candidate
  - 同轮 focused regression 重跑：
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass，且显式断言 slot key cooldown writeback
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog` pass，且显式断言 textual usage-limit fallback 也写入 slot key
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-slot-alias-cooldown` pass
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-idle-unavailable-slot-restart` pass，锁住 idle supervisor unavailable branch 的 slot-first restart 判定
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-cooldown-falls-back-to-active-slot` pass，锁住 `whoami.slot` 缺失时的 active-slot fallback
- 2026-03-25 06:05 PDT current slot-sweep-first continuation rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass，且显式验证：
    - 有 usable slot 时才切换
    - `all_unavailable` 时不再切到 earliest-reset slot
    - probe 失败后会恢复原 auth，而不是把无效 slot 留在真实 Codex 工作位
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass，且显式验证 manager bootstrap 之前会先 full sweep 并 promote 真实 usable slot
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass，且显式验证 all-slots-unavailable 后走低频真实 reprobe，而不是 cooldown-driven sleep-until-reset
  - `./bin/governance-check` pass，只有 10 条 legacy pre-brainstorm naming warning
- 2026-03-25 current slot-identity correction rerun:
  - `bash -n docs/system/workspace/scripts/runtime/ai-cli` pass
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool` pass
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-whoami-prefers-slot-identity` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass
- 2026-03-26 auth-failure control-plane continuation rerun:
  - `bash -n docs/system/workspace/scripts/runtime/freely` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-watchdog-live-during-active-ai` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `./bin/governance-check` pass，只有 10 条 legacy pre-brainstorm naming warning
- 2026-03-26 live-status / dispatcher-ready continuation rerun:
  - `bash -n docs/system/workspace/scripts/runtime/freely` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive` pass
- 2026-03-26 slot probe timeout observability continuation rerun:
  - `bash -n docs/system/workspace/skills/freely-watchdog-control-plane/scripts/availability-watchdog.sh` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass
  - `./bin/governance-check` pass with 10 legacy pre-brainstorm naming warnings only

## Next Action

- 当前 issue 已完成 canonical closeout writeback。
- 后续若同族还要继续推进，只保留两类下一跳：
  - 若 scheduler 未来还要演进，则以新的 lifecycle 承接 fairness / quota / transaction 等新边界
  - 新的 runtime/dev 缺口以新 lifecycle 承接

## 2026-03-25 Source Lane Retirement Audit

- Re-audited the remaining same-family source/supporting worktrees against this replay owner:
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-manager-runtime-process-churn-state-reconcile`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-interruption-handler-account-recovery`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-family-integration`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-strict-slot-probe-gating`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-slot-sweep-without-cooldown-governance`
- Their remaining local-only deltas are not missing desired capability in the replay owner:
  - `manager-runtime-process-churn-state-reconcile` still carries one local-only continuation commit (`d2ef386`), but this replay owner already preserves its broadened auth-failure detection plus the skip-launch/no-slot-ready regressions in canonical slot-first form
  - `interruption-handler-account-recovery` still points the interruption handler at the older account-ready path instead of the current slot-first contract
  - `watchdog-family-integration` still carries older availability-state / logging behavior that predates the current replay owner
  - `watchdog-strict-slot-probe-gating` still drops the broadened auth-failure detection and the no-launch test coverage now required by this replay owner
  - `watchdog-slot-sweep-without-cooldown-governance` is already an absorbed supporting-evidence lane; its remaining local commit is only retirement writeback, not a new owner path
- This round therefore treats all five branches as superseded local source/supporting lanes whose remaining unique commits should not be replayed onto the canonical owner.

## Revisit Trigger

- 任一 watchdog wait/reprobe 或 stale `ensure-manager.pid` 回归失败
- manager review 发现当前 doc/code/test 证据仍不一致
- `develop` 真实环境在 replay 后暴露新的 outer-watchdog/productization 缺口
- live replay 再次证明 cooldown 仍在主恢复路径上制造错误等待或错误可用性判断
