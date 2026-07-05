---
local_id: I-20260616T224707Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260616T224707Z
source_candidate: docs/B1-docs/raw-20260616T224707Z/candidates.md
canonical_issue_path: ''
platform_ids: {}
primary_platform: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-06-16 22:47:07+00:00
updated_at: 2026-06-16 22:47:07+00:00
intake_id: ''
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/acp-session-id-format-fix/pre-tests.md
verification_artifact_dir: docs/epics/acp-session-id-format-fix/code-reviews
platform_state: closed
---

# I-20260616T224707Z-A: ACP Session ID 格式污染修复

- source_candidate: `docs/B1-docs/raw-20260616T224707Z/candidates.md`
- pre_tests_path: `docs/B1-docs/raw-20260616T224707Z/pre-tests.md`
- verification_artifact_dir: `docs/B1-docs/raw-20260616T224707Z/code-reviews`
- milestone: M-20260616T224707Z-A
- acceptance_criteria:
  - `run-acp-prompt.py` 所有 launch_kind 分支输出统一 clean line 1 + label line 2
  - `monitor-ai-acp.sh` session ID 提取兼容 UUID v4 / `ses_` / `session id: <id>` 三种格式
  - `freely` `is_valid_uuid()` → `is_valid_session_id()` 向后兼容，同时接受 UUID v4 和 `ses_`
  - 连续 3 次 multi-turn cycle 后 session ID 保持 clean
  - restart-storm 检测不再因 session ID 污染误触发
  - UUID v4 路径 (Claude Code / Codex CLI) 不受影响

## 实现

三文件修改（commit `7974c430`），+23/-12 行：

### 1. `run-acp-prompt.py:447-451` — prompt 分支补全 clean 输出行
添加 `print(session_id, flush=True)` 作为 line 1，与其他分支 (fresh/resume/fork) 对齐。

### 2. `monitor-ai-acp.sh:427-451` — Session ID 提取兼容多格式
- 扩展 regex 匹配 UUID v4 和 `ses_` 两种格式
- 新增 `session_id_out_raw` 保留原始值供 label 检测
- `session_id_out="${session_id_out_raw%% *}"` 空格剥离 label 后缀
- `_fallback_sid` 提取同步扩展 regex

### 3. `freely:3622-3633` — `is_valid_session_id()` 向后兼容
- `is_valid_session_id()` 接受 `(ses_[A-Za-z0-9]+|UUID v4)` 组合 regex
- `is_valid_uuid()` 作为向后兼容 wrapper 委托给 `is_valid_session_id`

## Implementation Decision Note

见 `code-reviews/implementation-decision.md`
