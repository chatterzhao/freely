# Candidates

### C-20260318-A
- title: 主管自检与工位舰队异常恢复
- why:
  - Freely 自举时，主管不能依赖人工运行 `wt-fleet-status` 才发现 worker/supervisor 已失活。
  - `develop` 主管位必须能持续监督并在异常时自主恢复或重新委派。
- boundaries:
  - 主管只做监督、编排、委派、告警，不直接修业务或处理本地账号限额。
  - 账号切换、限额等待、进程重启属于目标工位 `runtime`/脚本职责。
  - worker 继续只负责自己工位的 doc loop / dev loop / verification。
- scope:
  - `runtime/freely`
  - `start-lead-agent.sh`
  - `wt-fleet-status`
  - `tests`
- acceptance:
  - 主管位能周期性读取项目级 fleet 视图，而不是只在首跳 prompt 注入一次。
  - 当应活跃的 worker 工位掉到 `down/down` 时，主管下一轮优先进入 supervision/recovery 路由。
  - `freely status` / `wt-fleet-status` 能区分“冻结工位”和“应运行但掉线的工位”。
  - 当异常 owner 属于本工位 runtime 时，主管只输出清晰恢复目标，不直接处理。
  - 账号限额后的切号与重启仍由当前工位脚本链完成，主管只负责观察与编排。
  - 至少有一个测试锁住“后台失活不需人工检查即可被主管发现”的行为。
- promoted_issue_path: pending://issue-materialization
- session_refs: []
- milestone: pending://milestone-binding
