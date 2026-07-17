---
candidate_id: C-20260717T060903Z-A
status: promoted
source_raw: raw-20260717T060903Z
created_at: 2026-07-17
milestone: M-20260717T060903Z-A
---

# Candidates

## C-20260717T060903Z-A: acp_bridge pid 族 per-tool 枚举与定向清理

- candidate_format_version: v2
- title: self-heal 逐文件枚举 + 清理 per-tool 化
- status: promoted
- decision_reason: glob 多行展开使 acp_bridge self-heal 静默失效；广播清理误伤活 bridge。Option B 两点收敛于 self-heal 层。见 brainstorms
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: 多 pid 文件并存时 self-heal 对每个文件独立判活清理（沙箱：一活一死 → 死清活留）
  - AC2: 清理 per-tool——死 bridge 清理不触碰其他工具的 sock/pid/pid.bin/pid.tool（沙箱断言）
  - AC3: E2E——真实 daemon 运行中手工放置 dead 别名 pid 文件 → 触发 self-heal → 活 claude bridge 文件完好且无重生 spawn 事件
- promotion_gate: 两缺陷 file:line 坐实；glob 行为可复现；AC 全可执行
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: 与 raw-20260717T004654Z 修复面零重叠核验；glob 展开 bash 语义确认
  - verdict: pass
- promoted_issue_id: I-20260717T060903Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/issues/I-20260717T060903Z-A.md
- milestone: M-20260717T060903Z-A
- session_refs: []
