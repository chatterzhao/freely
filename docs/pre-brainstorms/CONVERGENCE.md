# 候选项收敛（阶段 1）

日期：2026-03-05

## 收敛规则
每个候选项在进入 issue 队列前需通过反向约束检查：

1. 意图适配（`docs/PROJECT_INTENT.md`）
2. 宪法/法律适配（`docs/CONSTITUTION.md`、`docs/LAWS.md`）
3. 流程适配统一循环图（A1 -> A2 -> IBM+G/DDD -> A3）
4. 当前架构/范围内的实现可行性
5. 价值 > 成本（若改变循环/流程逻辑）

只有通过全部 5 项检查的候选项才能成为 issue-ready。

## Issue-Ready（立即入队）

### 批次 P0-核心
1. `C-20260304-601` Owner Loop 契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：循环契约 + 状态转换
- 依赖：无

2. `C-20260304-602` 门禁契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：可执行的门禁定义
- 依赖：C-20260304-601

3. `C-20260304-603` 恢复契约
- 路由：A1/A2 -> doc-loop(IBM+G)
- 输出目标：续接/桥接协议
- 依赖：C-20260304-601

4. `C-20260304-604` Issue 发现 + 路由器内核
- 路由：A1 -> A2 -> auto-loop(ADD)
- 输出目标：来源扫描 + 路由决策逻辑
- 依赖：C-20260304-601

5. `C-20260304-607` 文档契约编译器
- 路由：doc-loop(IBM+G) -> dev-loop(DDD)
- 输出目标：验收标准 -> 可执行检查
- 依赖：C-20260304-602

6. `C-20260303-101` CLI 编排 MVP
- 路由：auto-loop(ADD) / dev-loop(DDD)
- 输出目标：命令编排 + 重试/超时/日志
- 依赖：C-20260304-601

7. `C-20260303-102` 集成测试优先门禁
- 路由：dev-loop(DDD)
- 输出目标：提升前的集成门禁
- 依赖：C-20260304-602, C-20260304-607

8. `C-20260304-201` 后端 API 契约 v1
- 路由：doc-loop(IBM+G)
- 输出目标：前端解耦的稳定 API
- 依赖：C-20260304-601, C-20260304-602

### 批次 P1-后续
9. `C-20260304-203` 后端优先执行门禁
10. `C-20260303-003` 验收契约 + 自包含检查器
11. `C-20260303-103` 会话生命周期（续接/压缩/新会话）
12. `C-20260304-202` 多项目 UI 隔离实现
13. `C-20260304-606` 提升与清理执行器

## 需要研究（保留在候选池）
1. `C-20260303-002` 独立审计门禁
- 原因：当前阶段需要最小可实现边界。

2. `C-20260304-501` Freely-on-OpenClaw 配置
- 原因：外部运行时假设需重新检查当前架构。

3. `C-20260304-605` 子代理批量编排器
- 原因：并发边界和推广范围未收敛。

## 已放弃（超出当前架构范围）
1. `C-20260304-301` EvoMap 集成作为 P2 插件
2. `C-20260304-401` 验收到能力资产映射

## 下一步行动
- 先将批次 P0-核心转换为可执行 issue 规范。
- 保持所有流程/契约变更在价值验证检查之后。

## 变更（2026-03-05 自举 + 治理）

### 新增到 P0-核心
- `C-20260305-701` Worktree 根目录执行器 + 权限预检
- `C-20260305-702` 钩子策略模板编译器
- `C-20260305-704` Freely 自举治理契约

### 新增到 P1-后续
- `C-20260305-703` 钩子/Worktree 约束治理 UI

## 变更（2026-03-05 目录统一）

### 新增到 P0-核心
- `C-20260305-801` 目录迁移契约（Doc-Loop Contract）
- `C-20260305-802` 文档门禁对齐到新目录
- `C-20260305-901` Doc-loop 治理维护职责显式化（IBM+G）

### 新增到 P1-后续
- `C-20260305-803` Deferred 资产选择性迁移执行器

## 变更（2026-03-05 治理编译链对齐）

### 新增到 P0-核心
- `C-20260305-902` Governance Alignment Compiler for Skills / Hooks / Bin

## 变更（2026-03-05 字段收敛与口径统一）

