---
b1_id: B1-20260719T133426Z / phase_state: completed
---
# B1: pending→submitted
A2A标准状态: submitted。pending是旧名, a2a_task.py有pending→submitted映射。
但manager_exit_contract_kind L15641/L15684直接写死--status pending。
查询永远0结果 → contract_kind永远不是delegate_workers → worker永不启动。
