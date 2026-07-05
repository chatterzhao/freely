---
local_id: raw-20260509T090210Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260509T090210Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '267'
    url: https://github.com/chatterzhao/freely/issues/267
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-09T09:02:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 改动清单

### 数据模型

| 项 | 文件 | 改动 |
|----|------|------|
| 1 | `worker-store.py` | 新增 `handoffs` 表（或从 worker_delegation 升级），删 JSON 存储逻辑 |
| 2 | `freely` | 删除 `manager-exit-contract.env` 文件写入 |
| 3 | `freely` | 删除 `worker-exit-contract.env` 文件写入 |
| 4 | `freely` | 删除 `session-handoff.txt` 文件写入 |

### Runtime 函数（freely）

| 项 | 函数 | 改动 |
|----|------|------|
| 5 | `manager_exit_contract_file()` L1932 | 改为返回 handoffs 表记录 ID |
| 6 | `worker_exit_contract_file()` L1937 | 同上 |
| 7 | `handoff_file()` L1922 | 废弃，改为 SQL 查询 |
| 8 | `manager_bootstrap_handoff_file()` L1927 | 废弃 |
| 9 | `manager_worker_launch_state_file()` | 状态从 handoffs 表读 |
| 10 | `manager_worker_launch_state_reconcile_prompt_liveness()` L1559 | 从 handoffs 表读 pending worker |
| 11 | `worker_prompt_resolved_worktree()` L9013 | 从 handoffs 表读 worktree |
| 12 | `worker_prompt_launchable_for_manager_project()` L9695 | 增加 branch 校验（#264） |
| 13 | `worker_project_has_terminal_exit_contract()` L1588 | 从 handoffs 表读 status |
| 14 | `latest_manager_worker_prompt_csv_from_continuity()` | 废弃，改为 SELECT FROM handoffs |
| 15 | `manager_continuity_files_desc_for_project()` L2090 | 改为读 handoffs 表 |
| 16 | `latest_generated_manager_continuity_file_for_project()` L2140 | 同上 |
| 17 | `manager_continuity_gap_snapshot_for_project()` L2259 | 同上 |

### 启动/恢复

| 项 | 文件 | 改动 |
|----|------|------|
| 18 | `freely` L17988-17995 | startup 调用 worker-store.py init/migrate/mark-stale |
| 19 | `freely` L18017-18018 | clear_manager_operator_stop_boundary — 改为读 handoffs 表 |
| 20 | `freely` | `operator_stop` 恢复时从 handoffs 表恢复 worker 状态 |

### 文件（保留为文本备份，不再作为数据源）

| 项 | 文件 | 改动 |
|----|------|------|
| 21 | `manager-exit-contract.env` | 保留写入但标记 deprecated |
| 22 | `manager-continuity-*.md` | 保留（跨周期上下文） |
| 23 | `worker-prompts/*.txt` | 保留但不再用于 launch |
| 24 | `session-handoff.txt` | 废弃 |

### 其他脚本

| 项 | 文件 | 改动 |
|----|------|------|
| 25 | `start-lead-agent.sh` | 读 exit_contract → 改为读 handoffs 表 |
| 26 | `monitor-ai-cli.sh` | 读 LAUNCHED_WORKER → 改为读 handoffs 表 |
| 27 | `worker-store.py` | 新增 migrate 逻辑（旧 env → 新表） |
| 28 | `worker-store.py` | 新增 mark-stale 逻辑 |

### 不在此 issue 但相关

| 项 | 说明 | Issue |
|----|------|-------|
| worker launch branch 校验 | fix/* feature/* 强制 | #264 |
| 多项目 handoffs 协调 | 跨项目 patrol | #265 |

## 设计补充

### 文件命名

`worker-store.py` → `handoff.py`。一个文件管理一张表，role 字段区分主管/worker。不拆两个文件——共用 schema 和连接管理。

### 主管 prompt

主管 patrol 也有 prompt 文件（`prompt-*.txt`），同样记录在 handoffs 表：
- `role=manager` → `prompt_file=/path/to/prompt-20260509T024559Z.txt`
- `role=worker` → `prompt_file=/path/to/worker-prompts/p1.txt`

### 查询示例

\`\`\`sql
"-- 主管最新 patrol prompt"
"SELECT AGENTS.md Cargo.lock Cargo.toml README.md bin bun.lock docs index.html package.json public src src-tauri templates tests tsconfig.json vite.config.ts FROM handoffs WHERE role=manager ORDER BY created_at DESC LIMIT 1
- pre_tests_path: docs/B2-docs/handoff-sqlite-refactor/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/handoff-sqlite-refactor/code-reviews

- pre_tests_path: docs/B2-docs/handoff-sqlite-refactor/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/handoff-sqlite-refactor/code-reviews
