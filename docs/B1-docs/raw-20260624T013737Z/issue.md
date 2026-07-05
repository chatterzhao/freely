---
local_id: raw-20260624T013737Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T013737Z-A
platform_ids:
  github:
    issue_id: '3399'
    url: https://github.com/chatterzhao/freely/issues/3399
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T01:37:56Z'
updated_at: '2026-06-24T04:35:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标

**新增一个行业常见的 AI CLI tool（如 gemini-cli、qwen-cli、cline），只需编辑一个 TOML 配置文件，不用改任何源码。**

## 核心设计：Registry 作为翻译层

每种 AI CLI tool 有不同的"方言" — 同一个概念叫不同的字段名。Registry 把 Freely 的抽象概念翻译成各工具的土话：

```
Freely 抽象概念: "自动批准权限"
       │
       ▼ registry 翻译
Claude:   settings.json → permissionMode
Codex:    config.toml   → approval_policy  
OpenCode: settings.json → permission
Gemini:   settings.json → autoMode           ← 新工具，加一行 TOML 即可
```

工具没声明的概念 → 代码走 `else` 行业标配（比如没声明 `sandbox_mode` = 这个工具不用 config 管沙箱）。

## 文件格式：TOML（替换 JSON5）

**理由**：Freely 用户已熟悉 TOML（`config.toml`、`.codex/config.toml`），Python 3.11+ 内置 `tomllib`，无需额外依赖。

## 文件位置与合并优先级

```
~/.freely/tool-registry.toml        ← 用户自定义（优先）
<freely-install>/tool-registry.toml  ← 系统内置（兜底，随 git 发布）
```

查找逻辑：
1. 先查 `~/.freely/tool-registry.toml`（用户自己加的工具）
2. 再查安装目录的 `tool-registry.toml`（内置 claude/codex/opencode）
3. 合并时同名 tool key 用户覆盖系统

用户加新工具就是 `vim ~/.freely/tool-registry.toml`，不需要碰 Freely 源码。

## 完整 Registry Schema（TOML 格式）

