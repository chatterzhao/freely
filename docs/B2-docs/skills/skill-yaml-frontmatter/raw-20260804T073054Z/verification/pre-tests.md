# Pre-Tests: SKILL.md frontmatter YAML 修复 + 部署链校验
- issue_id: I-20260804T073054Z-A

## Acceptance Items

### AT-001
- id: AT-001
- requirement: 30 个损坏的 SKILL.md frontmatter 修复后可被 YAML 解析
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 全量 37 个 SKILL.md frontmatter 解析通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/verification/test-evidence/frontmatter-parse.log
- test_command: python3 docs/system/workspace/scripts/tests/test-skill-frontmatter-valid.py
- expected_output: OK (37/37 valid)
- expected_RED_output: 30 files fail (block scalar error)
- actual_RED_output: "total=37 invalid=31（block scalar 解析错误）"
- actual_output: pending
- evidence_file: pending
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: "单元测试 test-skill-frontmatter-valid.py，修复前 30 个文件解析失败"

### AT-002
- id: AT-002
- requirement: deploy-skills 对坏 frontmatter 拒绝部署
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 模拟坏 SKILL.md 时 deploy-skills 非零退出并列出文件
- evidence_level: integration
- artifact_ref: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/verification/test-evidence/deploy-gate.log
- test_command: python3 docs/system/workspace/scripts/tests/test-skill-deploy-gate.py
- expected_output: OK (bad frontmatter rejected)
- expected_RED_output: 无校验，坏文件被部署（断言失败）
- actual_RED_output: "FAIL: deploy-skills has no frontmatter YAML validation"
- actual_output: pending
- evidence_file: pending
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: "集成测试 test-skill-deploy-gate.py，修复前 deploy-skills 不校验 frontmatter"

### AT-003
- id: AT-003
- requirement: pre-commit hook 拦截坏 SKILL.md frontmatter
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 暂存坏 SKILL.md 时 pre-commit 拒绝提交
- evidence_level: integration
- artifact_ref: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/verification/test-evidence/precommit-gate.log
- test_command: bash docs/system/workspace/scripts/tests/test-skill-precommit-gate.sh
- expected_output: OK (pre-commit blocks invalid frontmatter)
- expected_RED_output: pre-commit 不校验，提交通过（断言失败）
- actual_RED_output: "FAIL: pre-commit hook has no skills frontmatter validation"
- actual_output: pending
- evidence_file: pending
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: "集成测试 test-skill-precommit-gate.sh，修复前 hook 无 skills 校验"

### AT-004
- id: AT-004
- requirement: 重新部署后 codex 启动无 Skipped loading 告警
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260804T073054Z-skill-yaml-frontmatter → local codex
- required_evidence: 部署后 `~/.codex/skills` 全部 freely-* SKILL.md 可解析
- evidence_level: real_env
- artifact_ref: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/verification/test-evidence/deploy-load.log
- test_command: python3 docs/system/workspace/scripts/tests/test-skill-deploy-load.py
- expected_output: OK (deployed skills parse; zero invalid)
- expected_RED_output: 部署目录含 30 个坏文件（断言失败）
- actual_RED_output: pending
- actual_output: pending
- evidence_file: pending
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: "端到端：deploy-skills 后解析 ~/.codex/skills 与源目录 frontmatter"

## Unit
- acceptance_target: frontmatter YAML 解析全量通过
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 37/37 valid
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: deploy-skills 与 pre-commit 拦截坏 frontmatter
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 两条拦截路径测试通过
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 部署后 codex 加载全部 skill 无告警
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260804T073054Z-skill-yaml-frontmatter → local codex
- required_evidence: deploy-load 测试 OK
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: (GREEN 后填写 codex 启动验证结果)
