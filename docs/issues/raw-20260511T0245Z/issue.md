---
local_id: raw-20260511T0245Z
kind: raw
phase_state: proposed
platform_ids: {}
---
## 问题
freely.db 路径构造分散在 19 处，格式不统一。
## 修复
抽出 project_db_path()，所有地方统一调用。
