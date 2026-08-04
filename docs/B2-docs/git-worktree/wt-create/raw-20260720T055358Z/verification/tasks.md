# Tasks: wt-create silent exit fix
- issue_id: I-20260720T055358Z-A

## Implementation
- [x] Add `|| true` after grep pipeline on line 311 of wt-create

## Verification
- [x] AT-001: Confirm `|| true` is present on line 311
- [x] AT-002: Confirm script no longer exits silently

## Documentation
- [x] Create pre-tests.md
- [x] Create I-* issue
- [x] Create code-review note
