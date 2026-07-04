---
candidate_id: C-20260704T004227Z-A
status: promoted
source_raw: raw-20260704T004227Z
created_at: 2026-07-04
milestone: M-20260704T004227Z-A
---

# Candidates

## C-20260704T004227Z-A: 修复 agent-id 子串匹配 + bridge 环境变量清理

- candidate_format_version: v2
- title: 修复 agent-id grep 子串匹配 + _ensure_acp_bridge_running 清理 AI 环境变量污染
- status: promoted
- decision_reason: |
  两个独立 bug 都在同一代码路径，合并为一个 candidate 修复：

  1. **agent-id 子串匹配**（line 4278）: `grep -F "$(pwd)"` 在 develop 上匹配所有 worktree 路径前缀，误识别为 worker_01。
  2. **环境变量污染**（line 14155-14177）: 父进程（Claude Code）设置的 `ANTHROPIC_MODEL=deepseek-v4-pro[1m]` 等变量被透传到 ACP binary。
     opencode slot 的 settings.json 没有 `env` 字段来覆盖这些变量，导致 opencode ACP binary 使用了错误的模型。
     对于有 `env` 字段的 slot（如 claude），`ai_cli_tool_with_auth_assemble` 会提取并覆盖，所以偶然没问题。

  根因诊断过程:
  - 排除了 OPENCODE_CONFIG 不生效的可能（bridge env 正确设置了）
  - 排除了 acp-bridge.py SDK 硬编码的可能（SDK 透传 env，不是主动设置模型）
  - 确认了当前 shell 环境有 ANTHROPIC_MODEL=deepseek-v4-pro[1m]（来自 Claude Code 父进程）
  - 确认了 `_ensure_acp_bridge_running` 和 `acp-bridge.py` 都没有清理环境变量

- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - agent-id 解析: develop 上 `_my_id` 正确解析为 `manager_01`，worktree 上仍正确
  - 环境变量清理: bridge 进程环境中无 `ANTHROPIC_*` 和 `CLAUDE_CODE_*` 残留变量
  - 模型正确: 启动后 session JSONL 中 model 与 agent-table slot 配置一致
  - opencode slot 正确使用 `deepseek-v4-flash-free`
  - claude slot 仍正确使用其 `env` 字段指定的模型
- promotion_gate: 代码修改完成，bridge 启动时环境变量干净
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查环境变量污染根因和修复方案，确认 env cleanse + grep 修复的正确性
  - verdict: pass
- promoted_issue_id: I-20260704T004227Z-A
- promoted_issue_path: docs/epics/{epic-name}/{story-name}/raw-20260704T004227Z/issues/I-20260704T004227Z-A.md
- milestone: M-20260704T004227Z-A
- session_refs: []
