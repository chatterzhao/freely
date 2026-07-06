---
local_id: I-20260321-1706
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260321-1706/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '37'
    url: https://github.com/chatterzhao/freely/issues/37
    synced_at: '2026-04-27T11:15:34Z'
  gitee:
    issue_id: IJFO5Z
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5Z
    synced_at: '2026-04-27T13:14:32Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:34Z'
hash: ''
created_at: '2026-04-27T11:15:34Z'
updated_at: '2026-04-27T11:15:34Z'
platform_state: closed
---

真实狗粮表明：worker 工位在 `operator_stop` 后，`freely chat` 虽然能 durable 接住新 signal，并通过 interruption dispatcher 归类成 delegated continuation / verification handoff，但不会把 worker 主循环重新拉起，导致插话只堆积在 intake，没人真正接棒。

这会破坏 Freely 的产品语义：如果 `chat` 是正式入口，那么当 signal 明确要求当前 worker 继续做事时，runtime 必须在安全条件下重新激活正确的 worker loop。

canonical: docs/B2-docs/human/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md
