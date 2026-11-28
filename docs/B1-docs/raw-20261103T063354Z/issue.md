---
schema_version: '1'
local_id: raw-20261103T063354Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T063354Z-A
platform_ids:
  github:
    issue_id: '4136'
    url: https://github.com/chatterzhao/freely/issues/4136
    synced_at: ''
  gitee:
    issue_id: IKSKV4
    url: https://gitee.com/zhaoquan/freely/issues/IKSKV4
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/issues/I-20261103T063354Z-A.md
last_synced_comment_at:
  github: '2026-11-28T08:12:26Z'
  gitee: '2026-11-28T08:12:26Z'
hash: ''
created_at: '2026-11-03T06:33:54Z'
updated_at: '2026-11-28T08:12:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T063354Z-A
source_candidate: ''
completed_at: '2026-11-28T08:12:25Z'
closeout_note: ''
---

# fix: pr-merge-guarded 关闭 Gitee PR 时把远端名当成平台名

workflow_kind: fix

## 现象
`freely pr-merge-guarded develop <branch>` 合并成功后输出：

    [MERGE-GUARD] closing origin PRs via platform-adapter...
    {"status": "error", "error": "unknown: origin"}

Gitee 侧 PR 实际已由平台合并关闭，但该步骤报错噪音，掩盖真实失败信号。

## 根因
合并收尾循环把 git remote 名（origin）当作 platform-adapter 的 platform 参数传入；platform-adapter 只认配置平台名（github/gitee）。

## 修复方向
1. 收尾循环使用 `configured_platforms()` 的平台名而不是 remote 名。
2. 补一条 dry-run/单测断言 close-pr 调用的 platform 参数属于 {github,gitee}。
3. 失败时输出结构化告警而不是伪错误，避免把“已由平台自动关闭”误报成 failed。

## 发现场景
2026-11-03 连续 5 次 guarded merge（owner-lane/chat-help/replica/scan/handler）均复现，PR 最终状态均为 merged。

### comment-20261128T081226Z
- source: system
- event: promote_finalized
- children: ["I-20261103T063354Z-A"]

拆解为以下任务:
1. [I-20261103T063354Z-A](will-be-updated)
