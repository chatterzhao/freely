---
local_id: raw-20260511T001900Z00Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '292'
    url: https://github.com/chatterzhao/freely/issues/292
primary_platform: github
platform_state: closed
---
sync_exit_contract_to_handoffs 用管道串两个 python3 → 2>/dev/null 吞错误 → false positive
修复: 单个 python3 直接查 SQLite，消掉管道失败模式
