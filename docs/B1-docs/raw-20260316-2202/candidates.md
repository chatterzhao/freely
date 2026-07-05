# Candidates: first-hop-must-execute-second-hop

- candidate_id: `C-20260316-2203`
- title: 首跳协议要求同工具场景必须继续执行第二跳而不是停在 next_prompt
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- acceptance_hint:
  - `start-lead-agent.sh` 明确要求同工具场景继续执行第二跳
  - `lead-agent` / tools 口径与启动器一致
  - 脚本回归锁住“不允许只输出 next_prompt 结束”
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
