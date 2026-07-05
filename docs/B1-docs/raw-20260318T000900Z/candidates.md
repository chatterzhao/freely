# Candidate List

- ID: C-20260318T000900Z-A
  Title: 为 Freely 增加项目级 `fleet-status` 多 worktree 监督视图
  Status: proposed
  Why:
  - 多个活跃 worktree 并行时，主监督者需要 CLI first 的全局盘面
  - 当前只能通过零散 `git` / `freely baseline-status` 命令手工拼装
  Acceptance Hint:
  - 可显示 branch、dirty state、supervisor/ai pid、最近运行态
  promoted_issue_path: pending://issue-materialization
  milestone: pending://milestone-binding
  session_refs: []

- ID: C-20260318T000900Z-B
  Title: 将“全部账号不可用时切到最早 reset 账号并 backoff”落成 runtime 能力
  Status: proposed
  Why:
  - 当前账号轮换只会切下一个，不足以处理全部账号都在 cooldown 的情况
  - 自举时高频空转重试会直接拉低自治质量
  Acceptance Hint:
  - runtime 记录 account cooldown
  - 全部账号不可用时选择最早 reset 的账号
  - sleep 到 reset 时间后自动继续
  promoted_issue_path: pending://issue-materialization
  milestone: pending://milestone-binding
  session_refs: []
