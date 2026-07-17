---
issue_id: I-20260717T124926Z-A
issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/issues/I-20260717T124926Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T124926Z-A
- issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T124926Z/issues/I-20260717T124926Z-A.md

## Implementation Decision Note

- decision: 六缺陷单体收敛于 wt-close 单文件——替换判定语义(gate kill→先收工/branch head-1→消歧/agent_working 坟头→前置/静默 force→event),零步骤删除
- why_this: 自治化本质是"让机器可判定"——换的不是步骤是对错判据;每个改点都是局部语义替换,不改删除顺序
- alternatives_considered: 拆成独立 closeout service(改动面大,留给后续架构线,否)
- boundary_non_goals: 不改调用方/bin wrapper/runtime cmd_wt_close/a2a-exit;不删 Phase 4.5 kill(保留给 --force);不修回滚机制本身
- residual_risk: Phase 0.5 polling 在 worker 不响应时超时=120s 阻塞 wt-close 进程——可接受(closeout 低频操作);分支消歧"拒绝+输出候选"需要 agent 根据候选重新调用——新增交互但正确
