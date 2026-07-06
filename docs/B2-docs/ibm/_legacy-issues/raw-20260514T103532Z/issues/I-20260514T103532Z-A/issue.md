---
local_id: I-20260514T103532Z-A
kind: linked
phase_state: completed
promoted_from: raw-20260514T103532Z32Z
source_candidate: docs/B1-docs/raw-20260514T103532Z32Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '344'
    url: https://github.com/chatterzhao/freely/issues/344
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-14 10:35:32+00:00
updated_at: '2026-05-15T17:53:44Z'
intake_id: ''
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/agent-handoff-protocol/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/agent-handoff-protocol/code-reviews
platform_state: closed
---

# I-20260514T103532Z-A: agent handoff protocol v2

- source_candidate: `docs/B1-docs/raw-20260514T103532Z32Z/candidates.md`
- pre_tests_path: `docs/B2-docs/agent-handoff-protocol/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/agent-handoff-protocol/code-reviews`

## 目标

实现 agent handoff protocol v2：将 handoffs 表从 AI 直接写 CLI 的碎片化管道，重构为 AI→JSON→Runtime 的统一协议。Manager 和 Worker 各按 agent doc 的表格规范输出 ` ```handoff ` JSON 块，Runtime 解析、验证、合并、写入 DB，驱动完整状态机。

## 范围

- `handoff.py`：表结构重建（5→1 reason 字段、+previous_worker_handoff_id、+last_activity_at、+consumed status）、乐观锁 UPDATE、`mark_stale` 改为不活跃检测、新增 `parse` 子命令
- `freely-agent-manager.md`、`freely-agent-worker.md`：交接章节改为 JSON 输出表格
- `freely` 脚本：`build_prompt` 上下文分层、WORKER_HANDOFF_INJECT 改为 fork-only 结构化注入、exit contract handler 替换为 parse_handoff_json + consume_* 方法、修复 handoff 携带结构化字段、scan 过滤活跃 Worker
- `freely` 脚本：`worktree_has_active_worker` 只查 launched、session 管理（fork/prompt delta 判断）

## 不在范围

- 不修改 ACP bridge 本身（`start-lead-agent.sh`）
- 不修改 fleet supervision / scan 生成逻辑（仅修改 scan 结果的 handoffs 交叉过滤）
- 不修改 `wt-close` / worktree 生命周期管理
