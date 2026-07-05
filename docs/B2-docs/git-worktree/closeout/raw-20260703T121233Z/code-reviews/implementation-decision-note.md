- issue_id: I-20260703T121233Z-A
## Implementation Decision Note
- decision: 三个修复——补全 pkill 模式 + pid 文件 guard + bridge 归一化比较
- why_this: 最小改动，不改架构，每个修复 <= 10 行
- alternatives_considered: 进程组杀（pgid）→ 否决（nohup 子进程不在同一组）；合并 watchdog → 否决（职责不同）
- boundary_non_goals: 不改变 watchdog 架构，不改变 bridge 启动流程
- residual_risk: opencode pkill 模式太宽（匹配所有 opencode 进程），可能误杀其他项目的 ACP
