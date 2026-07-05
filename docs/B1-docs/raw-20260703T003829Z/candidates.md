---
candidate_id: C-20260703T003829Z-A
status: absorbed
absorbed_into: I-20260703T003829Z-A
source_raw: raw-20260703T003829Z29Z
created_at: 2026-07-03
milestone: M-20260703T003829Z-A
---

## C-20260703T003829Z-A: legacy issue

- candidate_format_version: v2
- title: 修复 workcell-state.env unsafe source 导致命令注入，重构门禁为时间戳比较
- status: absorbed
- absorbed_into: I-20260703T003829Z-A
- decision_reason: |
  workcell-state.env 的 23 个字段实际承载三类职责：
  ① daemon 运行时状态（6字段，全局的）
  ② worker closeout 上下文（16字段，应按 raw_key 索引进 agent_working）
  ③ 测试时间戳（1字段，测试工位专属）
  
  本 fix 止血：source → meta_env_value + 门禁改为时间戳比较 + git 跟踪移除。
  后续重构：删掉 workcell-state.env 中 16 个冗余 LAST_WORKER_* 字段，门禁改从权威源读值（I-* issue / agent_working / 分支名）。
- next_action: N/A（已吸收到 I-* issue）
- revisit_trigger: workcell-state.env 删冗余副本、门禁从权威源读值的后续 issue
- acceptance_criteria:
  - `write_workcell_state()` 不再使用 `source` 读取 env 文件
  - daemon 启动不因 env 多词值执行意外命令
  - `.freely/run/workcell-state.env` 从 git 跟踪移除
  - 门禁改为时间戳比较，不再错误检查 closeout 字段
  - test-pre-merge 创建时初始化 `not_tested` 状态
  - wt-create 流程文档加 cd 提醒
  - 门禁报错使用用户友好中文提示
- promotion_gate:
  - brainstorms.md 完成职责三层分析
  - candidates.md 完成（本文件）
  - milestones.md 已更新
- open_questions:
  - workcell-state.env 中 16 个冗余 LAST_WORKER_* 何时删除？
  - monitor-ai-cli.sh 的 source 何时修复？
  - 门禁如何改为从权威源读 closeout 值而非 env 副本？
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 unsafe source 替换为 meta_env_value 的正确性，确认无其他同类问题
  - verdict: pass
- promoted_issue_id: I-20260703T003829Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260703T003829Z-A/issue.md
- milestone: M-20260703T003829Z-A
- session_refs: []
