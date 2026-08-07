---
local_id: raw-20260511T022900Z00Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '295'
    url: https://github.com/chatterzhao/freely/issues/295
primary_platform: github
platform_state: closed
---
## 问题
Worker 不知道 manager 中心 DB 路径和自己 handoff ID，无法汇报完成。
## 修复
Launch 时注入 handoff_id + db_path + 完成汇报指令到 worker prompt。
