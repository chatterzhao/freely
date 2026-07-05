# Code Review: write_task_mode ordering fix
- issue_id: I-20260618T091116Z-A

## Review Summary
- Change: 2 lines added (ensure_freely_db calls) in two functions
- Risk: Low — ensure_freely_db is idempotent, no ordering dependencies broken
- Verification: Syntax check passed, idempotency confirmed at L8099

## Review Dimensions
1. Correctness: ✅ ensure_freely_db is safe to call early
2. Performance: ✅ No impact — first call starts daemon, later calls are no-ops
3. Security: ✅ N/A
4. Governance: ✅ Properly tracked through B1_IBM → B2_IBM
5. Compatibility: ✅ No breaking changes
6. Documentation: ✅ Comments explain why ensure_freely_db is called early
