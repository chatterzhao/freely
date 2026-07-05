---
local_id: I-20260615T001626Z-A
issue_title: "移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)"
kind: linked
phase_state: in_b2_ibm
promoted_from: raw-20260615T001626Z26Z
source_candidate: docs/B1-docs/raw-20260615T001626Z26Z/candidates.md
canonical_issue_path: docs/B2-docs/a2a/handoff/issues/I-20260615T001626Z-A.md
platform_ids:
  github:
    issue_id: "2691"
    url: https://github.com/chatterzhao/freely/issues/2691
    synced_at: ""
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: "2026-06-15T00:16:42Z"
updated_at: "2026-06-15T00:16:42Z"
intake_id: ""
author: platform
channel: freely-feat-execution
session_refs:
  - tool: claude
    session_id: current-session
    jsonl_path: unavailable://session-continuity-not-enabled
    role: worker
pre_tests_path: docs/B2-docs/a2a/handoff/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/a2a/handoff/code-reviews
---

## I-20260615T001626Z-A: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)

| local_id | kind | phase | promoted_from |
|----------|------|-------|---------------|
| I-20260615T001626Z-A | linked | in_b2_ibm | raw-20260615T001626Z26Z |

### Pre-Brainstorm Summary

父 Epic a2a-replace-handoff 已完成 A2A 协议替换 Handoff 的核心实现。当前代码仍存在双路径（a2a-exit + 文本 JSON 解析 fallback），导致维护成本增加、行为不一致的风险。Phase 1+2 修复信号文件 WORKERS 字段并统一所有 Prompt 为 a2a-exit 指令，是消除双路径的第一步。

### Scope

- **Phase 1**: 修复 a2a_task.py 的 a2a-exit 路径，确保 WORKERS 字段正确写入 last-exit-task.env
- **Phase 2**: 更新所有 prompt 文件（manager-agent.md, worker-agent.md, 系统 prompt, WORKER_STATE_INJECT, repair prompt, delta prompt），将 JSON block 指令替换为 a2a-exit 指令
- **Non-goals**: 不删除 parse_a2a_task_json_reply、last-workers-csv.txt/last-exit-kind.txt 持久化、a2a_task_parser.py 等（Phase 3-6 后续完成）
- **回退**: FREELY_A2A_TEXT_PARSING_FALLBACK=1 可恢复旧行为

### References

- B1 预研: docs/B1-docs/raw-20260615T001626Z26Z/
- Candidate: docs/B1-docs/raw-20260615T001626Z26Z/candidates.md#C-20260615T001626Z-A
- 正式 Issue: docs/B2-docs/a2a/handoff/issues/I-20260615T001626Z-A.md
- PRD: docs/B2-docs/a2a/handoff/prd.md
- Pre-tests: docs/B2-docs/a2a/handoff/verification/pre-tests.md
- Tasks: docs/B2-docs/a2a/handoff/tasks.md

## Comments
