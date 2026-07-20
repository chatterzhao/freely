- issue_id: I-20260720T032133Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T032133Z/issues/I-20260720T032133Z-A.md
- phase_state: done_b2_ibm

## Implementation Decision Note

- decision: 在Manager prompt中注入委派vs插话决策规则，不增加硬编码去重
- why_this: 参照Routa设计——AI基于agent_working + a2a_tasks视图自行判断。硬编码去重会堵死session/prompt插话/纠正/澄清通道
- alternatives_considered: 在worker_launch加agent_working检查硬拦截——驳回，会阻止合法的prompt跟进
- boundary_non_goals: 不改worker_launch逻辑；不改a2a_tasks结构；不改agent_working
- residual_risk: AI可能仍忽略规则——通过Runtime防御层（后续issue）兜底
