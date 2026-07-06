# Issue: manager-owner-stance-and-source-patrol-governance

- issue_id: `I-20260326-1835`
- title: Manager owner stance and source-patrol completeness governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-owner-stance-and-source-patrol-governance`
- issue-name: `manager-owner-stance-and-source-patrol-governance`
- verification_artifact_dir: docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/raw-20260326-1835/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260326T181000Z/candidates.md#c-20260326-1705-a`
- source_brainstorm: `docs/B1-docs/raw-20260326T181000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
  - `docs/B2-docs/ibm/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md`
  - `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 在自举开发中已经形成了两层真源：

- 开发 Freely 的治理输入
- Freely 完成后会长期被消费的产品能力真源

但当前文档体系仍容易把这两层混成一层，进而导致两个持续偏差：

1. 把 `PROJECT_INTENT / CONSTITUTION / LAWS` 误读成运行期 manager / worker 的直接角色真源。
2. 在产品能力真源中，主管的主人姿态、插话只是 advisory signal、以及 interruption / milestone / progress / pre-brainstorm 的 source-patrol completeness 仍未被完整写死。

这条 issue 的目标不是发明新 loop，也不是继续扩 runtime，而是把上述边界稳定写回 Freely 的产品能力真源，使 Freely 自己和后续用户都能从 agent / skill / reference 里直接读出正确语义。

## Scope

1. 明确分层：
- 开发 Freely 的治理输入不直接充当产品化后的 manager / worker role contract。
- 产品能力真源以 `docs/system/workspace/**` 为落点。

2. 在产品能力真源中写清主管人格：
- 主管是项目主人、全局裁决者、节奏维护者、source-patrol 补账责任人。
- 主管不是客服、转单台、会议纪要员，也不默认以“等人澄清”为常规策略。

3. 在产品能力真源中写清插话语义：
- human interruption 是 advisory signal，而不是自带调度权的命令。
- 主管先判断兼容 / 冲突 / 阻塞 / 纠偏 / 可并行，再决定 absorption、queue、freeze 或 worker delegation。

4. 在产品能力真源中写清 source-patrol completeness：
- standing-source patrol 至少覆盖 interruption、milestone、progress、pre-brainstorm。
- 发现 source drift 时，主管默认补账、核实、重排、委派，而不是直接把不确定性回抛给人类插话者。

5. 这条 issue 只改产品能力真源：
- `docs/system/workspace/agents/**`
- `docs/system/workspace/skills/**`
- 必要的 reference
- 不把 `docs/PROJECT_INTENT.md`、`docs/CONSTITUTION.md`、`docs/LAWS.md` 当成这条 issue 的主要改写面

## Acceptance

- `manager-agent` 明确写出主管是项目主人，不是同步等待人类澄清的代理。
- `worker-agent` 明确写出 worker 只负责核实 / 执行 / 带回 evidence，不接管项目级方向裁决。
- interruption 相关 skill 明确写出 human interruption 是 advisory signal，不自带调度权。
- patrol / routing 相关 skill 或 reference 明确写出 standing-source patrol 至少覆盖 interruption、milestone、progress、pre-brainstorm。
- source drift 的默认动作被写清：补账、核实、重排、委派，而不是默认追问人。
- 新 wording 不与已有 manager trigger / delegation threshold / active lifecycle boundary 真源冲突。

## Completion

- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/brainstorms/b-manager-owner-stance-and-source-patrol-governance.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/prd.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/raw-20260326-1835/verification/pre-tests.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/tasks.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
- `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-manager-owner-stance-and-source-patrol-governance.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/code-reviews/20260326-manager-owner-stance-and-source-patrol-governance-verification.md`

## Verification

- `./bin/governance-check`
- wording review confirming:
  - dogfooding governance inputs and capability truth are not conflated
  - manager/worker/interrupt/patrol wording remains non-overlapping with adjacent issues

## Next

- 当前 lifecycle 已完成 truth-source 改写与 verification。
- 若后续还要把 source completeness 进一步脚本化、状态面 machine-readable 化，或让 runtime / manager 自动消费更强的 patrol transaction，应通过新的 lifecycle 承接，不扩大当前 issue scope。
