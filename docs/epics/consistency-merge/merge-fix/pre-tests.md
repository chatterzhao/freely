# Pre-Tests: consistency check — cherry-pick → git merge
- issue_id: I-20260630T095936Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: dev→test 不一致时提示 git merge 而非 cherry-pick
- acceptance_target: worktree-common.sh + wt-close 的消息中不含 "cherry-pick"，含 "git merge" 和 "Freely-Merge-Path"
- testing_layer: unit
- target_environment: fix-raw-20260630T095936Z-consistency-merge
- required_evidence: grep 确认 dev→test 方向的提示文本
- evidence_level: mock
- artifact_ref: docs/epics/consistency-merge/merge-fix/test-evidence/acceptance-1.log
- test_command: |
  echo "=== worktree-common.sh Check 2 ==="
  grep -A8 "dev has commits not in test" docs/system/workspace/scripts/worktree/worktree-common.sh | grep -q "git merge" && echo "PASS: git merge found" || echo "FAIL: no git merge"
  echo "=== wt-close Check 4 ==="
  grep -A8 "开发工位有提交未同步到测试工位" docs/system/workspace/scripts/worktree/wt-close | grep -q "git merge" && echo "PASS: git merge found" || echo "FAIL: no git merge"
- expected_output: "PASS: git merge found" x2
- expected_RED_output: "FAIL: no git merge" (修复前提示 cherry-pick)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: |
    修复前 worktree-common.sh:287: `git cherry-pick ...` — cherry-pick 被 hook 阻止
    修复前 wt-close:581: `git cherry-pick ...` — 同上

### acceptance-2
- id: AT-002
- requirement: test→dev 不一致时硬拒绝 + 给出正确流程指引
- acceptance_target: worktree-common.sh + wt-close 的消息中含 "⛔" 和 "丢弃式沙箱"，不含 "cherry-pick"
- testing_layer: unit
- target_environment: fix-raw-20260630T095936Z-consistency-merge
- required_evidence: grep 确认 test→dev 方向的提示文本
- evidence_level: mock
- artifact_ref: docs/epics/consistency-merge/merge-fix/test-evidence/acceptance-2.log
- test_command: |
  echo "=== worktree-common.sh Check 1 ==="
  grep -A10 "test has commits not in dev" docs/system/workspace/scripts/worktree/worktree-common.sh | grep -q "丢弃式沙箱" && echo "PASS: 硬拒绝提示" || echo "FAIL: missing"
  echo "=== wt-close Check 3 ==="
  grep -A10 "测试工位有提交未同步到开发工位" docs/system/workspace/scripts/worktree/wt-close | grep -q "丢弃式沙箱" && echo "PASS: 硬拒绝提示" || echo "FAIL: missing"
- expected_output: "PASS: 硬拒绝提示" x2
- expected_RED_output: "FAIL: missing" (修复前提示 cherry-pick 同步)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: |
    修复前 worktree-common.sh:260: 提示 cherry-pick 回开发工位
    修复前 wt-close:556: 提示 cherry-pick 回开发工位

### acceptance-3
- id: AT-003
- requirement: pre-commit hook 阻断 test-pre-merge-* 分支上的 git commit
- acceptance_target: pre-commit.sh 含有 test-pre-merge-* 分支检测和退出逻辑
- testing_layer: unit
- target_environment: fix-raw-20260630T095936Z-consistency-merge
- required_evidence: grep 确认 pre-commit.sh 中的测试工位阻断
- evidence_level: mock
- artifact_ref: docs/epics/consistency-merge/merge-fix/test-evidence/acceptance-3.log
- test_command: |
  grep -q "test-pre-merge-\*" docs/system/workspace/hooks/pre-commit.sh && echo "PASS: test-pre-merge block found" || echo "FAIL: missing"
  grep -q "不允许直接提交" docs/system/workspace/hooks/pre-commit.sh && echo "PASS: commit block message" || echo "FAIL: missing"
- expected_output: "PASS: test-pre-merge block found\nPASS: commit block message"
- expected_RED_output: "FAIL: missing" (修复前没有阻断)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: 修复前 pre-commit.sh 未对 test-pre-merge-* 分支做任何阻断

### acceptance-4
- id: AT-004
- requirement: 测试工位有未提交修改时 wt-close 硬拒绝而非提示提交
- acceptance_target: wt-close Check 2 消息不含 "git add" / "git commit"，含 "stash"
- testing_layer: unit
- target_environment: fix-raw-20260630T095936Z-consistency-merge
- required_evidence: grep 确认 wt-close 的 dirty test 提示
- evidence_level: mock
- artifact_ref: docs/epics/consistency-merge/merge-fix/test-evidence/acceptance-4.log
- test_command: |
  grep -A10 "测试工位有未提交的修改" docs/system/workspace/scripts/worktree/wt-close | grep -q "stash" && echo "PASS: stash mentioned" || echo "FAIL: missing"
  grep -A10 "测试工位有未提交的修改" docs/system/workspace/scripts/worktree/wt-close | grep -q "不允许在测试工位上直接提交" && echo "PASS: hard block" || echo "FAIL: missing"
- expected_output: "PASS: stash mentioned\nPASS: hard block"
- expected_RED_output: "FAIL: missing" (修复前提示 git add -A && git commit)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: |
    修复前 wt-close:527: `git add -A && git commit -m "test: results"`
    修复前 wt-close:531: `git cherry-pick ...` 提示同步回开发工位

## Unit
- acceptance_target: bash -n 语法检查三文件全通过
- testing_layer: unit
- target_environment: fix-raw-20260630T095936Z-consistency-merge
- required_evidence: 三个文件 bash -n 无错误
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: pr-create-guarded / pr-merge-guarded / pr-review-guarded / wt-close 四处一致性
- testing_layer: integration
- target_environment: test-pre-merge-20260630T095936Z-consistency-merge
- required_evidence: 四个命令的消息中 dev→test 方向均不含 "cherry-pick"
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 人工触发 dev→test 不一致场景，确认提示 git merge 而非 cherry-pick
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T095936Z-consistency-merge → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: 待 GREEN 阶段验证
