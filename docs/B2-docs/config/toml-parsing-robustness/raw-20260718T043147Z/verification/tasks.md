# Tasks: I-20260718T043147Z-A

- issue_id: I-20260718T043147Z-A
- owner: dev-loop

## Tasks

- [ ] T1: 修改 `.freely/agent-table.toml` — 将 `worker_slot` 从 `opencode-apikey-ds-flash-auto` 改为 `claude-apikey-ds-pro-auto`
  - 文件：`/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/agent-table.toml`
  - 改动：第 `worker_slot` 行，1 行替换
  - 注意：这是项目根目录的 agent-table.toml，不是 worktree 内的副本

- [ ] T2: 停止当前 daemon（`freely daemon stop` 或直接 kill）

- [ ] T3: 重启 daemon（`freely daemon start --task-mode auto`）并观察 worker bridge initialize 日志

- [ ] T4: 验证 AT-001/AT-002/AT-003（grep + live-status + fleet-status）并记录证据到 test-evidence/
