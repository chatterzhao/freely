# Tasks: revert AI_MODE default wait→auto
- issue_id: I-20260715T063959Z-A
- [x] 6 occurrences ${AI_MODE:-wait} → ${AI_MODE:-auto}
- [x] Verify 3 ${AI_MODE:-none} guards unchanged
- [x] bash -n syntax check PASS
