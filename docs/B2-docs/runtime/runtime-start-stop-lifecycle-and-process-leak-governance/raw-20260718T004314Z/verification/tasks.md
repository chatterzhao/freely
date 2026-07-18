# Tasks: L2120 孤儿行删除
- issue_id: I-20260718T004314Z-A
- owner_issue: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/issues/I-20260718T004314Z-A.md

## 任务分解
1. [x] 根因定位：三层 probe 缩小到 L2120 unbound（git log -L 溯源 aea0c5749）
2. [ ] RED：harness 复现 HEAD 版 unbound+probe 死
3. [ ] dev：删 L2120
4. [ ] GREEN：probe 正常返回 + bash -n + daemon start 推进
