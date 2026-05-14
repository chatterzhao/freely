# Code Review
- issue_id: I-20260514T001746Z-A
## Implementation Decision Note
- decision: reuse existing SubprocessTransport (marked DEPRECATED) for opencode acp via stdio
- why_this: SubprocessTransport already implements stdio JSON-RPC; only needed --agent to accept multi-word commands (split())
- alternatives_considered: (1) New StdioTransport class — duplicates SubprocessTransport (2) SocketTransport modification — wrong abstraction
- boundary_non_goals: Not changing bridge-based ACP (claude, codex continue as-is)
- residual_risk: SubprocessTransport was DEPRECATED for bridge reasons; opencode doesn't need a bridge
