# Issue: agent-execution-safety-review-and-security-decision-support

- issue_id: `I-20260401-1308-A`
- title: Agent execution safety review and security decision support
- phase_state: `in_verification`
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
- progress_path: `docs/progress/workspace-routing-foundation/p-agent-execution-safety-review-and-security-decision-support.md`
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
6. `freely security-review-brief` 能从当前 project posture 输出 machine-readable reviewer / committee guidance，而不是要求操作者靠会话记忆决定是否升级内部复核。
7. `skill:agent-execution-safety-review` 将 `none -> single-reviewer -> decision-committee` ladder 与 evidence writeback 要求固化为可复用能力真源。

## Completion

- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/brainstorms/b-agent-execution-safety-review-and-security-decision-support.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/prd.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/pre-tests.md`
- `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/tasks.md`
- `docs/system/workspace/skills/agent-execution-safety-review/SKILL.md`
- `docs/system/workspace/skills/agent-execution-safety-review/references/decision-ladder.md`
- `docs/system/workspace/skills/agent-execution-safety-review/references/evidence-writeback.md`
- `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/candidates.md`
- `docs/milestones.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
- `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
- `./bin/governance-check`

## Implementation Status

- `2026-04-01`: first execution-boundary automation slice landed in runtime.
  - `freely doctor` now audits activation-consent truth and project-scoped Codex posture drift instead of only checking docs/hooks.
  - `baseline-status` and `live-status` now expose `execution_boundary_audit_status` and `execution_boundary_audit_detail`.
  - focused regressions cover legacy auto consent drift, Codex approval-policy drift, and the aligned baseline snapshot.
- `2026-04-01`: reviewer/committee first-use slice landed as reusable runtime brief + skill.
  - `freely security-review-brief` now emits machine-readable decision support derived from execution-boundary truth.
  - `skill:agent-execution-safety-review` consumes that brief and freezes the pass/warn/fail decision ladder for future reviewer/committee orchestration.

## Next

- 当前 first slice 已把 execution-boundary review materialize 成自动化 runtime audit；本轮又补了 reviewer/committee first-use brief。后续若要加入真正的 multi-reviewer runtime orchestration，应继续吸收到本 owner，而不是回退成对话习惯。
- 更宽的 capability families，例如 supply-chain、secret/artifact exposure、incident remediation，应由后续 owner 继续拆分，不回灌本 issue 变成另一个 umbrella。
