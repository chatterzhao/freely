# Implementation Decision Note
- issue_id: I-20261104T075810Z-A
- issue_path: docs/B2-docs/config/toml-parsing-robustness/raw-20261104T075810Z/issues/I-20261104T075810Z-A.md
- decision: 契约落盘为 JSON 兼容 YAML 子集；单一 stdlib 校验器承担 fail-closed 判定；doctor 只做诊断接线
- why_this: 安装态机器不保证 PyYAML，缺依赖时校验会静默跳过（正是要修的病）；`contracts/` 不随包则安装态 doctor 找不到契约（R5.5 同族坑）；doctor 是诊断命令，若因历史坏配置 exit 1 会让每轮 commit/PR/selfhost 自锁（R8 实证）。
- alternatives_considered: ①PyYAML + 完整 YAML——安装态依赖不可靠；②校验逻辑直接写进 doctor——产生第二份判定且 CI 无法单独调用；③gate 改 fail-closed——改变豁免语义且自锁每轮 PR；④doctor 因配置错 exit 1——历史配置自锁；⑤校验 runtime 的 1,521 处隐式变量——超出 config.toml 范畴。
- boundary_non_goals: 不改 gate（逐字节不动）、不改模板（已是 list）、不合并角色配置双真相（#4172）、不改 doctor 既有退出码契约。
- residual_risk: ①`_load_skip_ibm_allowed_paths()` 对非 list 仍静默回退到内置默认白名单——本轮只提供可观测性，未改变判定语义（#4157 族，需独立评估自锁面）；②schema 的 `consumers` 来自静态 grep，若某键后续改由间接引用消费需同步更新；③`.freely/config.toml` 是 gitignored 本地状态，「一次性修正」不可随 PR 传播，外部项目仍需自己改（doctor 现在会报出来）；④`required` 只覆盖 4 个项目身份键，其余键缺失视为使用默认值，不报错。
- verification: AT-001 基线 RED `2 ok / 18 failed` → 工位 GREEN `20 ok / 0 failed`；真实 `freely doctor` 由 INVALID(:60) 变 ok；`bash -n`、`check-epics-map`（16 epics / 206 stories）、`bin/test-all --ci` 与相关回归基线对比 0 新增失败。
- self_bootstrap_findings: ①issue 说模板 `allowed_paths` 需修正，实测模板本来就是 8 项 list，验收标准 3 前半在基线已成立；②issue 报 gate `:392-397`，实测 `:408-433`（行号漂移）；③`.freely/config.toml` 是 gitignored，代码侧无法「一次性修正」所有本地实例，必须靠 schema + 诊断构成可移植修复；④模板 52 键是 config 58 键的真子集（6 个 runtime 追加键），schema 以 58 为准且对这 6 个设 required=false，否则新 init 项目会误报缺键。
