---
issue_id: I-20261125T094413Z-A
issue_path: docs/B2-docs/gate/test-evidence-equivalence/raw-20261125T094413Z/issues/I-20261125T094413Z-A.md
phase_state: completed
---

- issue_id: I-20261125T094413Z-A
- issue_path: docs/B2-docs/gate/test-evidence-equivalence/raw-20261125T094413Z/issues/I-20261125T094413Z-A.md

# Implementation Decision Note
- decision: 在 test-evidence.py 增加 attest-meta 与三态 validate，基于 lane 声明的敏感面做依赖判定，硬排除测试定义/代码路径。
- why_this: 用户项目与自举的测试对象不同，一刀切路径白名单会在自举漏测；语义判据是唯一安全边界。
- alternatives_considered: 放宽 HEAD 相等为任意祖先——会漏测；路径白名单一刀切——自举漏测；要求全量重跑——浪费（本会话 4 次）。
- boundary_non_goals: 不改 test-gate run 语义；不放宽代码/测试改动重测；不改 pr-create/merge。
- residual_risk: 依赖 lane 正确声明 sensitive_paths；默认无声明全敏感兜底；硬排除覆盖关键路径。
- followup_fix（同轮自举发现）: AT 默认源目录 parents[4] 落在 docs/ 导致 GREEN 无法运行 → parents[5]；TEST_DEFINITION_FINGERPRINT 原来只比较不持久化，是 no-op → 纳入 EQUIV_FIELDS，由 write/attest-meta 写入，缺失基线一律拒绝；AT 增 2 条指纹断言（13/0 GREEN、3/10 RED）。
