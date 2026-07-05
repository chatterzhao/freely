# Tasks: Merge Guard + Rebase Integrity

## Phase 1: Hook Scripts (done)
- [x] Create `docs/system/workspace/hooks/pre-rebase.sh` — save diff snapshot
- [x] Create `docs/system/workspace/hooks/post-rewrite.sh` — compare snapshot, write marker
- [x] Create `.githooks/post-rewrite` delegation script
- [x] Create `.githooks/pre-rebase` delegation script
- [x] Make all hook scripts executable
- [x] Verify syntax (`bash -n`)

## Phase 2: pr-merge-guarded Gates (done)
- [x] Add `check_rebase_integrity()` function — reads marker, blocks merge
- [x] Add `_set_governance_check_pass()` function — updates GitHub check to success
- [x] Call `check_rebase_integrity` in guard section (after promotion gate, before merge)
- [x] Remove `--admin` from `gh pr merge`, call `_set_governance_check_pass` before merge

## Phase 3: CI Workflow (done)
- [x] Rewrite `.github/workflows/pr-merge-guard.yml` — create `governance/pr-merge-guard` check (in_progress)
- [x] Document one-time branch protection setup (`gh api` command)

## Phase 4: Governance (done)
- [x] B1_IBM: brainstorms.md + candidates.md
- [x] B1_IBM: milestones.md candidate_issues entry
- [x] B2_IBM: I-issue, prd, pre-tests, tasks, code-review

## Phase 5: Test & Merge
- [ ] AT-001–AT-005, AT-008–AT-009: feature-local tests
- [ ] pr-create-guarded
- [ ] test-pre-merge: AT-006, AT-007 (GitHub environment)
- [ ] pr-merge-guarded develop fix/raw-20260617T055840Z-merge-guard-rebase-integrity
- [ ] wt-close
