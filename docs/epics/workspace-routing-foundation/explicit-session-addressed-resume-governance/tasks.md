# Tasks: explicit-session-addressed-resume-governance

## IBM-complete decomposition

- [x] 冻结工具差异真相
  - 记录 `codex`、`cc`、`iflow`、`kiro-cli`、`opencode` 当前 continuity contract
- [x] 收敛 truth-source 落点
  - 决定哪些定义进入 `tools.md`、`three-loop-capability-lifecycle.md`、runtime truth sources
- [x] 评估 runtime 改动面
  - 找出当前依赖 `--last` 或弱 resume 的位置
- [x] 选择最小验证面
  - 为并发安全 resume 选择最小测试与 smoke

## Dev-loop slices

- [x] 更新 `docs/system/workspace/tools.md`
  - 把 `codex` 默认 resume 样例改成显式 `SESSION_ID`
  - 把 `iflow` / `kiro-cli` 的当前强弱 contract 写清
- [x] 更新 `docs/system/workspace/three-loop-capability-lifecycle.md`
  - 将 session-addressed resume 写成 runtime continuity 真源
- [x] 更新 `docs/system/workspace/scripts/runtime/freely`
  - 保存并传递显式 resume target，而不是只依赖最近会话
- [x] 更新 `docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - `codex` 改为 `exec resume <SESSION_ID>`
  - 弱 contract 工具在缺少显式 target 时维持保守行为
- [x] 明确 manager -> worker handoff target
  - delegated continuation 不只写 restart point，还要收敛到 worker-scoped resume target
- [x] 处理 graceful preemption vs hard kill
  - 先定义最小 flush/checkpoint/evidence contract
  - 当前实现优先 `TERM` 触发本地 continuation re-entry，仅在超时后退回 hard kill fallback，并写入 preemption evidence
- [x] 更新最小测试面
  - `test-monitor-ai-cli-codex-args`
  - 相关 continuity / session evidence tests
