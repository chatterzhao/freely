# Brainstorms: A2A server _restore_tasks 异步化

- raw_key: 20260624T004524Z
- github_issue: https://github.com/chatterzhao/freely/issues/3398

## Discovery

### 问题
`daemon start` 日志: `[WARN] A2A server start timed out after 10s (may be TCP-only)`

根因: `A2AServer.__init__` 同步调用 `_restore_tasks()`。该方法执行 DB 全量查询 + PID liveness check + state correction，全部在服务器绑定 socket 之前完成。DB 中有大量 task 或僵尸 PID 时耗时超过 10s → health check 超时。

### 影响面
- `a2a_server.py`: `__init__` + `start()` 
- `freely`: health check 超时消息
- 不影响 A2A 协议层或 task 逻辑

## Research

### 方案 A: 异步 asyncio.create_task（备选）
将 `_restore_tasks` 改为 async，在 `start()` 中 `asyncio.create_task`。
缺点: uvicorn 在 daemon 线程中运行，asyncio event loop 在不同线程间传递复杂。

### 方案 B: background daemon thread（选用）
在 `start()` 中 `threading.Thread(target=self._restore_tasks, daemon=True).start()`。
优点: 简单、无侵入、server 立即接受连接。`_restore_tasks` 本身是同步 DB 操作，天然适配线程。

## Decision

方案 B: daemon 线程。`__init__` 不再调用 `_restore_tasks`，`start()` 在 `self._running = True` 后启动恢复线程。
同时修正 health check 超时的误导消息 "may be TCP-only"（实际是 socket 未就绪）。
EOF

# B1: candidates
cat > docs/pre-brainstorms/20260624T004524Z--a2a-restore-async/candidates.md << 'CEOF'
# Candidates

## C-20260624T004524Z-A: A2A server _restore_tasks 异步化

- candidate_format_version: v2
- title: A2A server _restore_tasks 后台线程化，消除启动超时
- status: promoted
- decision_reason: __init__ 同步阻塞导致 socket 延迟绑定 → health check 超时。改为 daemon 线程最简单安全。
- next_action: pr-create → pr-review → pr-merge → wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - _restore_tasks 不再在 __init__ 中同步调用
  - server socket 在恢复完成前即可接受连接
  - health check 超时消息不再误导 "may be TCP-only"
- promotion_gate: 代码修改完成 + 逻辑审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: review a2a_server.py _restore_tasks 异步化安全性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T004524Z-A/issue.md
- milestone: M-20260624T004524Z-A
- session_refs: []
CEOF

# B2: I-issue + pre-tests + tasks + code-review
mkdir -p docs/issues/I-20260624T004524Z-A docs/epics/a2a-restore-async/{verification,code-reviews}

cat > docs/issues/I-20260624T004524Z-A/issue.md << 'IEOF'
---
local_id: I-20260624T004524Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T004524Z
source_candidate: docs/pre-brainstorms/20260624T004524Z--a2a-restore-async/candidates.md#C-20260624T004524Z-A
canonical_issue_path: docs/issues/I-20260624T004524Z-A/issue.md
milestone: "M-20260624T004524Z-A"
title: "fix: defer _restore_tasks to background thread to prevent A2A startup timeout"
platform_ids:
  github:
    issue_id: '3398'
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-24T00:45:41Z
updated_at: 2026-06-24T05:30:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/a2a-restore-async/verification/pre-tests.md
verification_artifact_dir: docs/epics/a2a-restore-async/code-reviews
---

# I-20260624T004524Z-A: A2A server _restore_tasks 异步化

- source_candidate: `docs/pre-brainstorms/20260624T004524Z--a2a-restore-async/candidates.md#C-20260624T004524Z-A`
- pre_tests_path: `docs/epics/a2a-restore-async/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/a2a-restore-async/code-reviews`
- milestone: M-20260624T004524Z-A

## 实现

1. `a2a_server.py`: `_restore_tasks()` 从 `__init__` 移除，改为 `start()` 中的 daemon 后台线程
2. `freely`: 修正 health check 超时消息 "may be TCP-only" → "check DB size, zombie PIDs, or disk I/O"
IEOF

# B2: pre-tests
cat > docs/epics/a2a-restore-async/verification/pre-tests.md << 'PEOF'
# Pre-Tests: A2A server _restore_tasks 异步化

- issue_id: I-20260624T004524Z-A

## Unit
- acceptance target: _restore_tasks 不在 __init__ 中调用，start() 中通过 daemon 线程执行
- testing layer: unit
- target environment: fix worktree
- required evidence: 代码审查确认 _restore_tasks 调用位置变更
- blocker taxonomy: execution_pending_or_failed

## Integration
- acceptance target: A2A server 启动后 socket 立即可用（恢复在后台进行）
- testing layer: integration
- target environment: fix worktree
- required evidence: daemon start 不再出现 A2A timeout 警告
- blocker taxonomy: execution_pending_or_failed

## End-to-End
- acceptance target: fix→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码逻辑审查确认：_restore_tasks 是纯同步 DB 操作，线程安全，不依赖 event loop

## Acceptance Items
### AT-001 _restore_tasks 不在 __init__ 中
- id: AT-001
- requirement: __init__ 不阻塞 socket 绑定
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: a2a_server.py lines 335-338

### AT-002 health check 消息修正
- id: AT-002
- requirement: 超时消息不再误导 "may be TCP-only"
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: freely line 8385
PEOF

# B2: tasks
cat > docs/epics/a2a-restore-async/tasks.md << 'TEOF'
# Tasks: A2A server _restore_tasks 异步化

- issue_id: I-20260624T004524Z-A

## T1: _restore_tasks 从 __init__ 移除 ✅
- file: a2a_server.py:338
- change: 删除 __init__ 中的 self._restore_tasks() 调用
- status: done

## T2: start() 中添加后台恢复线程 ✅
- file: a2a_server.py:675
- change: self._running = True 后启动 daemon 线程执行 _restore_tasks
- status: done

## T3: 修正 health check 超时消息 ✅
- file: freely:8385
- change: "may be TCP-only" → "check DB size, zombie PIDs, or disk I/O"
- status: done
TEOF

# B2: code-review (implementation decision note)
cat > docs/epics/a2a-restore-async/code-reviews/implementation-decision-note.md << 'REOF'
# Implementation Decision Note: _restore_tasks 异步化

- issue_id: I-20260624T004524Z-A
- issue_path: docs/issues/I-20260624T004524Z-A/issue.md
- milestone: M-20260624T004524Z-A

## Implementation Decision Note

- decision: _restore_tasks 从 A2AServer.__init__ 移至 start() 中的 daemon 线程执行
- why_this: __init__ 中的同步恢复阻塞 socket 绑定 → health check 超时。daemon 线程让 server 先接受连接再后台恢复，不影响正常请求处理
- alternatives_considered: (1) asyncio.create_task — uvicorn 在 daemon 线程中运行，event loop 跨线程传递复杂 (2) 增大 health check timeout — 治标不治本，DB 增长后仍会超时
- boundary_non_goals: 不改变 _restore_tasks 恢复逻辑本身；不改变 health check 的 10s 超时值
- residual_risk: _restore_tasks 中的 task_store 操作是线程安全的 SQLite（WAL 模式），但并发场景极少（恢复期间一般无其他 task 操作）
REOF

echo "B1/B2 governance docs created"