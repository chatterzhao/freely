# Brainstorm: ACP Session ID 格式污染修复

## Discovery

### 问题触发
深度分析 Freely 运行时状态时发现：open code 环境下的 multi-turn session 全部丢失 context，每个 cycle 创建全新 session（而非 resume），prompt cache 命中率归零，且触发 restart-storm 检测。

### 影响范围
- opencode 工具的所有 multi-turn cycle（Claude Code / Codex CLI 不受影响，因其使用 UUID v4）
- session-store (SQLite) 中存储的 session ID 被 label 污染
- restart-storm 误检测触发（count=3）
- bridge 因反复 session/prompt 失败后死亡

### 根因链
通过逐层追踪 `session-state.env` → `monitor-ai-acp.sh` → `run-acp-prompt.py` → ACP bridge log → `freely` 脚本，定位到 3 个交互 Bug：

1. **Bug 1**: `run-acp-prompt.py` 的 `prompt` 分支只输出 1 行（带 label），其他分支输出 2 行（clean + label）→ 下游无法分离
2. **Bug 2**: `monitor-ai-acp.sh` 的 session ID 提取 regex 只匹配 UUID v4 格式 → opencode 的 `ses_` 格式永远无法匹配 → label 残留
3. **Bug 3**: `freely` 的 `is_valid_uuid()` 只接受 UUID v4 → session-store 恢复路径对 opencode 被阻断

## Research

### 三种 AI CLI Session ID 格式对比
| CLI | 格式 | 示例 | 代码路径 |
|-----|------|------|---------|
| Claude Code (cc) | UUID v4 | `a1b2c3d4-e5f6-...` | `claude|cc|cc-use-codex-cli` |
| Codex CLI | UUID v4 | `a1b2c3d4-e5f6-...` | `codex` |
| OpenCode | `ses_` prefix | `ses_12ef4d6cfffeWnAyWb17Uc2RdX` | `opencode` |

### 污染传播链验证
通过比对 cycle log (082601→083315→084212→084748) 确认：
- 083315: `session id: ses_AAA (prompt)` → 首次污染
- 084212: `session id: ses_AAA (prompt) (prompt)` → **双重 label**，确认污染传播
- 084748: 再次循环崩溃

### session-cache.sh 已有正确实现
`session_extract_id_from_log` 在 opencode 分支（line 157）已使用正确的 `ses_` regex。但 `monitor-ai-acp.sh` 未复用此逻辑。

## Decision

### 方案选择：统一 Session ID 提取规则

**选中方案**：空格剥离 + 扩展 regex

1. **`monitor-ai-acp.sh` 和 `freely`**：统一使用组合 regex `(ses_[A-Za-z0-9]+|[0-9a-f]{8}-...)` 匹配所有已知格式
2. **`session_id_out` 空格剥离**：利用 "session ID 不含空格、label 总是 ` (...)` 格式" 的特性，`%% *` 一次剥离
3. **`run-acp-prompt.py`**：与其他分支对齐，输出 clean line 1 + label line 2

**考虑的替代方案**：
- 按工具类型分派（session-cache.sh 的 switch/case 模式）：更好但改动面大，留待后续重构
- 仅修复 `ses_` regex 不修 label stripping：可能被未来新 label 变体打回

### 实施策略
Fix first（已完成 commit 7974c430）：3 文件、+23/-12 行、最小改动。

### 风险
- **低风险**：改动集中在 session ID 提取逻辑，不改变 ACP 协议交互
- **回归风险**：UUID v4 路径需验证（通过 is_valid_uuid 向后兼容 wrapper 保障）
- **未来扩展**：若新的 AI CLI 使用第三种 session ID 格式，需更新 regex

### Open Questions
- 无。根因明确，修复直接。
