# Pre-Tests: I-20260807T105604Z-A — .codex/config.toml 解除跟踪

- issue_id: I-20260807T105604Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: .codex/config.toml 解除跟踪后，本地配置不再污染 git 工作树
- acceptance_target: test-pre-merge 工位放置本地 .codex/config.toml 后，git ls-files .codex 为空、git status --porcelain 为空、git check-ignore 命中 .gitignore:78
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T105604Z-codex-config-untrack
- required_evidence: acceptance-1.log 包含三条命令输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/_legacy-issues/raw-20260807T105604Z/verification/test-evidence/acceptance-1.log
- test_command: cd test-pre-merge-20260807T105604Z-codex-config-untrack && git ls-files .codex; git status --porcelain; git check-ignore -v .codex/config.toml
- expected_output: ls-files 为空；porcelain 为空；check-ignore 输出 .gitignore:78:.codex/ 匹配
- expected_RED_output: 修复前 ls-files 输出 .codex/config.toml；porcelain 输出 M .codex/config.toml
- actual_RED_output: 修复前 develop：ls-files=.codex/config.toml；status= M .codex/config.toml
- actual_output: ls-files 为空；porcelain 为空；check-ignore 命中 .gitignore:78
- evidence_file: docs/B2-docs/ibm/_legacy-issues/raw-20260807T105604Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: (empty)
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1-A3
- case_design: 在 test-pre-merge 沙箱放入本地个人配置（模拟 develop 上被跟踪时的 dirty 场景），验证 untrack 后 tracked 列表 / porcelain / ignore 三种视图
- red_how: RED 在 develop 复现：git status --short 显示 M .codex/config.toml 且 git ls-files .codex 列出该文件

## Unit
- acceptance_target: 无 — 纯 git 索引状态变更，无可执行单元边界
- testing_layer: unit
- target_environment: N/A
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 改动是 git rm --cached 的索引操作，无函数/脚本输入输出可单测
- replacement_evidence: git ls-files 与 git status 输出即最终证据

## Integration
- acceptance_target: 无独立集成边界 — 由端到端 git 状态验证覆盖
- testing_layer: integration
- target_environment: test-pre-merge-20260807T105604Z-codex-config-untrack
- required_evidence: acceptance-1.log
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端 acceptance-1 已覆盖 tracked / porcelain / ignore 三种视图，无需重复集成层
- replacement_evidence: acceptance-1.log

## End-to-End
- acceptance_target: 本地 .codex/config.toml 存在时 git 工作树保持 clean
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T105604Z-codex-config-untrack
- required_evidence: acceptance-1.log（git ls-files / status --porcelain / check-ignore）
- blocker_taxonomy: execution_pending_or_failed
1. 放置本地 .codex/config.toml（个人字段内容）
2. 执行 git ls-files .codex，确认输出为空
3. 执行 git status --porcelain，确认输出为空
4. 执行 git check-ignore -v .codex/config.toml，确认命中 .gitignore:78

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 已在 test-pre-merge-20260807T105604Z-codex-config-untrack 实机执行，三条命令输出符合预期；RED 场景也在 develop 复现（M .codex/config.toml）
