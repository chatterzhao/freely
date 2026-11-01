- issue_id: I-20261101T031502Z-A

# Implementation Decision Note

## Implementation Decision Note

- decision: 把 Super-agent 对比研究物化为 I-20261101T031502Z-A，并在同一 issue 落 P0 实现 `freely harness-status`；覆盖理念、实现质量（路由/交接/缓存）与 harness 抽象。C-B/C/D 是 `proposed` 的下一阶段任务，不再停在“继续研究”。
- why_this: 研究已经给出明确结论（缺 ownership、缺类型化交接、缺能力契约），P0 可以把“能力与缓存不可观测”变成可运行探针；P1/P2 再改 A2A/scan/prompt。这样研究有交付，而不是只产出待办。
- alternatives_considered:
  - 直接 promote C-B：链路标准，但会产出一份没有行为盘点的 follow-up 协议设计，pre-tests 无法真实覆盖。
  - 直接 promote C-D：会把“基座抽象”做成未验证的接口，容易先写死 adapter 再发现能力矩阵不成立。
  - 走 doc-only 分支：最快，但 raw issue 无法吸收，candidate 失去 scan 入口。
  - 不建 I-*：无法通过 pr-create 的 absorbed 检查，也无法承载 B2 验收。
- boundary_non_goals: 本 issue 覆盖文档、概念映射、两张对比图、candidate 任务拆分，以及只读的 P0 `harness-status`；不改 A2A、scan、agent 提示词、ACP adapter 行为，也不实现 DSH adapter。
- residual_risk:
  - C-A 是“研究 + P0 探针”，不是 P1 能力实现；后续 C-B/C/D 需要新 issue，不能复用本 issue 的完成状态。
  - P0 的能力矩阵是手工维护的保守表，adapter 升级后必须同步，否则会给出过时能力。
  - 实测 cache hit/miss 全为 0 说明当前 adapter 未上报字段；`harness-status` 只能暴露“不可观测”，不能替代 provider 侧修复。
  - 文章原文未直接获取，依赖两篇二次报道；已在研究文档声明，并在两篇一致时才引用。
  - 原型只做静态阅读，未运行真实仓库；“已实现”只表示代码/文档存在；性能与缓存结论未实测。
  - DSH adapter 的 in-process/子进程选择只有设计判断，C-D 需要 spike 验证。
  - archify `visual-check` 因本机无 Chrome 被跳过；交互 HTML 的 9 项 composition 校验通过，静态 SVG 已栅格化目检。
