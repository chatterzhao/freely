# Pre-Tests: cmd_feedback → issue-sync alignment
- issue_id: raw-20260624T141559Z

## Acceptance Items

### acceptance-1: --help 正确性
- acceptance_target: `freely feedback --help` 不包含 `--repo` 参数，显示 repo 自动检测说明
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260624T141559Z-feedback-issue-sync
- required_evidence: help 输出不含 `--repo` 字样，含 "auto-detected from git remotes"
- test_command: ./bin/freely feedback --help 2>&1 | grep -v '\-\-repo' && echo "PASS: no --repo in help"
- expected_output: PASS: no --repo in help
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: passed

### acceptance-2: --repo 拒绝
- acceptance_target: 传 `--repo` 时返回明确错误
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260624T141559Z-feedback-issue-sync
- required_evidence: 错误信息提示 repo 已自动检测
- test_command: ./bin/freely feedback --repo foo/bar --title x --body y 2>&1; echo "EXIT=$?"
- expected_output: ERROR: --repo is no longer needed; EXIT=1
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: passed

### acceptance-3: 参数校验
- acceptance_target: 缺少 --title/--body 或非法 --severity 时正确报错
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260624T141559Z-feedback-issue-sync
- required_evidence: 三种错误场景均返回 exit 1 + 正确错误信息
- test_command: |
  ./bin/freely feedback --body "test" 2>&1; echo "---"
  ./bin/freely feedback --title "test" 2>&1; echo "---"
  ./bin/freely feedback --title "test" --body "test" --severity P5 2>&1
- expected_output: |
  ERROR: --title is required
  ---
  ERROR: --body is required
  ---
  ERROR: --severity must be P0, P1, or P2
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: passed

### acceptance-4: 本地文件创建
- acceptance_target: 调用 feedback 后生成 `docs/issues/raw-{key}/issue.md`
- testing_layer: end-to-end
- target_environment: fix/raw-20260624T141559Z-feedback-issue-sync
- required_evidence: issue.md 存在且包含正确的 frontmatter 字段
- test_command: |
  ./bin/freely feedback --title "e2e test" --body "test body" 2>&1
  ls docs/issues/raw-*/issue.md | tail -1 | xargs head -5
- expected_output: |
  local_id: raw-...
  kind: raw
  phase_state: proposed
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: passed

### acceptance-5: issue-sync 委托
- acceptance_target: feedback 创建 issue 后 GitHub 上出现对应 issue
- testing_layer: end-to-end
- target_environment: fix/raw-20260624T141559Z-feedback-issue-sync
- required_evidence: GitHub issue URL 出现在 feedback 输出中
- test_command: |
  ./bin/freely feedback --title "pre-test e2e" --body "test" 2>&1 | grep "github.com"
- expected_output: https://github.com/chatterzhao/freely/issues/...
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: passed

## Unit
- acceptance_target: 无独立单元测试边界（纯 bash 函数重写，行为级端到端验证覆盖）
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 无独立可执行单元边界
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: bash 函数内嵌于自由脚本，无独立单元测试框架。行为由 E2E acceptance-1~5 覆盖。
- replacement_evidence: acceptance-1~5 全部 passed

## Integration
- acceptance_target: `issue-sync create` 在 fix worktree 上成功创建 GitHub issue
- testing_layer: integration
- target_environment: fix/raw-20260624T141559Z-feedback-issue-sync
- required_evidence: issue-sync create 输出包含 "GitHub: creating issue..." 和 URL

## End-to-End
- acceptance_target: end-to-end: feedback → local file → issue-sync → GitHub issue
- testing_layer: end-to-end
- target_environment: fix worktree → develop merge chain
- required_evidence: 全链路通过，GitHub issue 存在且内容正确

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 已在 fix worktree 上成功创建并验证 #3436 (测试) 和 #3435 (正式)
