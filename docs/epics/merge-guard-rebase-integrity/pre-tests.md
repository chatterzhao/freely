# Pre-Tests: Merge Guard + Rebase Integrity

## Acceptance Items (v2)

### AT-001: pre-rebase hook saves snapshot
- **Given**: feature branch with unmerged changes vs develop
- **When**: `git rebase develop` is initiated
- **Then**: `.freely/run/pre-rebase-diffs/<timestamp>-<branch>.diff` exists with `git diff develop...HEAD --name-only` output
- **Verify**: `bash docs/system/workspace/hooks/pre-rebase.sh` → check snapshot file created
- **Test method**: manual

### AT-002: post-rewrite hook detects lost files
- **Given**: pre-rebase snapshot exists with file list including `foo.sh`
- **When**: rebase completes and `foo.sh` is no longer in `git diff develop...HEAD --name-only`
- **Then**: `.freely/run/rebase-lost-files` marker created, `post-rewrite.sh` exits 1
- **Test method**: manual (simulate by creating snapshot with extra file, run hook)

### AT-003: post-rewrite hook passes on clean rebase
- **Given**: pre-rebase snapshot matches post-rebase file list
- **When**: rebase completes without losing files
- **Then**: no marker file, `post-rewrite.sh` exits 0
- **Test method**: manual

### AT-004: pr-merge-guarded blocks on rebase integrity failure
- **Given**: `.freely/run/rebase-lost-files` marker exists
- **When**: `pr-merge-guarded develop <branch>` is called
- **Then**: `check_rebase_integrity` gate fails, merge blocked, lost files listed in output
- **Test method**: `bash -c 'source docs/system/workspace/scripts/worktree/pr-merge-guarded; check_rebase_integrity'` (mock marker)

### AT-005: pr-merge-guarded passes on clean rebase integrity
- **Given**: no `.freely/run/rebase-lost-files` marker
- **When**: `check_rebase_integrity` runs
- **Then**: gate passes silently
- **Test method**: manual (remove marker if exists)

### AT-006: _set_governance_check_pass updates check via API
- **Given**: CI workflow created `governance/pr-merge-guard` check (in_progress) on PR head SHA
- **When**: `_set_governance_check_pass <branch>` runs
- **Then**: check updated to conclusion=success
- **Test method**: manual (requires GitHub token, real PR)

### AT-007: CI workflow creates blocking check
- **Given**: PR opened against develop
- **When**: workflow `guard` job runs
- **Then**: `governance/pr-merge-guard` check run created with status=in_progress
- **Test method**: GitHub Actions (after merge to develop, open test PR)

### AT-008: Hook scripts pass syntax check
- **Given**: hook scripts exist
- **When**: `bash -n <script>` runs
- **Then**: no syntax errors
- **Verify**: `bash -n docs/system/workspace/hooks/pre-rebase.sh && bash -n docs/system/workspace/hooks/post-rewrite.sh`
- **Test method**: automated ✓ (verified during implementation)

### AT-009: Protected branches skipped by pre-rebase hook
- **Given**: current branch is `develop` or `main`
- **When**: pre-rebase hook runs
- **Then**: exits 0 without creating snapshot
- **Test method**: manual

## Test Lane

`feature-local`: 在 fix worktree 中运行 manual tests AT-001–AT-005, AT-008–AT-009
`premerge-integration`: AT-006, AT-007 需在 GitHub 环境（merge 后 test-pre-merge 验证）