```toml
# =============================================================================
# Freely Tool Capability Registry
# =============================================================================
# 每个 [tool] section 定义一个 AI CLI tool 的完整能力描述。
# 用户可在此文件或 ~/.freely/tool-registry.toml 中新增工具。
# 新增工具后，在 config.toml 设 AI_TOOL = "工具名-apikey-槽名" 即可使用。
# =============================================================================

# ── Claude Code ────────────────────────────────────────────────────────────

[claude]
display_name = "Claude Code"
binary_resolution = "path"          # "path" = 从 PATH 找, "cache" = 从缓存下载
aliases = ["cc", "cc-use-codex-cli", "kiro-cli", "iflow", "claude-code"]
fallback_priority = 40              # 多工具回退时的排序（越低越优先）
test_command = "claude -p 'say hi' --output-format text --dangerously-skip-permissions --bare --system-prompt '' --max-tokens 50"

[claude.acp]
binary = "claude-agent-acp"
args = []
bridge_socket_suffix = "acp"

[claude.permission]
# 如何从 slot config 读取权限，以及如何应用到 ACP session
mechanism = "session_set_mode"      # 通过 ACP session/set_mode RPC 设置
config_field = "permissionMode"     # 权限值在 slot config 中的字段名
fallback_field = "permissions.defaultMode"

[claude.slot]
# 如何找到 slot 配置目录/文件
discovery = "alias_cli_arg"         # 通过 shell alias 的 CLI flag 传入
alias_key = "--settings"            # 例: alias 中含 --settings ~/.ai-auth/.../settings.json
config_file = "settings.json"       # slot 目录下的配置文件名
is_dir = false                      # false = config_file 是文件, true = 整个目录
bridge_config_env = ""              # 传给 ACP 子进程的 env var 名（空 = 用 CLI arg）
post_init = ""                      # 初始化后钩子

[claude.config_schema]
# 工具原生配置文件的格式和字段映射
file_format = "json"                # json | toml
file_name = "settings.json"

[claude.config_schema.fields]
# 每个字段 = Freely 抽象概念 → 工具原生字段名的映射
# 未声明的概念 → 代码走 else 分支行业标配
permission_bypass = { path = "permissionMode", fallback_path = "permissions.defaultMode" }
model = { path = "model" }
api_base_url = { path = "env.ANTHROPIC_BASE_URL" }
# sandbox_mode — 未声明（Claude 用 --add-dir CLI flag，不走 config）
# writable_roots — 未声明（Claude 不需要）

[claude.session]
supports_fork = true
supports_resume = true
id_format = "uuid"                  # uuid | ses_xxx | freeform
directory_template = "${HOME}/.claude/projects/{slug}"
extract_regex = 'session[._]id[=:]\s*([a-f0-9-]{36})'

[claude.session.cli]
fresh = ["--session-id", "{id}"]
resume = ["--resume", "{target}"]
fork = ["--resume", "{parent}", "--fork-session", "--session-id", "{child}"]

[claude.adapters]
supported = ["direct", "acp"]
default = "acp"

[claude.adapters.launch_kinds]
acp = "fresh,resume,fork,fresh_with_handoff,prompt"
direct = "fresh,resume,fresh_with_handoff"

[claude.launch.direct]
binary = "claude"
args = ["-p"]
resume_flag = "--resume"
session_flag = "--session-id"
model_flag = "--model"
reasoning_flag = "--effort"
add_dir_boundary = true
add_dir_flag = "--add-dir"

[claude.launch.acp]
model_flag = "--model"
session_flag = "--session-id"
resume_flag = "--resume"

[claude.error_patterns]
auth_failure = [
    "401|402|403",
    "unauthorized",
    "invalid.?token|token.?expired",
    "authentication.?failed",
    "login required"
]
quota_exhausted = [
    "insufficient_quota|quota exceeded",
    "insufficient balance|insufficient credit",
    "payment required"
]
rate_limited = ["429 too many requests", "rate limit"]

[claude.auto_recovery]
command_name = "claude"
supports_same_tool_slot = true
supports_proxy_self_heal = false
requires_project_config = false

[claude.auto_recovery.failure_scope]
primary_rate_limit_exhausted = "slot_local"
auth_failure = "slot_local"
network_failure = "slot_local"

[claude.boundary]
project_config_surface = "none materialized by Freely yet"
launch_note = "adds `--add-dir {worktrees_root}`"
sync_note = "copy `.freely/config.toml`, then rematerialize wrapper in each new worktree"

[claude.process_match]
fragments = ["claude"]
fallback_token = "claude"
requires_project_owned_fallback = false

[claude.skill]
dir = "${HOME}/.claude/skills"

# ── Codex CLI ──────────────────────────────────────────────────────────────

[codex]
display_name = "Codex CLI"
binary_resolution = "cache"
aliases = []
fallback_priority = 10
test_command = "codex exec 'say hi' --max-tokens 50"

[codex.acp]
binary = "codex-acp"
args = []
auto_download = true
download_version = "0.15.0"
download_repo = "zed-industries/codex-acp"
bridge_socket_suffix = "acp"

[codex.permission]
mechanism = "slot_config_toml"      # Codex 直接从 slot 的 config.toml 读取权限字段
config_fields = ["approval_policy", "sandbox_mode"]

[codex.slot]
discovery = "alias_env_var"
alias_key = "CODEX_HOME"
config_file = ""
is_dir = true
bridge_config_env = "CODEX_HOME"
post_init = "ensure_writable_roots"

[codex.config_schema]
file_format = "toml"
file_name = "config.toml"

[codex.config_schema.fields]
permission_bypass = { path = "approval_policy" }
model = { path = "model" }
sandbox_mode = { path = "sandbox_mode" }
writable_roots = { path = "sandbox.writable_roots" }
api_base_url = { path = "openai_base_url" }

[codex.session]
supports_fork = true
supports_resume = true
id_format = "uuid"
directory_template = "${CODEX_HOME:-$HOME/.codex}/sessions"
extract_regex = '^session id: ([a-f0-9-]+)'

[codex.session.cli]
fresh = ["exec"]
resume = ["exec", "resume", "{target}"]
fork = ["exec", "resume", "{parent}"]

[codex.adapters]
supported = ["direct", "acp"]
default = "acp"

[codex.adapters.launch_kinds]
acp = "fresh,resume,fork,fresh_with_handoff,prompt"
direct = "fresh,resume,fresh_with_handoff"

[codex.launch.direct]
binary = "codex"
args = ["exec", "--skip-git-repo-check", "-C", "{project}"]
model_flag = "-m"
reasoning_flag = "-c"
add_dir_boundary = true
add_dir_flag = "--add-dir"

[codex.launch.acp]
model_flag = "--model"
session_flag = "--session-id"
resume_flag = "--resume"

[codex.error_patterns]
auth_failure = [
    "401|402 payment required|403 forbidden",
    "auth error: 402",
    "unauthorized|invalid.?token",
    "deactivated_workspace|workspace deactivated"
]
quota_exhausted = [
    "429 too many requests|exceeded retry limit",
    "subscription.?expired|usage limit",
    "预扣费额度失败|剩余额度不足|余额不足|insufficient balance|quota exceeded"
]
rate_limited = ["429 too many requests", "try again"]

[codex.auto_recovery]
command_name = "codex"
supports_same_tool_slot = true
supports_proxy_self_heal = true
requires_project_config = true      # 需要项目 .codex/config.toml

[codex.auto_recovery.failure_scope]
primary_rate_limit_exhausted = "slot_local"
auth_failure = "slot_local"
network_failure = "slot_local"

[codex.boundary]
project_config_surface = ".codex/config.toml"
launch_note = "adds `--add-dir {worktrees_root}`"
sync_note = "copy `.freely/config.toml`, then rematerialize `.codex/config.toml` and wrapper in each new worktree"

[codex.process_match]
fragments = ["codex exec", ".bun/bin/codex", "/codex/codex"]
fallback_token = "codex"
requires_project_owned_fallback = true

[codex.skill]
dir = "${HOME}/.codex/skills"

# ── OpenCode ───────────────────────────────────────────────────────────────

[opencode]
display_name = "OpenCode CLI"
binary_resolution = "path"
aliases = []
fallback_priority = 50
test_command = "opencode run 'say hi' --pure"

[opencode.acp]
binary = "opencode"
args = ["acp"]
bridge_socket_suffix = "opencode"

[opencode.permission]
mechanism = "env_var"
config_field = "permission"
env_var = "OPENCODE_CONFIG"

[opencode.slot]
discovery = "alias_env_var"
alias_key = "OPENCODE_CONFIG"
config_file = "settings.json"
is_dir = false
bridge_config_env = "OPENCODE_CONFIG"
post_init = ""

[opencode.config_schema]
file_format = "json"
file_name = "settings.json"

[opencode.config_schema.fields]
permission_bypass = { path = "permission" }
model = { path = "model" }
reasoning_effort = { path = "reasoning_effort" }
# sandbox_mode — 未声明（走标配：无）

[opencode.session]
supports_fork = true
supports_resume = true
id_format = "ses_xxx"
directory_template = "${HOME}/.opencode/sessions"
extract_regex = 'service=session id=(ses_[A-Za-z0-9_]*)'

[opencode.session.cli]
fresh = ["--session", "{id}"]
resume = ["--session", "{target}", "--continue"]
fork = ["--session", "{parent}", "--fork"]

[opencode.adapters]
supported = ["direct", "acp"]
default = "acp"

[opencode.adapters.launch_kinds]
acp = "fresh,resume,fork,fresh_with_handoff,prompt"
direct = "fresh,resume,fresh_with_handoff"

[opencode.launch.direct]
binary = "opencode"
args = ["run", "--print-logs", "--dir", "{project}"]
session_flag = "-s"
resume_flag = "-s"
add_dir_boundary = false

[opencode.launch.acp]
model_flag = "--model"
session_flag = "--session-id"
resume_flag = "--resume"

[opencode.error_patterns]
auth_failure = []
quota_exhausted = []
rate_limited = []

[opencode.auto_recovery]
command_name = "opencode"
supports_same_tool_slot = true
supports_proxy_self_heal = false
requires_project_config = false

[opencode.auto_recovery.failure_scope]
auth_failure = "slot_local"
network_failure = "network_local"

[opencode.boundary]
project_config_surface = "none materialized by Freely yet"
launch_note = "passthrough wrapper only"
sync_note = "copy `.freely/config.toml`, then rematerialize wrapper in each new worktree"

[opencode.process_match]
fragments = ["opencode"]
fallback_token = "opencode"
requires_project_owned_fallback = false

[opencode.skill]
dir = "${HOME}/.config/opencode/skills"
```

