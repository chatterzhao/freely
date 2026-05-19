# Pre-Brainstorm Candidates

## C-20260519T035908Z-A

- **title**: Consolidate 11 duplicate "supervisor crash: bash rc=0" raw issues
- **source_class**: bug_report_group
- **route_kind**: pre_brainstorm
- **phase_state**: in_pre_brainstorm
- **priority**: P2
- **problem**: 11 raw issues from 11 occurrences of the same supervisor crash (bash rc=0)
- **why_now**: Duplicates waste tracking capacity; need consolidation before further analysis
- **decision_reason**: B1_IBM decision: consolidate to P2. 10+ duplicate "supervisor crash: bash rc=0" raw issues from the same root cause. Keep raw-20260519T035908Z as canonical, absorb all others. Fix branch `fix/raw-20260519T035908Z-consolidate-supervisor-crash` created for analysis and consolidation.
- **next_action**: Consolidate 11 → 1 (keep raw-20260519T035908Z as canonical)
- **revisit_trigger**: Root cause investigation of supervisor crash
- **open_questions**:
  1. Confirmed root cause of supervisor crash with `bash rc=0` — is it a timeout, resource exhaustion, or code bug?
  2. Should we fix the crash or just add resilience/retry?
  3. Related: `feature/raw-20260517T081722Z-supervisor-rc0` may already have investigation
  4. How did older fix (`feature/raw-20260517T081722Z-supervisor-rc0`) fail to resolve this?
  5. What is the blast radius — does this affect all tools/adapters or only `oc-acp-ds-flash-auto`?
- **acceptance_criteria**:
  1. 11 raw issues consolidated into 1 canonical
  2. GitHub issues #618–#627 closed as duplicates of #617
  3. Remaining open issue links to canonical B1/issue for root cause analysis
  4. B1 candidates.md reflects full 11-issue scope
