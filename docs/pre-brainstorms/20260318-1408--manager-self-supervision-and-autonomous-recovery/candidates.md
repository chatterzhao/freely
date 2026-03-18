# Candidates

### C-20260318-A
- title: 主管自检与工位舰队异常恢复
- why:
  - Freely 自举时，主管不能依赖人工运行 `wt-fleet-status` 才发现 worker/supervisor 已失活。
  - `develop` 主管位必须能持续监督并在异常时自主恢复或重新委派。
- scope:
  - `runtime/freely`
  - `start-lead-agent.sh`
  - `wt-fleet-status`
  - `tests`
- acceptance:
  - 主管位能周期性读取项目级 fleet 视图，而不是只在首跳 prompt 注入一次。
  - 当应活跃的 worker 工位掉到 `down/down` 时，主管下一轮优先进入 supervision/recovery 路由。
  - `freely status` / `wt-fleet-status` 能区分“冻结工位”和“应运行但掉线的工位”。
  - 至少有一个测试锁住“后台失活不需人工检查即可被主管发现”的行为。
- promoted_issue_path: pending://issue-materialization
- session_refs: []
- milestone: pending://milestone-binding
