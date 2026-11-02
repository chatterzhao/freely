# Tasks：受控调用方显式标记

| # | 任务 | 产出 | 依赖 | 验收 |
| --- | --- | --- | --- | --- |
| T1 [x] | hook 级 RED 测试 | `docs/system/workspace/scripts/tests/test-guarded-caller-markers` | 无 | AT-001/002 红 |
| T2 [x] | reference-transaction 标记 | `docs/system/workspace/hooks/reference-transaction.sh` | T1 | AT-001 |
| T3 [x] | pre-push 标记 | `docs/system/workspace/hooks/pre-push.sh` | T1 | AT-002 |
| T4 [x] | 调用方设置标记 | `wt-create`、`wt-close` | T2/T3 | AT-003 |
| T5 [x] | 证据与门禁 | `verification/test-evidence/`、`governance-merge-gate` | T4 | 全绿 |

## 顺序

T1 → T2/T3 → T4 → T5

## 非目标

- 不改合并 receipt 与 develop/main 保护。
- 不做 ps 的跨平台替代实现。
