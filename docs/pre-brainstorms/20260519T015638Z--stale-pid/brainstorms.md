# Brainstorm: systematic stale_pid — worker process exits before handoff

## Discovery

Raw issue `raw-20260519T015638Z` (GitHub #601) 报告了系统性 worker 进程 stale_pid 问题：

- **时间窗口**: 2026-05-18T23:49 至 2026-05-19T01:45
- **频率**: 21 次连续 worker launch
- **表现**: 所有 worker 以 `exit_kind=stale_pid` 标记为 blocked
- **存活时间**: 2-10 分钟后进程死亡，无 `completion_summary`
- **影响范围**: 所有活跃 worktree — fix-batch-closeout-raw, feature-chat-conversation, 20260519-fix-cleanup-sync 等
- **连锁影响**:
  - Manager 委派无效，closeout 无进展
  - 30 state_mismatch 条目无法关闭
  - 4 个 ready worktree 无法合并
  - Fleet cleanup 停摆

## Suspected Root Causes

Issue 提出了三个假设：
1. Worker ACP session 超时早于任务完成
2. Worker 产生 handoff 但 runtime 未成功持久化
3. Worker launch pipeline 存在竞态条件

## 现有相关上下文

- `handoff.py` 中有 `mark_stale()` 函数（第 333-351 行），按 last_activity_at 超时 15 分钟标记 stale
- `validate_worker_exit_contract_for_project` 在 runtime 侧做字段验证
- `stale_pid` 在 handoff.py 中作为合法 exit_kind 被认可
- handoff DB 有 `consumed_by` 和 `status='consumed'` 的双层消费追踪

## 扩散思考

### 竞态路径 A: launch → detect stale → block 发生在 worker 产出 handoff 之前
worker launch 后，manager 或 watchdog 的 mark_stale 可能先判断 worker 死亡，产生 stale_pid → blocked。
后续 worker 的 handoff 到达时 status 已不是 launched → 被忽略。

### 竞态路径 B: ACP adapter 层面超时
ACP adapter 有内置超时，worker 执行时间长时 ACP 先断开 → supervisor 判断 worker 死亡 → stale_pid。

### 竞态路径 C: slot switch 导致 worker 进程被回收
auto-switch 或 slot 切换时旧 slot 关联的进程被回收，worker 恰好在新 slot 上 launch 但 supervisor 仍在旧 slot。

## Decision

此 issue 是 **系统性高影响 P1**，需要独立工位深入研究。建议：

1. **立即缓解**: `mark_stale` 超时从 15 分钟增加到 30 分钟，减少 false positive
2. **根因研究**: 需要 live-inspection runtime supervisor + ACP 源码的交互时序
3. **长期治理**: worker launch → heartbeat → stale detection 的时序契约需要写进 handoff 协议

**进入 B2 阶段**前必须完成 supervisor/ACP bridge 源码阅读（现有 `C-20260517T083200Z-A` 也在做类似研究）。
