---
local_id: I-20260326-1815
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '57'
    url: https://github.com/chatterzhao/freely/issues/57
    synced_at: '2026-04-27T11:17:35Z'
  gitee:
    issue_id: IJFO6R
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6R
    synced_at: '2026-04-27T13:15:01Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:35Z'
hash: ''
created_at: '2026-04-27T11:17:35Z'
updated_at: '2026-04-27T11:17:35Z'
platform_state: closed
---

Freely 已经把 `pre-tests.md` 定义成 issue-level acceptance 控制面，也把 verification 收敛成 integration / acceptance-first。但当前 enforcement 仍然不够强：

- `prd.md` 的 `Eval Plan` 仍可能先收缩成 truth-source wording review
- `pre-tests.md` 仍可能退化成“单独阅读某文档时能否看出语义”
- governance / agent / skill 改造型 issue 尤其容易缺少真实 runtime、application-native real-environment 与 end-to-end dogfood 验收面

对 Freely 这种自治 AI 开发系统来说，这会让最关键的能力线在 IBM 阶段就失去可执行 acceptance contract，后续 verification、replay 与 closeout 只能靠口头解释恢复。

canonical: docs/B2-docs/ibm/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md
