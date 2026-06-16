---
local_id: I-20260322-0135
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '45'
    url: https://github.com/chatterzhao/freely/issues/45
    synced_at: '2026-04-27T11:16:26Z'
  gitee:
    issue_id: IJFO6B
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6B
    synced_at: '2026-04-27T13:14:43Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:26Z'
hash: ''
created_at: '2026-04-27T11:16:26Z'
updated_at: '2026-04-27T11:16:26Z'
platform_state: closed
---

Freely 在狗粮过程中已经多次证明，真实缺口更常先通过端到端行为暴露，而不是先通过逐行代码审查暴露。现有真源已经要求 IBM 产出 `prd.md`、`pre-tests.md`、`tasks.md`，但还没有把下面这条口径明确写死：

- `pre-tests.md` 是 issue-level acceptance 的主控制面
- verification 默认应优先检查 integration / acceptance evidence
- code review 的默认角色是风险定位与缺口解释，而不是替代行为验收

如果这条规则不明确，后续 AI 容易重新退化成“先读代码，再补测试”，而不是“先跑验收，再定向读代码解释风险”。

canonical: docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md
