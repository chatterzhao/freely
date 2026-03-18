# 研究：AI CLI 可用性管理 Skill

## Context

- 日期：2026-03-18
- 触发：Freely 作为自主循环运行器，依赖 AI CLI 工具（codex、kiro-cli、iflow）持续运行。当工具遇到限流、凭证过期或服务中断时，整个自治循环会崩溃。需要设计一个 skill 来管理 AI CLI 的可用性。
- 核心判断：这是 Freely 的核心治理能力，必须作为 skill 实现，与 Freely 的恢复机制、状态追踪紧密集成。
- 自举约束：Freely 自身开发时也会遇到账号切换需求，必须先在自己身上验证。

## 问题域

### 1. Freely 面临的可用性挑战

| 场景 | 后果 | 频率 |
|------|------|------|
| AI CLI 限流（429/quota exceeded） | 循环中断，无人值守时彻底停止 | 高 |
| 多账号切换 | 手动操作繁琐，无法自动化 | 中 |
| 凭证过期 | 静默失败，难以定位原因 | 低 |
| 多项目并发 | 同一账号被多个实例占用，触发限流 | 中 |

### 2. 设计目标

1. **无缝续接**：限流时自动切换账号，循环不中断
2. **安全凭证**：凭证存储必须加密，不能明文落地
3. **状态可追溯**：每次切换、限流事件都有记录
4. **治理集成**：作为 skill 受 constitution-guard 和 laws-enforcer 约束
5. **工具无关**：支持 codex、kiro-cli、iflow 等多种 AI CLI

## 技术方案

### 核心思路：最小信任原则

Freely 不应该"拥有"或"复制"凭证。相反，Freely 应该：
1. 利用 AI CLI 工具原生的多账号能力
2. 通过环境变量注入配置路径
3. 只负责编排和监控，不触碰敏感数据

### 方案架构

```
┌─────────────────────────────────────────────────────┐
│                    Freely Core                       │
├─────────────────────────────────────────────────────┤
│  skill:ai-cli-availability-manager                  │
│  ├── 配置发现：检测工具支持的多账号模式              │
│  ├── 环境注入：启动 AI CLI 时设置 CONFIG_DIR        │
│  ├── 输出监控：解析限流信号                         │
│  ├── 账号切换：切换到下一个可用 profile             │
│  └── 事件记录：写入 recovery/progress               │
├─────────────────────────────────────────────────────┤
│              AI CLI 工具层                           │
│  codex    kiro-cli    iflow    ...                  │
│  各自管理自己的凭证，Freely 不介入                   │
└─────────────────────────────────────────────────────┘
```

### 工具配置模式矩阵

| 工具 | 多账号模式 | 环境变量 | 配置目录 |
|------|-----------|----------|----------|
| codex | 环境变量 | `CODEX_CONFIG_DIR` | `~/.codex/` |
| kiro-cli | 环境变量 | `KIRO_CONFIG_DIR` | `~/.config/kiro/` |
| iflow | 待确认 | `IFLOW_CONFIG_DIR`? | `~/.config/iflow/` |

**关键洞察**：大多数现代 CLI 工具都支持通过环境变量指定配置目录。这是实现多账号切换的最安全方式——Freely 只需要知道"用哪个目录"，不需要知道"目录里有什么"。

### Skill 职责边界

**负责**：
1. 维护 `{tool}_CONFIG_DIR` -> `profile_path` 映射
2. 在 `auto-loop-orchestrator` 启动 AI CLI 前注入环境变量
3. 监控 AI CLI 输出，检测限流模式
4. 触发切换时，选择下一个可用 profile
5. 将事件写入 recovery/progress

**不负责**：
1. 存储或复制凭证文件
2. 解析 token 或用户身份
3. 自动登录或刷新凭证

### 限流检测

```bash
LIMIT_PATTERNS=(
    "rate limit"
    "429"
    "quota exceeded"
    "too many requests"
    "limit reached"
    "token.*limit"
)
```

检测到限流后的流程：
1. 记录当前 profile 不可用（写入 recovery）
2. 从可用 profile 列表中选择下一个
3. 设置新的 `{TOOL}_CONFIG_DIR`
4. 重启 AI CLI 会话
5. 继续循环

