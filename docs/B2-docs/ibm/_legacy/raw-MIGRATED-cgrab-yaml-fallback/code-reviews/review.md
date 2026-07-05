# Code Review: cgrab YAML fallback
- issue_id: I-20260620T142838Z-A

## Review Summary
- Change: 5 lines in cgrab(), template + error table in skill doc
- Risk: Low — cgrab now falls back to YAML, grab() already had this pattern
- Verification: Test with YAML-format I-* files

## Review Dimensions
1. Correctness: ✅ Pattern matches existing grab() implementation
2. Performance: ✅ One extra regex attempt, negligible
3. Security: ✅ N/A
4. Governance: ✅ B1_IBM + B2_IBM tracked
5. Compatibility: ✅ Backward compatible (new format, existing still works)
6. Documentation: ✅ Skill template + error table updated
