# B1 Brainstorm: Agent 设计优化

## 问题领域

Freely 的 Manager/Worker agent 在以下方面存在设计缺陷：
skill 使用无约束、intent_kind 语义模糊、工具无角色绑定、agent doc 过载。

## Discovery: 当前状态

### 33 个技能

| 技能 | 归属 | 用途 | 当前使用情况 |
|------|------|------|-------------|
| freely-constitution-guard | 共享 | 宪法硬性约束门禁（预检） | Manager 首跳调用 |
| freely-laws-enforcer | 共享 | 法律级验收检查 | Manager 首跳调用 |
| freely-context-source-skill | 共享 | 输入来源判定与下一跳路由 | Manager 首跳调用 |
| freely-auto-loop-orchestrator | 共享 | 自主持续交付循环编排 | 未充分使用 |
| freely-agent-execution-safety-review | 共享 | 执行边界安全评审 | 未充分使用 |
| freely-config-backup-guard | 共享 | 配置修改前强制备份 | 未充分使用 |
| freely-dev-loop-execution | Worker | milestone issue 实现、测试与进度回写 | Worker 开发时 |
| freely-doc-B1_IBM-execution | Worker | raw issue → brainstorm → candidate | Worker B1 时 |
| freely-doc-B2_IBM-execution | Worker | milestone issue → prd/pre-tests/tasks/code-review | Worker B2 时 |
| freely-fix-execution | Worker | bug 快速修复流程 | Worker fix 时 |
| freely-feat-execution | Manager | 新功能完整开发流程编排 | 未充分使用 |
| freely-url-content-intake | Worker | URL 内容抓取与结构化 | 很少使用 |
| freely-rust-tauri-toolchain-bootstrap | Worker | Rust/Tauri toolchain 引导 | 很少使用 |
| freely-tool-cc-codex-mcp-runtime | Worker | Codex MCP 运行时安装配置 | 很少使用 |
| freely-workspace-skill-governance | Worker | skill 新增/拆分/重构/校准 | 很少使用 |
| freely-mem9-continuity-bridge | Worker | mem9 连续性后端接入 | 很少使用 |
| freely-multi-worktree-supervision | Manager | 同时监督多个 worktree | Manager patrol 时 |
| freely-worktree-maintenance-governance | Manager | worktree 状态核单、merge 顺序、fleet closure | Manager cleanup 时 |
| freely-worktree-hygiene-supervision | Manager | 单个 worktree dirty-budget/checkpoint | Manager 监督时 |
| freely-premerge-reconcile | Manager | 合并冲突的高风险协调 | 很少使用 |
| freely-milestone-planning-state-maintenance | Manager | 里程碑状态维护与 sequencing | 很少使用 |
| freely-branch-management | Manager | 完整自主分支生命周期管理 | Manager 委派前 |
| freely-candidate-acceptance-review | Manager | candidate acceptance 独立评审 | 很少使用 |
| freely-watchdog-control-plane | Manager | 外层监督与恢复控制面 | 很少使用 |
| freely-continuity-watchdog | Manager | 上下文连续性监督 | 很少使用 |
| freely-ai-cli-availability-manager | Manager | AI CLI 工具可用性管理 | 很少使用 |
| freely-signal-intent-understanding | Manager | signal 意图收敛 | 很少使用 |
| freely-human-interruption-manager-triage | Manager | 插话的主管级 routing | 很少使用 |
| freely-human-interruption-handling | Manager | 插话深度处理 | 很少使用 |
| freely-human-interruption-direct-answer | Manager | 插话直接回答 | 很少使用 |
| freely-chat-issue-routing | Manager | chat 消息路由到正确 issue | 很少使用 |
| freely-recovery-subagent-governance | Manager | 恢复耦合与子代理治理 | 很少使用 |
| freely-module-interface-governance | Manager | 模块接口版本治理 | 很少使用 |

