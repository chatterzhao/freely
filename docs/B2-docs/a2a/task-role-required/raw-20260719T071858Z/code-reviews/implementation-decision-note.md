---
issue_id: I-20260719T071858Z-A
issue_path: docs/B2-docs/a2a/task-role-required/raw-20260719T071858Z/issues/I-20260719T071858Z-A.md
phase_state: in_b2_ibm
---

- issue_id: I-20260719T071858Z-A

## Implementation Decision Note

- decision: prompt 模板补 --role worker + a2a_task.py --role 改为 required
- why_this: 当前 default="manager" 是 silent failure——Manager AI 按模板调用时忘传 --role，task 以错误 agent_id 创建，Runtime 查不到，Worker 永不启动，且无任何报错。改为 required 后若调用方漏传 --role 会直接报错退出，立刻暴露问题
- alternatives_considered: (A) 只在模板加 --role worker 不改 argparse default — 治标，未来新增调用方同样踩坑；(B) 改 default 为 "worker" — 错得更隐蔽，Manager 自身状态更新会受影响
- boundary_non_goals: 不修改 A2A Server 的 task 存储逻辑；不修改 Runtime 的 worker discovery 逻辑；不清理已有僵尸 task（独立 cleanup issue）
- residual_risk: 若全仓有未被 grep 发现的 a2a-exit 调用（如通过 shell 变量拼接），改为 required 后会导致该调用报错——这是期望行为，报错优于静默路由到错误 agent
