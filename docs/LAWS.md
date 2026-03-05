# Freely 法律

> 我是项目法律，只负责判定规则、验收证据、技能路由；不定义执行步骤。

---

## 1. 产品身份

判定规则：
1. 执行链保持“获取 Issue -> 文档 -> 开发 -> 验收 -> 获取 Issue”闭环。
2. 需求来源不退化为单一固定待办列表。
3. 无明确停止条件时维持自治循环与续接策略。

最小验收证据：
- issue 来源记录
- 路由记录
- 回流后下一轮输入状态记录

执行技能：
- `skill:auto-loop-orchestrator`
- `skill:laws-enforcer`

---

## 2. 分支与工作树策略（硬性要求）

判定规则：
1. 分支来源、merge 方向、保护分支策略符合宪法分支表。
2. `feature/*` 从 `pre-develop` 创建并在 worktree 内开发。
3. `main/develop/pre-develop` 保持 add/commit 禁止。
4. `pre-develop -> develop` 提升前，`TEST`（含集成验收）通过。
5. `PRE_TEST` 仅作为开发前基线，不得替代提升测试结果。
6. 提升前必须有评审记录、祖先可追溯证据、进度/恢复更新证据。
7. merge/promotion/release/cleanup 前执行 `./bin/wt-status-all`，结果全 `CLEAN`。
8. premerge 仅作冲突收敛，来源与回并目标均为 `pre-develop`。
9. 清理动作只能在 `verified-retirable` 后执行，且必须留痕。

最小验收证据：
- 分支来源与合并路径记录
- `wt-status-all` 输出记录
- 测试、评审、进度/恢复证据
- 分支/worktree 清理记录

执行技能：
- `skill:branch-management`
- `skill:premerge-reconcile`
- `skill:constitution-guard`

---

## 3. 版本命名规则（硬性要求）

判定规则：
1. tag 命名格式为 `YYYY.MM.DD-HHMM-stage`。
2. 分支与 stage 映射符合宪法表。
3. `alpha`/`beta` 为本地 tag，不得 push。

最小验收证据：
- tag 列表与分支映射记录

执行技能：
- `skill:branch-management`
- `skill:laws-enforcer`

---

## 4. 强制技术栈

判定规则：
1. 未经修订，不得替换强制技术栈（Tauri/Rust/React/Bun/xterm.js/Rust PTY）。
2. 涉及替换时必须提供显式修订与迁移证据。

最小验收证据：
- 技术栈检查记录
- 修订说明（如有）

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

---

## 5. 基线项目结构（硬性要求）

判定规则：
1. 项目至少满足宪法规定的基线结构。
2. 研究阶段允许最小 docs 集合，但必须保证可追溯证据不缺失。
3. 本阶段采用双轨验收：规范路径产物或等价可追溯证据，满足其一即可。

最小验收证据：
- 目录结构检查记录
- 等价证据索引（若未落规范路径）

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

---

## 6. 终端架构规则

判定规则：
1. 终端通过 PTY 执行真实 shell。
2. 循环实例会话/PID/状态隔离。
3. 监控和恢复目标对齐 AI CLI 会话生命周期。

最小验收证据：
- PTY 执行证据
- 会话隔离与监控记录

执行技能：
- `skill:constitution-guard`
- `skill:recovery-subagent-governance`

---

## 7. AI 执行模式

判定规则：
1. AI 规格符合 `tool:model:mode`。
2. `mode` 语义不被破坏（`auto`/`step`）。

最小验收证据：
- 运行配置与模式记录

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

---

## 8. 恢复策略（硬性要求）

判定规则：
1. 优先续接；不支持续接时执行桥接恢复。
2. 恢复记录必须含 branch/worktree/session 上下文。
3. 恢复后能回到可执行循环状态。

最小验收证据：
- 续接或桥接记录
- 恢复检查点记录

执行技能：
- `skill:recovery-subagent-governance`
- `skill:auto-loop-orchestrator`

---

## 9. 约束面

判定规则：
1. 仅使用宪法定义输入面（路径/意图/宪法/AI 规格）。
2. 其他上下文通过项目文件发现，不走隐式注入。

最小验收证据：
- 输入参数白名单检查记录

执行技能：
- `skill:constitution-guard`
- `skill:laws-enforcer`

---

## 10. 工程纪律

