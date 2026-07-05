# Implementation Decision Note: ACP Session ID 格式污染修复

- issue_id: I-20260616T224707Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-16

## Decision

采用 **空格剥离 + 扩展 regex** 策略修复 session ID 提取的三个交互 Bug，最小化改动面（3 files, +23/-12）。

## Why This

1. **空格剥离规则**（`session_id_out="${session_id_out_raw%% *}"`）：利用了 "session ID 不含空格、label 总是 ` (...)` 格式" 的结构特性，一次处理所有已知和未来的 label 变体，不依赖枚举。
2. **组合 regex**（`(ses_[A-Za-z0-9]+|UUID v4)`）：同步覆盖 OpenCode 和 Claude Code/Codex CLI，不需要按工具分派。
3. **向后兼容 wrapper**（`is_valid_uuid() → is_valid_session_id()`）：5 个现有 call site 无需改动，risk 最小。

## Alternatives Considered

### Alternative A: 按工具类型分派（session-cache.sh 模式）
- **描述**：在 `monitor-ai-acp.sh` 中按 `$tool` 变量 switch/case，对 opencode 用 `ses_` regex，对 cc/codex 用 UUID regex
- **Rejected because**: 改动面更大，需要传递 `$tool` 到 session ID 提取逻辑；当前 `monitor-ai-acp.sh` 的 session ID 提取在 `main()` 中不区分 tool
- **Future**: 如果第三种 AI CLI 使用完全不同的格式（无法通过 regex 扩展覆盖），考虑重构为此模式

### Alternative B: 仅修复 `ses_` regex，不做空格剥离
- **描述**：只扩展 regex 匹配 `ses_`，保留原有的 label 检测和 `_fallback_sid` 逻辑
- **Rejected because**: label 检测逻辑依赖 regex（line 441），同样需要扩展；且未来新 label 变体可能打回
- **Risk**: 枚举 label 的代码始终有遗漏风险

### Alternative C: run-acp-prompt.py 不再输出 label line
- **描述**：Python 侧只输出 clean ID，不在日志中附加 human label
- **Rejected because**: human label 对调试和 cycle log 审计有价值；且需要修改 5 个分支，改动面更大

## Boundary Check

- **CONSTITUTION.md**: 不涉及分支/worktree 边界，不涉及 develop 直接写入
- **LAWS.md**: 不涉及 skip governance 路径
- **ACP Protocol**: 不改变 ACP 协议交互（session/prompt、session/resume 调用不受影响）
- **session-store**: SQLite schema 和 `freely-db-cli` 接口不变

## Non-Goals

- 不重构 `monitor-ai-acp.sh` 为工具感知的 session ID 提取（session-cache.sh 已有此模式，留待后续统一）
- 不改变 session-store schema
- 不添加新的 session ID 格式支持（仅在已有 UUID v4 和 `ses_` 之间修复兼容性）

## Residual Risk

- **低风险**：组合 regex 中的 `ses_[A-Za-z0-9]+` 理论上可能匹配非 session ID 的 `ses_` 前缀字符串。但 cycle log 中的 `ses_` 前缀几乎肯定来自 OpenCode session ID，误匹配概率极低。
- **缓解**：`session_id_clean` 提取优先级为 regex（line 432），如果没有匹配则回退到 `session_id_out` 空格剥离（line 440）。双层保障。
- **UUID v4 回归**：通过 `is_valid_uuid` wrapper + 组合 regex 中 UUID v4 分支保留，UUID v4 路径完全不受影响。
