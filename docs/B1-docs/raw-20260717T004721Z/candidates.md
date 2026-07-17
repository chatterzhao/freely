---
candidate_id: C-20260717T004721Z-A
status: promoted
source_raw: raw-20260717T004721Z
created_at: 2026-07-16
milestone: M-20260717T004721Z-A
---

# Candidates

## C-20260717T004721Z-A: sse pid 校验参数顺序对齐家族约定

- candidate_format_version: v2
- title: 修复 valid_sse_watchdog_pid_for_project 参数反转
- status: promoted
- decision_reason: 参数反转使活 sse-watchdog 永判 invalid（kill -0 <项目路径> 恒失败），每轮 self-heal/reconcile 误清误杀；单点声明修复对齐 valid_* 家族 (project, pid) 约定。见 brainstorms.md Decision: Option B
- next_action: B2 物化 → RED（复现活进程判 invalid）→ dev（单行修复）→ GREEN → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - AC1: 函数签名为 local project="$1" pid="$2"，与家族约定一致（源码断言）
  - AC2: 行为——对刚启动的真实 sse-watchdog 进程，valid_sse_watchdog_pid_for_project(project, pid) 判定为 valid（沙箱提取函数 + 装饰进程实测）
  - AC3: 回归——真实 daemon 启动周期内不再出现针对活 sse-watchdog 的 startup_self_heal_stale_pid_cleared 事件
- promotion_gate: 根因为源码级事实（git -L 可考）；scope 单函数声明行；全部 AC 可执行
- open_questions: []
- acceptance_reviews:
  - reviewer: self-evident-single-line (root cause verified by git log -L fe8df8be9 + caller enumeration in B1)
  - mode: inline
  - summary: 单行家族约定修复，B1 已枚举全部调用方均传 (project, pid)，无边界争议
  - verdict: pass
- promoted_issue_id: I-20260717T004721Z-A
- promoted_issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/issues/I-20260717T004721Z-A.md
- milestone: M-20260717T004721Z-A
- session_refs: []
