# Progress: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- runtime_state: `resumable`
- branch: `feature/develop-merge-prep-fleet-closure-20260325`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-develop-merge-prep-fleet-closure`
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
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

- 2026-03-26 17:04 PDT authoritative fleet refresh re-ran `./bin/freely live-status --project ...`, `./bin/freely fleet-status --project ...`, `git worktree list --porcelain`, `./bin/wt-status-all`, targeted sibling `git status --short`, and `git rev-list --left-right --count develop...HEAD`, and found one more truth shift that supersedes the 16:38/16:53 wording: the authoritative fleet is now 12 worktrees with `Summary: total=12, dirty=1`, and the only dirty owner is the current closeout lane. `feature/manager-scheduler-capacity-candidate-replay-20260324` is now clean again, so `C-20260323-2045-A` stays frozen as `needs_research / retained-with-reason`, but no longer as a dirty research owner; its blocker remains canonical `develop` proof writeback only. This does not change the closeout verdict: the replay owner is still `ahead 162 / behind 12`, so protected manager merge judgement, latest-`develop` absorption, canonical replay, and develop-side completion verification remain mandatory before cleanup or issue completion.
- 2026-03-26 16:53 PDT current continuity stabilization rechecked the delegated continuation handoff, current `live-status`, and the six-file dirty set, and confirmed no new scope drift: all remaining edits are still same-family closeout evidence for `I-20260318-1630` plus the explicit `C-20260323-2045-A` blocker carry-forward. No additional fleet truth changed after the 16:38 PDT refresh; the closeout lane therefore stays `review-ready but not promote-closed`, and the writeback is now coherent enough for protected manager merge judgement. This worktree still cannot claim cleanup, because latest-`develop` absorption, canonical replay, and develop-side completion verification remain outstanding.
- 2026-03-26 16:38 PDT current refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. The authoritative fleet truth still remains a 10-worktree inventory with `Summary: total=10, dirty=2`; only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are dirty, and the clean sibling dispositions remain unchanged. The only new truth drift is branch divergence: this replay owner now sits `ahead 162 / behind 12` relative to latest `develop`, so manager merge judgement, latest-develop absorption, canonical replay, and develop-side completion verification remain mandatory before cleanup. The scheduler candidate blocker also stays unchanged: it is still blocked on canonical `develop` proof writeback from `I-20260318-1630`, not on replay-owner-local evidence.
- 2026-03-26 05:26 PDT current first-jump refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. The authoritative fleet truth remains a 10-worktree inventory with `Summary: total=10, dirty=2`; only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are dirty. The clean sibling dispositions remain unchanged: intake stays `supervision-needed`, latest-manager-continuity stays unresolved verification/cleanup followthrough, watchdog auth-failure stays `ownership-followthrough-needed`, watchdog live-status stays `cleanup-followthrough-needed`, and the two slot-gating trees stay `supervision-needed`. This branch still sits `ahead 162 / behind 10` relative to latest `develop`, so manager merge judgement, latest-develop absorption, canonical replay, and develop-side completion verification remain mandatory before cleanup. The scheduler candidate blocker also stays unchanged: it is still blocked on canonical `develop` proof writeback from `I-20260318-1630`, not on replay-owner-local evidence.
- 2026-03-26 04:57 PDT current authoritative refresh re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. The authoritative fleet truth remains a 10-worktree inventory, but the latest stable recheck has moved from `Summary: total=10, dirty=3` to `Summary: total=10, dirty=2`: only `feature/manager-scheduler-capacity-candidate-replay-20260324` and `feature/develop-merge-prep-fleet-closure-20260325` are still dirty. `feature/intake-absorption-closure-governance-20260326` is now clean and sits `develop...HEAD = 1/0`, so it no longer qualifies as a dirty unpublished lane or this issue's cleanup blocker; because canonical docs still lack explicit owner/phase absorption for that branch, it stays `supervision-needed`. This branch now sits `ahead 162 / behind 10` relative to latest `develop`, so manager merge judgement plus latest-develop absorption remain mandatory before any canonical replay or cleanup claim.
- 2026-03-26 04:47 PDT current fleet-refresh session re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、`git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. The authoritative truth has moved again: fleet inventory is now 10 worktrees with `Summary: total=10, dirty=3`; dirty owners are `feature/manager-scheduler-capacity-candidate-replay-20260324`, `feature/develop-merge-prep-fleet-closure-20260325`, and `feature/intake-absorption-closure-governance-20260326`. The scheduler lane remains `needs_research / retained-with-reason` but is no longer clean, while the intake lane is currently a stopped dirty unpublished lane whose candidate / issue / milestone materialization exists only in its local uncommitted docs. This branch now sits `ahead 162 / behind 8` relative to latest `develop`, so manager merge judgement plus latest-develop absorption remain mandatory before any canonical replay or cleanup claim.
- 2026-03-26 03:53 PDT current fresh session re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all`、`git status --short` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. The current truth is unchanged: authoritative fleet inventory remains 7 worktrees, `Summary: total=7, dirty=1`, the only dirty owner remains `feature/develop-merge-prep-fleet-closure-20260325`, and this branch still sits `ahead 162 / behind 6` relative to latest `develop`. A fresh manager continuity / prompt pair is therefore required, but no new worker prompt is admissible.
- 2026-03-26 03:49 PDT current live recheck re-read `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`, re-ran `./bin/freely live-status --project ...`、`./bin/freely fleet-status --project ...`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD`, and confirmed the route still stays `continuation -> completion_verification -> worktree-maintenance-governance`. `live-status` remains `last_launch_kind=fresh`, `last_rotation_reason=initial_start`, and `pending_delegated_continuation_ids=none`, so the current lane continues manager-owned closeout writeback instead of reopening doc/dev-loop or emitting a new worker prompt.
- 2026-03-26 03:43 PDT current continuation re-ran `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD` after absorbing the latest manager continuity, and the route still stays `continuation -> completion_verification -> worktree-maintenance-governance` with no new worker lane.
- 2026-03-26 03:33 PDT current fresh session re-ran `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD`，确认 closeout judgement 仍与 03:28 manager continuity 一致：route 继续保持 `continuation -> completion_verification -> worktree-maintenance-governance`，当前 lane 不释放新 worker prompt，也不降级回新的 doc/dev-loop。
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
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
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

