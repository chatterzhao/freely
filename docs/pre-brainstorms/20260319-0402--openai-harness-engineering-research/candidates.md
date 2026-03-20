# Candidates

## C-20260319-0402-01：定义 Freely 的 harness engineering 分层与缺口图

- status: `proposed`
- problem: Freely 已有 worktree/governance/doc-loop 基础，但“环境设计、反馈回路、约束执行、垃圾回收”仍分散存在，缺少统一 harness 视角。
- change:
  - 产出一份面向 Freely 的 harness architecture 草图
  - 把现有能力映射到 record system / feedback loops / invariants / cleanup 四层
  - 标出当前缺失的自动化接口与治理门
- acceptance_hint:
  - 能回答 Freely 目前哪些能力已经是 agent-first，哪些仍依赖人工隐性知识
  - 后续 issue 可以按 harness 分层而不是按零散脚本推进
- decision_reason: 这是本次研究里最接近“问题定义层”的候选项；若不先统一地图，后续容易继续碎片化补控制面。
- next_action: 继续 pre-brainstorm，先把 Freely 的 harness 分层与缺口图收束成稳定问题定义；边界稳定前不要 materialize。
- revisit_trigger: 当 record system、feedback loop、invariants、cleanup 四层之间的缺口可以被明确映射到最小可执行问题时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-02：把 worktree 级验证信号统一暴露成 agent 可消费接口

- status: `proposed`
- problem: 当前 worktree discipline 很强，但 runtime、日志、dirty budget、验证状态对 agent 的读取面仍不够统一。
- change:
  - 盘点 `status`、`wt-status-all`、测试、runtime 现有输出
  - 设计统一的 machine-readable 汇总接口
  - 优先补自主循环最依赖的最小字段
- acceptance_hint:
  - agent 能在少量上下文下直接拿到当前 worktree 的可执行状态摘要
  - 恢复、验证、promotion 决策减少对人工解释的依赖
- decision_reason: 这项最直接服务“自治开发应用”的主目标，因为它减少 agent 在三层循环里判断上下文时的额外成本。
- next_action: 继续 pre-brainstorm，先盘点现有 status / wt-status-all / runtime 输出，再决定要不要 materialize 成统一 machine-readable 汇总接口。
- revisit_trigger: 当可以明确指出哪些字段必须稳定暴露给 agent，而不是继续依赖人工解释时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-03：建立文档园艺与 AI 残渣清理的周期性后台循环

- status: `needs_research`
- problem: OpenAI 的经验表明，全 agent 代码库会持续产生漂移；如果 Freely 没有自动清理环，治理成本会不断上升。
- change:
  - 识别可机械检查的文档/代码漂移信号
  - 为 doc-gardening / cleanup PR 定义触发条件与最小验收
  - 优先从过期文档、未交叉链接、命名偏差、重复 helper 等模式开始
- acceptance_hint:
  - 清理动作可以周期性运行，而不是只在人工注意到时发生
  - “治理漂移”被前移到自动发现和小步修复
- decision_reason: 方向成立，但前提是 Freely 先把反馈面和 enforcement 面统一，否则会过早进入“自动清理自动化”而缺少稳定基线。
- next_action: 保持 `needs_research`，等前两个更基础的 harness 候选边界稳定后，再决定是否 materialize。
- revisit_trigger: 当反馈面和 enforcement 面已经可稳定消费后，再回看是否需要常驻 cleanup loop。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-04：不把吞吐量叙事和全 agent 纯度当近期目标

- status: `dropped`
- problem: 外部案例容易把讨论带偏到“更多 PR、更少人工、全 agent 生成代码”，但这不是 Freely 当前阶段的核心成功标准。
- change:
  - 在后续相关 issue / brainstorm 中明确记录不采用项
  - 优先用“自治闭环是否稳定、是否可恢复、是否能开发真实应用”作为判断标准
- acceptance_hint:
  - 后续方案不再把吞吐量或 agent 纯度当作主卖点
  - 自治开发应用的控制面与恢复能力保持优先级高于速度叙事
- decision_reason: 这不是要 materialize 的功能项，而是一个需要被明确记录的研究排除项。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