## AI_TOOL → Registry 查找流程

```
config.toml: AI_TOOL = "opencode-apikey-ds-flash-auto"
       │
       ▼
_resolve_tool_family()  → 去除 "-apikey-ds-flash-auto" → "opencode"
       │
       ▼ 查 ~/.freely/tool-registry.toml（优先）→ 未命中
       │ 查 <freely>/tool-registry.toml（兜底）  → 命中 [opencode]
       ▼
_tool_registry_get "opencode" "permission.config_field"        → "permission"
_tool_registry_get "opencode" "config_schema.fields.permission_bypass.path" → "permission"
_tool_registry_get "opencode" "session.cli.fresh"              → ["--session", "{id}"]
_tool_registry_get "opencode" "skill.dir"                      → "${HOME}/.config/opencode/skills"
_tool_registry_get "opencode" "launch.direct.binary"           → "opencode"
_tool_registry_get "opencode" "config_schema.fields.sandbox_mode" → "" (未声明 → 标配)
       │
       ▼
构建启动命令、部署 skill、读取/写入 slot config — 全部由 registry 驱动
```

未注册 tool → 明确报错：
> Tool 'xxx' not found in tool-registry.toml. Add it to ~/.freely/tool-registry.toml

## 加新工具示例：Gemini CLI

