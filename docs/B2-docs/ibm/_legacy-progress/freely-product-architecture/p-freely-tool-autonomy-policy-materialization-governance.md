# Progress: freely-tool-autonomy-policy-materialization-governance

- issue_id: `I-20260401-1303-A-2`
- issue_path: `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
- title: `Freely tool autonomy policy materialization governance`
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- updated_at: `2026-04-01`
- summary:
  - 当前 worktree 已把第一条 materialization 实现切片真正落到代码与工具文档层：`freely init` 生成的项目级 `.codex/config.toml` 现在按 `mode` 写入，`auto` 明确 materialize `approval_policy = "never"`。
  - `tools.md` 也已补齐 Codex project-local baseline、Codex launch-time auto injection、以及 Claude Code launch-time-only materialization 的 readback，避免再把不同消费层混成一条“工具配置”。
  - focused verification 已确认这条 owner 的当前 scope 足以从 `in_dev` 推进到 `in_verification`；下一步只剩 canonical completion writeback，而不是继续扩 scope。
- evidence:
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `docs/B2-docs/config/packaging/pre-tests.md`
  - `docs/B2-docs/config/packaging/code-reviews/20260401-freely-tool-autonomy-policy-materialization-verification.md`
- next:
  - further tool-surface or ACP adapter expansion should materialize as a narrower follow-on instead of reopening this bounded owner.

## Closure Evidence

- closure_status: `merged-and-verified`
- closure_evidence:
  - `merge_commit: 641cb55`
  - `docs/B2-docs/config/packaging/code-reviews/20260401-freely-tool-autonomy-policy-materialization-verification.md`
  - `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `./bin/governance-check`
