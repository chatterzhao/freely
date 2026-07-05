# Brainstorm: probe say hi

## Source
- GitHub issue #2111 (raw-20260522T045227Z27Z)
- Title: slot_probe 用 say hi 替代 hi

## Discovery
The generic slot_probe B1 (20260522T044515Z--slot-probe-generic-hi) defined using bare "hi" as the probe message for all tools (`codex exec 'hi'`, `claude -p 'hi'`, etc.).

Observation: bare "hi" is ambiguous — the probe sends `message: "hi"` and expects the AI to reply `"hi"`. In practice:
- Some tools may not echo back a simple "hi" in non-interactive mode
- The probe message should be a complete sentence (`say hi`) to get a more reliable non-empty response

## Research
- Current implementation in `availability-watchdog.sh:slot_probe()` already uses `printf 'say hi\n'` (line 1368) rather than bare `hi`
- The `_strip_probe_output_for_matching` logic (line 145) and matching comments (line 1562) still reference "hi" as the expected response
- The sibling B1 (20260522T044515Z) was promoted as `I-20260522T044515Z-A` with generic slot_probe — this refinement is a targeted fix on the probe message

## Decision
- Adopt "say hi" as the canonical probe message across all tools in `slot_probe()`
- Rationale: produces more reliable non-empty output; already matches implementation
- Absorb this raw issue as a targeted fix rather than expanding the scope of the generic slot_probe issue
- Candidate C-20260522T045227Z-A promoted to I-20260522T045227Z-A, kind=fix
