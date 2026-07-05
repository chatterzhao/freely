# Issue: source-routing-and-derived-worktree-governance

- issue_id: `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `source-routing-and-derived-worktree-governance`
- issue-name: `source-routing-and-derived-worktree-governance`
- verification_artifact_dir: `docs/epics/- epic-name: `workspace-routing-foundation`/- story-name: `source-routing-and-derived-worktree-governance`/code-reviews`
- source_candidate: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md#c-20260307-1201`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

收紧 Freely 自举时的整体路由逻辑，确保：
- 问题来源分层清晰
- candidate 必须进入 milestone 后再进入 IBM
- `IBM` 只处理 milestone-owned issue
- `progress` 只跟踪 dev-loop 执行态
- 依赖未合并父分支的子任务可以使用 derived worktree
- skill 以情景步骤而不是抽象约束来指导 AI 执行
- 首跳在同工具场景下必须继续执行第二跳，而不是把 `next_prompt` 当作终点

## Scope

1. 更新路由与边界治理文档。
2. 更新 `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`dev-loop-execution`、`branch-management`。
3. 增加标准 worktree 创建入口 `freely wt-create`。
4. 更新 hook / AGENTS 提示，使其支持 derived worktree 语义。
5. 明确 IBM 正式产物目录必须在 `docs/epics/{epic-name}/{story-name}/...`。
6. 对齐 `lead-agent`、`workspace/tools.md`、首跳启动 prompt 与脚本回归，禁止同工具场景只输出 `next_prompt` 结束。

## Acceptance

- `LAWS` 和 `PROJECT_INTENT` 对来源分层、IBM 边界、progress 边界、derived worktree 口径一致。
- 核心 skills 以“情景 -> 动作 -> 产物 -> 下一跳”表达。
- `doc-pre-brainstorm-execution` 明确 pre-brainstorm 应在合适 worktree 中写入。
- `doc-ibm-execution` 明确先确定 `epic-name/story-name/issue-name`，再写正式 IBM 产物。
- `freely wt-create` 可支持默认基线和 `--base` 派生基线。
- `lead-agent`、`workspace/tools.md` 与首跳启动 prompt 对“同工具继续第二跳”保持一致。
- 回归测试锁住“默认不要只输出 `next_prompt`”与“必须在当前会话内继续执行第二跳”。

## IBM Handoff

- implementation_scope_summary:
  - 把首跳来源分层、milestone-owned issue 边界、worktree 准备规则与同工具第二跳协议落实到 runtime prompt、workspace skills 和脚本回归。
  - 进入实现时优先承接已落盘的 `start-lead-agent.sh`、`workspace/tools.md`、`lead-agent.md` 与脚本测试改动，不重新打开 issue 边界。
- required_doc_refs:
  - `docs/system/workspace/agents/lead-agent.md`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/start-lead-agent.sh`
  - `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/dev-loop-execution/SKILL.md`

## Verification

- 实现承接了已存在的 runtime / prompt / 测试改动，当前验证重点是首跳在 `selected_tool == AI_TOOL` 时不会停在 route-only handoff。
- 已执行 `TEST`：
  - `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
  - `bash tests/test_doc_gate.sh`
- 已写入 review 证据：
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260316-first-hop-second-hop-verification.md`
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260326-source-routing-canonical-replay-verification.md`
- 当前研究阶段尚未启用正式 `docs/progress/**`，本轮 dev-loop 等价执行证据写入 `docs/pre-brainstorms/CONVERGENCE.md`。

## Next

- canonical replay 已确认旧的 dirty sibling blocker 不再存在，当前 fleet truth 已收敛到 `Summary: total=4, dirty=0`。
- 本 issue 已完成；后续若继续调整首跳分类或派生 worktree 策略，应通过新的 lifecycle 承接。
