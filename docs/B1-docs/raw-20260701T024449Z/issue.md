---
local_id: raw-20260701T024449Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T024449Z-A
platform_ids:
  github:
    issue_id: '3676'
    url: https://github.com/chatterzhao/freely/issues/3676
    synced_at: ''
  gitee:
    issue_id: IJY01L
    url: https://gitee.com/zhaoquan/freely/issues/IJY01L
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T02:45:10Z'
updated_at: '2026-07-01T02:45:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## Bug 描述

当 ACP bridge 不可用（daemon 未运行）时，`pr-review-guarded` 回退到人工审查路径，但 L506 引用了未定义的变量 `$_review_guide`，配合 `set -euo pipefail` 导致脚本 crash：

```
line 506: _review_guide: unbound variable
```

## 根因

`bin/pr-review-guarded` L506:
```bash
echo "  审查指南: $_review_guide"
```

`_review_guide` 在整个脚本中从未定义。`review_file` 等变量已正确定义（L164），只有 `_review_guide` 缺失。

## 影响

ACP 不可用时无法完成人工审查流程——脚本在打印指南前就崩溃退出。review 文档虽然可以手动写好，但脚本无法正常走完 manual_required 路径并给出 exit 0。

## 修复方案

将 L506 改为直接输出 skill 引用，不依赖变量：
```bash
echo "  审查指南: skill:freely-tdd-review"
```
