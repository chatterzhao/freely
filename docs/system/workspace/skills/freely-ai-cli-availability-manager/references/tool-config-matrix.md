# AI CLI 工具配置矩阵

本文档记录各 AI CLI 工具的多账号支持方式和配置切换方法。

> **用户配置模板**：`templates/ai-auth/` 提供了 Claude Code、Codex、OpenCode
> 三种工具的 slot 配置 `.example` 模板，含完整注释。新用户按
> `templates/ai-auth/README.md` 操作即可在 10 分钟内建好第一个可用 slot。
>
> ★ **命名约定**：slot 目录名 = `.zshrc` alias 名 = `config.toml` `AI_TOOL` 值，
> 三者必须一致。格式：`{tool}-{type}-{name}`，Freely 靠 `-apikey-` / `-account-`
> 前缀识别工具族。

## 支持情况汇总

| 工具 | 配置目录切换 | 环境变量 | 推荐方案 |
|------|-------------|----------|----------|
| codex | ✅ 支持 | `CODEX_HOME` | 环境变量切换 |
| iflow | ⚠️ 部分支持 | `IFLOW_*` 配置项 | 环境变量覆盖配置 |
| kiro | 待确认 | 待确认 | 待调研 |

## codex

### 配置目录
- 默认：`~/.codex/`
- 凭证文件：`auth.json`
- 配置文件：`config.toml`

### 多账号支持

**环境变量方式（推荐）**：
```bash
# 切换到个人账号
export CODEX_HOME="$HOME/.codex-personal"
codex "hello"

# 切换到工作账号
export CODEX_HOME="$HOME/.codex-work"
codex "hello"
```

**配置文件结构**：
```
~/.codex-personal/
├── auth.json        # 个人账号凭证
├── config.toml      # 个人配置
└── AGENTS.md        # 个人指令

~/.codex-work/
├── auth.json        # 工作账号凭证
├── config.toml      # 工作配置
└── AGENTS.md        # 工作指令
```

**Profile 方式（替代方案）**：
```bash
# 在 config.toml 中定义多个 profile
codex --profile work
```

### 限流检测模式
```regex
5-hour.*limit|weekly.*limit|rate limit|429|token.*limit|concurrent|subscription expired
```

## iflow

### 配置目录
- 默认：`~/.iflow/`
- 凭证文件：`oauth_creds.json`, `iflow_accounts.json`
- 配置文件：`settings.json`

### 多账号支持

**环境变量覆盖方式**：
```bash
# 使用不同的 API key
export IFLOW_apiKey="sk-xxxxx"
export IFLOW_baseUrl="https://apis.iflow.cn/v1"
iflow
```

**注意**：iflow 没有明确的配置目录切换环境变量（如 `IFLOW_HOME`），但支持：
1. `IFLOW_*` 环境变量覆盖 `settings.json` 中的配置项
2. 项目级配置文件 `.iflow/settings.json`
3. `IFLOW_CLI_SYSTEM_SETTINGS_PATH` 指定系统级配置路径

**推荐方案**：
```bash
# 方案1：通过环境变量切换账号（不切换目录）
export IFLOW_apiKey="sk-account1-key"
export IFLOW_baseUrl="https://apis.iflow.cn/v1"
iflow

# 方案2：使用多个配置目录 + 软链接
# 准备多个配置目录
~/.iflow-personal/
~/.iflow-work/

# 切换时替换软链接
ln -sfn ~/.iflow-personal ~/.iflow
iflow
```

### 限流检测模式
```regex
rate limit|429|quota exceeded|limit reached|too many requests
```

## kiro-cli

### 状态
未安装，待调研。

### 预期支持
根据公开信息，kiro-cli 可能支持 `KIRO_CONFIG_DIR` 环境变量。

## 实现建议

### 优先级策略

1. **优先使用环境变量切换目录**（codex）
   - 安全：不复制凭证
   - 简单：一个环境变量完成切换

2. **次选环境变量覆盖配置**（iflow）
   - 灵活：可覆盖任意配置项
   - 局限：无法切换所有状态（如历史记录）

3. **兜底方案：软链接或配置目录复制**
   - 复杂：需要额外的同步逻辑
   - 最后手段

### Freely 集成方式

```yaml
# ~/.config/freely/ai-cli-profiles.yaml
profiles:
  codex:
    personal:
      env: { CODEX_HOME: ~/.codex-personal }
    work:
      env: { CODEX_HOME: ~/.codex-work }
  
  iflow:
    personal:
      env: { IFLOW_apiKey: sk-xxxxx }
    work:
      env: { IFLOW_apiKey: sk-yyyyy }
```

Freely 在启动 AI CLI 时：
1. 读取当前活跃 profile
2. 注入对应环境变量
3. 启动 AI CLI 进程
