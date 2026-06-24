# Implementation Decision Note: deploy-skills registry-driven default

## Decision
修复 `opencode` 通配符（`opencode)` → `opencode*)`）并从 `tool-registry.json5` 驱动默认 tool 检测。

## Why This
- `opencode` 缺 `*` 是明显的 copy-paste bug，所有其他 tool 都用通配符
- 默认只部署到 `AI_TOOL` 单值 → daemon fallback 时其他 tool 无 skill
- registry 已经定义了全部 tool，是默认部署列表的权威数据源

## Alternatives Considered
1. **只修 opencode 不换默认值**：治标不治本，daemon 启动仍只部署一个 tool
2. **用 registry skill_dir 替换 tool_dir() case 分支**：正确方向但属于 #3399 重构范畴。当前保持 case 分支
3. **保留旧 fallback 链，在最后加 registry**：增加复杂度，旧链已无价值（AI_TOOL 也是 registry 中的 tool）

## Boundary Non-Goals
- 不修改 `tool_dir()` 的 case 映射（留给 #3399）
- 不改变 `--tools` 显式指定行为
- 不改变 skill 部署的目标目录结构

## Residual Risk
- registry JSON5 → TOML 迁移 (#3399) 时需同步更新 JSON5 读取逻辑
- `command -v` 检测在极少数环境可能不可靠（如刚安装未 refresh PATH）
