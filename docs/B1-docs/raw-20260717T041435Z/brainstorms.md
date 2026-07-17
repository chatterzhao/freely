---
b1_id: B1-20260717T041435Z
phase_state: completed
source_raw: raw-20260717T041435Z
produced_candidate: C-20260717T041435Z-A
created_at: 2026-07-17
---

# B1_IBM: pretests-gate 与 pr-review-guarded 对 verification_artifact_dir 解析互斥

## Input
2026-07-17 四条修复 lane 实测：无引号值被 pr-review-guarded 拦（sed 只认单引号包裹），有引号值被 pretests-gate 拦（extract 只剥反引号，引号进 VERIFICATION_DIR_RE 失配）。同一字段两门禁要求互斥格式，lane 只能用双行 workaround（I-20260717T004721Z-A 为范例）。

## Problem（代码坐实）
1. `docs/system/workspace/scripts/quality/pretests-gate` ~L164-166：`extract` 正则 `^- field:\s*`?([^`\n]+)`?$` 只剥反引号，不剥 `'`/`"`
2. `bin/pr-review-guarded` ~L211：`sed "s/.*: *'\([^']*\)'/\1/"` 只在单引号包裹时才取值，否则返回整行

## Brainstorm
### Option A：统一规定必须无引号，改 pr-review-guarded
- 可行但存量文件（今日多条已合并 lane 的 I-* 用引号或双行）需迁移
### Option B：两端解析器都做"引号可选"，接受 '\''、"、` 与裸值（选定）
- 向后兼容全部存量格式（含双行 workaround），不需要文档迁移；解析 robustness 属工具层职责
### Option C：连 runtime_pid_file_for_role acp_bridge glob 展开问题一并修
- 该问题在 runtime/freely 且语义是"多 pid 文件枚举"而非引号剥离，拆出独立处理（记录于 candidate open_questions 转 dropped-note）

## Decision: Option B

## 边界
- 只改 pretests-gate 的 extract 与 pr-review-guarded 的取值 sed；不改 VERIFICATION_DIR_RE 本身、不改 I-* 文档格式规范
- raw 附带的 acp_bridge glob 问题不在本 lane（另行 B1，见 candidate revisit_trigger）

## Candidate
- candidate_id: C-20260717T041435Z-A
- status: promoted
- milestone: M-20260717T041435Z-A
