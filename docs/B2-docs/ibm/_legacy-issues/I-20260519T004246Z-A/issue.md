---
local_id: I-20260519T004246Z-A
kind: i_issue
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
promoted_from: raw-20260519T004246Z46Z
source_candidate: docs/B1-docs/raw-20260519T004246Z46Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '581'
    url: https://github.com/chatterzhao/freely/issues/581
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T00:42:46Z'
updated_at: '2026-05-19T00:42:46Z'
intake_id: ''
author: zhaoquan
channel: manager-promotion
session_refs: []
pre_tests_path: docs/B2-docs/ibm/_legacy-issues/I-20260519T004246Z-A/pre-tests.md
verification_artifact_dir: ''
platform_state: closed
---

# I-20260519T004246Z-A: handoff.py 增加 evidence_paths 为 worker_done 必填字段

- source_candidate: `docs/B1-docs/raw-20260519T004246Z46Z/candidates.md` (C-20260519T004246Z-A)
- candidate: C-20260519T004246Z-A
- milestone: M-20260519T004246Z-A
- execution_base: `develop`
- integration_target: `develop`

## 目标

handoff.py REQUIRED_FIELDS 中 worker_done 当前只要求 completion_summary，但 runtime 的 validate_worker_exit_contract_for_project 要求 evidence_paths 必填。补齐此缺口，使 handoff.py 层的 validate_handoff_json 能在 AI 产出不含 evidence_paths 的 worker_done 时提前拒绝，避免运行时被 runtime 拒绝。

## 范围

1. handoff.py:30 REQUIRED_FIELDS['worker_done'] 增加 'evidence_paths'
2. validate_handoff_json 函数已具备通用必填字段检测逻辑，增加 REQUIRED_FIELDS 后自动生效，无需额外改动
3. 不影响其他 exit_kind 的字段验证
4. 不影响已存在的兼容路径（missing reason → fallback to completion_summary, missing next_action → 'see reason'）

## 不在范围

- 不修改 worker-agent.md / manager-agent.md（#2-#4 已由 `5b19bc25` 修复）
- 不修改 runtime 验证逻辑
- 不修改 DB schema（evidence_paths 列已存在）
- 不清理 DB 中已有的缺失 evidence_paths 的 worker_done 记录

## Acceptance

- handoff.py REQUIRED_FIELDS['worker_done'] = ['completion_summary', 'evidence_paths']
- validate_handoff_json 对缺少 evidence_paths 的 worker_done JSON 返回 (False, errors)
- 不影响其他 exit_kind 的必填字段验证
- 所有 handoff.py 单元测试通过
