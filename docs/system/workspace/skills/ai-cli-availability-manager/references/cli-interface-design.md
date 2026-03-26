# CLI 接口设计原则

## 核心原则：CLI First

**所有功能必须优先提供 CLI 接口，UI 只是可选的展示层。**

```
CLI (核心) → API (可选) → UI (可选)
```

## 交互模式

### 非交互式（默认）

适合脚本、CI/CD、AI Agent 调用：

```bash
# 直接执行，无确认提示
freely ai-cli switch codex work@company.com-1 --yes

# 输出结构化数据
freely ai-cli list --format json
freely ai-cli whoami --format json

# 返回码
# 0 = 成功
# 1 = 一般错误
# 2 = 参数错误
# 3 = 认证错误
# 4 = 未找到
```

### 交互式

适合人工操作：

```bash
# 有确认提示
freely ai-cli switch codex work@company.com

# 输出：
# 当前 slot: personal@outlook-com-1
# 切换到: work@company.com-1
# 确认? [y/N] y
# 已切换到 work@company.com

# 选择菜单
freely ai-cli switch codex
# > personal@outlook-com-1
#   work@company.com-1
#   backup@gmail.com-2
```

## CLI 调用者类型

| 调用者 | 模式 | 输出格式 |
|--------|------|----------|
| AI Agent (codex/iflow) | 非交互式 | JSON |
| 脚本/CI | 非交互式 | JSON/YAML |
| 人类用户 | 交互式 | 文本表格 |

## 命令设计

### 全局选项

```bash
freely ai-cli <command> [options]

选项:
  --yes, -y        跳过确认（非交互式）
  --format FORMAT  输出格式: text|json|yaml
  --quiet, -q      静默模式，仅输出错误
  --dry-run        模拟执行，不实际修改
```

### 命令列表

```bash
# 初始化
freely ai-cli init [--yes]

# 显示当前 slot
freely ai-cli whoami [tool]

# 保存当前登录（自动检测 auth email 并生成 slot）
freely ai-cli save codex [--yes]

# 切换 slot
freely ai-cli switch codex [slot] [--yes]
# slot 省略时自动 probe 并只切到当前真实可用的 slot

# 列出 slot
freely ai-cli list [--format json|yaml|text]

# 状态
freely ai-cli status [--format json|yaml|text]

# 删除
freely ai-cli delete codex <account> [--yes]
```

## Slot 与 auth 元数据

`.ai-auth/<slot>` 是唯一身份；`save` 和 `whoami` 会从 auth.json 提取 `auth_email` 作为元数据：

```bash
# codex: 从 JWT id_token 提取 email
freely ai-cli save codex
# Detected auth email: worahe3973@outlook.com
# Saved to: ~/.ai-auth/codex-worahe3973@outlook-com-1/

# iflow: 从环境变量读取（需配置）
freely ai-cli save iflow
# iflow uses environment variables. Set IFLOW_*_KEY in your shell config.
```

## 输出格式示例

### text（默认）

```
Tool: codex
Auth: present
Slot: worahe3973@outlook-com-1
Auth email: worahe3973@outlook.com
Last modified: Mar 16 15:50:34 2026
```

### json

```json
{
  "tool": "codex",
  "auth": "present",
  "slot": "worahe3973@outlook-com-1",
  "auth_email": "worahe3973@outlook.com",
  "account": "worahe3973@outlook.com",
  "last_modified": "Mar 16 15:50:34 2026"
}
```

## 目录结构

```
~/.ai-auth/
├── codex-personal@outlook-com-1/auth.json
├── codex-work@company-com-1/auth.json
└── codex-backup@gmail-com-2/auth.json
```

## AI Agent 集成示例

```bash
# 检测当前 slot
SLOT=$(freely ai-cli whoami --format json --quiet | jq -r '.slot')

# 检测到限流后切换
if echo "$output" | grep -qE "5-hour.*limit|rate.?limit"; then
  freely ai-cli switch codex --yes --format json
fi
```
