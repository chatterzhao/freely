# Freely 打包形态

Freely core 只有一套：scan、Manager/Worker/Reviewer、B1/B2、SDD/TDD、gates、worktree、handoff、PR。不同打包形态只替换 **host/UI/harness**，不复制 loop。

| 形态 | 目录/入口 | host | 说明 |
| --- | --- | --- | --- |
| CLI/TUI | `bin/freely`、终端 | Freely | 当前主入口；`live-status`/`fleet-status`/chat |
| Desktop/Web | `src/` + `src-tauri/` | Freely/Tauri | Freely 自己的前端 probe；不是 DSH profile |
| ACP harness | `docs/system/workspace/scripts/runtime/run-acp-prompt.py` | Freely | 外部 Claude/Codex/OpenCode/Cline |
| **DSH plugin** | `packaging/dsh-freely/` | **DSH** | Freely 保留 loop，DSH 提供 Session/Agent/模型/工具 |

## dsh-freely 的准确位置

- 从产品分发看：它是 **Freely 的一种打包形态**（Freely-as-DSH-plugin），和 CLI/Desktop 并列。
- 从技术层看：它是 **DSH bundle plugin**，被 DSH 的 `web`/`tui`/`desktop` profile 消费；它不是 DSH profile 本身，也不是 Freely 的 TUI/Web/Desktop 前端。
- 因此目录放 `packaging/dsh-freely/`，而不是 `plugins/`（`plugins/` 是 DSH 的插件语义，不是 Freely 的产品层级）。

## 约束

- 不加载 `dsh-superagent`；DSH Router/Ticket 不接管 loop。
- 宿主基线：`dsh 0.2.1-rc.5` + `web` profile；headless/desktop 未验证。
- 真实 issue→PR E2E 未过前，不宣称 dsh-freely 产品完成。
