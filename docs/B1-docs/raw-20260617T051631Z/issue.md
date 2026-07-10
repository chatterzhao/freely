---
local_id: raw-20260617T051631Z31Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T051631Z-A
platform_ids:
  github:
    issue_id: '2892'
    url: https://github.com/chatterzhao/freely/issues/2892
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T05:16:48Z'
updated_at: '2026-06-17T05:16:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`src/frontend_probe_v0/AppShell.tsx` 第 208 行中，Project Switch 下拉框的项目列表是硬编码的：

```tsx
{["freely", "freely-sandbox", "frontend-probe-demo"].map(...)}
```

## 期望

项目列表应从运行时配置或后端 snapshot 中动态获取，而非硬编码在前端代码中。这样 Freely 管理多个项目时，前端 probe 能自动发现并切换。

## 影响范围

- `src/frontend_probe_v0/AppShell.tsx` — Project Switch select
- 可能需要 adapter/contract 层支持项目列表查询
