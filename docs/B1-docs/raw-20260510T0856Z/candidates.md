# Candidates
## C-20260510T0856Z-A: legacy issue
- title: task_mode 切换后看门狗豁免一次
- status: promoted
- decision_reason: wait→auto 切换竞态导致看门狗误杀 supervisor，需要 mode_just_switched 豁免机制
- promoted_issue_path: docs/issues/I-20260510T0856Z-A/issue.md
- milestone: M-20260510T0856Z-A
- completion_note: I-20260510T0856Z-A 已完成 closeout，切换豁免机制已吸收到 develop
