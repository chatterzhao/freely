# Issue: freely-tool-autonomy-policy-materialization-governance

- issue_id: `I-20260401-1303-A-2`
- title: Freely tool autonomy policy materialization governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `freely-tool-autonomy-policy-materialization-governance`
- issue-name: `freely-tool-autonomy-policy-materialization-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260401-1303/candidates.md#c-20260401-1303-a`
- source_brainstorm: `docs/B1-docs/raw-20260401-1303/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-freely-tool-autonomy-policy-materialization-governance.md`
- verification_artifact_dir: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/code-reviews`
- depends_on:
  - `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经明确选择默认高自治方向，但“这份姿势如何被具体工具消费”仍然缺少独立 owner。

当前仓库里最明显的 split 是：

1. `tools.md` 与 runtime launcher 在 `auto` 路径下已经把 `codex` / `cc` 定义成免交互、自动批准。
2. 本条最初 materialize 时，`freely init` 生成的项目级 `.codex/config.toml` 仍写入 guarded posture。
3. product owner 已经把 Freely canonical posture 与 activation consent 冻结成上位真源，但还没有独立 owner 来回答“project-local config、launch-time injection、manual-only hint 分别怎么落”。

如果不把这层 materialization 单独收口，Freely 就会继续停在“理念上默认自治，但具体接线还在自相矛盾”的状态。

## Scope

1. 冻结 `Freely canonical policy -> tool adapter injection -> tool-local config materialization` 的 contract。
2. 收口当前 `tools.md` / launcher auto posture 与 `.codex/config.toml` historical guarded posture 的 split，并把已落地切片写回真相。
3. 明确哪些工具配置应：
   - 写入项目级配置
   - 在启动时动态注入
   - 仅作为 manual-only guidance 保留给用户级配置
4. 为 `codex`、`cc`、`cc-use-codex-cli` 写清 auto posture 的 materialization path。
5. 明确 ACP 是后续可选 adapter boundary，不是本条的前置 blocker。

## Non-Goals

1. 不重新定义 product-facing activation consent 文案。
2. 不把用户 home 目录里的工具配置变成默认自动改写面。
3. 不在本条中落 reusable security capability / skill 设计。
4. 不要求 ACP 先收口后本条才能继续。

## Acceptance

1. Freely canonical policy、tool adapter injection、tool-local config materialization 的职责分层清楚。
2. 当前 `tools.md` / launcher 与 `.codex/config.toml` 的 split 被写成明确的 reproduced fact，并有统一收口方向；已落地的 first slice 不再被误写成未解决现状。
3. `codex`、`cc`、`cc-use-codex-cli` 的 auto posture materialization path 可解释、可实现、可验证。
4. 用户全局配置默认仍保持 manual-only guidance，不被 Freely 静默污染。
5. ACP 被明确定位为 follow-on adapter boundary，而不是 owner 前置依赖。
6. issue contract 足够窄，后续实现可直接映射到 `init`、launcher、tool docs 和 focused tests。

## Completion

- `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/issues/freely-tool-autonomy-policy-materialization-governance.md`
- `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/brainstorms/b-freely-tool-autonomy-policy-materialization-governance.md`
- `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/prd.md`
- `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/pre-tests.md`
- `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/tasks.md`
- `docs/B1-docs/raw-20260401-1303/brainstorms.md`
- `docs/B1-docs/raw-20260401-1303/candidates.md`
- `docs/B1-docs/raw-20260323-1435/brainstorms.md`
- `docs/B1-docs/raw-20260323-1435/candidates.md`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- wording review confirming:
  - product-owned posture truth and tool-owned materialization are not mixed
  - project-local config, launch-time injection, and manual-only guidance are clearly distinguished
  - ACP remains optional follow-on instead of a blocker

## Implementation Status

- `2026-04-01`: the current worktree contains the first focused implementation slice for project-local tool materialization.
  - `freely init` now writes project-level [`.codex/config.toml`](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260401-feature-freely-security-baseline-governance/.codex/config.toml) defaults through a mode-aware path:
    - `auto` writes `approval_policy = "never"`
    - project-local `sandbox_mode = "workspace-write"` and `network_access = false` remain recommended Codex defaults rather than Freely hard blockers
  - focused shell tests for `codex`, `cc`, and `cc-use-codex-cli` were updated to accept the blocking activation-consent contract via `--accept-default-autonomy`
  - init/chat fixture tests that now depend on hook truth were updated to create `.githooks` wrappers
- `2026-04-01`: the current worktree also contains the follow-through doc/readback slice for remaining tool surfaces.
  - [`tools.md`](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260401-feature-freely-security-baseline-governance/docs/system/workspace/tools.md) now explicitly distinguishes:
    - Codex project-local baseline materialization via `.codex/config.toml`
    - Codex launch-time auto posture injection via `--dangerously-bypass-approvals-and-sandbox`
    - Claude Code profiles as launch-time materialization surfaces rather than fake project-local config owners
  - the issue-bound brainstorm now records the original split as historical reproduced fact plus the landed first slice, instead of leaving `.codex/config.toml` described as currently unresolved guarded posture
- verified in this lane:
  - `bash -n docs/system/workspace/scripts/runtime/freely`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `./bin/governance-check`
- observed but not absorbed into this issue:
  - the worker-reactivation and local-reentry residuals were split out to `docs/B1-docs/raw-20260401-1831/`, then promoted to separate owner `I-20260401-1831-A`
  - they are now tracked as separate workspace-routing truth rather than open regressions in this issue

## Next

- 这条 issue 的当前 contract、第一条 project-local slice、以及 tool-doc/readback follow-through 已经在当前 worktree 完成 feature-bound验证，当前进入 develop-bound verification。
- 若后续再出现新的 materialization drift，应只针对新增工具 / ACP adapter seam 开更窄的 follow-on，而不是重新把本 owner 扩回 umbrella。