### Latest rerun

- 2026-03-24 02:25:39 PDT fresh session rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills` pass
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

## Next Action

- 当前批次的 strict probe-gating contract replay 与 focused verification 已完成。
- no-launch gate、all-unavailable hold、inventory-change wake evidence 已补齐；当前 worktree 已进入 manager merge judgement / develop replay followthrough 前的 review-ready 状态，但仍保持 `in_verification`，等待 manager 吸收。
- 2026-03-26 当前首跳 closeout audit 进一步收窄了 closure judgement：
  - `git worktree list --porcelain`、`./bin/wt-status-all` 与相关 worktree `git status` 当前 authoritative fleet truth 已前移到 12 棵 worktree，latest stable recheck 现为 `Summary: total=12, dirty=1`；dirty owner 只剩当前 closeout lane。此前 continuity 中的 5-tree / 7-tree / 9-tree / 10-tree inventory，以及 04:47 PDT 写下的 `dirty=3`，都只应视为 stale history
  - scheduler replay lane 继续保持 `needs_research / retained-with-reason`，但当前已经 clean；它的 blocker 仍是 canonical `develop` proof writeback，而不是 replay-owner-local evidence
  - intake absorption closure lane 当前 `develop...HEAD = 3/0`、supervisor/AI 都 down、worktree clean；canonical docs 仍缺准确 owner/phase，因此本轮 fleet closure 只能把它视为 `supervision-needed`
  - 当前 replay owner 分支相对最新 `develop` 的分叉真相已前移到 `ahead 162 / behind 12`，因此即便 manager 认可当前 worktree 的 review-ready 状态，也还不能直接写成 “ready to merge and cleanup”；必须先吸收最新 `develop`，再做 canonical replay / completion verification
  - 两棵 develop-absorbed 20260326 watchdog companion trees 的 disposition 也已拆开：`feature/watchdog-auth-failure-control-plane-recovery-20260326` 当前仍缺 canonical branch owner/phase，因此是 `ownership-followthrough-needed`；`feature/watchdog-live-status-and-dispatcher-ready-20260326` 已有 completed canonical issue、但缺 branch/worktree cleanup 留痕，因此是 `cleanup-followthrough-needed`
  - `feature/watchdog-probe-early-deactivated-workspace-detect-20260326` 也已出现在 authoritative fleet 中，当前 `develop...HEAD = 1/1`；canonical owner/phase 仍缺，因此同样保持 `supervision-needed`
  - `feature/watchdog-slot-switch-global-launch-gate-20260326` 与 `feature/watchdog-switch-stability-and-probe-freeze-20260326` 当前虽 clean，但 canonical owner/phase 仍缺，且当前分别 `develop...HEAD = 5/0` 与 `6/1`，只能继续保持 `supervision-needed`
  - 这让本 issue 当前固定结论变成：`review-ready but not promote-closed; cleanup not yet admissible`
  - `./bin/freely live-status --project ...` 已确认 delegated continuation wave 被当前工位吸收，`pending_delegated_continuation_ids=none`，所以这一轮继续是 manager-owned completion verification / fleet closure writeback，而不是新 worker lane
  - 当前 `live-status` 继续保持 `last_launch_kind=fresh`、`last_rotation_reason=initial_start`；较早的 `context_compacted -> fresh_with_handoff` 轮换现在只保留为历史 continuity 背景，不再代表当前 runtime 真相。因此本轮 continuity 应以前述 authoritative refresh 与 `.freely/run/manager-continuity-20260326-045718.md` 为准，避免后续会话继续消费 04:47 PDT 的 stale snapshot
  - 2026-03-26 16:38 PDT current refresh 继续确认 route、dirty=2 与 scheduler blocker judgement 没有变化，但 `develop...HEAD` 已前移到 `12 162`；本轮 continuity 需以前移到 `.freely/run/manager-continuity-20260326-163850.md` 为准，并把 scheduler candidate 缺口继续明确写成 canonical `develop` proof writeback blocker
  - 2026-03-26 16:53 PDT current continuity stabilization 再次确认 delegated continuation 已被当前工位完全吸收，且六个 dirty 文档已经形成同一条 closeout writeback；因此本轮不再需要额外 worker pass，下一跳是 protected manager merge judgement，而不是继续扩写 verification 文本
- 2026-03-25 23:41 PDT 的 `402 Payment Required` / `deactivated_workspace` cycle 仍保留为历史 closeout evidence：`.freely/logs/cycle-20260325-234105.log`
  - 它解释了为什么本 issue 需要 broadened auth-failure + no-launch-until-usable-slot contract
  - 但在 2026-03-26 canonical proof wave 与 latest manager-continuity worker-consumption repair 之后，它已不再是当前 closeout 的直接 blocker
  - 当前 blocker 已收窄为 manager merge judgement、吸收最新 `develop`、canonical replay，以及 develop-side completion verification

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
