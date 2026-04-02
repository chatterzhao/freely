# Issue: agent-execution-safety-review-and-security-decision-support

- issue_id: `I-20260401-1308-A`
- title: Agent execution safety review and security decision support
- phase_state: `done_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `agent-execution-safety-review-and-security-decision-support`
- issue-name: `agent-execution-safety-review-and-security-decision-support`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/candidates.md#c-20260401-1308-a`
- source_brainstorm: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 的产品面已经在收口“默认高自治 + activation consent + 非阻塞 safeguard guidance”。但运行时如果遇到高风险或高不确定，不能只有单 agent 直觉，也不能轻易退化成用户逐步批准。

因此需要一条可复用 capability owner，专门承接：

1. 当前执行边界是否真的符合 Freely 声明。
2. 下游 tool flags、project-local config、launch-time injection 是否一致。
3. 当单 agent 不应独断时，如何拉起一个或多个 security-focused reviewer 形成内部决策委员会。

这条 issue 的目标不是一口气做完所有 security skills，而是先把 execution-boundary review 和 security decision support materialize 成第一条 capability owner。

## Scope

1. 定义可复用的 execution-boundary review contract：
   - downstream tool runtime flags
   - project-local tool config
   - launch-time injected policy
   - observed posture summary
2. 定义 security decision support 的最小能力 contract：
   - one or more reviewer agents
   - risk summary
   - suggested policy / adapter adjustments
   - reviewer-backed continuation guidance
3. 明确 safeguard recommendation 属于支持面：
   - 允许输出更安全运行建议
   - 但不把 safeguard 缺失默认升级成 runtime blocker
4. 明确这条 capability 与产品 owner 的边界：
   - 不接管 product-facing activation consent
   - 不重写 Freely 默认 autonomy posture

## Non-Goals

1. 不一次承接 supply-chain、secret scanning、artifact exposure 全部 capability。
2. 不把 `init` / `doctor` 的产品默认策略重写成 skill owner。
3. 不把用户重新拉回逐步人工批准。
4. 不在本 issue 中直接实现全量 remediation automation。

## Acceptance

1. issue artifacts 明确 execution-boundary review 是可复用 capability，而不是某个单一产品页面逻辑。
2. issue artifacts 明确 security decision support 是内部 AI reviewer / committee 能力，而不是 product consent owner。
3. 文档明确：
   - tool flags
   - project-local config
   - launch-time injection
   - observed posture
   之间需要可比对、可解释、可写回 evidence 的 review contract。
4. 文档明确 safeguard recommendation 是 capability 输出的一部分，但 safeguard 缺失本身不默认等于 runtime 必须停机。
5. 本 issue 与 Freely-self 产品 owner 不再抢同一层 owner。

## Completion

- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/brainstorms/b-agent-execution-safety-review-and-security-decision-support.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/prd.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/pre-tests.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/tasks.md`
- `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/candidates.md`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- wording review confirming:
  - capability boundary is distinct from Freely-self product baseline
  - internal reviewer / committee semantics are clear
  - safeguard recommendation remains non-blocking by default

## Next

- 这条 issue 先承接 execution-boundary review 和 security decision support。
- 更宽的 capability families，例如 supply-chain、secret/artifact exposure、incident remediation，应由后续 owner 继续拆分，不回灌本 issue 变成另一个 umbrella。
