# B1_IBM: zombie worker self-recovery on daemon restart

## Discovery
Daemon stop kills processes without updating A2A task state. Workers left in 'working' become zombies on restart — Manager marks all as 'failed', losing all in-progress work.

## Research
A2A spec: 'input-required' is interrupted state (non-terminal) — "task paused, awaiting external input." Daemon stop = pause, start = resume signal. Stop-side update before killing A2A server preserves recoverable state.

## Decision
Phase 1 (this fix): stop-side — transition working→input-required before A2A server shutdown. Phase 2 (follow-up): restart-side — Manager checks input-required workers for resumability instead of marking failed.
