---
schema_version: '1'
local_id: raw-20261107T133328Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261107T133328Z-A
platform_ids:
  github:
    issue_id: '4221'
    url: https://github.com/chatterzhao/freely/issues/4221
    synced_at: ''
  gitee:
    issue_id: IKTO77
    url: https://gitee.com/zhaoquan/freely/issues/IKTO77
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/governance/raw-20261107T133328Z/issues/I-20261107T133328Z-A.md
last_synced_comment_at:
  github: '2026-11-07T13:39:26Z'
  gitee: '2026-11-07T13:39:26Z'
hash: ''
created_at: '2026-11-07T13:33:28Z'
updated_at: '2026-11-07T13:45:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261107T133328Z-A
source_candidate: ''
completed_at: '2026-11-07T13:39:25Z'
closeout_note: ''
---

# fix: wt-close 复制评论 resolution 逻辑，把系统事件评论当人类评论并阻塞收口

workflow_kind: fix

workflow_kind: fix

## 根因

`wt-close` 在 Phase 0 自己复制了一份「人类评论是否都有 resolution」的判定：

- `docs/system/workspace/scripts/worktree/wt-close:454-462`
  - `_unresolved=$(echo "$_raw_text" | grep -c "^### comment-" || true)`
  - `_resolved=$(echo "$_raw_text" | grep -c "^#### resolution-" || true)`
- 同一判定在 `docs/system/workspace/scripts/quality/comment-resolution-scan.py`（pr-create-guarded Step 2e 使用）也有实现。

两份实现都不区分「系统事件评论」与「人类评论」。`promote` / `promote_finalize` 会写入 `### comment-<ts>` + `- source: system` 的机器评论，于是：

- 系统评论被当成人类评论，要求补 `#### resolution-`；
- 而补了 resolution 又会引入「本地独有块」，让 raw 副本一致性检查（`raw_reconciliation`）再次不一致 —— 形成一个无法同时满足的闭环。

## 证据

- R13（`raw-20261104T082556Z`）真实收口：`pr-create-guarded` Step 2e 报 `1 comments, 0 resolutions — 1 unresolved`；修好 python scan 后 Step 2e 通过、PR 合并成功；
- 随后 `freely wt-close --raw-key 20261104T082556Z` 仍被同一判定阻塞（用的是 wt-close 自己的那份 copy），且报错信息本身有 bug：`$_((_unresolved - _resolved)) unresolved` 直接打印成字面量 `((_unresolved - _resolved)) unresolved`。

## 影响

- 任何经过 `promote` / `promote-finalize` 的 raw 都无法收口（wt-close 必然失败），只能 `--force` 绕过 —— 而 `--force` 会永久丢弃实现。
- 两份实现必然漂移：R13 已把 python scan 改成识别 `- source: system`，wt-close 里的 copy 仍是旧语义，两边对同一文件给出相反结论。
- 报错文案损坏，用户看不到真实的未解决数量。

## 修复方案

1. `wt-close` 不再自算，改为调用单一真源 `quality/comment-resolution-scan.py`（对整个 `docs/B1-docs` 扫一遍，只对本 issue 的命中行报错），消除第二份实现。
2. 数量与文案由 python scan 统一输出，杜绝 `$((...))` 类拼写错误进消息。
3. 补测：`- source: system` 的评论不算未解决；人类评论未标记 resolution 必须仍被拦；带 resolution 后放行；wt-close 与 pr-create 对同一文件结论一致。

## 验收标准

- RED：构造一个只有系统事件评论的 raw，`wt-close` 当前阻塞（rc≠0）；同一文件 `comment-resolution-scan.py` 在修复前也判未解决。
- GREEN：上述 raw 的 `wt-close` 评论检查通过（rc=0），且 `- source: system` 不计入未解决。
- GREEN：人类评论无 resolution 时 wt-close 与 scan 都拦（rc≠0），补 resolution 后都放行。
- GREEN：`wt-close` 源码内不再出现 `grep -c "^### comment-"` 的重复实现。

### comment-20261107T133926Z
- source: system
- event: promote_finalized
- children: ["I-20261107T133328Z-A"]

拆解为以下任务:
1. [I-20261107T133328Z-A](will-be-updated)
