# Implementation Decision Note — I-20260712T125520Z-A
- issue_id: I-20260712T125520Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260712T125520Z/issues/I-20260712T125520Z-A.md
- source_candidate: docs/B1-docs/raw-20260712T125520Z/candidates.md

## Decision
Fix remaining unguarded `$AI_MODE` reference AND correct default value from `auto` to `wait` in all 6 occurrences.

## Rationale
- raw-20260712T124601Z (first hotfix) fixed one occurrence of unguarded `$AI_MODE` but used `:-auto` as default
- raw-20260712T125520Z (this fix) found another unguarded occurrence: `--mode "$AI_MODE"` on the lead-agent launch command
- Design docs (raw-20260618T091116Z, raw-20260509T024559Z) specify that task_mode default is `wait`, not `auto`
- `wait` is the safe default: daemon should wait for human input, not run autonomously by default

## Scope
All 6 `${AI_MODE:-auto}` → `${AI_MODE:-wait}` in freely runtime script, covering:
- mode resolution functions (lines 2211, 2221, 5882)
- AI CLI launch commands (lines 13028, 20268, 22752)

## Verification
- bash -n: PASS
- No unguarded `$AI_MODE` references: PASS
- All defaults correctly set to `wait`: PASS
