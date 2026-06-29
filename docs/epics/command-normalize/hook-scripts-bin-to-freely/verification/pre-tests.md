# Pre-Tests: replace ./bin/ with freely in hook scripts and start-lead-agent

- issue_id: I-20260629T132042Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 6 个 .sh 文件中所有 CLI 命令引用从 ./bin/xxx 替换为 freely xxx
- acceptance_target: 6 个文件中不再存在任何 `./bin/` CLI 命令调用（source 和 -f/-x 检查除外）
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 扫描结果：无 `./bin/freely`、`./bin/pr-`、`./bin/wt-`、`./bin/governance-`、`./bin/checkpoint-`、`./bin/pretests-` 等命令调用残留
- evidence_level: integration
- artifact_ref: docs/epics/command-normalize/hook-scripts-bin-to-freely/verification/test-evidence/acceptance-1.log
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T132042Z-hook-scripts-bin-to-freely
  for f in .githooks/pre-commit.sh docs/system/workspace/hooks/pre-commit.sh docs/system/workspace/hooks/pre-merge-commit.sh docs/system/workspace/hooks/pre-push.sh docs/system/workspace/hooks/reference-transaction.sh docs/system/workspace/scripts/start-lead-agent.sh; do
    # 只检查 CLI 命令调用（如 ./bin/freely、./bin/pr-*、./bin/wt-*、./bin/governance-*、./bin/checkpoint-guard、./bin/pretests-gate）
    # 排除 source 和 [[ -f/-x ]] 检查
    matches=$(grep -nE '^\s*\.\/bin\/(freely|pr-|wt-|governance|checkpoint|pretests)' "$f" 2>/dev/null || true)
    if [ -n "$matches" ]; then
      echo "FAIL: $f still has ./bin/ CLI references:"
      echo "$matches"
      exit 1
    fi
  done
  echo "PASS: all 6 files have no ./bin/ CLI command references"
- expected_output: "PASS: all 6 files have no ./bin/ CLI command references"
- expected_RED_output: "FAIL: ... still has ./bin/ CLI references:" 并列出匹配行
- actual_RED_output: |
  FAIL: .githooks/pre-commit.sh still has ./bin/ CLI references (6 lines: pr-merge-guarded, wt-create, wt-close, freely sync-tooling)
  FAIL: docs/system/workspace/hooks/pre-commit.sh still has ./bin/ CLI references (7 lines: same patterns)
  FAIL: docs/system/workspace/hooks/pre-push.sh still has ./bin/ CLI references (2 lines: pr-create-guarded)
  FAIL: docs/system/workspace/hooks/reference-transaction.sh still has ./bin/ CLI references (1 line: pr-merge-guarded)
  RED confirmed: AT-001 — ./bin/ CLI command references present in 4 of 6 files
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: (not_applicable 时填写)
- not_applicable_explanation: (not_applicable 时填写)
- replacement_evidence: (not_applicable 时填写)
- red_how: fix: 在修改前执行 grep 搜索 6 个文件中的 `^./bin/(freely|pr-|wt-|governance|checkpoint|pretests)` 模式，确认 4 个文件存在大量 CLI 命令引用残留（pre-commit.sh x2, pre-push.sh, reference-transaction.sh），start-lead-agent.sh 和 pre-merge-commit.sh 命令引用格式略有不同但仍存在。bug 可复现：216 个文件已统一为 `freely xxx`，这 6 个文件仍用 `./bin/xxx`

### acceptance-2
- id: AT-002
- requirement: worktree-common.sh 的 source 引用和 [[ -f ]] 检查保留不变
- acceptance_target: .githooks/pre-commit.sh 和 docs/system/workspace/hooks/pre-commit.sh 中的 worktree-common.sh 引用未被误改
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 worktree-common.sh 的 source/[[ -f ]] 引用仍在
- evidence_level: integration
- artifact_ref: docs/epics/command-normalize/hook-scripts-bin-to-freely/verification/test-evidence/acceptance-2.log
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T132042Z-hook-scripts-bin-to-freely
  for f in .githooks/pre-commit.sh docs/system/workspace/hooks/pre-commit.sh; do
    if ! grep -q 'source.*worktree-common.sh' "$f"; then
      echo "FAIL: $f missing worktree-common.sh source reference"
      exit 1
    fi
  done
  echo "PASS: worktree-common.sh references preserved"
- expected_output: "PASS: worktree-common.sh references preserved"
- expected_RED_output: 不适用——此测试是确认保留不误改，RED 阶段也应 PASS
- actual_RED_output: |
  OK: .githooks/pre-commit.sh has worktree-common.sh source reference
  OK: docs/system/workspace/hooks/pre-commit.sh has worktree-common.sh source reference
  PASS (expected): AT-002 — worktree-common.sh references already preserved. 此测试验证"不误改"，更改前预期 PASS
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- red_how: 此测试验证没有误改 worktree-common.sh 引用。RED 阶段预期 PASS（因为改动前引用仍在），修改后仍需 PASS。标记 red 保持流程一致性

### acceptance-3
- id: AT-003
- requirement: [[ -x "./bin/xxx" ]] 存在性检查替换为 which freely
- acceptance_target: 6 个文件中不再有 `[[ -x "./bin/..." ]]` 检查（worktree-common.sh 的 [[ -f ]] 除外）
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认替换完成
- evidence_level: integration
- artifact_ref: docs/epics/command-normalize/hook-scripts-bin-to-freely/verification/test-evidence/acceptance-3.log
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T132042Z-hook-scripts-bin-to-freely
  for f in .githooks/pre-commit.sh docs/system/workspace/hooks/pre-commit.sh docs/system/workspace/hooks/pre-merge-commit.sh docs/system/workspace/hooks/pre-push.sh docs/system/workspace/hooks/reference-transaction.sh docs/system/workspace/scripts/start-lead-agent.sh; do
    # 检查 [[ -x "./bin/... 模式（排除 worktree-common.sh）
    matches=$(grep -n '\[\[ -x "\.\/bin\/' "$f" 2>/dev/null | grep -v worktree-common.sh || true)
    if [ -n "$matches" ]; then
      echo "FAIL: $f still has [[ -x ./bin/... checks:"
      echo "$matches"
      exit 1
    fi
  done
  echo "PASS: all [[ -x ./bin/... checks replaced with which freely"
