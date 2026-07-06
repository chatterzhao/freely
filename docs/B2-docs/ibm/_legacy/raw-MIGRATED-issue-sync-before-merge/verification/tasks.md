# Tasks: pr-merge-guarded issue-sync before merge

- issue_id: I-20260626T155612Z-A

## 1. Move issue-sync before merge
- [x] Remove _sync_issues_changed_in_merge call from attempt_develop_push_followthrough_if_needed
- [x] Add call in do_initial_merge before git merge --no-commit
- [x] Add _target parameter to function signature

## 2. Change diff comparison
- [x] Replace HEAD vs HEAD^ with target vs source_branch
- [x] Handle case where source branch has no new issues

## 3. Auto-commit + push
- [x] After issue-sync, git add docs/issues/ in source worktree
- [x] git commit with conventional message
- [x] git push origin source_branch
- [x] git fetch origin to refresh local ref

## 4. Governance
- [x] B1_IBM: brainstorms.md, candidates.md, milestones.md
- [ ] B2_IBM: I-* issue, pre-tests.md, tasks.md, code-review
- [ ] pr-create-guarded
- [ ] pr-review-guarded
- [ ] pr-merge-guarded
- [ ] wt-close
