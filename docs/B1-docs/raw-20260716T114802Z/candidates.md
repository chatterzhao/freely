---
candidate_id: C-20260716T114802Z-A
status: promoted
source_raw: raw-20260716T114802Z
created_at: 2026-07-16
milestone: M-20260716T114802Z-A
---

# Candidates

## C-20260716T114802Z-A: liveness 兜底链修复（进程态前缀匹配 + base_tool 安全推导）

- candidate_format_version: v2
- title: stall 误判复发修复 — _ai_shows_liveness_acp S2/S3 失效
- status: promoted
- decision_reason: 06:11:47 误杀的根因是兜底链被两个实现缺陷击穿（S2 精确匹配 vs macOS 修饰进程态 SN；S3 unbound base_tool），S1 长推理静默过期是正常行为必须被兜住。见 brainstorms Decision: Option B
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: 对真实 niced 存活进程（ps 态 SN），_ai_shows_liveness_acp 判活（行为沙箱 + 真实 nice 进程）
  - AC2: 源码断言——进程态为前缀匹配 R*/S*；base_tool 在函数内安全推导
  - AC3: set -u 下 base_tool 未定义时函数不再因 unbound 失败（沙箱断言）
  - AC4: 回归——真实 daemon auto 启动 ≥150s 观察窗内，AI 存活期间 0 次 runtime_stalled_ai_recovery_triggered
- promotion_gate: 根因代码坐实（L13919 精确匹配 + L13928 unbound）；scope 两处单函数；AC 全可执行
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: 两缺陷均经源码逐行核实与今日 ps 快照（SN 态）实证；06:11 事件链与五信号逐一对照成立
  - verdict: pass
- promoted_issue_id: I-20260716T114802Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/issues/I-20260716T114802Z-A.md
- milestone: M-20260716T114802Z-A
- session_refs: []
