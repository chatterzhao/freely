# Candidates - 20260326-1705--manager-owner-stance-and-source-patrol

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326-1705-A
- title: Manager owner stance and source-patrol completeness governance
- problem: 当前真源分别定义了 manager patrol、human interruption、progress continuation 与 pre-brainstorm 生命周期，但仍缺少一条分层清楚的治理语义：开发 Freely 的治理文档不能直接充当产品化后的 manager / worker 能力真源；而产品能力真源里也还没有把“主管是项目主人、插话只是 advisory signal、主管要巡检 interruption / milestone / progress / pre-brainstorm 直到状态闭环”完整写死。
- why_now: 这已经在 Freely 自举中造成真实歧义。若不先把“开发治理输入”和“产品能力真源”拆清，再去定义主管人格与 source patrol contract，就很容易把开发期文档错当运行期角色真源，或者把状态缺口留在未补账的 source 里。
- acceptance_hint:
  - 明确区分开发 Freely 的治理输入与 Freely 产品能力真源，两者不得互相代替
  - 产品能力真源明确写出主管是项目主人，不是客服、转单台或同步等待人类的代理
  - 产品能力真源明确写出人类插话是 advisory signal，不自带调度权
  - 产品能力真源明确主管面对插话时先判断兼容/冲突/阻塞/纠偏/可并行，再决定吸收或重排
  - 产品能力真源明确 standing-source patrol 至少覆盖 interruption、milestone、progress、pre-brainstorm 四类来源
  - 产品能力真源明确发现 source drift 后，主管应补账、核实、重排、委派，而不是默认追问人
  - worker 能力真源同步明确只负责核实/执行/带回 evidence，不接管项目级裁决
- priority: P0
- status: needs_research
- decision_reason: 方向已经明确，但还需要先把“开发治理输入 vs 产品能力真源”的分层、人格 wording、以及 source completeness transaction 对齐，避免与已存在的 manager-trigger、active-lifecycle、milestone-maintenance 真源产生平行定义。
- next_action: 继续 pre-brainstorm，先冻结四块边界：开发治理输入与产品能力真源的分层、主管主人姿态 wording、advisory interruption semantics、以及 source-patrol completeness transaction；边界稳定后再 materialize 成正式 issue，对 agent/skill/reference 真源做一致性改写。
- revisit_trigger: 当治理输入与能力真源的分层、主管人格、interruption owner semantics、standing-source completeness 范围与 worker handoff contract 可以被冻结成最小一致 issue scope 时，重新进入 materialization 判断。
- promoted_issue_path: `pending://manager-owner-stance-and-source-patrol-governance`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
