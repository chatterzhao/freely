# Tasks: AI_MODE default correction + remaining unguarded fix
- issue_id: I-20260712T125520Z-A
- [x] freely line 22752: --mode "$AI_MODE" → --mode "${AI_MODE:-wait}"
- [x] freely lines 2211,2221,5882,13028,20268,22752: ${AI_MODE:-auto} → ${AI_MODE:-wait} (6 occurrences)
- [x] B1 docs: candidate promoted to I-* issue
- [x] B2 docs: I-* issue + pre-tests + code-review materialized
- [x] bash -n syntax check PASS
- [x] grep verification: no :-auto defaults, no unguarded $AI_MODE
