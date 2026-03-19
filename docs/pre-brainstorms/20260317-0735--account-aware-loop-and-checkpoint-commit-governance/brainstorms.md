# 20260317-0735 Account-Aware Loop And Checkpoint Commit Governance

## 背景

当前 `develop` 已有 `freely ai` 能力，可以手工执行账号保存、查看、切换，但狗粮中的 Freely auto loop 仍未把该能力接入运行时。

当前活跃 worktree 也暴露了第二个问题：大量文档、runtime、前后端代码同时处于未提交状态，说明 Freely 还没有把“何时提交、何时切 checkpoint、何时暂停继续集成验证”收敛成正式能力。

这两个缺口在自治开发里会互相放大：

- 配额打满时，Freely 无法自动基于 account/cooldown 做切换与恢复。
- 脏树持续累积时，Freely 无法在合适的 issue 边界形成可恢复的 checkpoint commit。
- 结果就是 supervisor 虽然能持续拉起 Codex，但自治质量会退化成“长时间脏树 + 高频恢复 + 难以合并”。

## 现状判断

### 1. `freely ai` 已可手工切换账号

`docs/system/workspace/scripts/runtime/ai-cli` 已提供：

- `freely ai init`
- `freely ai login codex`
- `freely ai save codex [account]`
- `freely ai switch codex <account>`
- `freely ai whoami`
- `freely ai status`

但它当前仍是独立 CLI，不是 Freely auto loop 的组成部分。`runtime/freely`、`monitor-ai-cli.sh`、`start-lead-agent.sh` 里都还没有把 account 状态、cooldown、switch/restart/recovery 接起来。

### 2. checkpoint commit 仍靠人判断

当前 dogfood worktree 已经同时积累：

- runtime/control-plane 变更
- routing/session lifecycle 文档与测试
- frontend probe 文档
- Rust/Tauri probe bridge 代码
- Vite/frontend shell 代码

这说明 Freely 当前没有下列强约束：

- issue 边界上的 commit checkpoint
- dirty-tree 上限
- “验证通过后必须提交”的门
- “上下文占用/限流前必须落 commit 或 recovery artifact”的门

### 3. 当前缺的不是“提醒”，而是 control plane 能力

如果只是给 agent 文案里加一句“记得提交”，不会稳定生效。真正缺的是：

- account-aware runtime orchestration
- rate-limit-aware account rotation
- issue-aware checkpoint commit governance
- multi-worktree integration batching

## 应收敛的能力

### A. Account-aware auto loop

Freely 应把 `freely ai` 从独立 CLI 升级为 runtime capability：

1. 启动 AI 前读取当前 active account
2. 将 account 身份、cooldown、失败状态纳入 `.freely/state`
3. 检测 usage limit / auth failure 时：
   - 先写 recovery
   - 停当前进程
   - 执行 `freely ai switch ...`
   - 再按 session lifecycle 恢复
4. 若无可用 account，则转阻塞态并记录 reset_at / intervention needed

### B. Checkpoint commit governance

Freely 应新增正式 checkpoint 规则：

1. `done_ibm -> in_dev` 前，必须明确该 issue 的 commit boundary
2. 每次通过一个最小验证门后，必须形成 checkpoint commit 或 checkpoint branch note
3. worktree dirty scope 超阈值时，不允许继续新增实现，先切 checkpoint
4. 命中 context rotate / usage-limit 前，优先：
   - 更新 issue/progress/recovery
   - 形成 checkpoint commit
   - 再 `fresh_with_handoff`

### C. Multi-worktree promotion gate

多 worktree 并行时，Freely 应知道：

- 哪个 worktree 允许继续积累未提交改动
- 哪个 worktree 必须先 checkpoint
- 哪个 worktree 只允许 doc-loop，不允许 dev-loop
- 哪个 worktree 已具备进入 integration batch 的条件

## 为什么当前 worktree 没做好

不是 Codex 单点失误，而是 Freely 自己还缺制度化约束：

1. runtime 只负责 `fresh/resume/handoff`，还没负责 checkpoint commit
2. `freely ai` 已存在，但未纳入 runtime 的限流恢复链路
3. 当前没有 `tests/integration/<issue>.sh` 强门，导致“验证完成”和“应该提交”之间没有硬连接
4. 当前没有 worktree-level WIP budget，所以一个工位会越堆越多

## 预期落点

- `docs/LAWS.md`
  - 增加 account rotation 与 checkpoint commit 的治理规则
- `docs/system/workspace/scripts/runtime/freely`
  - 增加 account-aware retry/switch hooks
  - 增加 dirty-tree / checkpoint policy hooks
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
  - 输出可供 runtime 判定的 rate-limit / auth-failure / account metadata
- `docs/system/workspace/scripts/runtime/ai-cli`
  - 增加 machine-readable status / active account / cooldown output
- `docs/system/workspace/hooks/`
  - 增加 checkpoint 与 integration gate
- `tests/integration/`
  - issue 级集成测试绑定 checkpoint 与 promote 门

## 建议优先级

1. 先把 `freely ai status/switch` 接入 runtime 的 machine-readable 恢复链路
2. 再落 dirty-tree + verification-driven checkpoint commit gate
3. 最后把多 worktree promotion/integration batch 统一到 supervisor 视图
