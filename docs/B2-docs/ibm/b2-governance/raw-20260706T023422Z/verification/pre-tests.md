# Pre-Tests: docs-structure-refactor 遗漏补完
- issue_id: I-20260706T023422Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 生产代码零旧路径引用
- acceptance_target: bin/ + .githooks/ + quality/ + runtime/ + skills/ 中零 docs/pre-brainstorms/ + docs/issues/ + docs/epics/ 旧路径
- testing_layer: unit
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers
- required_evidence: grep -r 全量搜索零结果
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/verification/test-evidence/acceptance-1.log
- test_command: |
  grep -rn 'docs/pre-brainstorms/\|docs/issues/raw-\|docs/epics/' \
    bin/ .githooks/ docs/system/workspace/scripts/quality/ \
    docs/system/workspace/scripts/runtime/ docs/system/workspace/scripts/worktree/ \
    docs/system/workspace/skills/ 2>/dev/null | grep -v 'B1-docs\|B2-docs\|\.bak\|_legacy' | wc -l
  [ $? -eq 0 ] && echo "PASS: 零旧路径" || echo "FAIL"
- expected_output: PASS: 零旧路径
- expected_RED_output: 非零残留
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)

### acceptance-2
- id: AT-002
- requirement: I-* 文件 verification_artifact_dir 含 raw-{key} 层
- acceptance_target: 所有 I-* verification_artifact_dir 匹配 docs/B2-docs/{epic}/{story}/raw-{key}/code-reviews
- testing_layer: unit
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers
- required_evidence: 正则检查 4 层路径格式
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/verification/test-evidence/acceptance-2.log
- test_command: |
  find docs/B2-docs -name 'I-*.md' -exec grep -l 'verification_artifact_dir' {} \; | while read f; do
    v=$(grep 'verification_artifact_dir' "$f" | head -1)
    if ! echo "$v" | grep -qE 'raw-\d+'; then echo "FAIL: $f"; fi
  done
  echo "PASS: all have raw-{key} layer"
- expected_output: PASS: all have raw-{key} layer
- expected_RED_output: FAIL lines
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)

### acceptance-3
- id: AT-003
- requirement: B2-docs 非 legacy 文件均在 raw-{key} 目录下
- acceptance_target: 除 _legacy/_misplaced 外的 B2-docs 文件路径含 raw-{key}
- testing_layer: integration
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers
- required_evidence: find 检查文件路径含 raw-
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/verification/test-evidence/acceptance-3.log
- test_command: |
  find docs/B2-docs -type f -name '*.md' | grep -v '_legacy\|_misplaced' | while read f; do
    if ! echo "$f" | grep -q '/raw-'; then echo "MISSING: $f"; fi
  done
  echo "PASS: all files under raw-{key}"
- expected_output: PASS: all files under raw-{key}
- expected_RED_output: MISSING lines
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)

## Unit
- acceptance_target: grep + 正则检查无旧路径 + 路径格式正确
- testing_layer: unit
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers
- required_evidence: AT-001 + AT-002 全部通过
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: B2-docs 目录结构符合设计规范
- testing_layer: integration
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers
- required_evidence: AT-003 通过
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 全部门禁通过（governance-gate + pretests-gate）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T023422Z-fix-refactor-leftovers → develop merge chain
- required_evidence: freely pr-create-guarded 全部 PASS
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 路径替换 + 文件移动，grep/find 测试充分覆盖。无运行时变更。
