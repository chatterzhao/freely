# Candidates

### C-20260318-A
- title: 全局 AI 账号 watchdog 与主管拉起
- why:
  - 当全局账号限额导致所有 AI 都不可用时，不能再依赖 manager/worker/project runtime 自行恢复。
  - Freely 需要纯脚本先切号，再启动主管，由主管继续监督所有工位。
- boundaries:
  - manager 不负责切号
  - worker 不负责切号
  - 当前项目 runtime 不负责全局账号生命线
  - 全局 watchdog 只负责账号恢复和主管拉起，不直接替主管做项目级编排
- scope:
  - `runtime/ai-cli`
  - `runtime/freely`
  - 新的全局 watchdog / ensure 脚本
- acceptance:
  - 文档明确规定：账号限额后的切号与主管拉起由全局脚本负责，不属于 manager/worker
  - 至少存在一个 CLI-first 入口，可在无 AI 帮助时恢复账号并拉起主管
  - 主管恢复后继续负责 worker fleet 监督
  - 所有账号都不可用时，会切到最早恢复账号并等待唤醒，而不是要求 AI 持续存活
- promoted_issue_path: pending://issue-materialization
- session_refs: []
- milestone: pending://milestone-binding
