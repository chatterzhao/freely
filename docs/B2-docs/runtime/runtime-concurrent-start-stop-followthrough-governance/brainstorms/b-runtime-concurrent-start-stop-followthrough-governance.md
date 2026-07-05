# Brainstorm: runtime-concurrent-start-stop-followthrough-governance

## Narrow owner boundary

- The source candidate originally mixed a generated-truth status repair with a same-project runtime followthrough repair.
- Canonical `develop` already absorbed the generated-truth half.
- This owner exists only to carry the remaining runtime followthrough to canonical truth.

## Why this is not a reopen of the broad packet

- The status-surface half is no longer speculative; it is already green on `develop`.
- The unresolved defects are runtime correctness edges around same-project supervisor discovery, attach, stop, and stop-marker preservation.
- Treating the remaining diff as candidate-only closeout would leave a develop-bound runtime change without a lawful owner chain.

## Acceptance spine

1. degraded bootstrap attach does not kill or bypass a healthy in-flight same-project supervisor
2. stop terminates every discovered same-project supervisor
3. stop-marker cleanup preserves stop intent until the last supervisor exits
4. adjacent generated-truth status regressions remain green
