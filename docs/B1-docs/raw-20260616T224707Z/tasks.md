# Tasks: ACP Session ID 格式污染修复

- issue_id: I-20260616T224707Z-A
- status: completed

## Task Breakdown

### T1: run-acp-prompt.py prompt 分支 clean 输出
- status: done
- commit: `7974c430`
- file: `docs/system/workspace/scripts/runtime/run-acp-prompt.py`
- change: +1 line (`print(session_id, flush=True)`)

### T2: monitor-ai-acp.sh session ID 提取兼容化
- status: done
- commit: `7974c430`
- file: `docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`
- change: 扩展 regex 匹配 UUID v4 和 `ses_`；新增 `session_id_out_raw`；label 空格剥离；fallback regex 同步

### T3: freely is_valid_session_id 向后兼容
- status: done
- commit: `7974c430`
- file: `docs/system/workspace/scripts/runtime/freely`
- change: `is_valid_session_id()` 接受两种格式；`is_valid_uuid()` 作为 backward compat wrapper

### T4: B1_IBM 治理产物
- status: done
- commit: `680ad409`
- artifacts: brainstorms.md, candidates.md, milestones.md

### T5: B2_IBM 治理产物
- status: in_progress
- artifacts: I-* issue, prd.md, pre-tests.md, tasks.md, code-review

### T6: test-pre-merge 验证
- status: pending
- 在 test-pre-merge 运行单元验证脚本 + daemon 端到端验证

### T7: pr-create-guarded → pr-merge-guarded → wt-close
- status: pending
