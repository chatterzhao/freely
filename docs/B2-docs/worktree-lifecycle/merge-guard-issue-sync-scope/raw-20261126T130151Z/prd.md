# PRD: raw-20261126T130151Z

## Goal
封装命令在合法等价提交后自动沿袭测试证据，消除每轮收口的手工步骤。

## 实现
- `pr-merge-guarded` 新增 `_attest_test_evidence_equivalent()`，在 issue-sync commit 同步 test 工位成功后调用。
- sensitive paths 保守默认：`docs/system/workspace/scripts/,bin/,docs/B2-docs/**/verification/`；若已有 `EQUIVALENCE_SENSITIVE_PATHS` 则复用。
- 成功回执：from→to + verdict；失败：`[MERGE-GUARD] warning: test evidence stale; run freely test-gate run ...`。

## 非目标
不改 test-evidence.py / wt-close 判据；不掩盖真实代码变更。

## Dev-Loop Handoff
RED：AT 结构断言 develop 无 helper；GREEN：结构+stub 行为全绿，test-all CI 回归。
