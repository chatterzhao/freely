# PRD: ACP Session ID 格式污染修复

## Goal

修复 opencode 环境下 multi-turn session ID 被 label 污染导致 cycle 崩溃的问题，同时保持 Claude Code / Codex CLI 的 UUID v4 路径正常工作。

## Scope

- **In**: `run-acp-prompt.py` 输出格式对齐、`monitor-ai-acp.sh` session ID 提取、`freely` session ID 验证
- **Out**: ACP 协议层改动、session-store schema 改动、tool switch 逻辑改动
- **Non-goal**: 重构 session ID 提取为按工具分派模式（session-cache.sh 已有此模式，monitor-ai-acp.sh 暂不跟进以减少改动面）

## Non-functional

- 向后兼容：UUID v4 路径通过 `is_valid_uuid` wrapper 完全保持
- 未来扩展：若新的 AI CLI 使用第三种 session ID 格式，只需更新组合 regex

## Dev-Loop Handoff

- 代码已提交（commit `7974c430`）：3 files, +23/-12
- 需在 test-pre-merge 验证 multi-turn cycle 后 session ID 清洁度
- 验证通过后走 pr-merge-guarded → develop → wt-close
