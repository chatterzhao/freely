---
local_id: raw-20260707T172110Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3815'
    url: https://github.com/chatterzhao/freely/issues/3815
    synced_at: ''
  gitee:
    issue_id: IJZHSG
    url: https://gitee.com/zhaoquan/freely/issues/IJZHSG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T17:21:31Z'
updated_at: '2026-07-07T17:21:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

scan.py 用 sys.argv[1] 取项目路径，但 shell harness 传的是 --project。project = Path("--project") 导致所有 git/gh/gitee 操作失败，返回 0 items。

## 7 个缺陷

| # | 缺陷 | 严重度 |
|---|------|--------|
| A | 参数解析 mismatch: sys.argv[1] vs --project | 🔴 CRITICAL |
| B | head_changed=False 跳过文件扫描 | 🟡 |
| C | 1b_reopen 是 dead code | 🟡 |
| D | 不检测无 raw-{key} 的平台 issue | 🟡 |
| E | 硬编码平台检测（应复用 platform-adapter） | 🟡 |
| F | agent_working import 静默失败 | 🟡 |
| G | extract_github_id 只查 GitHub（Gitee ID 漏了） | 🟡 |

## 修复方案

1. 改为 argparse --project（参照 bak.py）
2. 平台检测改用 platform-adapter.configured_platforms()
3. 平台查询改用 platform-adapter.list_open_issues()
4. 修复 1b_reopen dead code
5. extract_id 支持所有平台
6. 增加无 raw-{key} 平台 issue 检测
7. 修 agent_working import
