---
issue_id: I-20261103T091157Z-A
issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/issues/I-20261103T091157Z-A.md
phase_state: completed
---

- issue_id: I-20261103T091157Z-A
- issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/issues/I-20261103T091157Z-A.md

## Implementation Decision Note

- decision: 先修 Gitee search 分页（根因），再用 adapter pull 物化 open 文档、按证据关闭 4 个 Gitee 漂移镜像、回填本地编号，最后用实时 parity 测试锁定。
- why_this: 分页截断让历史镜像无法被 identifier 解析，是漂移长期未被发现的直接原因；活跃面（open+本地追溯）是唯一有生命周期价值的对齐口径，历史总量相等会制造归档污染。
- alternatives_considered: 历史 closed 批量补建镜像（否决）；只关 4 个漂移镜像（否决，元数据缺口仍在）。
- boundary_non_goals: 不批量补建历史镜像、不删除平台 issue、不改 gate/scan。
- residual_risk: 历史 closed 总量差异（GH 2610 / GT 471）仍是遗留债；若未来要求归档级对齐需另立 issue。
