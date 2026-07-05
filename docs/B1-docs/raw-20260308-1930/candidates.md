# Candidates: 业务阻塞与系统崩溃恢复分层

## C-20260308-1930-A: legacy issue

- title: 业务阻塞状态与系统崩溃恢复定位治理
- status: promoted
- decision_reason: `blocked_*` 与系统崩溃不能混用；auto-loop 需要一套固定的恢复定位顺序和最小恢复字段，才能在 PID 消失后继续原 `in_*` 或做正确诊断。
- promoted_issue_path: `docs/B2-docs/runtime/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- acceptance_hint: 1) `blocked_*` 被硬定义为业务阻塞；2) PID/CLI 崩溃不直接改 `phase_state`；3) 恢复定位顺序固定为 `recovery -> progress -> issue -> milestone -> active worktree`; 4) 恢复最小字段包含 `tool/session_id/jsonl_path/branch/worktree_path/phase_state/runtime_state/resume_hint`；5) 相关 skills 统一按该顺序检查。
- scope:
  - `docs/LAWS.md` 恢复与阻塞边界
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`
  - 相关 issue / milestone 口径
- impact: 高 - 直接影响 auto-loop 如何处理崩溃后的续接与误判
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
