# Issue: agent-ready-prd-for-freely-flow

- issue_id: `I-20260321-1530`
- title: Agent-ready PRD architecture for Freely IBM flow
- phase_state: `completed`
- milestone: `M-20260321-ai-native-doc-loop`
- epic-name: `ai-native-doc-loop`
- story-name: `agent-ready-prd-for-freely-flow`
- issue-name: `agent-ready-prd-for-freely-flow`
- source_candidate: `docs/B1-docs/raw-20260321-1530/candidates.md#c-20260321-1530-a`
- source_brainstorm: `docs/B1-docs/raw-20260321-1530/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 现有的 `prd.md` 普遍偏短，能表达“这轮要做什么”，但还不足以让 AI 在 doc-loop 和 dev-loop 中稳定继续工作。外部研究显示，AI 时代的 PRD 不应只是说明文，而应成为能驱动 prototype、eval、task slicing 和模型升级重判的执行控制面。

如果 Freely 自己不先把这个结构说明白，后续由 AI 生成 PRD 时就只能继续输出“Goal + Product Surface”一类的薄文档，难以支撑更强的 agentic loop。

## Scope

1. 明确 Freely 中 `B` 与 `PRD` 的边界
2. 给出 AI-ready PRD 在 Freely 中的最小结构
3. 把结构冻结为正式 IBM 产物：
   - issue
   - issue-bound brainstorm
   - `prd.md`
   - `pre-tests.md`
   - `tasks.md`
4. 给出下一跳实现/治理改造应如何消费这份 PRD

## Non-Goals

- 本 issue 不直接修改所有既有 `prd.md`
- 不在本轮把 `doc-ibm-execution` skill、模板生成器或 runtime 提示词全部改完
- 不把“AI 时代 PM 流程”扩成完整组织设计方法论

## Acceptance

- Freely 中 `B` 不是被误写成“单独产出 PRD 的过程”
- `prd.md` 明确包含 agent-ready 所需字段，而不只是人类摘要
- `pre-tests.md` 和 `tasks.md` 能从该 PRD 自然派生
- 当前 IBM 产物已经足够驱动后续治理或实现改造

## Completion

- `docs/B1-docs/raw-20260321-1530/brainstorms.md`
- `docs/B1-docs/raw-20260321-1530/candidates.md`
- `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md`
- `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/brainstorms/b-agent-ready-prd-for-freely-flow.md`
- `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/prd.md`
- `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/pre-tests.md`
- `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/tasks.md`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/tests/test-doc-ibm-prd-quality-bar`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-doc-ibm-prd-quality-bar`

## Next

- `doc-ibm-execution` 的最小门槛、governance-check 与回归测试已在本轮落盘；后续若要继续推进，可再开治理 issue 决定是否补模板生成器或更强的自动 lint
- 若只是把本 issue 当作研究真源，后续可按 story 逐个吸收，不强制一次性迁移全部历史 PRD
