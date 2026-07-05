# Brainstorms: ai-autonomy-checkpoint-commit-governance

- id: `b-20260318-0715-a`
- date: `2026-03-18`
- status: `active`
- source: `review/test + current worktree verification continuity for I-20260318T093000Z`

## Context

Freely 已经有 `checkpoint-guard`、项目级 dirty budget、首跳 prompt 注入与 `pre-commit` 范围门禁，但“AI 自治时应在何时主动提交”仍不够硬：

- 仅靠 git hook 太晚，拦不住 AI 在 commit 之前已经把工位扩写得很乱
- 仅靠聊天提醒不可靠，不能算 Freely 能力
- 目前已有 worker 在达到 checkpoint 边界后自行收口的正向案例，但仍依赖人工观察与临场介入

这意味着 Freely 还缺“AI 自治提交治理”的正式控制面规则：当达到 checkpoint 条件且最小验证已通过时，下一轮应优先 commit，而不是继续扩 scope。

## Why not IBM or dev yet

- 当前只确认了问题方向，还没有稳定的 issue-owned 边界、验收口径和控制面落点拆分。
- 该问题跨 `LAWS`、runtime、checkpoint 判定和 manager-worker 监督，不适合直接塞回 `I-20260318T093000Z` 的 verification scope。
- 按法律要求，dev-loop / verification 暴露出的边界外新问题应先回到 pre-brainstorm，再由 milestone 承接。

## Current boundary

- 核心问题：当 worktree 达到 checkpoint 条件且最小验证已通过时，Freely 是否必须把“continuity + commit/checkpoint”升级为下一轮默认动作。
- 约束边界：
  - 不能只靠 git hook 末端阻断。
  - 不能要求主管或人类人工观察后再提醒。
  - 需要兼容单工位与多 worktree supervisor/worker 排班。
- 当前仍未定：
  - “最小验证已通过”的结构化判定口径
  - runtime 默认动作和 skill/hook 分工
  - 是否需要独立 skill 或只增强现有 control-plane

## Questions

1. `checkpoint_required=true` 时，是否应把“下一轮优先 commit/checkpoint”提升成 runtime 级默认动作，而不是只作为 prompt 提醒？
2. “已通过最小验证门”应如何结构化判定，避免 AI 在未验证时过早提交，或在已验证后继续无界扩写？
3. 这类能力应落在哪些层：`LAWS`、`runtime/freely`、`start-lead-agent.sh`、`checkpoint-guard`、`pre-commit/pre-push`、还是新的 skill？
4. 在多 worktree / manager-worker 模式下，主管应如何监督 worker 的提交节奏，而不是等到 merge 前才发现问题？

## Initial conclusions

- 自治提交治理必须是 Freely 控制面能力，不是人工习惯。
- git hook 只应作为末端兜底；真正的提交时机应在 AI 工具启动前、轮次间和 checkpoint 边界上由 runtime 决定。
- 达到 checkpoint 边界后，至少应先写 phase-appropriate continuity，再决定 `commit-first`、`fresh_with_handoff` 或按 ownership 分流。
- 主管位需要能看到 worker 的提交压力，并在排班时把“先收口再继续”作为正式监督动作。

## Boundary stabilization

当前边界已收敛到 3 个必须同时成立的子问题：

1. checkpoint-ready 判定
- 输入至少包括：当前 worktree dirty budget、staged scope、最近验证结果、是否存在未写 continuity。
- 输出至少区分：`continue_without_commit`、`continuity_first`、`commit_first`、`split_scope_first`。

2. control-plane ownership
- `LAWS` 负责定义什么时候必须优先 continuity + commit。
- `runtime/freely` 负责把该结论升级为下一轮默认动作。
- `checkpoint-guard` 负责给出可执行判定，而不是只返回模糊 warning。
- supervisor 视图负责把 worker 的 commit pressure 暴露出来。

3. anti-regression guard
- 不能让未过最小验证的工位被误判为应先 commit。
- 不能让已达 checkpoint-ready 的工位继续无限扩写实现。
- 不能把 control-plane 和 product-plane 混在同一个 checkpoint commit 里通过。

## Likely IBM shape

若继续收敛顺利，后续 issue-bound IBM 应至少包含：

- issue focus: `checkpoint-ready commit governance`
- likely epic/story: `workspace-routing-foundation / ai-autonomy-checkpoint-commit-governance`
- minimum artifact targets:
  - `docs/LAWS.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/quality/checkpoint-guard`
  - `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
  - 相关脚本级测试

## Promotion gate to IBM

满足以下条件后再进入 `doc-ibm-execution`：

- “最小验证已通过”的结构化字段来源已经明确，而不是自然语言约定。
- runtime / guard / supervisor 三者的职责分层已经冻结。
- 能说清它是增强现有 control-plane，还是需要独立 skill；不能两种方案并存推进。

## Recommended next hop

- 下一跳：继续 `doc-pre-brainstorm-execution`
- 原因：需要先把“commit-first after checkpoint-ready”的边界、验收口径和 control-plane 归属收敛到可 materialize 的 candidate，再决定是否进入 IBM
