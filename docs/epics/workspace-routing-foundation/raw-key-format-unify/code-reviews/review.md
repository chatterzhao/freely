# Code Review — raw key 格式统一

- reviewer: `subagent`
- verdict: `approved`
- reviewed_at: `2026-05-05T00:00:00Z`
- issue_id: `I-20260504T1132Z-A`
- issue_path: `docs/epics/workspace-routing-foundation/raw-key-format-unify/issues/I-20260504T1132Z-A.md`

## Scope

18 files changed: 6 code + 4 scripts + 8 docs. All regex/glob/date patterns updated to accept both old (`YYYYMMDD-HHMM`) and new (`YYYYMMDDTHHMMZ`) raw key formats.

## Verification

| Check | Result |
|-------|--------|
| scan 无回归 (old format) | PASS: 20260503-0200 still at branch_deleted |
| scan 识别 new format | PASS: 20260504T1132Z detected at b1_candidate |
| wt-create 提取新旧 key | PASS: all 4 patterns (raw old/new, I old/new) |
| pre-push 接受新旧格式 | PASS: both formats accepted |
| merge-gate GATE 2a 双格式 | PASS: ts_prefix strips -/T/Z correctly |
| existing branches unaffected | PASS: old format branches still work |

## Implementation Decision Note

- decision: `All regex/glob patterns accept both YYYYMMDD-HHMM and YYYYMMDDTHHMMZ formats via [-T] and Z? qualifiers. New items use ISO format.`
- why_this: `ISO 8601 compact format already used by GitHub issue-sync. Unifying eliminates 3-format fragmentation without breaking existing data.`
- alternatives_considered: `(1) Full migration script — rejected: risky, unnecessary churn. (2) Only fix new code — rejected: scan/sync would break on old data. (3) Dual-format compatibility — chosen: safe, backward-compatible, allows natural aging-out of old format.`
- boundary_non_goals: `NOT changing: chat-inbox DB 14-digit format (separate concern), git tag YYYY.MM.DD-HHMM format (different domain), human-readable display formats.`
- residual_risk: `New format keys with Z suffix could confuse regexes in external tooling. Mitigated by keeping old format support indefinitely. Chat-inbox consumed matching still broken (separate issue).`
