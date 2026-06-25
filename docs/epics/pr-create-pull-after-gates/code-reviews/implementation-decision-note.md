# Implementation Decision Note

**Decision**: Move `git pull origin develop` from Step 1 to Step 3 (between
gate-passed marker and push) in `pr-create-guarded`.

**Rationale**: All gates (clean check, phase_state check, dry-run, IBM
governance, pretests) are local-only checks. Only the push at Step 4 needs
up-to-date remote state. Moving pull to just before push eliminates redundant
network round-trips on every gate failure retry, without changing any semantics.

**Trade-offs**: The pull and push are now adjacent, forming a tight atomic
sequence. If someone uses FREELY_SKIP_IBM_GATE=1 and remote has diverged, the
pull could introduce conflicts — same risk as before, just manifested later.

**Evidence**: bash -n passes. Script flow verified. All gate exits precede pull.

Issue: I-20260625T050000Z-A
Date: 2026-06-25
