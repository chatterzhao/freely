# 宪法门禁

1. 产品身份：执行链保持“获取 Issue -> 文档 -> 开发 -> 验收 -> 获取 Issue”闭环，且来源不退化为固定待办。
2. 分支与工作树：分支来源、merge 方向、保护分支与 sibling worktree 根目录符合宪法表；主分支禁止 add/commit。
3. 版本命名：标签遵循 `YYYY.MM.DD-HHMM-stage`，且分支 / stage 映射正确。
4. 强制技术栈：未显式修订前，不替换 Tauri / Rust / React / Bun / xterm.js / Rust PTY。
5. 基线结构：当前研究阶段至少保留 `PROJECT_INTENT`、`CONSTITUTION`、`LAWS` 与 `B1-docs/` 活跃文档集合。
6. 终端架构：终端必须经 PTY 驱动真实 shell，会话/PID/状态隔离。
7. AI 执行模式：AI 规格遵循 `tool:model:mode`，`auto` / `step` 语义不被破坏。
8. 恢复策略：续接优先，不支持续接时桥接恢复；恢复记录保留 branch/worktree/session。
9. 约束面：除最小输入面外，其余上下文从项目文件发现，不走隐式配置注入。
10. 工程纪律：代码/文档冲突时优先代码/测试修正；规范文档改动需专用 feature/worktree 且绑定实现或门禁证据。
11. 三个 loop：`auto-loop` 编排并进入 sibling 的 `doc-loop` / `dev-loop`；worker 只推进并产出 evidence，completion / cleanup judgment 必须回到 `auto-loop`，且整体闭环必须可追溯。`PRE_TEST` 仅作基线，提升门禁使用已执行的 `TEST`。
12. 子代理：委托前定义边界与完成标准，批次未收敛不得宣告成功。
13. 并行开发：并行任务必须使用独立 worktree，存在明确 ownership 边界，热点有串行窗口或排序策略。
14. 模块接口：破坏性变更具备版本化、迁移与回滚路径；第三方 API 契约为外部事实源。
15. 配置备份：配置修改前先备份；备份名包含源文件基名、`.bak` 与 UTC 时间戳。
16. 自举开发：Freely 开发 Freely 时，hooks/bin 与治理文档必须保持同源，不得自我豁免。
