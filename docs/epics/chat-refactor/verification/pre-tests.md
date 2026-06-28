# Pre-Tests: chat 重构 — comment + discuss + archive skill
- issue_id: I-20260628T005815Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: freely comment --issue 写评论到 GitHub，本地不留
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: GitHub issue 出现新评论，本地 docs/issues/ 无新增文件
- test_command: ./bin/freely comment --issue raw-20260628T005815Z "test comment at $(date -u +%Y%m%dT%H%M%SZ)"
- expected_output: 命令返回成功，GitHub #3601 出现该评论，本地 docs/issues/raw-20260628T005815Z/issue.md 无变化
- actual_output: (由 skill:freely-test-execution 执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-2
- acceptance_target: freely comment 对已关闭 issue 直接拒绝
- testing_layer: unit
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: 命令返回非零退出码，stderr 包含"已关闭"提示
- test_command: ./bin/freely comment --issue raw-20260601T000000Z "should fail" 2>&1; echo "exit=$?"
- expected_output: 提示 issue 已关闭，exit=1
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-3
- acceptance_target: freely discuss 新建 session，创建平台 Discussion
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: 本地 DB 有 discussion 记录，GitHub 有 Discussion 创建
- test_command: ./bin/freely discuss --project <project> --message "test discussion $(date -u +%Y%m%dT%H%M%SZ)"
- expected_output: 返回 session id，本地 DB discussions 表有记录，GitHub Discussions 有新帖子
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-4
- acceptance_target: freely discuss --archive 手工导出，产出评论或 raw issue
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: session 标记 archived，平台有对应评论或新 issue
- test_command: ./bin/freely discuss --archive <session-id>
- expected_output: 导出成功，session 状态变为 archived，平台有产出物
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-5
- acceptance_target: agent-table.toml 配置 discuss_slot + pool=1
- testing_layer: unit
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: 配置语法正确，agent-table-query 返回讨论 slot
- test_command: grep -A2 "discuss_slot" <project>/.freely/agent-table.toml && echo "OK"
- expected_output: discuss_slot 行和 pool: 1 行，最后输出 OK
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

### acceptance-6
- acceptance_target: 旧 chat --issue 入口重定向提示
- testing_layer: unit
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: 运行旧命令提示使用新命令
- test_command: ./bin/freely chat --issue raw-xxx "test" 2>&1; echo "exit=$?"
- expected_output: 提示使用 freely comment，exit=1
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

## Unit
- acceptance_target: cmd_comment 函数、cmd_discuss 函数、讨论归档 skill 函数单元测试
- testing_layer: unit
- target_environment: feature-raw-20260628T005815Z-chat-refactor
- required_evidence: 每个函数核心逻辑可独立验证
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 这些是 bash 脚本命令，无独立单元测试框架。验证通过端到端 acceptance items 覆盖。
- replacement_evidence: acceptance 1-6 的端到端测试结果

## Integration
- acceptance_target: comment → discuss → export 三者联调不冲突
- testing_layer: integration
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor
- required_evidence: 连续执行 comment + discuss + discuss --archive 无异常

## End-to-End
- acceptance_target: 完整 chat 重构后 Freely 自举开发流程不受影响
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T005815Z-chat-refactor → develop merge chain
- required_evidence: feature worktree 能正常完成 feedback → wt-create → B1 → B2 → dev → pr-create → merge

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 需要在真实 GitHub + GitCode 环境中验证跨平台行为
