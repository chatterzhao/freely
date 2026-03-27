# Candidates - 20260326-1733--ibm-pretests-real-environment-acceptance-quality

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326-1733-A
- candidate_format_version: v2
- title: IBM pre-tests executable real-environment acceptance quality governance
- problem: 现有真源已经要求 `pre-tests.md` 是 issue-level acceptance 控制面，并强调 integration / acceptance-first，但 enforcement 仍不足。新 issue 仍会把 `pre-tests.md` 写成文档阅读检查，特别是治理型 issue，导致 Freely 这种自治 AI 系统缺少必须的集成、真环境和端到端狗粮验收 contract。
- why_now: 这是上游能力，不先收紧，后续所有业务和治理 issue 都会继续在弱验收下推进。当前就已经在 `manager-owner-stance-and-source-patrol-governance` 上复现，说明问题不是个别写法，而是 IBM 质量门槛还不够硬。
- acceptance_criteria:
  - 候选明确区分“truth-source wording review”与“executable acceptance contract”，并把后者定义为默认主面
  - 候选明确规定 Freely 自治能力默认必须回答 integration、application-native real-environment、end-to-end dogfood 三类验收面；若不适用必须写明理由
  - 候选明确规定 `prd.md` 的 `Eval Plan` 不能先收缩成文档阅读检查
  - 候选明确指出本条生命周期优先服务上游 IBM/testing 真源，应先于一般业务能力被合并消费
- promotion_gate:
  - 已确认这不是 `I-20260322-0135` 的简单 continuation，而是其 aftercare/enforcement follow-on
  - 已确认 scope 不等同于某一条具体业务 issue 的 pre-tests 重写，而是修改通用 IBM 质量门槛
  - 已给出最小 landing zones，并能解释后续如何通过真实 runtime/dogfood 场景验证
- open_questions:
  - 需要新增固定 `pre-tests.md` 模板字段，还是只强化 quality bar 与 checklist
  - verification review 模板是否要与 IBM 一起升级，防止 closeout 仍按弱验收进行
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The problem is clearly distinct from the already-completed integration-acceptance-first governance issue: this follow-on is about making executable acceptance harder to under-specify for governance issues and other IBM outputs. The remaining uncertainty is about the minimal fixed structure and whether verification templates should be upgraded in the same lifecycle.`
    verdict: `needs_more_research`
- acceptance_hint:
  - `pre-tests.md` 默认先写可执行 acceptance，而不是“只读某文档时应能看出什么”
  - 对 Freely 自治能力，必须写出至少一条真 runtime / dogfood 场景，而不是仅停在 wording review
  - 需要显式写出环境、证据、失败判据、post-merge replay expectation
  - 若某条 issue 不需要其中某类测试，必须写出不适用的理由和替代证据面
- priority: P0
- status: needs_research
- decision_reason: 方向和优先级已经清楚，但是否要引入新的 `pre-tests.md` 固定字段、是否同步升级 verification review 模板、以及如何表达“真环境测试必做但不等于每次都写新脚本”这几个点仍需再收敛，先保持在 pre-brainstorm。
- next_action: 继续 pre-brainstorm，先评审现有 IBM truth source、若干强/弱 `pre-tests.md` 样本，以及最小 runtime dogfood 场景表达方式；收敛后再决定是直接 materialize 成 issue，还是拆成 IBM gate 与 verification template 两条 issue。
- revisit_trigger: 当 executable acceptance contract 的最小结构、环境/证据/失败判据字段，以及与 verification closeout 的边界都能冻结成独立 issue scope 时，重新进入 materialization 判断。
- promoted_issue_path: `pending://ibm-pretests-real-environment-acceptance-quality-materialization`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
