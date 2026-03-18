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
freely ai-cli switch codex work --yes

# 输出结构化数据
freely ai-cli list --format json
freely ai-cli status --format yaml

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
freely ai-cli switch codex work

# 输出：
# 当前 profile: personal
# 切换到: work
# 确认? [y/N] y
# 已切换到 work

# 选择菜单
freely ai-cli switch
# > personal
#   work
#   backup
```

## CLI 调用者类型

| 调用者 | 模式 | 输出格式 |
|--------|------|----------|
| AI Agent (codex/iflow) | 非交互式 | JSON |
| 脚本/CI | 非交互式 | JSON/YAML |
| 人类用户 | 交互式 | 文本表格 |

## AI Agent 调用约定

```bash
# AI Agent 调用示例（非交互式）
freely ai-cli status --format json --yes

# 输出
{
  "tool": "codex",
  "active_profile": "personal",
  "profiles": ["personal", "work", "backup"],
  "last_switch": "2026-03-18T10:30:00Z"
}

# 返回码
echo $?
# 0 = 成功
```

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

# 保存当前登录
freely ai-cli save <tool> <profile> [--yes]

# 切换 profile
freely ai-cli switch <tool> [<profile>] [--yes]
# profile 省略时显示选择菜单

# 列出 profiles
freely ai-cli list [--format json|yaml|text]

# 状态
freely ai-cli status [--format json|yaml|text]

# 删除
freely ai-cli delete <tool> <profile> [--yes]

# 自动切换（限流触发）
freely ai-cli auto-switch <tool> [--format json]
```

## 输出格式示例

### text（默认）

```
Tool: codex
Active: personal
Profiles:
  * personal (个人账号)
    work (工作账号)
    backup (备用账号)
```

### json

```json
{
  "tool": "codex",
  "active": "personal",
  "profiles": [
    {"name": "personal", "description": "个人账号", "active": true},
    {"name": "work", "description": "工作账号", "active": false},
    {"name": "backup", "description": "备用账号", "active": false}
  ]
}
```

### yaml

```yaml
tool: codex
active: personal
profiles:
  - name: personal
    description: 个人账号
    active: true
  - name: work
    description: 工作账号
    active: false
```

## AI Agent 集成示例

```bash
# codex 检测到限流后调用
if echo "$output" | grep -qE "5-hour.*limit|rate.?limit"; then
  # 非交互式切换
  freely ai-cli auto-switch codex --format json --yes
  
  # 读取返回的 profile 信息
  # {"switched": true, "profile": "work", "method": "copy_auth"}
fi
```

## 错误处理

```bash
# 非交互式：返回码 + JSON 错误
freely ai-cli switch codex nonexistent --yes --format json
# {"error": "profile_not_found", "message": "Profile 'nonexistent' does not exist"}
# exit code: 4

# 交互式：提示用户
freely ai-cli switch codex nonexistent
# 错误: Profile 'nonexistent' 不存在
# 可用 profiles: personal, work, backup
```
