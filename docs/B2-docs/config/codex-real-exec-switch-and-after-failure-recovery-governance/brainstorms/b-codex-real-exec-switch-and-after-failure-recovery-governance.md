# Brainstorm: codex-real-exec-switch-and-after-failure-recovery-governance

## Direction

Freeze a bounded follow-on owner that turns the observed real bad-slot replay into canonical runtime truth:

1. real `codex exec` is the availability truth that matters for runtime recovery
2. manual switch and after-failure recovery are different contracts
3. slot-local network failures should fast-fail and advance instead of stalling
4. real `bin/ai xx` execution belongs in the owner evidence, not just in ad hoc notes

## Boundaries

- do not reopen the testing-governance root-cause analysis owner
- do not add periodic probing as a default runtime path
- do not treat URL/OAuth inventory as stronger than real `codex exec` for live recovery