- 候选字段统一：`promoted_issue_path`、`milestone`、`session_refs` 不再留空，统一使用显式 pending/空列表值。
- 路由口径统一：`doc-loop(IBM)` 统一升级为 `doc-loop(IBM+G)`，匹配当前治理职责定义。

## 变更（2026-03-05 pre-test-merge 职责迁移）

### 新增到 P0-核心
- `C-20260305-903` `pre-develop` -> `pre-test-merge` 职责迁移
- `C-20260305-904` `wt-enter` / `post-checkout` worktree 引导修复

## 变更（2026-03-06 hooks 安装模式）

### 新增到 P0-核心
- `C-20260306-001` Freely 托管 hooks 默认落在 `.freely/.githooks`
- `C-20260306-002` Hooks 托管模式前端开关与用户接管退出路径

## 变更（2026-03-06 标准 worktree 提示统一）

### 新增到 P0-核心
- `C-20260306-1001` 标准 `git worktree` 提示统一

## 变更（2026-03-06 issue 绑定头脑风暴路由）

### 新增到 P0-核心
- `C-20260306-1101` `auto-loop-lead-agent.md`
- `C-20260306-1102` `context-source-skill.md`
- `C-20260306-1103` `no-skill.md`
- `C-20260306-1104` `has-skill.md`
- `C-20260306-1105` `auto-loop-orchestrator` / guidance 对齐到两层 auto-loop 模型

## 变更（2026-03-08 状态联动与会话证据治理）

### 新增到 P0-核心
- `C-20260308-0101` 状态联动、流程标识词典与 session evidence 传播治理

## 变更（2026-03-08 premerge / pre-test-merge 收敛批次）

### 批次背景
- 目的：收敛 `feature/governance-alignment-hardening-20260305`、`feature/issue-brainstorm-routing-guard-20260306`、`feature/state-sync-and-session-evidence-governance-20260308`
- 临时验证路径：
  - `pre-test-merge`
  - `feature/premerge-20260308-0235--governance-convergence`
- 原因：旧 feature 与当前 `develop` 在治理文档、hooks 与路由模型上出现高冲突，直接顺序 merge 风险高

### 合并与验证证据
- `feature/state-sync-and-session-evidence-governance-20260308` 先固化为提交 `efca6c4`
- `feature/premerge-20260308-0235--governance-convergence` 收敛提交链：
  - `85a10eb` merge `feature/governance-alignment-hardening-20260305`
  - `a08ba20` merge `feature/issue-brainstorm-routing-guard-20260306`
  - `b4eeb8b` merge `feature/state-sync-and-session-evidence-governance-20260308`
  - `d74a543` 修复历史 candidate 字段格式，消除 `bmad-check` 阻塞
- `pre-test-merge` 验证批次提交：`454d0e3`
- 提升到 `develop` 的提交：`64cd6d4`
- 验证命令与结果：
  - `./bin/wt-status-all` -> `CLEAN`
  - `./bin/bmad-check` -> `passed`
  - `./bin/test-pre-push-hook` -> `pass=6 fail=0`

### cleanup 结果
- 已删除本地分支与 worktree：
  - `feature/premerge-20260308-0235--governance-convergence`
  - `pre-test-merge`
  - `feature/state-sync-and-session-evidence-governance-20260308`
  - `feature/governance-alignment-hardening-20260305`
  - `feature/issue-brainstorm-routing-guard-20260306`
  - `feature/loop-routing-derived-worktree-governance-20260307`
  - `feature/ai-tool-worktree-directory-access-20260307`
  - `feature/freely-githooks-install-strategy-20260306`
  - `feature/worktree-date-prefix-20260307`
  - `feature/worktree-naming-doc-sync-20260307`
- 当前 worktree 卫生状态：
  - 仅保留主工作树 `develop`
  - `./bin/wt-status-all` 汇总：`total=1, dirty=0`

## 变更（2026-03-08 里程碑状态标识符语义收敛）

### 收敛结论
- `C-20260308-1501` 里程碑状态标识符重命名与职责边界收紧
  - 问题：`milestone_state=in_progress` 与 `loop_stage` 存在语义重叠
  - 初步方案：将 `in_progress` 改为 `active`，`completed` 改为 `delivered`
  - 后续处理：该方案已被 `20260308-1630--stage-prefixed-progress-identifier` 吸收并替代，不再单独进入 milestone 或 issue materialization
  - 当前状态：dropped，保留为前置探索记录
