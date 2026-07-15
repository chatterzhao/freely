# Tasks: revert AI_MODE default wait→auto
- issue_id: I-20260715T063959Z-A
- [ ] 6 occurrences ${AI_MODE:-wait} → ${AI_MODE:-auto}
- [ ] Verify 3 ${AI_MODE:-none} guards unchanged
- [ ] bash -n syntax check PASS
