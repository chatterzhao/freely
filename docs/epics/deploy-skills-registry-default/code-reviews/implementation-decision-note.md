# Implementation Decision Note: deploy-skills registry-driven default

- issue_id: I-20260624T004510Z-A
- issue_path: docs/issues/I-20260624T004510Z-A/issue.md
- milestone: M-20260624T004510Z-A

## Implementation Decision Note

- decision: 修复 `opencode` 通配符（`opencode)` → `opencode*)`）并从 `tool-registry.json5` 驱动默认 tool 检测
- why_this: `opencode` 缺 `*` 是 copy-paste bug（所有其他 tool 都用通配符）；默认只部署到 `AI_TOOL` 单值会导致 daemon fallback 时其他 tool 无 skill；registry 已是 tool 列表的权威数据源
- alternatives_considered: (1) 只修 opencode 不换默认值 — 治标不治本 (2) 用 registry skill_dir 替换 tool_dir() case 分支 — 正确方向但属于 #3399 范畴 (3) 保留旧 fallback 链在 registry 之上 — 增加复杂度且旧链无增量价值
- boundary_non_goals: 不修改 tool_dir() 的 case 映射（留给 #3399）；不改变 --tools 显式指定行为；不改变 skill 部署的目标目录结构
- residual_risk: registry JSON5→TOML 迁移 (#3399) 时需同步更新 JSON5 读取逻辑；`command -v` 检测在极少数环境可能不可靠
