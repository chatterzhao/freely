## Implementation Decision Note

- issue_id: I-20260624T081358Z-A
- issue_path: docs/issues/I-20260624T081358Z-A/issue.md
- decision: skills 和 AGENTS.md 的测试描述从硬编码 daemon 改为委托 pre-tests.md
- why_this: 测试方式由改动类型和 pre-tests.md 决定，不应由 skill 文档硬编码
- alternatives_considered: 
  1. 枚举示例（CLI/daemon/库/配置）— 仍有遗漏风险
  2. 指向 B2_IBM + test-execution — 职责清晰，每层只做自己的事
- boundary_non_goals: 不改 pre-tests.md 模板格式（B2_IBM 已定义）
- residual_risk: 无。纯文档修整，不影响运行时行为
