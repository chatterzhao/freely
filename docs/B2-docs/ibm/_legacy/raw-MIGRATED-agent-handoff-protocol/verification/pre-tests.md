# Pre-Tests: Agent Handoff Protocol v2

## Acceptance Items

### AI-1: handoffs 表结构正确
- **行为**: `handoff.py init --db <db>` 创建的表包含 25 字段（含 previous_worker_handoff_id、last_activity_at），status CHECK 含 consumed
- **验证**: `sqlite3 <db> ".schema handoffs"` 输出与 brainstorms.md 的 CREATE TABLE 一致
- **证据**: schema dump 文件
- **adequacy**: v2 — 直接对比 SQL 文本，不依赖运行时行为

### AI-2: AI JSON 提取与解析
- **行为**: `handoff.py parse --db <db> --reply-text <包含 ```handoff 块的文本>` 正确提取 JSON、验证必填字段、合并 Runtime 字段、写入 DB
- **验证**: 输入 6 种合法 exit_kind 的 JSON 示例 + 2 种非法示例（缺必填字段、无效 exit_kind），检查 DB 中 INSERT 的记录字段完整性
- **证据**: parse 命令 stdout + DB 查询结果
- **adequacy**: v2 — 覆盖合法和非法输入

### AI-3: Manager JSON 输出规范
- **行为**: Manager agent 在回复末尾输出 ` ```handoff ` JSON 块，只包含 exit_kind + 该 exit_kind 的必填 AI 字段
- **验证**: 对 delegate_workers / resume_manager / stop_ai 三种 exit_kind，检查 JSON 块中不含 Runtime 管理字段（handoff_id, role, raw_key 等）
- **证据**: AI reply 文本中的 ` ```handoff ` 块内容
- **adequacy**: v2 — 三种 exit_kind 全覆盖

### AI-4: Worker JSON 输出规范
- **行为**: Worker agent 在回复末尾输出 ` ```handoff ` JSON 块
- **验证**: 对 worker_done / worker_blocked / worker_handoff_needed，检查必填字段完整
- **证据**: AI reply 文本
- **adequacy**: v2 — 三种 exit_kind 全覆盖

### AI-5: 乐观锁防御竞态
- **行为**: `consume_worker_done` 的 UPDATE 使用 `WHERE status='launched'`；`mark_stale` 使用 `WHERE status='launched' AND last_activity_at < ?`
- **验证**: 并发场景模拟——先 UPDATE status=completed（模拟 consume_worker_done），再执行 mark_stale，检查 mark_stale affected_rows=0
- **证据**: affected_rows 日志
- **adequacy**: v2 — 并发模拟覆盖竞态窗口

### AI-6: auto-consume 触发正确
- **行为**: Manager 创建新 handoff 时，同 raw_key 下所有 status IN (completed,blocked,rejected) AND consumed_by='' 的 worker 被标记为 consumed
- **验证**: 手动创建 3 条 unconsumed worker 记录（completed/blocked/rejected 各一），执行 parse_handoff_json（delegate_workers），检查 3 条全部 consumed
- **证据**: DB 查询 consumed 前后的 status 变化
- **adequacy**: v2 — 三种终态全覆盖

### AI-7: 不活跃检测替代墙钟超时
- **行为**: Worker 持续运行 2 小时但 log 持续更新 → `mark_stale` 不触发。Worker log 停止更新 15 分钟 → `mark_stale` 触发 `→ blocked`
- **验证**: 手动设置 `last_activity_at` 为 16 分钟前、`launched_at` 为 2 小时前，执行 mark_stale，检查 `last_activity_at` 超阈值触发 blocked
- **证据**: mark_stale 前后的 status 变化
- **adequacy**: v2 — 区分"慢但不阻塞"和"真正不响应"

### AI-8: 修复 handoff 携带结构化字段
- **行为**: parse_handoff_json 验证失败 → INSERT 的修复记录包含 repair_target_role、repair_target_handoff_id、validation_errors_json
- **验证**: 输入缺 worker_prompts_csv 的 delegate_workers JSON，检查修复记录的三个字段非空且值正确
- **证据**: DB 中修复记录的字段值
- **adequacy**: v2 — 检查结构化字段的具体值

### AI-9: scan 过滤活跃 Worker
- **行为**: scan 产出结果时，`worktree=? AND role='worker' AND status='launched'` 命中 → 该条目被排除
- **验证**: 创建一条 launched worker 记录指向某 worktree，运行 scan，检查该 worktree 对应的条目不在结果中
- **证据**: scan JSON 输出
- **adequacy**: v2 — 检查过滤前后 scan 结果

### AI-10: WORKER_HANDOFF_INJECT fork-only
- **行为**: fork 启动时 WORKER_HANDOFF_INJECT 注入结构化字段（handoff_id + parent + previous_worker + completion）；delta turn 时不注入
- **验证**: 检查 fork 启动的 worker prompt 文件末尾含 HANDOFF_INJECT 块，delta turn 的 prompt 不含
- **证据**: prompt 文件内容
- **adequacy**: v2 — fork vs delta 两种启动模式对比

### AI-11: #343 回归验证
- **行为**: #343 的四个 bug（validator 读 worker_prompts_csv、launcher 读 pending worker、Step B/C 分步、worktree_has_active_worker 误伤 pending）在新协议下不存在
- **验证**: 走一遍完整 delegate_workers → worker_done → manager 消费流程，确认单一数据源（worker_prompts_csv → consume_delegate_workers → INSERT+launch 原子执行）
- **证据**: 全流程日志
- **adequacy**: v2 — 端到端回归
