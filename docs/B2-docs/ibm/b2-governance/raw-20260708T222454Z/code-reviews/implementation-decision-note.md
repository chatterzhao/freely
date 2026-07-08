# Implementation Decision Note
- issue_id: I-20260708T222454Z-A
- decision: _sync_platform_direct 先 update 后 close；platform-only 检测通过遍历所有平台 OPEN issues 实现；逐平台状态用 fetch_issue_state
- why_this: 平台同步必须先记录状态再关闭；纯平台 issue 需要被 scan 发现才能触发后续流程
- alternatives_considered: (1)在 Manager prompt 中处理→不可靠;(2)单独脚本→重复逻辑。选择在 scan 中直接处理
- boundary_non_goals: 不改 platform-adapter API;不改 Manager prompt 模板
- residual_risk: fetch_issue_state 对每个平台逐个调用 API，大量 issue 时可能慢
