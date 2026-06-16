# Code Review - I-20260616T055035Z-A: A2A server hygiene + after-run worker detection

- issue_id: I-20260616T055035Z-A
- reviewer: claude (automated governance gate)

## Implementation Decision Note

- decision: apply three fixes to the freely runtime script for A2A reliability and prompt-mode worker dispatch
- why_this: zombie A2A processes (5 observed) block socket binding; socket-only startup check misses TCP-only mode; end_turn exit without a2a-exit leaves workers undetected
- alternatives_considered: none — fixes are targeted at specific observed runtime failures
- boundary_non_goals: does not refactor a2a_server.py or the worker prompt pipeline; only fixes the lifecycle gaps in the launching/stopping/after-run detection in the freely script
- residual_risk: pkill by process name pattern could theoretically match unrelated processes; the pattern is scoped to project path and `--start` flag to minimize false positives

## Verification

- A2A zombie cleanup: PID file verified, terminate_pid_with_graceful_wait tested
- HTTP health check: Python script connects via Unix socket and validates HTTP response
- After-run detection: mirrors the same filesystem scan pattern already used in manager_exit_contract_kind() Step 4
