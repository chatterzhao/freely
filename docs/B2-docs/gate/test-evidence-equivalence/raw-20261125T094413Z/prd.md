# PRD: raw-20261125T094413Z
## Goal
test 证据沿袭元数据等价提交：语义判据（依赖面∩diff）替代 HEAD 精确相等，fail-closed。
## 实现方案
test-evidence.py 新增 attest-meta 子命令：解析 gate、计算 tested..HEAD diff、与 sensitive-paths 求交、硬排除路径无条件拒绝、成功写 EQUIVALENCE_CHAIN（保留原证据 hash）；validate 支持沿袭链并输出 verdict 三态。
## Dev-Loop Handoff
RED 4/5 → GREEN 9/0；回归 test-evidence-chain；不改 test-gate run。
