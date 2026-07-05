---
local_id: raw-20260630T224941Z41Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T224941Z-A
platform_ids:
  github:
    issue_id: '3669'
    url: https://github.com/chatterzhao/freely/issues/3669
    synced_at: ''
  gitee:
    issue_id: IJXYCA
    url: https://gitee.com/zhaoquan/freely/issues/IJXYCA
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T22:50:02Z'
updated_at: '2026-06-30T22:50:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景
config.toml.example 多处注释不准确、字段缺失、缺少影响说明。init 不能从无到有创建 config.toml。

## 要做的
### config.toml.example
- 新增 FREELY_ACP_*_BIN 字段（第十六节）
- 全面审查各字段在代码中的实际用法，修正注释
- 固定值字段填写正确默认值
- 说明不填/填错的影响
- 区分 init 自动填入 vs 用户手写

### init 逻辑
- 无 config.toml: 从 example 复制 → 自动填 PROJECT_ROOT/INTENT_FILE/CONSTITUTION_FILE/FREELY_HOME → 提示编辑
- 有 config.toml: 只补缺失 ACP 字段，不动已有值
- --reset: 备份(时间戳) → example 覆盖 → 同无 config.toml 流程
- --auto --reset: 自动确认 | 无 --auto: y/N 交互 30s 超时

### merge lock
- 检测真实并发 vs 死锁 → 清晰提示 + 清理指引
