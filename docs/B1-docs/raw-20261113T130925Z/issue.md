---
schema_version: '1'
local_id: raw-20261113T130925Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T130925Z-A
platform_ids:
  github:
    issue_id: '4349'
    url: https://github.com/chatterzhao/freely/issues/4349
    synced_at: ''
  gitee:
    issue_id: IKV7VC
    url: https://gitee.com/zhaoquan/freely/issues/IKV7VC
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261113T130925Z/issues/I-20261113T130925Z-A.md
last_synced_comment_at:
  github: '2026-11-13T13:28:50Z'
  gitee: '2026-11-13T13:28:50Z'
hash: ''
created_at: '2026-11-13T13:09:25Z'
updated_at: '2026-11-13T13:28:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T130925Z-A
source_candidate: ''
completed_at: '2026-11-13T13:28:49Z'
closeout_note: ''
severity: P1
---

# fix: issue-sync batch 不关闭首次同步的 completed linked，本地终态与平台无法对齐

workflow_kind: fix

## fix: issue-sync batch 不关闭首次同步的 completed linked，本地终态与平台无法对齐

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T130925Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T13:09:25Z |
| updated | 2026-11-13T13:09:25Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T130925Z`。实现前请用 `wt-create --raw-key 20261113T130925Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

用户要求「同步本地与平台 issue 状态并对齐」，执行唯一的设计入口：

    ./bin/freely issue-sync --project <工位> batch

结果：

    [issue-sync] batch: 8 issue(s) to process (865 skipped as closed)
    [issue-sync] progress: 8/8

**0 条 close / 0 条 create / 0 条 update**，8 条全部静默跳过。本地 `phase_state: completed` 的 linked（#4330 / #4332 / #4334 / #4340）平台仍 OPEN。

## 根因（已定位）

`bin/issue-sync.d/cmd-batch.sh` 的 `linked)` 分支：

    if _changed_since_last_sync "$local_id" "$issue_file"; then
        cmd_update "$local_id" || true
        if [[ "$phase" == "completed" ]]; then
            cmd_close_linked "$local_id" || true
        fi
    fi

而 `lib-state.sh::_changed_since_last_sync`：

    # No previous hash = first sync of this issue. Consider it unchanged
    # to avoid spamming updates on initial batch run.
    [[ -z "$last_hash" || "$last_hash" == "None" ]] && return 1

因此**首次同步（scan-state 无该 issue 记录）时永远判 unchanged**。而这些 I-* 在 promote 时就已是 `completed`，之后内容不再变化 → 永远不会进入 close 分支。

## 与设计意图的矛盾（已核实）

- `bin/issue-sync` 头注释：`promotion_finalized (absorbed/open) → configured-platform close (absorbed/closed)`；
- `cmd-batch.sh` 的 linked 分支注释就是「complete 后关闭」，说明作者意图是 **linked 到达 completed 就应关闭**；
- `wt-close` Phase 3 也写明「Raw and linked issue metadata must already be terminal before cleanup」——终态本地与平台必须一致。

「终态应关闭」是**状态判据**，不应被「内容 hash 变化」这个**变更判据**挡住。当前实现把两者混在同一个门里。

## 影响

- 本地 completed 的 linked 永远无法通过设计入口关闭，只能靠 `wt-close` 针对**当前 raw** 的 children 关闭（R33.15 已实现的 Phase 2.5）；对**已收口 raw 的历史 children**（工位已删）无效。
- 结果就是长期累积的「linked 残留」，与 goal 的完成判据（平台 closed）冲突。
- `scan` 也会因为 `last_sync_at: never` + 空 scan-state 把所有历史文档当变更，跑 `batch` 时噪声大、但真正该关的 linked 又被跳过。

## 期望

1. 把「终态关闭」从「内容变更」中解耦：`linked` 分支在 `phase_state == completed && platform_state != closed` 时应直接 `cmd_close_linked`，**不依赖** `_changed_since_last_sync`（关闭本身是幂等的）。
2. `_changed_since_last_sync` 的「首次不刷屏」语义只约束 `cmd_update`，不约束 close。
3. `batch` 输出统计（closed/created/updated/skipped）并打印每条 close 的 local_id，避免「8 条处理但什么都没做」的黑箱。
4. AT：
   - 首次同步（无 hash）且 `phase=completed, platform_state!=closed` → 必须关闭且 adapter 被调用；
   - `phase=in_dev` → 不关闭、不写平台（负向控制）；
   - 已有 hash 且内容未变但 phase completed → 仍关闭（幂等）；
   - 基线（develop）同场景必须 0 关闭（红）。

## 边界

- 不改 `cmd_close` 对 linked 的拒绝（直连仍应走 batch）；
- 不放宽 raw 的 strict 契约与 `cmd_close_linked` 的 Phase 1 校验；
- 不改 `_raw_effect` / adapter；
- 修复后用它完成一次真实对齐（#4330 / #4332 / #4334 / #4340 等）。

### comment-20261113T132850Z
- source: system
- event: promote_finalized
- children: ["I-20261113T130925Z-A"]

拆解为以下任务:
1. [I-20261113T130925Z-A](will-be-updated)
