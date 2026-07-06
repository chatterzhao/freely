---
local_id: raw-20260706T091733Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260706T091733Z-A
platform_ids:
  github:
    issue_id: '3779'
    url: https://github.com/chatterzhao/freely/issues/3779
    synced_at: ''
  gitee:
    issue_id: IJZ4R7
    url: https://gitee.com/zhaoquan/freely/issues/IJZ4R7
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T09:17:54Z'
updated_at: '2026-07-06T09:17:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
当前可通过三种方式完全绕过门禁:
1. git push/commit --no-verify → 跳过本地 hook
2. gh pr merge --admin → 跳过 CI check
3. git update-ref → 直接改 develop ref，无 hook 触发

## 修复方案
### A. CI 硬拦截 (最后防线，客户端不可绕过)
- PR Merge Guard CI: 检查每个 commit 是否有 hook 证据文件
- 无证据 → HARD BLOCK (不是 warning)
- GitHub branch protection: Require CI pass + Include administrators

### B. Workflow skill 铁律置顶
- 第一条: 改任意字符必须走完整流程
- 禁止: --no-verify, --admin, --force, gh pr merge, git update-ref

### C. 平台同步受控
- freely develop-push attempt 作为唯一合法跨平台同步入口
