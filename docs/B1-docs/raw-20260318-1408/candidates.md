# Candidates

### C-20260318-1408-A: legacy issue
- title: 主管自检与工位舰队异常恢复
- why:
  - Freely 自举时，主管不能依赖人工运行 `wt-fleet-status` 才发现 worker/supervisor 已失活。
  - `develop` 主管位必须能持续监督并在异常时自主恢复或重新委派。
- boundaries:
  - 主管只做监督、编排、委派、告警，不直接修业务或处理本地账号限额。
  - 账号切换、限额等待、进程重启属于目标工位 `runtime`/脚本职责。
  - 主管若判断需要恢复，只能输出 `runtime_recovery_requested` 这一管理决策；真正恢复由 runtime 执行。
  - worker 继续只负责自己工位的 doc loop / dev loop / verification。
  - 当 AI 响应结束、进程已退出、命中限额/认证失败、或发生 `context compacted` 需要新进程续接时，应一律视为 `runtime-owned`，不得要求 manager/worker 在已结束的响应内“自己重启自己”。
- scope:
  - `runtime/freely`
  - `start-lead-agent.sh`
  - `wt-fleet-status`
  - `tests`
- acceptance:
  - 主管位能周期性读取项目级 fleet 视图，而不是只在首跳 prompt 注入一次。
  - 当应活跃的 worker 工位掉到 `down/down` 时，主管下一轮优先进入 supervision/recovery 路由。
  - `freely baseline-status` / `wt-fleet-status` 能区分“冻结工位”和“应运行但掉线的工位”。
  - 当异常 owner 属于本工位 runtime 时，主管只输出清晰恢复目标，不直接处理。
  - 账号限额后的切号与重启仍由当前工位脚本链完成，主管只负责观察与编排。
  - 文档明确列出哪些情况属于“AI/manager/worker 无能为力”，并由 runtime / scripts 接管。
  - 至少有一个测试锁住“后台失活不需人工检查即可被主管发现”的行为。
- promoted_issue_path: `docs/B2-docs/ibm/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- legacy_id_mapping: I-20260318-1408  # 历史遗留的 issue id
- session_refs: []
- milestone: `M-20260306-workspace-routing-foundation`