```toml
# ~/.freely/tool-registry.toml
[gemini]
display_name = "Gemini CLI"
binary_resolution = "path"
fallback_priority = 60
test_command = "gemini -p 'say hi' --max-tokens 50"

[gemini.acp]
binary = "gemini-agent-acp"

[gemini.permission]
mechanism = "env_var"
config_field = "autoMode"

[gemini.slot]
discovery = "alias_env_var"
alias_key = "GEMINI_CONFIG"
config_file = "settings.json"
is_dir = false
bridge_config_env = "GEMINI_CONFIG"

[gemini.config_schema]
file_format = "json"
file_name = "settings.json"

[gemini.config_schema.fields]
permission_bypass = { path = "autoMode" }
model = { path = "model" }
# sandbox_mode — 未声明，走标配

[gemini.session]
supports_fork = true
supports_resume = true
id_format = "uuid"
directory_template = "${HOME}/.gemini/sessions"
extract_regex = 'session[._]id[=:]\s*([a-f0-9-]+)'

[gemini.session.cli]
fresh = ["--session-id", "{id}"]
resume = ["--resume", "{target}"]

[gemini.adapters]
supported = ["direct", "acp"]
default = "acp"

[gemini.launch.direct]
binary = "gemini"
args = ["-p"]
add_dir_boundary = false

[gemini.error_patterns]
auth_failure = ["401|unauthorized"]
rate_limited = ["429"]

[gemini.auto_recovery]
command_name = "gemini"

[gemini.skill]
dir = "${HOME}/.gemini/skills"
```

然后在 `config.toml` 里设 `AI_TOOL = "gemini-apikey-mykey"`，立即可用。**零代码改动。**

## 职责边界

| 层 | 文件 | 内容 | 性质 |
|----|------|------|------|
| **Registry** | `tool-registry.toml` | 工具的接口/机制/字段映射 — 所有人一样 | tool-type metadata |
| **Slot Config** | `~/.ai-auth/{slot}/settings.json` 等 | 实际 API Key、model、permission 值 — 每个用户不同 | instance values |
| **项目配置** | `.freely/config.toml` | 项目用哪个 tool+slot、fallback 顺序 | user choice |

Registry 只描述"这个工具用什么字段名、什么机制"，不存储实际的 API Key 或 model 值。这些敏感/个性化数据留在 slot config 里。

## 实施阶段

### Phase 1: JSON5 → TOML 格式迁移 + 文件优先级（P0）
- `tool-registry.json5` → `tool-registry.toml`，完整 schema
- 实现 `~/.freely/tool-registry.toml`（用户优先）+ `<freely>/tool-registry.toml`（系统兜底）
- `tool-registry-query.py` 适配 TOML + 合并逻辑

### Phase 2: `config_schema` 驱动 slot config 读写（P0）
- 重构 `monitor-ai-acp.sh` — 用 `config_schema.fields.permission_bypass` 替代硬编码 `permissionMode`/`approval_policy`
- 重构 `freely:_bridge_env_for_registered_tool` — 用 `config_schema.file_format` 选 parser，`config_schema.fields.*` 替代字段名硬编码
- 重构 `tool-launchers.sh:_apply_tool_alias_settings` — 同上

### Phase 3: `session` 字段消除硬编码（P1）
- `session-cache.sh` 全部 7 个 case → `session.cli.*` + `session.directory_template` + `session.extract_regex`

### Phase 4: `launch` + `adapters` 字段消除硬编码（P1）
- `tool-launchers.sh` 启动语法 6 个 case → `launch.direct.*` + `launch.acp.*`

### Phase 5: 其余字段（P2）
- `error_patterns` → `monitor-ai-cli.sh` 错误检测
- `auto_recovery` → `freely` 恢复链
- `process_match` → `freely` 进程发现
- `skill.dir` → `deploy-skills`
- `boundary`、`fallback_priority` 等

## 验收标准

1. **加新工具不改代码**：在 `~/.freely/tool-registry.toml` 加一个 `[newtool]` section，配好 `config_schema.fields`、`session.cli`、`launch`，然后 `AI_TOOL = "newtool-apikey-test"` 即可启动
2. **字段未声明走标配**：新工具不声明 `sandbox_mode` → 代码自动走沙箱无关路径
3. **用户自定义优先**：`~/.freely/tool-registry.toml` 的同名 tool 覆盖系统内置
4. **向后兼容**：现有 claude/codex/opencode 三工具行为不变

