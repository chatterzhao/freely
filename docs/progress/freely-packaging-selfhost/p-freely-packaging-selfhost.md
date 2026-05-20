# Progress: Freely 打包与自举验证

- issue_id: I-20260502-0500-A
- issue_path: docs/epics/freely-packaging-selfhost/issues/freely-packaging-selfhost.md
- phase_state: in_dev

## B2_IBM 完成

B2 产物已提交:
- PRD: docs/epics/freely-packaging-selfhost/prd.md
- Pre-Tests: docs/epics/freely-packaging-selfhost/pre-tests.md (+ v2 adequacy judgments)
- Tasks: docs/epics/freely-packaging-selfhost/tasks.md
- Code Reviews: docs/epics/freely-packaging-selfhost/code-reviews/Implementation-Decision-Note.md
- Brainstorm: docs/epics/freely-packaging-selfhost/brainstorms/b-packaging-selfhost.md

## Dev-Loop 实现

### T-001: package-allowlist.txt 增强
- 添加了每个路径的维护责任 Owner 标注
- Owner 分为 workspace-governance / runtime-maintainer / tooling-maintainer / templates-maintainer

### T-002: bin/freely-package 增强
- 版本号格式校验（YYYYMMDD-nightly / YYYY.MM.DD-stable），非法版本号报错退出
- 缺失文件从 WARN 改为 ERROR，汇总后退出
- 打包完成后完整性验证（所有 allowlist 路径在产物中存在）

### T-003: bin/test-pre-merge-selfhost 增强
- 新增 --timeout 参数控制超时（默认 300s）
- 执行顺序: 打包 → install → doctor → daemon start → Manager cycle → daemon stop
- 每步有独立退出码（1-7），失败时报告具体错误
- daemon stop 后确认 supervisor 已退出

## 待完成

- T-004: develop HEAD 打包验证（需要 develop 分支可用）
- T-005: 治理和文档产物维护（已完成）
