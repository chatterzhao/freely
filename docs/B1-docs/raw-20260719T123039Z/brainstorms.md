---
b1_id: B1-20260719T123039Z
phase_state: completed
source_raw: raw-20260719T123039Z
source_url: https://github.com/chatterzhao/freely/issues/4014
produced_candidate: C-20260719T123039Z-A
created_at: '2026-07-19'
---

# B1: agent_working 全生命周期正确性验证

## 已验证正确的部分

直接 SQLite 测试（不依赖 daemon）：

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | agent_assign(worker_03) | worker_id='worker_03:ses_test123' 写入 ✅ |
| 2 | agent_next_free(worker,10) | occupied={worker_03}, free 不含 worker_03 ✅ |
| 3 | agent_release_all(raw_key) | 行删除, occupied={}, worker_03 恢复 ✅ |
| 4 | wt-close 调用 agent_release_all | 代码中存在 ✅ |

Python/DB 层完全正确。

## 仍然破损

| 问题 | 状态 |
|------|------|
| agent_working 旧行 worker_id=NULL (3行) | 需清理 |
| agent_working 旧行 slot=claude (3行) | 需清理 |
| 测试只 grep 代码不查 DB | 需改为查 DB |

## 修复

1. 清理 agent_working 中 worker_id=NULL 的非 __manager__ 行
2. 写一个真实的 DB 验证测试：assign → verify DB → next_free → verify → release → verify
