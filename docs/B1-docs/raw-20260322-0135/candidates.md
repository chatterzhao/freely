# Candidates

- id: C-20260322-0135-A
- title: Integration-acceptance-first IBM and verification governance
- status: promoted
- adoption_type: n/a
- source_brainstorm: `docs/B1-docs/raw-20260322-0135/brainstorms.md`
- why_now: Freely 狗粮反复证明，很多真实缺口先通过端到端行为暴露；如果 verification 仍默认从代码阅读开始，就会错过 `pre-tests.md` 本应承担的 acceptance 控制面。
- proposed_scope:
  - clarify `pre-tests.md` as the issue-level acceptance control surface emitted by IBM
  - define verification/default review as integration-acceptance-first, with code review serving risk localization instead of replacing acceptance
  - write this priority back to the canonical loop / IBM truth sources
- acceptance_hint:
  - IBM truth sources state `pre-tests.md` is not an appendix but the issue-level acceptance control surface
  - verification defaults prioritize integration/acceptance evidence before targeted code review
  - three-loop truth sources describe AI-native verification as behavior-first rather than line-by-line review-first
- promoted_issue_path: `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
- legacy_id_mapping: I-20260322-0135  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
