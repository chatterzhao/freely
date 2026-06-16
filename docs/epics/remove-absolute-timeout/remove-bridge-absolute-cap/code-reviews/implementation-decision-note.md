- issue_id: I-20260616T044825Z-A
- issue_path: docs/issues/I-20260616T044825Z-A/issue.md
## Implementation Decision Note
- decision: Remove absolute timeout (BRIDGE_TIMEOUT) check from _send_request() session/prompt handling
- why_this: Industry standard (6 ACP projects) uses only idle timeouts. Absolute 30-min cap kills legitimate long-running AI sessions even when actively producing output. Idle timeout (ACP_IDLE_TIMEOUT) already provides sufficient protection against hung sessions.
- alternatives_considered: Increase threshold (postpones problem), configurable timeout (adds complexity without solving the issue), per-request timeout (requires significant refactoring)
- boundary_non_goals: Not changing non-session/prompt methods (they keep their own timeout). Not changing ACP_IDLE_TIMEOUT value. Not changing ACP protocol or bridge configuration.
- residual_risk: Extremely low. Idle timeout remains intact and catches hung sessions. Sessions producing continuous output will not be interrupted.
