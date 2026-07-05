# Code Review: sqlite3 migration
- issue_id: I-20260617T063755Z-B

1. Correctness: ✅ Same SQL semantics (project+role+status+tool LIKE)
2. Compatibility: ✅ Backward compatible (tool_like is optional)
3. Architecture: ✅ Routes through DB daemon, not direct sqlite3
