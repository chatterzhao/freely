# 进程生命周期与会话恢复

本文档分析限流切换账号时的进程管理和会话恢复策略。

## 核心问题

**已运行的 AI CLI 进程无法动态切换账号。**

环境变量（如 `CODEX_HOME`、`IFLOW_apiKey`）在进程启动时读取，运行中修改不会生效。

## 解决方案

### 方案对比

| 方案 | 实现复杂度 | 会话连续性 | 适用场景 |
|------|-----------|-----------|----------|
| 重启进程 + resume | 中 | 部分保留 | 有会话恢复能力的工具 |
| 重启进程 + 新会话 | 低 | 无 | 无会话恢复或会话不可用 |
| 动态切换（不支持） | N/A | N/A | 当前工具不支持 |

### 推荐策略

**统一策略**：Kill 当前进程 → 用新账号启动新进程 → 尝试恢复会话

```bash
# 伪代码
on_rate_limit() {
  # 1. 记录当前会话 ID
  session_id=$(get_current_session_id)
  
  # 2. 标记当前 profile 冷却
  mark_profile_cooling "$current_profile"
  
  # 3. 选择新 profile
  new_profile=$(select_next_profile)
  
  # 4. 终止当前进程
  kill_ai_cli_process "$pid"
  
  # 5. 用新账号启动，尝试恢复会话
  env=$(get_profile_env "$new_profile")
  if can_fork_session "$session_id"; then
    exec env=$env codex fork "$session_id"
  else
    exec env=$env codex  # 新会话
  fi
}
```

## 各工具实现细节

### codex

**会话存储位置**：`$CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl`

**切换账号后的问题**：
- 切换 `CODEX_HOME` 后，新目录下没有旧会话文件
- 无法直接 `resume` 旧会话

**解决策略**：

```bash
# 策略 A：保持会话目录不变（推荐）
# 将会话目录软链接到公共位置
mkdir -p ~/.codex-sessions-shared
ln -sf ~/.codex-sessions-shared ~/.codex-personal/sessions
ln -sf ~/.codex-sessions-shared ~/.codex-work/sessions
# 切换账号后会话仍然可访问

# 策略 B：使用 fork 命令
# 在切换前先复制会话到新目录
cp -r ~/.codex-personal/sessions/latest ~/.codex-work/sessions/
CODEX_HOME=~/.codex-work codex fork <session-id>

# 策略 C：放弃会话连续性
# 直接用新账号启动新会话
CODEX_HOME=~/.codex-work codex
```

**推荐配置**：
```yaml
# 在 ai-cli-profiles.yaml 中
tools:
  codex:
    profiles:
      personal:
        env:
          CODEX_HOME: ~/.codex-personal
        # 共享会话目录
        shared_sessions_dir: ~/.codex-sessions-shared
      work:
        env:
          CODEX_HOME: ~/.codex-work
        shared_sessions_dir: ~/.codex-sessions-shared
```

### iflow

**会话存储位置**：`~/.iflow/history/<project-hash>/`

**切换账号后的问题**：
- iflow 的会话存储在固定位置 `~/.iflow/`
- 切换 `IFLOW_apiKey` 等环境变量不会影响会话文件位置
- 会话文件仍然可访问

**解决策略**：

```bash
# iflow 切换账号后会话保持可用
# 直接修改环境变量启动新进程即可

# 方式 1：continue 最近会话
IFLOW_apiKey=new-key iflow -c

# 方式 2：resume 指定会话
IFLOW_apiKey=new-key iflow -r <session-id>
```

**注意**：
- iflow 使用 `IFLOW_*` 环境变量只覆盖 API 相关配置
- 会话历史、项目配置等仍使用 `~/.iflow/` 目录
- 这是 iflow 的优势：切换账号不会丢失会话

## Freely 实现建议

### 进程监控

```bash
# Freely 需要维护 AI CLI 进程状态
monitor_ai_cli_process() {
  local pid=$1
  local tool=$2
  local session_id=$3
  
  while kill -0 "$pid" 2>/dev/null; do
    # 检查输出中的限流信号
    if check_rate_limit "$output" "$tool"; then
      handle_rate_limit "$tool" "$session_id"
      break
    fi
  done
}
```

### 会话恢复优先级

```
1. 尝试 fork/continue 当前会话
2. 尝试 resume 最近会话
3. 启动全新会话
```

### 切换流程

```
检测限流
    ↓
记录当前会话 ID 和进度
    ↓
Kill 进程（SIGTERM 优雅终止）
    ↓
等待进程退出（最多 5 秒）
    ↓
超时则 SIGKILL
    ↓
选择新 profile
    ↓
注入新环境变量
    ↓
启动新进程（尝试 resume/fork）
    ↓
恢复上下文（从 recovery 文件）
```

## 风险和限制

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 会话丢失 | 中 | 将关键上下文写入 recovery 文件 |
| 切换延迟 | 低 | 进程终止通常 < 1 秒 |
| 新账号也限流 | 中 | 立即检测，继续切换或暂停 |
| 会话认证失败 | 低 | 检测 401 后重新处理 |

## 总结

| 工具 | 切换方式 | 会话连续性 | 实现复杂度 |
|------|----------|-----------|-----------|
| codex | `CODEX_HOME` 切换目录 | 需要共享会话目录 | 中 |
| iflow | `IFLOW_*` 覆盖配置 | 自动保持（优势） | 低 |
| kiro | 待确认 | 待确认 | 待评估 |

---

## 附录：账号切换实现方案对比

### 方案 A：环境变量切换目录（原方案）

```bash
CODEX_HOME=~/.codex-work codex
```

- 优点：不触碰凭证文件
- 缺点：需要处理会话目录连续性（软链接或复制会话）

### 方案 B：复制授权文件（推荐）

```bash
# 切换流程
cp ~/.codex/auth.json ~/.codex/auth.json.bak           # 备份
cp ~/.codex-profiles/work/auth.json ~/.codex/auth.json # 复制
kill $pid && codex resume --last                       # 重启
```

- 优点：
  - CODEX_HOME 不变，会话自动连续
  - 实现简单，无需预配置
  - auth.json 通常 < 5KB，复制成本低
- 缺点：
  - 需要 Freely 介入凭证文件管理（但仅复制，不读取内容）

### 推荐方案

**codex 使用方案 B（复制授权文件）**

```yaml
# ai-cli-profiles.yaml
tools:
  codex:
    method: copy_auth  # 复制授权文件方式
    profiles:
      personal:
        auth_file: ~/.codex-profiles/personal/auth.json
        config_file: ~/.codex-profiles/personal/config.toml  # 可选
      work:
        auth_file: ~/.codex-profiles/work/auth.json
```

**iflow 使用环境变量覆盖**（iflow 会话位置固定，切换 IFLOW_* 不影响）

### 安全考量

复制授权文件时：
1. 使用 `cp` 而非 `cat`，避免在进程表中暴露内容
2. 备份文件权限设置为 `600`
3. Freely 不解析 auth.json 内容