**关键发现：33 个技能中，仅约 6-8 个被实际使用。** 大部分技能定义了但 Agent 从未调用。

### Agent Doc 现状

**Manager Agent (344 行):**
- 有"可用技能"表格（按角色分）
- 有"可用工具"表格（按用途分）
- 有"巡逻工作流"步骤
- 但**没有触发条件**——Agent 不知道什么时候该调哪个 skill
- "首跳路由流程"过于复杂，Manager 经常跳过直接 patrol

**Worker Agent (189 行):**
- **没有 skill 触发条件**——只在"可用技能"表格里列出，不给"何时使用"
- **intent_kind 定义过于简单**：edit/cleanup/promotion 三个词，没例子
- **步骤流程不强制**——"限时 10 秒/20 秒"但允许跳过

### 行业对比

| 特性 | Hermes | OpenClaw | Freely 当前 |
|------|--------|----------|------------|
| Skill 加载 | 索引+按需 view | 按 workspace 安装 | 全量部署到文件系统 |
| 触发条件 | "When to use" 明确 | AGENTS.md 路由 | 无 |
| 角色隔离 | 共享 memory 独立 | 每 specialist 独立 workspace/memory | 共享所有 |
| 工具权限 | per-tool approval | per-action gate | 无隔离 |
| 自改进 | Nudge Engine 自动 patch | Workflow Crystallization | 无 |
| Agent doc 大小 | 精简+冻结前缀缓存 | 精简 | 344+189 行 |

## Research: 改进方向

### 1. Skill 使用约束

**方案 A: Worker prompt 必须指定 skill**
```
rationale: "因为 X，所以做 Y"
skill: freely-fix-execution   ← 新增必填字段
```

**方案 B: Agent doc 里加触发条件表**
```
| 场景 | 必须调用 |
|------|---------|
| 收到 fix 任务 | skill:freely-fix-execution |
| 需要 B1 预研 | skill:freely-doc-B1_IBM-execution |
| 需要 B2 实现 | skill:freely-doc-B2_IBM-execution |
| 修改代码前 | skill:freely-config-backup-guard |
| 提交前 | skill:freely-constitution-guard |
```

### 2. intent_kind 语义

当前 3 个值太粗，建议细化：

| intent_kind | 含义 | 允许操作 | 举例 |
|-------------|------|---------|------|
| `edit` | 代码/文档修改 | 写文件、提交 | 修 bug、加功能、改文档 |
| `merge` | 合并分支 | pr-merge-guarded | feature → develop |
| `closeout` | 批量收口 | issue-sync close、wt-close | 关闭 issue、退役工位 |
| `sync` | 平台同步 | issue-sync create/update | 推送 issue 到 GitHub |
| `cleanup` | 治理清理 | 删除过期分支、工位 | 清理 test-pre-merge |
| `promotion` | 发布升级 | 打 tag、推 release | 版本发布 |

或者保持 3 个但加子类型：`edit:bugfix`、`edit:feature`、`cleanup:merge`、`cleanup:closeout`

### 3. Agent Doc 重构

**Manager Agent 精简方向:**
- 巡逻工作流压缩为决策树
- 每个 patrol 阶段绑定必调 skill
- 首跳简化为：读宪法 → 读法律 → 读 fleet → 判路由

**Worker Agent 精简方向:**
- 开头：必调 skill 约束表
- 中间：按 intent_kind 选择 skill → 执行 → 交接
- 结尾：JSON5 模板（已有）

### 4. 工具角色绑定

| 工具 | Manager | Worker |
|------|---------|--------|
| wt-create | ✅ | ❌（由 Manager 创建工位后委派） |
| pr-merge-guarded | ✅ | ✅（Worker 执行合并） |
| wt-close | ✅ | ✅ |
| issue-sync | ✅ | ✅ |
| deploy-skills | ✅ | ❌ |
| freely-package | ✅ | ❌ |

## Decision

待写。基于以上研究，需要决定具体实施方案。
