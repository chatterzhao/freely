# Implementation Decision Note
- issue_id: I-20261109T085539Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261109T085539Z/issues/I-20261109T085539Z-A.md
- decision: 派发通道 TSV → JSON Lines + NUL 分隔流；畸形行显式报告；lint 提供可计数基线；状态文件协议迁移拆 #4252
- why_this: AI prompt 含 tab 是常态，TSV 让字段整体错位并把 worktree 路径吞进 message，后续 `[[ ! -d ]]` 恒真导致 worker 永久派不出去且原因误导；NUL 是唯一不会出现在 JSON 字符串值、又能被 bash `read -r -d ''` 安全消费的分隔符。
- alternatives_considered: ①tab 替空格（破坏 prompt）；②`printf %q` 后仍 TSV（跨平台不一致）；③bash eval/source 解码结果（重引入执行面）；④一次改完 108 个 lint 候选（会破坏合法路径插值）；⑤本轮迁移状态文件格式（需兼容期）。
- boundary_non_goals: 派发循环体逐字不动；其它 3 处 `IFS=$'\t'` 通道不动；`|| true` 上游语义不动；不改 `load_meta_env_snapshot`；不机械替换 lint 候选。
- residual_risk: ①NUL 流用临时文件承载，并发调用需各自 mktemp（已用 `mktemp` + 函数内 `rm -f` 双清理）；②emitter/decoder 的 stderr 现在进 daemon 日志，畸形行会新增可见告警（预期）；③lint 的 108 个候选中大量是 `${project}/...` 内部路径，属候选清单，逐处判定与迁移需后续轮次；④状态文件 `source` 仍存在 20 处，已拆 #4252 处理。
- verification: AT-001 基线 RED `3 ok / 13 failed` → GREEN `16 ok / 0 failed`；真机 bash 冒烟确认 tab/引号保留与 6 字段边界；`bash -n`、`check-epics-map`、`bin/test-all --ci`、6 个相关回归基线对比 0 新增失败。
- self_bootstrap_findings: ①`IFS=$'\t'` 在 `freely` 有 4 处，静态断言必须精确匹配含 `_task_id` 的派发行，一刀切会误伤其它通道；②对照组不能用已修源码验证旧行为，改为直接模拟旧拼接公式；③status 文件 20 读/15 写的协议迁移无法与「行为不变」同 PR 验证，按 R22 先例拆分；④lint 全仓 108 候选（runtime 63），说明缺的是「禁止新增」边界而非一次清完。
