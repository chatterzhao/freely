# Brainstorms: deploy-skills 默认部署到全部已安装 tool

- raw_key: 20260624T004510Z
- github_issue: https://github.com/chatterzhao/freely/issues/3397

## Discovery

### 问题
`daemon start` 时 `deploy-skills` 退出码 1，日志显示 `WARNING: unsupported tools: opencode-apikey-ds-flash-auto`。

根因有两个层面：
1. `opencode` 在 `tool_dir()` case 中是精确匹配（`opencode)`），缺少 `*` 通配符，导致 `opencode-apikey-*` 格式的 tool 名无法匹配
2. 默认 tool 列表从 `AI_TOOL` config 单值获取，不检查 registry 中其他已安装 tool

### 影响面
- `bin/deploy-skills` 的 tool 匹配和默认值解析逻辑
- 不影响其他模块

## Research

### 现有 tool 匹配逻辑
```
claude*    → ~/.claude/skills/       (前缀匹配 ✅)
codex*     → ~/.codex/skills/         (前缀匹配 ✅)
oc-*|opencode) → ~/.config/opencode/skills/ (opencode 精确 ⚠️)
cc*        → ~/.claude/skills/        (前缀匹配 ✅)
```

`opencode` 是唯一一个没加 `*` 通配符的 tool 名。注释里写的是 "opencode" 而非 "opencode*"，是典型的 copy-paste 遗漏。

### 默认 tool 选择
旧逻辑：`--tools` > `AI_TOOL` config > `FREELY_TOOLS` env > global config > `"claude"`

问题：daemon start 时调用 deploy-skills 不带 `--tools`，只会部署到 `AI_TOOL` 配置的那一个 tool。如果用户切换 tool 或使用 fallback，其他 tool 缺少 skill。

新逻辑：`--tools` > tool-registry.json5 全部已安装 tool > `"claude"`

### tool-registry.json5 读取
registry 已有三个 tool（claude、codex、opencode），每个有 `test_command` 字段可提取二进制名。通过 `command -v` 检测是否已安装。

## Decision

### 方案：最小修改
1. `opencode)` → `opencode*)`（1 字符修改）
2. 默认 tool 列表从 registry 驱动：读取所有 tool key → 用 `test_command` 第一段检测二进制 → 部署到所有已安装 tool

无需修改 `tool_dir()` 的其他 case 分支（claude*、codex*、cc* 已经正确使用通配符）。

### 替代方案评估
- **A: 彻底用 registry 的 skill_dir 驱动 tool_dir()**：需要 registry 字段扩展，属于 #3399 范畴。当前保持 case 分支，等 #3399 统一处理。
- **B: 只修 opencode 不加 registry 默认值**：治标不治本，daemon 启动仍只部署一个 tool。

### 结论
方案选择：最小修改，修复 opencode bug + registry 驱动默认值。
risk: low（仅影响 deploy-skills 脚本，不影响 daemon 主流程）
revisit_trigger: #3399 重构 registry 格式时需同步更新 deploy-skills 的 JSON5 读取逻辑
