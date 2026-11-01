- issue_id: I-20261101T031502Z-A

# Implementation Decision Note

- decision: 把 Super-agent 对比研究作为独立研究交付物物化为 I-20261101T031502Z-A；研究同时覆盖理念、实现质量（路由/交接/缓存）与 harness 抽象，三个 candidate 保持 `needs_research`，不 promote、不实现。
- why_this: 研究已经有可执行验收（结构、概念映射、图产物、治理门禁），但没有可验证的运行时行为设计；直接 promote 任一 candidate 会把“待研究”伪装成“待实现”。
- alternatives:
  - 直接 promote C-A：链路标准，但会产出一份没有行为盘点的 follow-up 协议设计，pre-tests 无法真实覆盖。
  - 直接 promote C-C：会把“基座抽象”做成未验证的接口，容易先写死 adapter 再发现能力矩阵不成立。
  - 走 doc-only 分支：最快，但 raw issue 无法吸收，candidate 失去 scan 入口。
  - 不建 I-*：无法通过 pr-create 的 absorbed 检查，也无法承载 B2 验收。
- boundary: 本 issue 只覆盖文档、概念映射、两张对比图、candidate 登记与治理产物；不改 runtime、A2A、scan、agent 提示词或 harness adapter。三个 candidate 的后续实现各自新开 issue。
- residual_risk:
  - I-* 与 candidate 不是 1:1 promote，后续 promote C-A/B/C 需要新 issue，不能复用本 issue 的完成状态。
  - 文章原文未直接获取，依赖两篇二次报道；已在研究文档声明，并在两篇一致时才引用。
  - 原型只做静态阅读，未运行真实仓库；“已实现”只表示代码/文档存在；性能与缓存结论未实测。
  - DSH adapter 的 in-process/子进程选择只有设计判断，C-C 需要 spike 验证。
  - archify `visual-check` 因本机无 Chrome 被跳过；交互 HTML 的 9 项 composition 校验通过，静态 SVG 已栅格化目检。
