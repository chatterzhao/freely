---
local_id: I-20260321-1045
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '34'
    url: https://github.com/chatterzhao/freely/issues/34
    synced_at: '2026-04-27T11:15:09Z'
  gitee:
    issue_id: IJFO5V
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5V
    synced_at: '2026-04-27T13:14:28Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:09Z'
hash: ''
created_at: '2026-04-27T11:15:09Z'
updated_at: '2026-04-27T11:15:09Z'
platform_state: closed
---

现有 `worktree-maintenance-governance` 已能处理单棵树 audit、平面 merge-prep 与 retirement handoff，但 dogfooding 证明还缺少一类高频现实场景：

- 当前 worktree 不是从 `develop` 直接派生，而是依赖未合并父分支
- child 分支完成并不代表可以直接并入 `develop`
- parent 自己的 cleanliness / docs / issue / review 也是 gate
- 基于最新 `develop` 的 merge-prep worktree 会暴露新的 additive governance conflict 或 integration bug

如果 skill 不显式表达这条链路，Freely 仍会反复靠人工经验判断“下一步该合谁、该在哪一层停下、问题归因到哪一层”。

canonical: docs/B2-docs/ibm/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md
