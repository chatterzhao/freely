---
local_id: I-20260322-1801
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '50'
    url: https://github.com/chatterzhao/freely/issues/50
    synced_at: '2026-04-27T11:16:52Z'
  gitee:
    issue_id: IJFO6I
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6I
    synced_at: '2026-04-27T13:14:51Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:52Z'
hash: ''
created_at: '2026-04-27T11:16:52Z'
updated_at: '2026-04-27T11:16:52Z'
platform_state: closed
---

Freely 这次不是遇到一次性 merge 事故，而是暴露出 `pre-test-merge` 作为治理对象的定义不完整：

- 它是临时预集成验证批次，但当前系统还不能稳定表达这个批次何时开始、何时 stale、何时必须退休。
- 它被误当成比较基线、旧实现回收中转站，甚至接近“事实主线”，与 `develop` 的长期集成真相角色发生混淆。
- 进入 `develop` 的 promotion 语义也不清楚：到底是保留整个批次快照，还是回放来源 feature 的已验证结果。

如果这层职责定义不先稳定，Freely 之后即使补 runtime/status 也只是围绕不清晰的治理对象加功能，仍会继续在狗粮过程中反复误用 `pre-test-merge`。

canonical: docs/B2-docs/ibm/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md