判定规则：
1. 命令面可脚本化且确定性。
2. 状态可落盘且可检查。
3. `AGENTS.md` 在项目根存在并可用。
4. 代码与文档冲突时，先走代码/测试修复路径。
5. 规范文档改动必须在独立 `feature/*` + worktree 且绑定实现或门禁证据。
6. 任一法律门失败时必须阻断提升/发布，并记录修复路径。

最小验收证据：
- 命令与状态检查记录
- 违例记录与修复记录

执行技能：
- `skill:laws-enforcer`
- `skill:dev-loop-execution`

---

## 11. 方法论总述（硬性要求）

判定规则：
1. Doc-loop 产物完整（`IBM` 业务产物与 `G` 治理产物按 issue 范围满足其一或组合，并保持可追溯）。
2. Dev-loop 产物完整，且测试证据可追溯。
3. Auto-loop 路由可解释，回流状态正确。
4. `map` 阶段定义 `PRE_TEST` 基线，提升/合并阶段使用执行后的 `TEST` 结果。

最小验收证据：
- doc/dev/auto 三循环产物链
- 治理资产一致性证据（当 issue 触发治理维护时）
- 路由与状态链路记录

执行技能：
- `skill:doc-loop-execution`
- `skill:dev-loop-execution`
- `skill:auto-loop-orchestrator`
- `skill:laws-enforcer`

---

## 12. 子代理规划与委托（硬性要求）

判定规则：
1. 委托前有边界、完成标准、合并标准。
2. 父级对批次具备等待语义与收敛语义。
3. 子代理失败时有可追溯回退路径。

最小验收证据：
- 任务映射与完成状态记录
- 回退决策记录

执行技能：
- `skill:recovery-subagent-governance`
- `skill:laws-enforcer`

---

## 13. 并行开发的领域模型（硬性要求）

判定规则：
1. 物理领域：并行任务使用独立 worktree。
2. 逻辑领域：并行任务拥有明确文件/模块所有权边界。
3. 共享热点采用串行窗口或显式排序策略。

最小验收证据：
- 领域边界记录
- 冲突窗口与排序记录

执行技能：
- `skill:recovery-subagent-governance`
- `skill:laws-enforcer`

---

## 14. 可插拔模块架构与接口版本控制（硬性要求）

判定规则：
1. 接口版本策略明确。
2. 破坏性变更具备迁移与回滚路径。
3. 合约测试覆盖当前/候选实现。
4. 第三方 API 以提供方契约为外部事实源，本地实现做适配。

最小验收证据：
- 版本与迁移文档
- 合约测试记录

执行技能：
- `skill:module-interface-governance`

---

## 15. 变更前配置备份（硬性要求）

判定规则：
1. 配置修改前必须备份。
2. 备份命名符合宪法约束。
3. 备份路径可追溯。

最小验收证据：
- 备份文件路径与时间记录

执行技能：
- `skill:config-backup-guard`

---

## 16. Freely 自举开发（硬性要求）

判定规则：
1. Freely 自身开发遵守同一治理链（意图/宪法/法律/skills）。
2. 架构治理变更先进入 pre-brainstorms，再进入 doc/dev 落地。
3. 工具链治理能力可复用到托管项目。

最小验收证据：
- pre-brainstorms -> doc/dev 落地链路
- 自举治理检查记录

执行技能：
- `skill:constitution-guard`
- `skill:branch-management`
- `skill:laws-enforcer`

---

## 附录 A. 执行路由（固定顺序）

默认执行链：
1. `skill:constitution-guard`（硬约束门禁）
2. `skill:laws-enforcer`（法律门禁与证据校验）
3. 业务技能（`auto/doc/dev/branch/...`）

说明：
- 法律只定义门与证据，不定义操作步骤。
- 操作步骤以 `docs/system/workspace/skills/` 为唯一执行事实源。

## 附录 B. 三层职责边界（宪法 / 法律 / skills）

1. 宪法（What/Why）：边界与原则，不写执行步骤。
2. 法律（Check/Accept/Route）：判定门、证据口径、技能路由，不写执行步骤。
3. skills（How）：可执行操作步骤，不扩展宪法边界、不替代法律验收。
4. skills 可在不冲突前提下补充实现细节（如依赖安装、配置引导、环境预检、修复脚本）；若该细节需成为强制放行门，必须回写法律章节。
