---
local_id: I-20260331-2012-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260331-2012/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '74'
    url: https://github.com/chatterzhao/freely/issues/74
    synced_at: '2026-04-27T11:21:35Z'
  gitee:
    issue_id: IJFO7E
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7E
    synced_at: '2026-04-27T13:15:29Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:35Z'
hash: ''
created_at: '2026-04-27T11:21:35Z'
updated_at: '2026-05-17T12:21:21Z'
platform_state: closed
---

Freely 已经把两条规则写成 canonical truth：

1. unresolved candidate 不能从 active scans 中消失
2. develop merge 需要 `C-* -> M-* -> I-*` 的可追踪 owner 链

但这之间仍有一个缺口：当前 gates 过去只检查“candidate 出现在某个 milestone 队列里”，没有证明这条 candidate 被放进了正确且仍 active、会继续消费它的 milestone。结果就是：

- `milestone: unassigned` 仍可能漏过
- `pending://milestone-binding` 会把 candidate 伪装成已排期
- completed milestone 也可能意外承接新的 unresolved candidate
- 当前 milestone 已确定不消费的 `needs_research` candidate 可能长期悬空

本 owner 的任务就是把这层 placement correctness 变成正式 gate，并补齐最小 r

canonical: docs/B2-docs/ibm/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md
