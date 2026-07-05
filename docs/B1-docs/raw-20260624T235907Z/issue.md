---
local_id: raw-20260624T235907Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3451'
    url: https://github.com/chatterzhao/freely/issues/3451
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T23:59:07Z'
updated_at: '2026-06-25T08:00:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260624T235907Z-A
source_candidate: docs/B1-docs/20260624T235907Z--anti-cheating-gate/candidates.md#C-20260624T235907Z-A
---

## 问题

`pretests-retirement-gate` 的 GREEN 检查逻辑错误：

1. **现状**：`workcell-state.env` 不存在时（#3446 fallback）扫描 `docs/epics/**/pre-tests.md` 文件存在就放行
2. **问题**：pre-tests.md 存在只证明 RED（文档写好了），不代表 GREEN（测试执行了）
3. **后果**：`pr-create-guarded` Step 2c 形同虚设——只要有 B2 文档就能过

## 正确设计

### RED vs GREEN 边界

| 阶段 | 含义 | 证据 | 谁负责 |
|------|------|------|------|
| RED | 测试计划定义完整 | pre-tests.md 结构正确（有 id/requirement/evidence_level） | B2_IBM skill |
| GREEN | 测试已执行通过 | actual_output ≠ "(执行后填写)" + status=pass + evidence_file 存在 | test-execution skill 或手工 |

### gate 行为

- IBM governance gate（已有）：检查 RED ✅
- pretests-retirement-gate（待修）：检查 GREEN

### GREEN 检查逻辑（不依赖 Worker）

1. 有 `workcell-state.env` → 从中读 pre_tests_path（快速定位）
2. 没有 → 扫描 `docs/epics/**/pre-tests.md`
3. 无论哪种 → 最终都检查每个 acceptance item：
   - `actual_output` ≠ 占位符（如 "(执行后填写)"）
   - `status` == "pass"
   - `evidence_file` 字段存在且路径可访问
4. 缺失 GREEN 时明确报错指向 `skill:freely-test-execution`

### Worker 是优化，不是依赖

- Worker 路径：test-execution → 回写 actual_output → 写 workcell-state.env
- 手工路径：手动执行 → 手动填 actual_output → 无 workcell-state.env
- gate 同时支持两条路径，以 pre-tests.md 为唯一真相源

### pr-create-guarded Step 2c

Step 2c 调用 pretests-retirement-gate 检查 GREEN——gate 修好后自动生效，pr-create 零改动。

## 回退内容

回退 #3446 的 fallback 逻辑（只检查文件存在即放行），替换为基于 actual_output 字段填写状态的检查。

## 用户影响

- Freely 自举项目：手工 + Worker 两条路径都支持
- 未来用户项目：不引入 Worker 依赖，手工执行也能过门禁
- 报错精确：RED 缺→看 B2_IBM skill，GREEN 缺→看 test-execution skill
