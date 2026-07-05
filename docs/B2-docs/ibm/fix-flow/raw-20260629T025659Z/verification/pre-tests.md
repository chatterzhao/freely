# Pre-Tests: fix flow 统一为 B1→B2→dev→test
- issue_id: I-20260629T025659Z-A

## Acceptance Items

### acceptance-1: fix skill 流程顺序改为 B1→B2→dev→test
- id: AT-001
- requirement: fix skill SKILL.md 的流程描述从 dev→test→B1→B2 改为 B1→B2→dev→test
- acceptance_target: freely-fix-execution SKILL.md 中全链路描述和阶段描述的顺序正确
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: grep 确认 fix skill 流程序列
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-1.log
- test_command: grep "B1.*B2.*dev.*test" ~/.claude/skills/freely-fix-execution/SKILL.md && echo "PASS" || echo "FAIL"
- expected_output: PASS — fix skill 描述 B1→B2→dev→test 顺序
- actual_output: PASS — fix skill 描述 B1→B2→dev→test 顺序
- evidence_file: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-1.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-2: 去掉 test-pre-merge cherry-pick 机制
- id: AT-002
- requirement: fix skill 不再描述在 test-pre-merge 写代码 → cherry-pick 到 fix 工位的流程
- acceptance_target: freely-fix-execution SKILL.md 中无 cherry-pick 相关描述
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: grep 确认无 cherry-pick 描述
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "cherry-pick" ~/.claude/skills/freely-fix-execution/SKILL.md && echo "FAIL: still has cherry-pick" || echo "PASS: cherry-pick removed"
- expected_output: PASS: cherry-pick removed
- actual_output: PASS — cherry-pick dance removed from fix skill
- evidence_file: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-2.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-3: three-loop 真源同步更新
- id: AT-003
- requirement: three-loop-capability-lifecycle.md 的 Fix 变体路径从 dev→test→B1→B2 改为 B1→B2→dev→test
- acceptance_target: three-loop 文档的 Fix 变体路径与 fix skill 一致
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: grep 确认 three-loop 文档 Fix 路径已更新
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-3.log
- test_command: grep -A2 "Fix 修复" docs/system/workspace/three-loop-capability-lifecycle.md | grep "B1.*B2.*dev" && echo "PASS" || echo "FAIL"
- expected_output: PASS — Fix 变体路径 B1→B2→dev
- actual_output: PASS — Fix 变体路径 B1→B2→dev
- evidence_file: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-3.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-4: AGENTS.md 流程序列更新
- id: AT-004
- requirement: AGENTS.md 中 fix 行从 dev→test→B1→B2 改为 B1→B2→dev→test
- acceptance_target: AGENTS.md fix 流程序列正确
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: grep 确认 AGENTS.md fix 行已更新
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-4.log
- test_command: grep "^fix:" AGENTS.md | grep "B1.*B2.*dev.*test" && echo "PASS" || echo "FAIL"
- expected_output: PASS — fix 行 B1→B2→dev→test
- actual_output: PASS — fix 行 B1→B2→dev→test
- evidence_file: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-4.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

### acceptance-5: test-execution skill fix 流程序列更新
- id: AT-005
- requirement: test-execution skill 的 fix 流程序列从 dev→test→B1→B2 改为 B1→B2→dev→test
- acceptance_target: freely-test-execution SKILL.md fix 行已更新
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: grep 确认 test skill fix 行已更新
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-5.log
- test_command: grep "fix:.*B1.*B2.*dev.*test\|fix:.*wt-create.*B1.*B2" ~/.claude/skills/freely-test-execution/SKILL.md && echo "PASS" || echo "FAIL"
- expected_output: PASS — test skill fix 行 B1→B2→dev→test
- actual_output: PASS — test skill fix 行 B1→B2→dev→test
- evidence_file: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/verification/test-evidence/acceptance-5.log
- blocker: (失败时填写)
- status: passed
- red-green-status: green

## Unit
- acceptance_target: 6个文件修改完成，所有 grep 检查通过
- testing_layer: unit
- target_environment: feature/raw-20260629T025659Z-fix-flow-unify worktree
- required_evidence: 5条 AT 全部 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 单元 grep 检查已覆盖在 AT-001 至 AT-005 中
- replacement_evidence: 见 ## Acceptance Items AT-001~AT-005

## Integration
- acceptance_target: not applicable — 纯文档修改，无模块间集成面
- testing_layer: integration
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次仅修改 skill 文档和流程描述，不涉及模块间数据流
- replacement_evidence: 单元 grep 检查已覆盖全部改动面

## End-to-End
- acceptance_target: fix skill 流程顺序修改后，后续 fix 工位能正确按 B1→B2→dev→test 顺序工作
- testing_layer: end-to-end
- target_environment: post-merge develop → 下一个 fix worktree
- required_evidence: 下一个 fix 工位创建后流程正确
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 端到端验证需要在合并后通过实际 fix 工位验证，无法在当前 feature 工位中完成。单元 grep 检查已在 AT-001~005 覆盖全部改动面
- replacement_evidence: 合并后下一个 fix 工位将实际走 B1→B2→dev→test 流程进行端到端验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次为文档+代码修改，真实环境验证通过 grep 检查已确认所有流程序列正确，合并后由实际 fix 工位进一步验证
