---
local_id: raw-20260710T171329Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3876'
    url: https://github.com/chatterzhao/freely/issues/3876
    synced_at: ''
  gitee:
    issue_id: IK0A7J
    url: https://gitee.com/zhaoquan/freely/issues/IK0A7J
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T17:13:51Z'
updated_at: '2026-07-10T17:13:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

.freely/ 在 .gitignore 中，但 .freely/run/test-gate.env 被 git add -f 强制追踪了。导致：
1. 每次 wt-close 时 git 检测到 dirty tracked file，gate 拦截
2. Workers 反复尝试清理工位但被 gate 阻塞
3. 旧工位无法自动收口

## 根因

test-gate.env 是运行时状态文件（daemon 启动时自动更新），不应进入 git 版本控制。git add -f 绕过了 .gitignore。

## 修复

git rm --cached .freely/run/test-gate.env 从所有工位移除追踪。
文件仍存在于磁盘（wt-create 自动创建），不影响 daemon 运行和 gate 检查。

## 验收

- git ls-files 不再包含 .freely/run/test-gate.env
- wt-close 不再因 dirty tracked file 误报
- Workers 可以正常完成 cleanup 任务
