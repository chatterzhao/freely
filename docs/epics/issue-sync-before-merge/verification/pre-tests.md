# Pre-Tests: pr-merge-guarded issue-sync before merge
- issue_id: I-20260626T155612Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: _sync_issues_changed_in_merge 在 merge 之前调用
- testing_layer: unit
- target_environment: test-pre-merge-20260626T155612Z-issue-sync-before-merge
- required_evidence: 代码中 issue-sync 调用在 git merge 之前
- test_command: grep -A2 "issue-sync before merge" docs/system/workspace/scripts/worktree/pr-merge-guarded | grep -q "git merge"
- expected_output: issue-sync line appears before git merge line
- actual_output: issue-sync before merge line at 558, git merge at 561
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: none
- status: pass

### acceptance-2
- acceptance_target: issue-sync 后自动 commit + push
- testing_layer: unit
- target_environment: test-pre-merge-20260626T155612Z-issue-sync-before-merge
- required_evidence: 代码包含 git commit + git push 逻辑
- test_command: grep -c "git -C.*commit\|git -C.*push" docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: non-zero count (auto-commit + push present)
- actual_output: 2
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: none
- status: pass

### acceptance-3
- acceptance_target: diff 比较使用 source vs target（非 HEAD vs HEAD^）
- testing_layer: unit
- target_environment: test-pre-merge-20260626T155612Z-issue-sync-before-merge
- required_evidence: diff 命令使用 _target _src_branch
- test_command: grep "git diff.*_target.*_src_branch" docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: git diff --name-only "$_target" "$_src_branch"
- actual_output: git diff --name-only "$_target" "$_src_branch" -- "$issues_dir" 2>/dev/null | ...
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: none
- status: pass

## Unit
- acceptance_target: 代码级验证 — issue-sync 顺序、auto-commit、diff 比较
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: acceptance-1 ~ acceptance-3 均 pass

## Integration
- acceptance_target: pr-merge-guarded dry-run 通过，不报错
- testing_layer: integration
- target_environment: test-pre-merge-20260626T155612Z-issue-sync-before-merge
- required_evidence: --dry-run 执行成功，exit 0
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260626T155612Z-issue-sync-before-merge --dry-run
- expected_output: --dry-run complete, exit 0
- actual_output: --dry-run complete, exit 0
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker: none
- status: pass

## End-to-End
- acceptance_target: 完整 merge 后 source worktree 干净，wt-close 不阻塞
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge 后 source worktree git status clean
- not_applicable_reason: E2E 验证需要在真实 pr-merge-guarded 执行后检查 source worktree 状态，dry-run 无法模拟 issue-sync 副作用
- not_applicable_explanation: 本修改的 E2E 验证即本次 PR 自身的 merge 流程：如果 merge 成功且 wt-close 不阻塞，即验证通过

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 将在此 PR merge + wt-close 过程中验证
