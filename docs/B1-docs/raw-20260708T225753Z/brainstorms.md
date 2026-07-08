---
b1_id: B1-20260708T225753Z
phase_state: completed
source_raw: raw-20260708T225753Z
---
# B1: scan full test coverage
## Test Matrix (7 types)
1. raw+proposed+no platform → raw_not_started ✅
2. raw+proposed+platform=closed → merged_develop ✅
3. raw+empty+platform=closed → merged_develop ✅
4. I-*+in_dev → i_non_terminal ✅
5. I-*+done_b2_ibm → i_non_terminal ✅
6. I-*+in_verification → i_non_terminal ✅
7. raw+absorbed → merged_develop (sync batch) ✅

## Fix
_build_sync_batch: keep individual items visible, prepend batch as summary
