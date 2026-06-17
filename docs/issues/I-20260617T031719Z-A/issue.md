---
local_id: I-20260617T031719Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T031719Z
source_candidate: docs/pre-brainstorms/20260617T031719Z--acp-a2a-final-review-fixes/candidates.md
canonical_issue_path: ""
created_at: 2026-06-17T03:17:19Z
updated_at: 2026-06-17T03:17:19Z
author: zhaoquan
channel: freely-fix-execution
pre_tests_path: ""
verification_artifact_dir: docs/pre-brainstorms/20260617T031719Z--acp-a2a-final-review-fixes/code-reviews
---

# I-20260617T031719Z-A: ACP/A2A Final Review Fixes

- source_candidate: `docs/pre-brainstorms/20260617T031719Z--acp-a2a-final-review-fixes/candidates.md`
- pre_tests_path: ""
- verification_artifact_dir: `docs/pre-brainstorms/20260617T031719Z--acp-a2a-final-review-fixes/code-reviews`

## 实现

9 个修复：ACP _fatal_detected + stopReason + session_ping; A2A extended ops → _db_rpc; G1 Signal 5 liveness.

## Implementation Decision Note

见 `docs/pre-brainstorms/20260617T031719Z--acp-a2a-final-review-fixes/code-reviews/implementation-decision.md`

## 实现清单
- [x] ACP-1: _read_stderr fatal detection → _fatal_detected
- [x] ACP-2: _dispatch() stopReason normalization  
- [x] ACP-3: monitor-ai-acp.sh session_ping loop
- [x] A2A-1: extended ops via _db_rpc
- [x] G1: _ai_shows_liveness_acp Signal 5
