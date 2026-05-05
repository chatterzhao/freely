# Pre-Tests — raw key 格式统一

## Unit

| id | requirement | evidence_level | status | artifact_ref | surface_kind | target_lane | promotion_gate |
|----|-------------|---------------|--------|-------------|-------------|-------------|---------------|
| U1 | pre-push regex accepts old format | command_output | pass | `grep -qoE 'raw-[0-9]{8}[-T][0-9]{4}Z?'` → 0 | regex | feature | premerge-integration |
| U2 | pre-push regex accepts new format | command_output | pass | `grep -qoE 'raw-[0-9]{8}[-T][0-9]{4}Z?'` → matched | regex | feature | premerge-integration |
| U3 | wt-create extracts old format key | command_output | pass | `grep -oE` → `raw-20260503-0200` | cli | feature | premerge-integration |
| U4 | wt-create extracts new format key | command_output | pass | `grep -oE` → `raw-20260504T1132Z` | cli | feature | premerge-integration |
| U5 | scan chain trace no regression | command_output | pass | scan output: 20260503-0200 at branch_deleted | scan | feature | premerge-integration |

## Integration

| id | requirement | evidence_level | status | artifact_ref | surface_kind | target_lane | promotion_gate |
|----|-------------|---------------|--------|-------------|-------------|-------------|---------------|
| I1 | scan recognizes new format raw-* | command_output | pass | scan: 20260504T1132Z at b1_candidate | scan | premerge-integration | develop_merge |
| I2 | scan recognizes new format I-* | command_output | pass | `_base_key("I-20260504T1132Z-A")` → `20260504T1132Z` | scan | premerge-integration | develop_merge |
| I3 | merge-gate GATE 2a both formats | code_review | pass | review.md: ts_prefix strips -/T/Z | gate | premerge-integration | develop_merge |
| I4 | date generators use ISO 8601 UTC | command_output | pass | `date -u '+%Y%m%dT%H%M%SZ'` | scripts | premerge-integration | develop_merge |

## End-to-End

| id | requirement | evidence_level | status | artifact_ref | surface_kind | target_lane | promotion_gate |
|----|-------------|---------------|--------|-------------|-------------|-------------|---------------|
| E1 | old format items unchanged after refactor | command_output | pass | scan total and stages unchanged | scan | premerge-integration | develop_merge |
| E2 | new format branch passes pre-push hook | command_output | pass | `feature/raw-20260504T1132Z-raw-key-format-unify` created | hooks | premerge-integration | develop_merge |

## Real-Environment

- real_environment_status: `pass`
- real_environment_reason: `本次为 regex 重构，不涉及运行时行为变更。所有更改仅在模式匹配层，不需要真实环境测试。`

## Acceptance Items

| id | requirement | evidence_level | status | artifact_ref | surface_kind | target_lane | promotion_gate |
|----|-------------|---------------|--------|-------------|-------------|-------------|---------------|
| A1 | All regex patterns accept both old and new formats | command_output | pass | 18 files changed, all patterns verified | regex | premerge-integration | develop_merge |
| A2 | No regression in scan output for existing items | command_output | pass | scan total unchanged, old items same stage | scan | premerge-integration | develop_merge |
| A3 | Governance merge gate passes with new format artifacts | gate_output | pass | `governance-merge-gate --range "develop..HEAD"` passed | gate | premerge-integration | develop_merge |
