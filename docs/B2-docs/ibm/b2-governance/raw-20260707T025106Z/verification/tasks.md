# tasks: pr-review-guarded 工位清洁检查

- issue_id: I-20260707T025106Z-A
- created_at: 2026-07-07

## Task 1: bin/pr-review-guarded — 审查前清洁检查（入口闸门）

- **文件**: `bin/pr-review-guarded`（修改）
- **改动**: 约 L108 后插入 Step 0 清洁检查代码块（约 25 行）
- **逻辑**: git status --porcelain + git ls-files --others → dirty 时阻塞
- **验证**: AT-001, AT-004
- **状态**: pending

## Task 2: bin/pr-review-guarded — 审查后清洁检查（出口闸门）

- **文件**: `bin/pr-review-guarded`（修改）
- **改动**: 在 review verdict 写入后、exit 前插入 Step 5 清洁检查代码块（约 25 行）
- **逻辑**: 同 Task 1，但错误消息针对"review 产生未提交修改"场景
- **验证**: AT-002
- **状态**: pending

## Task 3: pr-merge-guarded — 合并前兜底检查（最后防线）

- **文件**: `docs/system/workspace/scripts/worktree/pr-merge-guarded`（修改）
- **改动**: 在 merge 执行前插入清洁检查代码块（约 25 行）
- **逻辑**: 同 Task 1，但错误消息针对"可能遗漏 review 修改"场景
- **验证**: AT-003
- **状态**: pending

## Task 4: 验证 — 全部 AT GREEN + bash -n 语法检查

- **操作**: 逐条执行 AT-001~AT-005，确认全部 GREEN
- **验证**: AT-001~AT-005
- **状态**: pending

## 依赖

Task 1, 2, 3 互相独立（修改不同位置）。Task 4 依赖 1-3。
