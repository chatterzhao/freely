# Implementation Decision Note
- issue_id: I-20260708T211928Z-A
- decision: parse_frontmatter bullet补充YAML + _detect_station is_linked分流 + 所有命令用--kind fix
- why_this: I-* issue的mixed YAML+bullet格式导致phase_state读为空; raw/linked未区分导致分类错误; 旧参数--skill已废弃
- alternatives_considered: (1)只修parse_frontmatter不修分类→I-*仍误判;(2)只修分类不修参数→命令无效
- boundary_non_goals: 不改scan分类三大类逻辑;不改platform-adapter集成;不改A2A检查
- residual_risk: 现有I-* issue的phase_state准确性依赖原始文档——若文档本身错误, 分类也会偏差
