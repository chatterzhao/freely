# Issue: agent-execution-safety-review-and-security-decision-support

- issue_id: `I-20260401-1308-A`
- title: Agent execution safety review and security decision support
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `agent-execution-safety-review-and-security-decision-support`
- issue-name: `agent-execution-safety-review-and-security-decision-support`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-1308-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-agent-execution-safety-review-and-security-decision-support.md`
- verification_artifact_dir: `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/code-reviews`
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

- `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
- `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/brainstorms/b-agent-execution-safety-review-and-security-decision-support.md`
- `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/prd.md`
- `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/pre-tests.md`
- `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/tasks.md`
- `docs/progress/workspace-routing-foundation/p-agent-execution-safety-review-and-security-decision-support.md`
- `docs/system/workspace/skills/agent-execution-safety-review/SKILL.md`
- `docs/system/workspace/skills/agent-execution-safety-review/references/decision-ladder.md`
- `docs/system/workspace/skills/agent-execution-safety-review/references/evidence-writeback.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-security-review-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
- `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
- `bin/pretests-gate --issue docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`

## Implementation Status

- `2026-04-01`: advisory-only execution-boundary review slice landed on `develop`.
  - project-local security review truth is visible in status surfaces.
  - `baseline-status`, `live-status`, and `doctor` expose canonical execution-boundary posture.
  - the workspace skill exists as a reusable advisory capability instead of doc-only prose.
- `2026-04-01`: reviewer/committee first-use slice landed in this lane as runtime brief + writeback references.
  - `freely security-review-brief` emits machine-readable reviewer / committee guidance from execution-boundary truth.
  - `skill:agent-execution-safety-review` now freezes the decision ladder and evidence writeback fields for future reviewer-backed continuation.

## Next

- Advisory-only execution-boundary review is already canonical on `develop`; this lane extends that capability with a reusable runtime brief and writeback contract rather than reopening product-owner scope.
- Later draft continuations that rematerialize the same execution-boundary audit plus `security-review-brief` surface, including the narrower `2246/2325` follow-on attempts, should be treated as absorbed by this completed owner rather than reopened as parallel ownership.
- If Freely later needs true multi-reviewer runtime orchestration, it should continue under this owner and consume the same brief keys rather than inventing a second security-review vocabulary.
- Broader capability families such as artifact exposure, supply-chain review, secret scanning, and incident remediation should continue as dedicated owners rather than widening this owner into another umbrella.
