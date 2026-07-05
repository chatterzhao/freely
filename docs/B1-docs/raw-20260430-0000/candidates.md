# Candidates - 20260430-0000--acp-session-store-and-lifecycle

### C-20260430-0000-A: ACP session identity store + cycle-log fallback removal

- title: `ACP session identity in SQLite, replacing cycle-log text parsing`
- status: `absorbed`
- scope: |
  session-store.py CLI + SQLite, run-acp-prompt.py clean UUID output,
  monitor-ai-acp.sh session persistence, select_launch_kind DB query,
  extract_tool_session_id_from_log ACP removal, freely.db rename
- priority: `P0`
- type: `hotfix`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `runtime_fix`
- phase_state: `done_pre_brainstorm`
- promoted_issue_path: `docs/B2-docs/human/chat-inbox-sqlite/issues/I-20260429-2040-A.md`
- decision_reason: `session-store reuses the same freely.db SQLite and CLI pattern introduced by the chat-inbox-sqlite issue; no independent lifecycle needed`
- session_refs:
  - {tool: ccds, session_id: "20260430-acp-session-store", role: "author"}
- acceptance_criteria:
  - `LAST_TOOL_SESSION_ID` 永远是合法 UUID，不含 "(resumed)" 等注解
  - `select_launch_kind` ACP 分支不扫描 cycle log 或工具目录
  - ACP bridge 重启后 session failed 标记正确，下次 fresh
  - 非 ACP 工具无回归
- promotion_gate: `governance-merge-gate`
- open_questions: []
- next_action: `已吸收到 chat-inbox-sqlite issue，同仓库合并。`

- stale_lock_cleanup: `2026-04-30`

- resume_evidence_fix: `2026-04-30`

- alias_env_inheritance: `2026-04-30`

- issue_id_date_false_positive: `2026-04-30`

- bridge_pid_after_fork: `2026-04-30`

- restart_storm_auto_force: `2026-04-30`

- pre_tests_update: `2026-04-30`

### C-20260430-0000-B: Claude stream-json adapter (prototype, shelved)

- title: `Claude stream-json direct adapter replacing claude-agent-acp`
- status: `dropped`
- scope: |
  stream-json-bridge.py + monitor-ai-stream-json.sh.
  Direct claude communication without claude-agent-acp dependency.
- priority: `P1`
- type: `experiment`
- decision_reason: `No cross-process cache hits — claude -p mode generates new system prompt each invocation. ACP confirmed 60% cache improvement via session/resume. Shelved until Claude CLI supports persistent --session-id in -p mode or we implement process-level session persistence.`
- next_action: `Revisit when upstream supports persistent sessions in print mode.`
