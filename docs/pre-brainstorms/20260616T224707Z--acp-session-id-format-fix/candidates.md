# Candidates

## C-20260616T224707Z-A: ACP Session ID 格式污染修复 — 兼容三种 AI CLI 的 Session ID 提取

- candidate_format_version: v2
- title: ACP Session ID 格式污染修复 — 兼容三种 AI CLI (Claude Code / Codex CLI / OpenCode) 的 Session ID 提取
- status: promoted
- decision_reason: P0 runtime-critical: opencode 下 multi-turn session 全部崩溃，每次创建新 session 导致 cache=0%、restart-storm 误触发。根因明确，修复直接（3 文件、+23/-12 行），无需更多 research。
- next_action: B2_IBM → dev-loop → test-pre-merge 验证 → pr-merge-guarded → wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `run-acp-prompt.py` 所有 launch_kind 分支输出统一的 clean line 1 + label line 2
  - `monitor-ai-acp.sh` session ID 提取兼容 UUID v4、`ses_`、`session id: <id>` 三种格式
  - `freely` 的 `is_valid_uuid()` 扩展为 `is_valid_session_id()`，同时接受 UUID v4 和 `ses_` 格式
  - 连续 3 次 `LAUNCH_KIND="prompt"` multi-turn cycle 后 session ID 保持 clean
  - restart-storm 检测不再因 session ID 污染而误触发
  - 切换到 cc 或 codex 工具后 UUID v4 路径不受影响
- promotion_gate: code-review 通过 + pre-tests 验证三种 format 的 session ID 提取
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-sonnet-4-6
  - mode: subagent
  - summary: 验证 3 处 UUID-only 假设已全部修复，regex 覆盖 UUID v4 和 `ses_` 两种格式，向后兼容通过 is_valid_uuid wrapper 保障
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260616T224707Z-A/issue.md
- milestone: M-20260616T224707Z-A
- session_refs: []
