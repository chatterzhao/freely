# Tasks: Agent Handoff Protocol v2

## 1. handoff.py 重构
- [x] DROP 旧表，CREATE 新表：5→1 reason、+previous_worker_handoff_id、+last_activity_at、status CHECK +consumed
- [x] INSERT/UPDATE 适配新字段
- [x] 所有 UPDATE 加 `WHERE status='<期望当前状态>'` 乐观锁
- [x] `mark_stale` 改为 `WHERE status='launched' AND last_activity_at < ?`（不活跃检测）
- [x] 新增 `parse` 子命令：grep ` ```handoff ` → json.loads → 验证 → 合并 Runtime 字段 → INSERT → dispatch consume_*
- [x] 新增 `list_by_raw_key_and_status` / `has-active-worker` / `latest-completed-worker` 查询
- [ ] pre-tests: AI-1, AI-2, AI-5

## 2. agent docs 更新
- [x] `freely-agent-manager.md`：旧 CLI 指令替换为 3 列表格 + JSON 示例
- [x] `freely-agent-worker.md`：旧 CLI 指令替换为 3 列表格 + JSON 示例
- [ ] pre-tests: AI-3, AI-4

## 3. freely — build_prompt + WORKER_HANDOFF_INJECT
- [x] `build_prompt` Manager 路径：注入线程历史(10条摘要) + 未消费 worker 列表 + fleet/scan
- [x] `build_prompt` Worker 路径：仅 Task + agent doc + WORKER_HANDOFF_INJECT（fork 时注入）
- [x] `WORKER_HANDOFF_INJECT`：结构化字段（handoff_id + parent + previous_worker + completion），不注入线程历史和 bash 命令
- [x] 删除 `append_*_exit_contract_directive_if_needed` 中的 CLI 指令文本
- [ ] pre-tests: AI-10

## 4. freely — exit contract handler → consume_*
- [x] 实现 `parse_handoff_json_reply`：提取 ` ```handoff ` 块 → 验证 → 合并 Runtime 字段
- [x] 实现 `consume_delegate_workers`：读 CSV → 去重 → parse headers → 判断 fork/prompt → INSERT → launch
- [x] 实现 `consume_resume_manager`：UPDATE manager → auto-consume
- [x] 实现 `consume_stop_ai`：UPDATE manager → auto-consume → 通知 supervisor
- [x] 实现 `consume_worker_done`：UPDATE worker completed
- [x] 实现 `consume_worker_handoff_needed`：UPDATE worker completed（会话保持）
- [x] 实现 `consume_worker_blocked`：UPDATE worker blocked
- [x] 实现 auto-consume：新 manager handoff 创建时批量消费 unconsumed worker
- [x] 实现结构化修复 handoff：repair_target_role + repair_target_handoff_id + validation_errors_json（独立列）
- [ ] 删除旧 `validate_manager_exit_contract_for_project` 对旧字段的检查
- [ ] pre-tests: AI-6, AI-7, AI-8

## 5. freely — scan 过滤 + session 判断
- [x] scan 产出前：`has-active-worker` 查 worktree + raw_key → 排除活跃条目
- [x] `worktree_has_active_worker` 改为只查 `status=launched`
- [x] `consume_delegate_workers` 中判断 fork vs prompt delta（_is_followthrough 检测）
- [x] Runtime 在检测到 Worker 活跃信号时 UPDATE `last_activity_at`
- [ ] pre-tests: AI-9

## 6. 集成验证
- [ ] #343 回归：全流程 delegate_workers → worker_done → manager 消费
- [ ] Manager patrol → scan(过滤后) → delegate → Worker fork → Worker delta followthrough → complete → auto-consume
- [ ] 修复循环：无效 JSON → 结构化修复 handoff → Manager 定位纠正
- [ ] 不活跃检测：Worker log 停更 → mark_stale → blocked → Manager 介入
- [ ] pre-tests: AI-11
