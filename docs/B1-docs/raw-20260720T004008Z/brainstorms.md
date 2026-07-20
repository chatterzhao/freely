---
b1_id: B1-20260720T004008Z / phase_state: completed / source_raw: raw-20260720T004008Z
---
# B1: launch-kind跨tool用new
L13347: --launch-kind fork硬编码。daemon日志确认跨tool发出了fork→session-id capture timeout 30s。
Routa方案: 全部用session/new,不用fork。Freely保留fork(同tool缓存命中),跨tool用new。
