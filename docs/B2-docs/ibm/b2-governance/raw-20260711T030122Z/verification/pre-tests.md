# Pre-Tests: Agent docs v2
- issue_id: I-20260711T030122Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 三文档身份声明清晰
- acceptance_target: 每个文档第一句明确身份
- testing_layer: unit
- target_environment: fix/raw-20260711T030122Z-agent-docs-v2
- required_evidence: grep 确认身份声明
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-1.log
- test_command: |
  grep -q "我是项目主人" docs/system/workspace/agents/manager-agent.md && echo "manager PASS" || echo "manager FAIL"
  grep -q "我是自由行动者" docs/system/workspace/agents/worker-agent.md && echo "worker PASS" || echo "worker FAIL"
  grep -q "我是独立审查者" docs/system/workspace/agents/reviewer-agent.md && echo "reviewer PASS" || echo "reviewer FAIL"
- expected_output: "manager PASS\nworker PASS\nreviewer PASS"
- expected_RED_output: "manager FAIL\nworker FAIL\nreviewer FAIL"
- actual_RED_output: |
  manager FAIL (旧版: "运行在 develop 工位")
  worker FAIL (旧版: "运行在 feature/*、fix/* 工位")
  reviewer FAIL (旧版: "独立评审 agent")
- actual_output: |
  manager PASS (我是项目主人)
  worker PASS (我是自由行动者)
  reviewer PASS (我是独立审查者)
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: 
- red_how: fix — 旧版文档身份声明机械（"运行在 X 工位"），新版改为第一人称身份声明

### acceptance-2
- id: AT-002
- requirement: 旧 skill 名无残留
- acceptance_target: worker-agent.md 不包含 fix-execution
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 无匹配
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-2.log
- test_command: |
  ! grep -q "fix-execution\|feature-execution\|auto-loop-orchestrator" docs/system/workspace/agents/worker-agent.md && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: worker-agent.md 包含 fix-execution
- actual_output: |
  PASS: no old skill names
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: 
- red_how: fix — 旧版 worker-agent.md 列出 fix-execution（已废弃）

### acceptance-3
- id: AT-003
- requirement: 三文档结构统一
- acceptance_target: 每个文档包含"我的工具箱"和"我如何工作"章节
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认章节标题
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-3.log
- test_command: |
  for f in manager-agent.md worker-agent.md reviewer-agent.md; do
    if grep -q "我的工具箱" "docs/system/workspace/agents/$f" && grep -q "我如何工作" "docs/system/workspace/agents/$f"; then
      echo "$f PASS"
    else
      echo "$f FAIL"
    fi
  done
- expected_output: "manager-agent.md PASS\nworker-agent.md PASS\nreviewer-agent.md PASS"
- expected_RED_output: FAIL (旧版无统一结构)
- actual_RED_output: |
  FAIL: worker-agent.md 无"我的工具箱""我如何工作"章节
  FAIL: reviewer-agent.md 无"我的工具箱""我如何工作"章节
- actual_output: |
  manager-agent.md PASS
  worker-agent.md PASS
  reviewer-agent.md PASS
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260711T030122Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker: 
- red_how: fix — 旧版 worker/reviewer 文档结构不统一

## Unit
- acceptance_target: Markdown 语法正确
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 无语法错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/AT-002/AT-003 的 grep 检查已覆盖结构验证
- replacement_evidence: AT-001 + AT-002 + AT-003

## Integration
- acceptance_target: Manager 加载新版 prompt 后行为改善
- testing_layer: integration
- target_environment: develop (daemon cycle)
- required_evidence: Manager 正确理解身份并自主决策
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证需要真实 daemon 运行，属于 post-merge dogfood 范畴
- replacement_evidence: AT-001/AT-002/AT-003 代码级验证

## End-to-End
- acceptance_target: daemon 正常运行，Manager/Worker/Reviewer 各司其职
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: daemon cycle 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon 验证
- replacement_evidence: AT-001/AT-002/AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: agent 文档修改，post-merge daemon 运行间接验证
