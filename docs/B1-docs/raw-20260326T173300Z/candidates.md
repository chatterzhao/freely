# Candidates - 20260326-1733--ibm-pretests-real-environment-acceptance-quality

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326T173300Z-A: legacy issue
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
  - 已确认这不是 `I-20260322T013500Z` 的简单 continuation，而是其 aftercare/enforcement follow-on
  - 已确认 scope 不等同于某一条具体业务 issue 的 pre-tests 重写，而是修改通用 IBM 质量门槛
  - 已给出最小 landing zones，并能解释后续如何通过真实 runtime/dogfood 场景验证
- open_questions:
  - 后续若要 machine-readable schema，应落在 `pre-tests.md` 还是独立 acceptance manifest
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The issue boundary is now stable: keep the lifecycle focused on IBM truth-source enforcement, not verification-template unification. The minimal structure can be enforced through doc-ibm-execution, PRD quality, completion gate, and issue materialization checklist without introducing a new schema in this round.`
    verdict: `ready_to_materialize`
- acceptance_hint:
  - `pre-tests.md` 默认先写可执行 acceptance，而不是“只读某文档时应能看出什么”
  - 对 Freely 自治能力，必须写出至少一条真 runtime / dogfood 场景，而不是仅停在 wording review
  - 需要显式写出环境、证据、失败判据、post-merge replay expectation
  - 若某条 issue 不需要其中某类测试，必须写出不适用的理由和替代证据面
- priority: P0
- status: promoted
- decision_reason: 候选边界已稳定。当前最小可交付是收紧 IBM 真源本身，让 `pre-tests.md` 更难被写成弱验收；verification review 模板统一和 machine-readable schema 继续作为后续问题保留，不并入本轮。
- next_action: materialize issue-bound IBM artifacts，冻结 `pre-tests.md` 的 executable acceptance contract 质量门槛，然后进入 truth-source dev 改写。
- revisit_trigger: 当本 issue 完成后，若仍需要统一 verification review 模板或引入 machine-readable acceptance schema，通过新的 lifecycle 承接。
- promoted_issue_id: `I-20260326T181500Z`
- promoted_issue_path: `docs/B2-docs/ibm/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
- legacy_id_mapping: I-20260326T181500Z  # 历史遗留的 issue id
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
