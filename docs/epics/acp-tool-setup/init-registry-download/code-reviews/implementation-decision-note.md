---
issue_id: I-20260630T124528Z-A
issue_path: docs/epics/acp-tool-setup/init-registry-download/raw-20260630T124528Z/issues/I-20260630T124528Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260630T124528Z-A
- issue_path: docs/epics/acp-tool-setup/init-registry-download/raw-20260630T124528Z/issues/I-20260630T124528Z-A.md

## Implementation Decision Note

- decision: freely init 统一入口 + tool-registry 驱动 + config.toml 持久化
  1. tool-registry 每个 [tool.acp] 新增 install_method + download_url — 唯一下载源
  2. ensure-codex-acp → ensure-acp-binary --tool <name> — 通用下载脚本
  3. cmd_init() 循环 registry 对每个 tool 发现/下载/写 config.toml
  4. _ensure_acp_bridge_running 优先读 config.toml 的 FREELY_ACP_<TOOL>_BIN
  5. 修复 _acp_bridge_health_check Shell 注入

- why_this:
  1. 当前 ACP binary 发现逻辑在 init 和 runtime 中各写一份，硬编码 codex vs *，不一致且脆弱
  2. tool-registry 已有 binary/args/auto_download 字段，但缺少 download_url 和 install_method 来完成下载
  3. config.toml 是项目级配置中心，binary 路径应持久化在这里而非每次重新计算
  4. 循环 registry 保证未来新增工具零代码改动
  5. 所有工具都需用户确认下载——包括 claude/codex 的独立 ACP binary
  6. download_url 是唯一合法下载源——不在 registry 配置的地址不允许下载

- alternatives_considered:
  - 懒下载（runtime 首次用到时下载）: 体验差，daemon start 卡住等待，非交互模式无法确认
  - 保留现状只改报错: 没解决任何实际问题
  - 分成两个 candidate（A=registry, B=init）: B 依赖 A，拆开增加协调成本

- boundary_non_goals:
  - 不修改 ACP SDK (agent-client-protocol) 的安装逻辑
  - 不修改 agent-table.toml 结构
  - 不修改 ACP bridge session/fork/resume 逻辑
  - 不实现多 tool 同时运行的 ACP bridge 架构（未来需求）
  - 不修改 _acp_bridge_health_check 的检查逻辑（只修复 Shell 注入，不改变检查内容）

- residual_risk:
  - npm install -g 需 Node.js 环境，部分系统可能缺失
  - github_release 下载依赖 curl + tar，网络不通时失败——需友好报错
  - .freely/config.toml 是项目级文件，binary 路径可能因机器不同而变化——需在每台机器跑 freely init
  - 交互式确认依赖 stdin，CI 环境可能无法交互——需支持 --accept-default-autonomy 跳过确认