补充结论（2026-03-18）：
- Codex 的限额不能只按单一“5小时窗口”理解；实际运行里至少存在两档结构化限额：
  - `primary`：短窗口限额（当前日志里常见 `window_minutes=300`）
  - `secondary`：长窗口限额（当前日志里可见 `window_minutes=10080`）
- Freely runtime 不能只在 `primary.used_percent >= 100` 时切账号；若 `secondary.used_percent >= 100`，也必须进入同一条 account-aware 恢复链。
- 恢复留痕至少应写出：
  - 哪一档限额触发（`primary_rate_limit_exhausted | secondary_rate_limit_exhausted`）
  - 对应的 `reset_at`
  - 当前切到的 account
- 验证口径不能只看“切账号命令被调用”，还要确认 `session-state/status` 已写回最新 account 与限额元数据。

### 与现有 Skill 的集成

```
constitution-guard ──┬──> 预检：AI CLI 工具是否支持环境变量模式
                     └──> 预检：profile 配置是否完整
                     
laws-enforcer ───────┬──> 验证：切换事件是否记录
                     └──> 验证：recovery 状态是否一致
                     
auto-loop-orchestrator ──> 调用：启动前注入 CONFIG_DIR
                           
recovery-subagent-governance ──> 协作：限流后触发恢复流程
```

### 目录结构

```
docs/system/workspace/skills/ai-cli-availability-manager/
├── SKILL.md                    # skill 定义
└── references/
    ├── tool-config-matrix.md   # 各工具的配置模式
    ├── limit-patterns.md       # 限流检测模式
    └── profile-management.md   # profile 管理规范
```

## 安全策略

### 凭证安全三原则

1. **不触碰**：Freely 不读取、不复制、不存储凭证文件
2. **不传输**：日志和事件记录中不包含 token 或凭证片段
3. **不信任**：所有敏感操作由 AI CLI 工具自己完成，Freely 只做路径编排

### Profile 存储位置

Profile 目录由用户自己管理，Freely 只需知道路径：

```
# 用户自行准备的多个 profile
~/.codex-personal/   # 个人账号
~/.codex-work/       # 工作账号
~/.codex-backup/     # 备用账号
```

Freely 的配置只需要：
```yaml
ai_cli_profiles:
  codex:
    profiles:
      - name: personal
        config_dir: ~/.codex-personal
      - name: work
        config_dir: ~/.codex-work
    active: personal
```

## 待收敛问题

1. **自动切换 vs 通知用户**：限流后是否静默切换，还是通知用户确认？
2. **profile 耗尽**：所有 profile 都不可用时如何处理？
3. **多项目并发**：如何避免多个 Freely 实例抢占同一 profile？
4. **使用统计**：是否需要记录每个 profile 的使用时长，用于负载均衡？

## 下一步

- [ ] 确认 codex、kiro-cli、iflow 的环境变量支持情况
- [ ] 设计 profile 配置格式
- [ ] 实现 SKILL.md 和 references

---

## 迭代讨论（2026-03-18 续）

### CLI First 原则

讨论发现所有功能应优先 CLI 接口，UI 只是展示层。

架构优先级：
```
CLI (核心) → API (可选) → UI (可选)
```

边界原则：
1. 所有功能必须有 CLI 接口
2. CLI 必须支持非交互式模式（`--yes`）
3. CLI 必须支持结构化输出（`--format json|yaml`）
4. CLI 返回码必须语义化

已写入 `docs/CONSTITUTION.md` 第 10.1 章。

### 登录命令设计

用户反馈：手工操作繁琐
```bash
# 之前
codex login
freely ai-cli save codex personal
```

改进为统一入口：
```bash
freely ai login codex
# 自动：登录 -> 提取账号 -> 保存授权
```

### 账号自动检测

从 `auth.json` 的 JWT `id_token` 中提取 email：
- 无需用户指定账号名
- 目录命名：`codex-{email}`
- 只替换 `.` 为 `-`，保留 `@`（macOS/Linux 支持）

### 命令简化

`freely ai-cli` → `freely ai`

理由：更简洁，与 Freely 品牌一致。
