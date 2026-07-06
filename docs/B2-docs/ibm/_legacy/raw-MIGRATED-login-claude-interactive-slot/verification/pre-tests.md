# Pre-Tests: login claude 交互式 slot

## Acceptance Items

| id | requirement | evidence_level | status | artifact_ref | surface_kind | target_lane | promotion_gate |
|----|-------------|---------------|--------|-------------|--------------|-------------|----------------|
| AI-01 | `login claude` 提示 auth_mode → 提示 slot name → 创建 slot + alias | application-native real-environment | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |
| AI-02 | `login claude apikey --name foo` 非交互创建 | integration | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |
| AI-03 | `login claude account --name foo` 非交互创建 | integration | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |
| AI-04 | 空输入终止 exit 2 | integration | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |
| AI-05 | `--yes` 无 `--name` 报错 exit 2 | integration | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |
| AI-06 | settings.json 为 Anthropic 完整骨架 | script-regression | pass | `docs/B2-docs/login-claude-interactive-slot/code-reviews/test-log.md` | cli | premerge-integration | develop_merge |

## Unit

- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: 修改为 bash 脚本，无可独立运行的单元。所有验证通过端到端 CLI 调用完成。
- replacement_evidence: 6 场景端到端测试覆盖所有代码路径

## Integration

| test | environment | evidence | failure signal | failure handling |
|------|-------------|----------|---------------|-----------------|
| `login claude apikey --name foo` | local shell | 创建 `~/.ai-auth/claude-apikey-foo/settings.json` + alias | 非零 exit code，或无文件/alias | 检查 `bash -n` 语法，复查 ai-cli 修改 |
| `login claude account --name foo` | local shell | 创建 `~/.ai-auth/claude-account-foo/` + alias `claude-account-foo="claude"` | 非零 exit code，或无目录/alias | 同上 |
| `login claude apikey` 交互 | local shell | 提示 "Enter slot name for claude apikey" | 无 prompt 或管道输入失败 | 检查 `prompt_value` 调用 |
| 空输入终止 | local shell | ERROR 输出 + exit 2 | exit 0 或目录被创建 | 检查空值检查逻辑 |
| `login claude --yes` 无 --name | local shell | ERROR "--name is required" + exit 2 | exit 0 或继续执行 | 检查 YES_MODE 分支 |

## End-to-End

| scenario | environment | evidence | failure signal | replay |
|----------|-------------|----------|---------------|--------|
| 完整交互流程 `login claude` | local shell | 两步 prompt → 目录 + alias | 任一步失败 | 重新运行 ai-cli |
| apikey 路径 `login claude apikey` | local shell | settings.json 验证 + alias 验证 | 文件格式错误或缺字段 | 检查模板 |
| settings.json schema 验证 | local shell | `python3 -c "import json; json.load(open(...))"` 成功 | JSON 语法错误 | 修复模板中的转义 |

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本次实现已在真实 shell 环境中完成 6 场景端到端测试，覆盖所有交互模式（非交互 `--name`、交互 prompt、空输入终止、`--yes` 报错）。测试涉及真实文件系统（`~/.ai-auth/`）和 shell rc（`~/.zshrc`）写入，验证了完整命令链路。

## Completion Gate

- acceptance target: 6 个 acceptance items 全部 pass
- testing layer: integration + real-environment
- target environment: local shell / test-pre-merge worktree
- required evidence: test-log.md 含全部场景输出
- blocker taxonomy: `execution_pending_or_failed`
