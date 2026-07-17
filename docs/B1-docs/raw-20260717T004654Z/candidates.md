---
candidate_id: C-20260717T004654Z-A
status: promoted
source_raw: raw-20260717T004654Z
created_at: 2026-07-16
milestone: M-20260717T004654Z-A
---

# Candidates

## C-20260717T004654Z-A: bridge 孤儿回收 + 暖机宽限 + lazy-start 守卫

- candidate_format_version: v2
- title: ACP bridge 生命周期三点收口
- status: promoted
- decision_reason: 孤儿路径不杀进程、健康检查 5s<冷启动 8s、per-cycle 无条件 ensure 三者叠加造成泄漏与 lazy-start 违约；三点同属 bridge 生命周期域一体修。见 brainstorms Option B
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: reuse 检查 fall-through 重生前对存活旧 pid 执行 terminate（源码断言）
  - AC2: 健康检查失败但 bridge 龄 <20s 时按 warming 复用不重生（源码断言）
  - AC3: per-cycle ensure 含 lazy 守卫——非 manager 且无 pid 文件的工具不 eager 启动（源码断言）
  - AC4: E2E——wait 模式 100s 窗口：acp_bridge_started 事件 ≤1（仅 manager）、存活 acp-bridge.py ≤1、opencode/cline 进程为 0
- promotion_gate: 三缺陷代码坐实（L14250 前无 terminate；5s vs 8s 注释自认；L22540 块无守卫）；AC 全可执行
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: 三处代码事实逐行核实；17:16 泄漏实验（+12 进程/分）与 00:33 auto 对照（bridge 稳定）支撑成因分析
  - verdict: pass
- promoted_issue_id: I-20260717T004654Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/issues/I-20260717T004654Z-A.md
- milestone: M-20260717T004654Z-A
- session_refs: []
