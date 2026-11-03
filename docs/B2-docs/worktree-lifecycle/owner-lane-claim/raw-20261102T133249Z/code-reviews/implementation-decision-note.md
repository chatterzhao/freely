- issue_id: I-20261102T133249Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/owner-lane-claim/raw-20261102T133249Z/issues/I-20261102T133249Z-A.md

## Implementation Decision Note

- decision: 删除 bash 侧的路径不等守卫，把“该不该认领”完全交给 `owner_lane.claim`；失败原因写入日志；同时让 db daemon 自建 `.freely/run`。
- why_this: 守卫在“daemon 于工位内启动”这一唯一需要认领的场景下恒为假，且失败表现与原状完全一致，导致上一轮误判为已修复。规则写在 bash 里既不可单测，又与 claim 内部四条守卫重复。
- alternatives_considered:
  - 保留守卫但改成“相等也要认领”：等于在 bash 里再实现一遍 worktree 判定，同一规则两处维护。
  - 只加日志不改守卫：能看见问题，但认领仍然不发生。
- boundary_non_goals: 不改 claim 的四条守卫；不改表结构；不处理 test-gate 在启动失败后写 completed 的问题。
- residual_risk:
  - 认领后行会保留到 wt-close，没有 TTL。
  - wiring 测试是源码断言（防止回归），不是行为测试；行为由 AT-003 的真实启动覆盖。
  - `rows_unreadable` 时仍拒绝认领：若 db daemon 尚未就绪，daemon 启动会失败——本轮通过 db 先启动 + mkdir 缓解，但没有重试。
