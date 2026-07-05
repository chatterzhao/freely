# Candidates - 20260326-1705--manager-owner-stance-and-source-patrol

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326-1705-A: legacy issue
- candidate_format_version: v2
- title: Manager owner stance and source-patrol completeness governance
- problem: 当前真源分别定义了 manager patrol、human interruption、progress continuation 与 pre-brainstorm 生命周期，但仍缺少一条分层清楚的治理语义：开发 Freely 的治理文档不能直接充当产品化后的 manager / worker 能力真源；而产品能力真源里也还没有把“主管是项目主人、插话只是 advisory signal、主管要巡检 interruption / milestone / progress / pre-brainstorm 直到状态闭环”完整写死。
- why_now: 这已经在 Freely 自举中造成真实歧义。若不先把“开发治理输入”和“产品能力真源”拆清，再去定义主管人格与 source patrol contract，就很容易把开发期文档错当运行期角色真源，或者把状态缺口留在未补账的 source 里。
- acceptance_criteria:
  - 明确区分开发 Freely 的治理输入与 Freely 产品能力真源，两者不得互相代替
  - candidate 明确冻结主管主人姿态、advisory interruption semantics 与 source-patrol completeness 的最小边界
  - candidate 明确指出本条 lifecycle 只改产品能力真源，不把开发治理文档当成运行期角色 contract
  - candidate 已给出稳定 issue 归属、story name 与下一跳 IBM 范围
- promotion_gate:
  - 与 `manager-watchdog-trigger-and-drift-reconcile-governance` 的关系已收窄为依赖，不重复定义 patrol dual-entry / restart-point routing
  - 与 `manager-delegation-after-sufficient-patrol-evidence-governance` 的关系已收窄为依赖，不重复定义 evidence-sufficient 后的 delegation threshold
  - 与 `active-lifecycle-boundary-and-dogfooding-capability-discovery` 的关系已收窄为治理前提，不再把 `PROJECT_INTENT` 当成运行期角色真源
  - story-name / issue-name / issue scope 已稳定，可直接进入 issue-bound IBM
- open_questions:
  - 最终 wording 应优先落在 `manager-agent` / `worker-agent`，还是先在 skill reference 中冻结再回写 agent contract
  - `pre-brainstorm` source patrol completeness 是放在 patrol reference 里主写，还是由 `context-source-skill` / `doc-pre-brainstorm-execution` 分担
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `Candidate scope is now stable enough to materialize because it no longer treats dogfooding governance docs as runtime role truth, and its overlap with existing patrol/delegation issues has been reduced to explicit dependencies.`
    verdict: `ready_to_materialize`
- acceptance_hint:
  - 明确区分开发 Freely 的治理输入与 Freely 产品能力真源，两者不得互相代替
  - 产品能力真源明确写出主管是项目主人，不是客服、转单台或同步等待人类的代理
  - 产品能力真源明确写出人类插话是 advisory signal，不自带调度权
  - 产品能力真源明确主管面对插话时先判断兼容/冲突/阻塞/纠偏/可并行，再决定吸收或重排
  - 产品能力真源明确 standing-source patrol 至少覆盖 interruption、milestone、progress、pre-brainstorm 四类来源
  - 产品能力真源明确发现 source drift 后，主管应补账、核实、重排、委派，而不是默认追问人
  - worker 能力真源同步明确只负责核实/执行/带回 evidence，不接管项目级裁决
- priority: P0
- status: promoted
- decision_reason: 候选边界已经稳定，可以进入正式 issue-bound IBM。当前下一跳不再是继续讨论“要不要有这条治理”，而是把它 materialize 成 milestone-owned issue，并冻结会改哪些产品能力真源。
- next_action: materialize 正式 issue、issue-bound brainstorm、`prd.md`、`pre-tests.md` 与 `tasks.md`，把 story scope 冻结为产品能力真源改写，不在本条 lifecycle 中回写开发治理文档。
- revisit_trigger: 当 IBM 产物完成后，进入 `done_ibm` 并切到 dev-loop；若实现阶段发现仍需要改动开发治理输入，再回到新的 pre-brainstorm，而不是扩大当前 issue。
- promoted_issue_id: `I-20260326-1835`
- promoted_issue_path: `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- legacy_id_mapping: I-20260326-1835  # 历史遗留的 issue id
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