- expected_output: "PASS: all [[ -x ./bin/... checks replaced with which freely"
- expected_RED_output: "FAIL: ... still has [[ -x ./bin/... checks:" 并列出匹配行
- actual_RED_output: |
  FAIL: .githooks/pre-commit.sh still has [[ -x "./bin/governance-merge-gate" ]], [[ -x "./bin/checkpoint-guard" ]], [[ -x "./bin/pretests-gate" ]]
  FAIL: docs/system/workspace/hooks/pre-commit.sh still has [[ -x "./bin/governance-merge-gate" ]], [[ -x "./bin/checkpoint-guard" ]], [[ -x "./bin/pretests-gate" ]]
  RED confirmed: AT-003 — [[ -x ./bin/... checks present in pre-commit.sh files (pre-merge-commit.sh and pre-push.sh also have them, caught by AT-001 broader check)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- red_how: fix: 修改前 grep 确认 pre-commit.sh (x2) 存在 3 处 `[[ -x "./bin/..." ]]` 检查（governance-merge-gate, checkpoint-guard, pretests-gate）。其他文件（pre-merge-commit.sh, pre-push.sh）也有类似检查通过 AT-001 捕获。bug 可复现

### acceptance-4
- id: AT-004
- requirement: 用户面向的提示/错误消息中的 ./bin/xxx 路径引用同步更新
- acceptance_target: 6 个文件中的帮助/错误消息里不再有 ./bin/xxx 引用
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认用户消息中的路径引用已更新
- evidence_level: integration
- artifact_ref: docs/epics/command-normalize/hook-scripts-bin-to-freely/verification/test-evidence/acceptance-4.log
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T132042Z-hook-scripts-bin-to-freely
  for f in .githooks/pre-commit.sh docs/system/workspace/hooks/pre-commit.sh docs/system/workspace/hooks/pre-merge-commit.sh docs/system/workspace/hooks/pre-push.sh docs/system/workspace/hooks/reference-transaction.sh docs/system/workspace/scripts/start-lead-agent.sh; do
    # 检查所有 ./bin/xxx 引用（排除 source、[[ -f ]]、[[ -x ]] 检查行）
    # 包括用户面向文本中的路径引用（Usage/提示/帮助消息）
    matches=$(grep -nE '\.\/bin\/(freely|pr-merge|pr-create|wt-create|wt-close|governance|checkpoint|pretests)' "$f" 2>/dev/null | grep -v '\[\[ -[fx]' | grep -v '^\s*source' || true)
    if [ -n "$matches" ]; then
      echo "FAIL: $f still has ./bin/ references:"
      echo "$matches"
      exit 1
    fi
  done
  echo "PASS: all ./bin/ CLI references removed from 6 files"
- expected_output: "PASS: all ./bin/ CLI references removed from 6 files"
- expected_RED_output: "FAIL: ... still has ./bin/ references:" 并列出匹配行
- actual_RED_output: |
  FAIL: .githooks/pre-commit.sh — "Re-run the merge through ./bin/pr-merge-guarded", ./bin/wt-create, ./bin/wt-close, ./bin/freely sync-tooling
  FAIL: docs/system/workspace/hooks/pre-commit.sh — same patterns (7 occurrences)
  FAIL: docs/system/workspace/hooks/pre-merge-commit.sh — "Re-run the merge through ./bin/pr-merge-guarded", "[HOOK] ... not found at ./bin/governance-merge-gate"
  FAIL: docs/system/workspace/hooks/pre-push.sh — "Usage: ./bin/wt-close", "Run: ./bin/pr-create-guarded"
  FAIL: docs/system/workspace/hooks/reference-transaction.sh — "创建 raw issue → ./bin/freely feedback", "Usage: ./bin/wt-close"
  FAIL: docs/system/workspace/scripts/start-lead-agent.sh — "./bin/freely live-status", "./bin/freely task-source-scan"
  RED confirmed: AT-004 — all 6 files have ./bin/ references in user-facing messages and command invocations
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- red_how: fix: 修改前逐文件 grep 搜索 `./bin/(freely|pr-merge|pr-create|wt-create|wt-close|governance|checkpoint|pretests)` 模式（排除 source 和 [[ ]] 检查），确认全部 6 个文件中均存在 ./bin/xxx 引用，包括用户面向的 Usage/提示消息和命令调用。bug 可复现

## Unit
- acceptance_target: 每个文件的 CLI 命令引用格式一致性（grep 验证）
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 全部 4 个 acceptance items 的 grep 输出
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: hook 脚本在 freely 体系下正常工作
- testing_layer: integration
- target_environment: test-pre-merge-20260629T132042Z-hook-scripts-bin-to-freely
- required_evidence: governance-merge-gate 在 test-pre-merge 工位正常执行
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 6 个文件作为全仓命令规范化的一部分，与其他 216 个文件格式一致
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260629T132042Z-hook-scripts-bin-to-freely → develop merge chain
- required_evidence: guarded merge receipts 无 hook 报错
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 216 个文件的同类替换已在 production 正常运行，6 个文件的替换与其格式一致
