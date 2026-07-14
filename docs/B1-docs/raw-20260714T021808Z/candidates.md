---
candidate_id: C-20260714T021808Z-A
status: promoted
source_raw: raw-20260714T021808Z
created_at: 2026-07-14
milestone: M-20260714T021808Z-A
---

## C-20260714T021808Z-A: task_mode 传递链修复 + AI_MODE 守卫

- candidate_format_version: v2
- title: fix task_mode propagation + AI_MODE unguarded crash + listen fallback
- status: promoted
- decision_reason: Option C 最小链路修复——打通 task_mode 从 daemon start → daemon-run 的传递，修正 watchdog listen/fallback，守卫 AI_MODE 裸引用。不改动不必要的函数签名。
- next_action: B2 阶段物化 I-* issue → 实现修复
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `freely daemon start --task-mode auto` 后 daemon 以 auto 模式运行
  - `freely daemon start`（无 --task-mode）默认 wait
  - watchdog 重启时 listen 模式不被误判为 auto
  - watchdog 重启时 DB 无值 fallback 为 wait
  - daemon 启动后 AI cycle 可达 L040（不再 crash 在 AI_MODE 裸引用）
- promotion_gate: 代码审查通过 + bash -n 语法检查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: manual
  - summary: 审查 4 项缺陷的修复方案，确认传递链、fallback、守卫的正确性
  - verdict: pass
- promoted_issue_id: I-20260714T021808Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/issues/I-20260714T021808Z-A.md
- milestone: M-20260714T021808Z-A
- session_refs: []
