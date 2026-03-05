# Freely 法律

> 我是项目法律，负责判定标准与验收口径。

---

## 0. 法律定位

法律只定义三类内容：
- 判定规则（什么算合规）
- 验收证据（什么算完成）
- 技能路由（由哪个 skill 执行）

法律不重复执行步骤。执行步骤以 `docs/system/workspace/skills/` 为唯一执行事实源。

---

## 1. 当前阶段约束

在文档模型重构阶段，`docs/` 最小集合：
- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`
- `docs/CONSTITUTION.md`
- `docs/pre-brainstorms/`

判定规则：
1. 新讨论与新决策进入 `docs/pre-brainstorms/<YYYYMMDD-HHMM--topic>/`。
2. 历史执行态文档不在工作区保留，通过 git 历史追溯。
3. 三件套（意图/法律/宪法）未一致前，不扩展旧目录模型。

---

## 2. 执行路由

默认执行链：
1. `skill:constitution-guard`（硬约束门禁）
2. `skill:laws-enforcer`（法律验收门禁）
3. 业务执行 skill（按场景）

业务执行 skill：
- 外循环编排：`skill:auto-loop-orchestrator`
- 文档内循环：`skill:doc-loop-execution`
- 开发内循环：`skill:dev-loop-execution`
- 分支与发布：`skill:branch-management`
- 复杂冲突：`skill:premerge-reconcile`
- 恢复与子代理：`skill:recovery-subagent-governance`
- 模块/接口治理：`skill:module-interface-governance`
- 配置备份：`skill:config-backup-guard`

---

## 3. 法律验收门

### 3.1 分支与发布门

通过条件：
1. `feature/*` 来源为 `pre-develop`。
2. `main/develop/pre-develop` 保持 add/commit 禁止。
3. merge 方向符合宪法分支表。
4. stage tag 符合 `YYYY.MM.DD-HHMM-stage` 与分支映射。
5. `alpha/beta` 不可 push。

执行技能：
- `skill:branch-management`
- `skill:constitution-guard`

### 3.2 Doc Loop 门

通过条件：
1. intake/brainstorm/map 产物完整。
2. candidates 的 route/status 一致。
3. milestone 与 issue 映射同步。

执行技能：
- `skill:doc-loop-execution`
- `skill:laws-enforcer`

### 3.3 Dev Loop 门

通过条件：
1. 代码与测试产物存在。
2. 进度/状态文档完成更新。
3. 验收与实现一致，无文档漂移。

执行技能：
- `skill:dev-loop-execution`
- `skill:laws-enforcer`

### 3.4 Auto Loop 门

通过条件：
1. issue 发现来源可追踪。
2. 路由决策可解释（doc-loop/dev-loop）。
3. 回流后下一轮输入状态正确。

执行技能：
- `skill:auto-loop-orchestrator`
- `skill:laws-enforcer`

### 3.5 冲突与回退门

通过条件：
1. 冲突决策按语义，不按提交时间。
2. 合并后治理语义无回退（分支策略/worktree/命名/tag 口径一致）。
3. premerge 分支从 `pre-develop` 拉出并回并 `pre-develop`。

执行技能：
- `skill:premerge-reconcile`
- `skill:branch-management`

### 3.6 恢复与子代理门

通过条件：
1. 恢复记录含 branch/worktree/session 上下文。
2. 子代理任务有边界、状态与合并影响记录。
3. 不存在所有权不清的续接执行。

执行技能：
- `skill:recovery-subagent-governance`

### 3.7 模块接口门

通过条件：
1. 接口版本策略明确。
2. 破坏性变更有迁移路径与回滚路径。
3. 合约测试覆盖当前/候选实现。

执行技能：
- `skill:module-interface-governance`

### 3.8 配置备份门

通过条件：
1. 任何配置修改前已完成备份。
2. 备份命名符合宪法约束。
3. 执行记录可追溯备份路径。

执行技能：
- `skill:config-backup-guard`

---

## 4. 清理与退役

判定规则：
1. 分支/worktree 仅在 `verified-retirable` 后删除。
2. 不能因“已合并”立即删除，必须先完成语义回退检查与测试。
3. 删除动作需保留记录（可追溯到合并与验证结果）。

执行技能：
- `skill:branch-management`

---

## 5. 违例处理

任一门禁失败：
1. 阻断后续 promotion/release。
2. 记录失败门、证据与修复路径。
3. 需要时转入 `skill:premerge-reconcile`。
