# Agent 上下文入口

只读链接：
- 宪法：docs/CONSTITUTION.md
- 项目意图：docs/PROJECT_INTENT.md
- 法律：docs/LAWS.md

---

## 项目概述

Freely 是一个自主工程循环系统，AI 担任项目所有者角色，自主管理需求发现、头脑风暴、EPIC/STORY 规划、开发和验证。

### 核心方法论

三层循环架构：
```
A:auto-loop（外循环）
│
├── 发现 Issue
├── 路由到内循环
│   ├── D:doc-loop(IBM)（文档循环）
│   └── D:dev-loop(DDD)（开发循环）
├── 完成 → 发现下一个 Issue
│
└── 循环，除非明确停止
```

### 可追溯链路

```
Intent -> PRD -> EPIC -> STORY -> Code/Test
```

---

## 命令

### Freely CLI (`./bin/freely`)

```bash
# 初始化项目用于自主循环
./bin/freely init \
  --project <绝对路径> \
  --intent <绝对文件路径> \
  --constitution <绝对文件路径> \
  --ai <工具[:模型][:模式]>

# 运行文档门禁检查
./bin/freely doctor --project <绝对路径>

# 启动自主循环
./bin/freely start --project <绝对路径>

# 查看状态
./bin/freely status --project <绝对路径>

# 停止运行实例
./bin/freely stop --project <绝对路径>
```

### AI 工具规格

格式：`工具:模型:模式`
- **工具**：`codex`、`kiro-cli`、`iflow`
- **模式**：
  - `auto` - 非交互式，自动批准（如果支持）
  - `step` - 交互式/批准模式

### BMAD 检查 (`./bin/bmad-check`)

在实现或合并前运行 BMAD 基线检查：

```bash
./bin/bmad-check
```

### Hook 回归测试 (`./bin/test-pre-push-hook`)

合并前验证本地推送策略：

```bash
./bin/test-pre-push-hook
```

### 工作树命令

```bash
# 进入/切换到分支工作树
source ./bin/wt-enter <分支名>

# 带工作树检查执行 add
source ./bin/wt-add <分支名> -- <git-add-参数>
```

---

## 分支规则

| 分支 | push | add/commit | merge 来源 | merge 到 | 备注 |
|------|------|------------|-----------|----------|------|
| main | ✅ | ❌ | release/* | - | hotfix 可用 `FREELY_ALLOW_MERGE=1` 绕过 |
| develop | ✅ | ❌ | pre-develop | - | hotfix 可用 `FREELY_ALLOW_MERGE=1` 绕过 |
| pre-develop | ✅ | ❌ | feature/* | develop | 不允许绕过 |
| feature/* | ✅ 同名 | ✅ worktree | - | pre-develop | 必须在 worktree 中开发 |
| release/* | ✅ 同名 | ✅ worktree | - | main, develop | 从 develop 创建 |
| hotfix/* | ✅ 同名 | ✅ worktree | - | main, develop | 从 main 创建 |

**关键规则**：
- `feature/* -> pre-develop` 用于测试集成
- `pre-develop -> develop` 仅在验证后
- 直接推送/合并到 `develop` 被本地 hook 策略阻止
- hotfix 合并到 main/develop 后必须同步到 pre-develop

---

## 版本命名

格式：`YYYY.MM.DD-HHMM-stage`

| 版本示例 | 分支 | 阶段 | Tag | 对外 |
|---------|------|------|-----|------|
| `2026.03.01-1430-alpha` | `feature/*` | 开发中 | 本地轻量 tag | 否 |
| `2026.03.01-1430-beta` | `pre-develop` | 测试集成 | 本地轻量 tag | 否 |
| `2026.03.01-1430-nightly` | `develop` | 夜间构建 | 推送 tag | 是 |
| `2026.03.01-1430-stable` | `main` | 正式发布 | 推送 tag | 是 |
| `2026.03.01-1430-hotfix` | `hotfix/*` | 紧急修复 | 推送 tag | 是 |

---

## 技术栈（硬性约束）

- **桌面外壳**：Tauri
- **核心运行时/编排器/监控/恢复**：Rust
- **前端 UI**：React
- **前端包/运行时工具**：Bun
- **终端渲染**：xterm.js
- **终端进程后端**：Rust PTY（系统 shell + PTY 进程）

---

## 项目结构

```
freely/
├── bin/                    # 可执行脚本
│   ├── freely              # 主 CLI
│   ├── bmad-check          # BMAD 门禁检查
│   ├── new-review          # 评审辅助
│   ├── test-pre-push-hook  # Hook 回归测试
│   ├── worktree-common.sh  # 工作树工具函数
│   ├── wt-add              # 工作树感知的 git add
│   └── wt-enter            # 进入工作树
├── docs/                   # 文档
│   ├── CONSTITUTION.md     # 硬性约束
│   ├── PROJECT_INTENT.md   # 项目目标
│   ├── LAWS.md             # 详细方法论
│   ├── brainstorms/        # 头脑风暴记录
│   ├── continuity/         # 进度与恢复
│   ├── epics/              # EPIC 实例
│   ├── planning/           # PRD/EPIC/STORY
│   ├── progress/           # 进度历史
│   ├── reviews/            # 评审记录
│   └── validation/         # PRE_TEST
├── src/                    # 源代码
├── templates/              # 文档模板
├── tests/                  # 测试脚本
├── .githooks/              # Git 钩子
│   ├── post-checkout
│   ├── pre-commit
│   └── pre-push
└── .env.example            # 环境变量模板
```

---

## 文档门禁要求

开发开始前，以下文档必须存在并通过验证：

- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/brainstorms/BRAINSTORM.md`
- `docs/planning/PRD.md`
- `docs/planning/EPIC.md`
- `docs/planning/STORY.md`
- `docs/validation/PRE_TEST.md`（必须包含至少一个 `CASE-*`）
- `docs/continuity/PROGRESS.md`
- `docs/continuity/RECOVERY.md`

---

## 开发工作流

1. **实现前**：
   - 运行 `./bin/bmad-check` 验证 BMAD 基线
   - 运行 `./bin/freely doctor` 验证文档门禁

2. **功能开发**：
   - 从 `develop` 创建 feature 分支
   - 在专用工作树中工作（`source ./bin/wt-enter <分支名>`）
   - 先写测试（`docs/validation/PRE_TEST.md`）
   - 实现 → 评审 → 测试

3. **集成**：
   - 合并 feature 到 `pre-develop` 进行测试
   - 验证后提升到 `develop`
   - 创建 release 分支用于 `main`

4. **恢复**：
   - 检查 `docs/continuity/RECOVERY.md` 获取检查点
   - 从最后已知状态恢复

---

## 环境变量

复制 `.env.example` 到 `.env` 并配置：

```bash
AI_TOOL=codex          # codex | kiro-cli | iflow
AI_MODEL=gpt-5-codex   # 模型标识
AI_MODE=auto           # auto | step
```