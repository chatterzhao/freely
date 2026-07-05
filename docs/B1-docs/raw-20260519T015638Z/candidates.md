# Candidate: Systematic stale_pid — worker process exits before handoff

## C-20260519T015638Z-A: legacy issue

- **status**: `needs_research`
- **premerge**: allowed
- **priority**: P1
- **title**: Investigate and fix systematic stale_pid — worker process exits before producing handoff
- **source_raw**: `raw-20260519T015638Z38Z` (GitHub #601)

### acceptance_criteria

1. Identify root cause: which component (ACP adapter / runtime mark_stale / supervisor) produces the stale_pid before worker completion
2. Fix identified: if race condition, add lock/ordering; if timeout, adjust window; if slot switch, add process migration
3. Short-term mitigation: increase mark_stale inactivity threshold if shown to be false positive
4. Regression prevention: add test that simulates long-running worker and verifies stale_pid is not false positive
5. Confirm 21 blocked workers are absorbable (consumed or re-dispatched) after fix

### promotion_gate

- [ ] Root cause identified with evidence (code location + trace)
- [ ] Fix deployed and tested with at least 3 successful worker round-trips
- [ ] No new stale_pid blocks in 1 hour of continuous operation
- [ ] governance-check passes

### overlap / dependency

- Supervisor crash rc=0 consolidation (`C-20260517T083030Z-A`) studies similar supervisor/ACP boundary — may share root cause
- Worth coordinating with `C-20260517T083200Z-A` (supervisor crash detection research)

### open_questions

- stale_pid 的来源是 `mark_stale()` 还是 ACP adapter 直接报告的 `launch_blocked`？
- handoff DB 中这些 blocked worker 的 `last_activity_at` 实际值是多少？
- worker 是否真的在产生 handoff JSON 之前就死了，还是产生了但 runtime 没收到？

### acceptance_reviews

- None yet
