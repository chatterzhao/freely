---
local_id: raw-20260710T002224Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T002224Z-A
platform_ids:
  github:
    issue_id: '3852'
    url: https://github.com/chatterzhao/freely/issues/3852
    synced_at: ''
  gitee:
    issue_id: IK013Y
    url: https://gitee.com/zhaoquan/freely/issues/IK013Y
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T00:22:47Z'
updated_at: '2026-07-10T00:22:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
pre-scan-fix.sh 中使用了不存在的 `--skip-ibm` 参数：
- `freely feedback --skip-ibm` — feedback 不支持此参数
- `pr-create-guarded --skip-ibm` — 不存在
- `pr-merge-guarded --skip-ibm` — 不存在

## 修复
替换为 LAWS.md §304 定义的 `FREELY_SKIP_IBM_GATE` 环境变量机制：
- `freely feedback` — 正常语法（无需 skip）
- `FREELY_SKIP_IBM_GATE=1 freely pr-create-guarded`
- `FREELY_SKIP_IBM_GATE=1 freely pr-merge-guarded`

## 验收
- bash -n 语法检查通过
- 所有命令使用实际存在的参数
