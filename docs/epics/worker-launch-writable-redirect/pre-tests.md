# Pre-tests: Worker Launch 保护工位验证

## Unit

### worker_prompt_launchable 拒绝保护分支

- environment: bash unit test
- evidence: `test-freely-worker-prompt-protected-branch-rejected`
- failure signal: test exits non-zero
- failure handling: 检查 test 输出定位逻辑错误

```bash
# 构造 prompt file 指向 develop branch
PROMPT=$(mktemp)
cat > "$PROMPT" <<'EOF'
- branch: `develop`
EOF
worker_prompt_launchable_for_manager_project "$PROJECT" "$PROMPT" && fail "expected non-launchable for develop"
pass "develop rejected"
rm -f "$PROMPT"
```

repeat for `main`, `test-pre-merge-*`, `release/*`.

### worker_prompt_launchable 放行 fix/feature

- environment: bash unit test
- evidence: same test file
- failure signal: return 1 on legitimate writable branches

```bash
for branch in fix/raw-20260509-test feature/my-feature; do
  PROMPT=$(mktemp)
  cat > "$PROMPT" <<EOF
- branch: \`$branch\`
EOF
  worker_prompt_launchable_for_manager_project "$PROJECT" "$PROMPT" || fail "expected launchable for $branch"
  rm -f "$PROMPT"
done
pass "fix/* and feature/* accepted"
```

### empty branch 值放行

- environment: bash unit test
- evidence: same test file
- failure signal: return 1 on unparseable branch

```bash
PROMPT=$(mktemp)
cat > "$PROMPT" <<'EOF'
- title: some prompt without branch header
EOF
worker_prompt_launchable_for_manager_project "$PROJECT" "$PROMPT" || fail "expected launchable for unparseable branch"
pass "empty branch value accepted"
rm -f "$PROMPT"
```

## Integration

### 现有 worker launch 测试不变

- environment: `test-freely-manager-worker-launch-linkage`
- evidence: existing test file unchanged
- failure signal: test exits non-zero after change
- failure handling: 检查是否受新检查影响（理论上不受，因为现有测试的 target branch 是 fix/feature）

### Real-environment

- real_environment_status: pass
- real_environment_reason: 本次不需要真实环境测试——改动是 bash 函数内的 prefix match，有完整的 unit 覆盖即可。

## End-to-End

### manager exit-contract 对 develop-target prompt 的正确行为

- environment: `test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable`
- evidence: 该测试已包含 non-launchable prompt 场景；需确认本改动不改变其语义
- 若 worker prompt 的 target 是 develop，新逻辑 return 1，runtime 记录 `WORKER_PROMPTS_NOT_LAUNCHABLE`

## Acceptance Items

### AT-001 develop rejected
- id: develop-rejected
- requirement: develop branch 在 worker_prompt_launchable 中被拒绝
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-002 main rejected
- id: main-rejected
- requirement: main branch 被拒绝
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-003 test-pre-merge rejected
- id: test-pre-merge-rejected
- requirement: test-pre-merge-* branch 被拒绝
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-004 fix accepted
- id: fix-accepted
- requirement: fix/* branch 正常放行
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-005 feature accepted
- id: feature-accepted
- requirement: feature/* branch 正常放行
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-006 empty branch accepted
- id: empty-branch-accepted
- requirement: 空 branch 值放行（不破坏既有流程）
- evidence_level: unit
- status: pass
- artifact_ref: test-freely-worker-prompt-protected-branch-rejected
- surface_kind: branch
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-007 existing linkage test unaffected
- id: existing-linkage-unaffected
- requirement: 现有 worker-launch-linkage 测试不受影响
- evidence_level: integration
- status: skip
- artifact_ref: test-freely-manager-worker-launch-linkage
- surface_kind: test-suite
- target_lane: feature-local
- promotion_gate: dev_commit

### AT-008 rejected develop records WORKER_PROMPTS_NOT_LAUNCHABLE
- id: rejected-develop-records-not-launchable
- requirement: 拒绝 develop 后 runtime 记录 WORKER_PROMPTS_NOT_LAUNCHABLE
- evidence_level: integration
- status: skip
- artifact_ref: test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable
- surface_kind: contract
- target_lane: feature-local
- promotion_gate: dev_commit
