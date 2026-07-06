# Pre-Tests: ./bin/xxx → freely xxx
- issue_id: I-20260705T231534Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 用户可见文本中零 ./bin/ 引用
- acceptance_target: grep 搜索只剩 -f/-x 文件检查 + chmod + source
- testing_layer: unit
- target_environment: test-pre-merge-20260705T231534Z-fix-bin-to-freely
- required_evidence: grep 结果仅含保留模式
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260705T231534Z/verification/test-evidence/acceptance-1.log
- test_command: |
  grep -rn '\./bin/' .githooks/ bin/ docs/system/workspace/scripts/quality/ docs/system/workspace/scripts/worktree/ docs/system/workspace/scripts/runtime/ *.md docs/system/workspace/skills/ 2>/dev/null | grep -v '\.bak\|test-\|source \.\/bin\|chmod.*\.\/bin\|\\-x.*\.\/bin\|\\-f.*\.\/bin'
- expected_output: (空 — 仅剩保留模式)
- expected_RED_output: 多处 ./bin/ 可见引用
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)

### acceptance-2
- id: AT-002
- requirement: freely xxx 命令可正常执行
- acceptance_target: freely wt-status-all 语法不报错
- testing_layer: integration
- target_environment: test-pre-merge-20260705T231534Z-fix-bin-to-freely
- required_evidence: bash -n 检查通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260705T231534Z/verification/test-evidence/acceptance-2.log
- test_command: |
  for f in .githooks/pre-commit.sh .githooks/pre-push.sh .githooks/pre-merge-commit.sh bin/git-worktree-guard; do
    bash -n "$f" && echo "PASS: $f" || echo "FAIL: $f"
  done
- expected_output: 全部 PASS
- expected_RED_output: N/A
- actual_RED_output: N/A
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: not_applicable
- red-green-not-applicable-reason: 语法应始终正确，RED/GREEN 不适用
- status: pending
- blocker: (失败时填写)

## Unit
- acceptance_target: grep 验证零可见 ./bin/
- testing_layer: unit
- target_environment: test-pre-merge-20260705T231534Z-fix-bin-to-freely
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: bash -n 语法 + freely xxx 可执行
- testing_layer: integration
- target_environment: test-pre-merge-20260705T231534Z-fix-bin-to-freely
- required_evidence: AT-002
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: freely pr-create-guarded 全部门禁通过
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260705T231534Z-fix-bin-to-freely → develop merge chain
- required_evidence: PR 创建成功
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯文本替换，grep + bash -n 验证充分
