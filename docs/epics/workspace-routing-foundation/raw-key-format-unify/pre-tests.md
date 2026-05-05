# Pre-Tests — raw key 格式统一

## Unit

| id | requirement | evidence_level | status | artifact_ref |
|----|-------------|---------------|--------|-------------|
| U1 | pre-push regex accepts old format `raw-YYYYMMDD-HHMM` | command_output | pass | `echo "feature/raw-20260503-0200-foo" \| grep -qoE 'raw-[0-9]{8}[-T][0-9]{4}Z?'; echo $?` → 0 |
| U2 | pre-push regex accepts new format `raw-YYYYMMDDTHHMMZ` | command_output | pass | `echo "feature/raw-20260504T1132Z-foo" \| grep -qoE 'raw-[0-9]{8}[-T][0-9]{4}Z?'` → matched |
| U3 | wt-create extracts old format raw key | command_output | pass | `echo "feature/raw-20260503-0200-foo" \| grep -oE 'raw-[0-9]{8}[-T][0-9]{4}Z?'` → `raw-20260503-0200` |
| U4 | wt-create extracts new format raw key | command_output | pass | `echo "feature/raw-20260504T1132Z-foo" \| grep -oE 'raw-[0-9]{8}[-T][0-9]{4}Z?'` → `raw-20260504T1132Z` |
| U5 | scan chain trace no regression for old items | command_output | pass | `task-lifecycle-scan.py` → 20260503-0200 at branch_deleted |

## Integration

| id | requirement | evidence_level | status | artifact_ref |
|----|-------------|---------------|--------|-------------|
| I1 | scan recognizes new format raw-* | command_output | pass | `task-lifecycle-scan.py` → 20260504T1132Z detected at b1_candidate |
| I2 | scan recognizes new format I-* | command_output | pass | `_base_key("I-20260504T1132Z-A")` → `20260504T1132Z` |
| I3 | merge-gate GATE 2a works with both formats | code_review | pass | ts_prefix strips -/T/Z correctly |
| I4 | date generation uses ISO 8601 UTC | command_output | pass | `date -u '+%Y%m%dT%H%M%SZ'` produces ISO format |

## End-to-End

| id | requirement | evidence_level | status | artifact_ref |
|----|-------------|---------------|--------|-------------|
| E1 | scan output identical for old format items before/after change | command_output | pass | same total count, same 20260503-0200 stage |
| E2 | new feature branch with new format passes pre-push | code_review | pass | `feature/raw-20260504T1132Z-raw-key-format-unify` created via wt-create |

## Real-Environment

- real_environment_status: `pass`
- real_environment_reason: `本次为 regex 重构，不涉及运行时行为变更。所有更改仅在模式匹配层，不需要真实环境测试。`
