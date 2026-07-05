---
b1_id: B1-20260630T124528Z
phase_state: completed
source_raw: raw-20260630T124528Z
source_url: https://github.com/chatterzhao/freely/issues/3657
produced_candidate: C-20260630T124528Z-A
created_at: 2026-06-30
---

# B1_IBM: freely init ACP 工具准备 + tool-registry 下载配置

## Input
- raw issue: `docs/B1-docs/raw-20260630T124528Z/issue.md`
- 平台: GitHub #3657

## Discovery — 现状调研

### 1. 当前代码全景

freely 有三个地方涉及 ACP binary：

| 位置 | 职能 | 问题 |
|------|------|------|
| `cmd_init()` L20073-20132 | 安装时预检 | 硬编码 codex vs *，不做下载，只报错退出 |
| `_ensure_acp_bridge_running()` L13969-14118 | 运行时启动 bridge | 从 registry 读了 binary/args/auto_download，但也只调 ensure-codex-acp |
| `_acp_bridge_health_check()` L13859-13879 | 健康检查 | **Shell 注入**: `sock.connect('$socket')` |

### 2. tool-registry.toml 现有 ACP 字段

```
              claude              codex              opencode            cline
              ─────               ─────              ────────            ─────
[tool]
binary_resolution  "path"              "cache"            "path"              "path"

[tool.acp]
binary        claude-agent-acp    codex-acp          opencode            cline
args          []                  []                 ["acp"]             ["--acp"]
bridge_suffix acp                 acp                opencode            cline
auto_download (无)                true               (无)                (无)
download_ver  (无)                0.15.0             (无)                (无)
download_repo (无)                zed-industries/...  (无)                (无)
```

**缺失字段**: 除 codex 外都没有 download_url、install_method。

### 3. config.toml 当前无 ACP binary 路径存储

`_ensure_acp_bridge_running` 不读 config.toml 查 binary 路径。只读两个 env var：
- `FREELY_CODEX_ACP_BIN` — 仅 codex
- `FREELY_CLAUDE_ACP_BIN` — 仅 claude（且只在 registry 查不到时 fallback）

opencode/cline 完全没有路径记录机制。

### 4. ensure-codex-acp 脚本

- 硬编码 codex，名不符实（注释说是通用但名称为 codex）
- 缓存路径: `~/.cache/freely/acp/codex-acp/{version}/{triplet}/codex-acp`
- 已缓存则跳过下载，缓存位置固定不随机
- 被两个地方引用: `_ensure_acp_bridge_running` L13992, `tool-launchers.sh` L182

### 5. 时效性判断

- 问题当前仍在：今天启动时 `deploy-skills exited 1` 和 ACP startup timeout 反复出现
- 直接影响新用户首次配置体验
- **结论: 值得投入**

## Problem — 根因分析

### 根因 1: ACP binary 发现逻辑分散、不一致

`cmd_init()` 和 `_ensure_acp_bridge_running()` 各自独立实现了 binary 查找逻辑：
- init: 硬编码 `case codex` vs `case *`
- runtime: 读 registry → fallback
- 两条路径不共享逻辑，各自有各自的 bug

**应按单一来源（tool-registry → config.toml）统一。**

### 根因 2: 无下载机制

`cmd_init()` 只检查存在性→报错退出。用户必须手动安装。
`_ensure_acp_bridge_running()` 有 `ensure-codex-acp` 懒下载但仅限 codex。

### 根因 3: 无 config.toml 持久化

binary 路径算一次丢一次。后续运行时重新计算。
应该 `freely init` 搜到/下载后写入 config.toml，runtime 直接读。

### 根因 4: opencode/cline 完全未被处理

registry 已有它们的 ACP 配置，但 init 和 runtime 都不认识。

### 根因 5: _acp_bridge_health_check Shell 注入（附加发现）

L13868: `sock.connect('$socket')` — 变量直接拼入 Python -c 字符串。
与之前修复的 A2A 健康检查（PR #3648）和 freely-cycle（PR #3645）同类问题。

## Brainstorm — 方案评估

### 方案需解决的完整范围

| # | 改动点 | 文件 |
|---|--------|------|
| 1 | tool-registry 新增 download_url + install_method | tool-registry.toml |
| 2 | ensure-codex-acp → ensure-acp-binary（通用化） | ensure-codex-acp |
| 3 | cmd_init() 新增 ACP 工具准备步骤 | freely (cmd_init) |
| 4 | _ensure_acp_bridge_running 从 config.toml 读路径 | freely |
| 5 | 修复 _acp_bridge_health_check Shell 注入 | freely |
| 6 | config.toml 新增 ACP binary 路径字段 | config.toml.example |

### Option A: 全部在 freely init 中处理（推荐）

**流程:**
```
freely init --ai claude:sonnet:auto
  │
  ├─ 现有逻辑（平台检查、SDK 检查等）
  │
  ├─ [新增] ACP 工具准备:
  │    │
  │    ├─ 循环 tool-registry 的每个 [tool] section
  │    │   对每个 tool:
  │    │     ├─ 读 [tool.acp].binary / .download_url / .install_method
  │    │     ├─ 搜系统（PATH、npm list -g --depth=0、~/.cache/freely/acp/）
  │    │     ├─ 找到 → 记录路径，跳过
  │    │     └─ 未找到 → 提示确认下载
  │    │          "claude-agent-acp 未安装。从 npm 下载？ [y/N]"
  │    │          y → 按 download_url + install_method 下载
  │    │          n → 跳过（runtime 用到时再报错）
  │    │
  │    └─ 写入 config.toml:
  │         FREELY_ACP_CLAUDE_BIN = "/path/to/claude-agent-acp"
  │         FREELY_ACP_CODEX_BIN  = "/path/to/codex-acp"
  │         FREELY_ACP_OPENCODE_BIN = "/path/to/opencode"
  │         FREELY_ACP_CLINE_BIN    = "/path/to/cline"
  │
  ├─ [新增] 修复 Shell 注入: _acp_bridge_health_check → env var
  │
  └─ 现有后续逻辑（agent-table, hooks 等）
```

**优点:**
- 统一入口，用户只跑一次 `freely init` 就全配好
- config.toml 持久化，runtime 直接读，不需要重复搜索/下载
- 循环 registry，未来新增工具零代码改动

**缺点:**
- `cmd_init()` 函数变长
- 需处理交互式确认（freely 是 CLI 工具，支持 stdin 交互）

### Option B: 懒下载（runtime 首次用到时才下载）

**流程:** daemon start → _ensure_acp_bridge_running → 发现 binary 不在 → 调通用下载函数

**优点:** init 不变，改动面小

**缺点:**
- 用户启动 daemon 时卡住等待下载，体验差
- daemon start 是非交互的（auto mode），无法提示确认
- 与用户要求（init 时确认）冲突

### Option C: 保留现状，只改 registry + 确保报错信息清晰

**优点:** 零代码改动

**缺点:** 用户仍需手动安装，没有解决任何实际问题

## Decision: Option A

**理由:**
1. init 是用户首次接触 freely 的入口，此时完成所有准备工作最合理
2. config.toml 持久化避免每次启动重新搜索
3. 循环 registry 保证未来扩展性——新增工具只需加 registry 条目
4. Shell 注入顺便修掉

### 子决策

#### tool-registry.toml 字段设计

```toml
[claude.acp]
binary = "claude-agent-acp"
args = []
# 新增:
install_method = "npm"                    # npm | github_release | cargo | pip
download_url = "npm:@anthropic-ai/claude-agent-acp"  # npm: 前缀或 https:// URL
bridge_socket_suffix = "acp"

[codex.acp]
binary = "codex-acp"
args = []
auto_download = true                      # 保留兼容，新字段优先
install_method = "github_release"
download_url = "https://github.com/zed-industries/codex-acp/releases/download/v{version}/codex-acp-{version}-{triplet}.tar.gz"
download_version = "0.15.0"              # 保留，{version} 占位符替换
download_repo = "zed-industries/codex-acp" # 保留兼容
bridge_socket_suffix = "acp"

[opencode.acp]
binary = "opencode"
args = ["acp"]
install_method = "npm"
download_url = "npm:@anthropic-ai/opencode"
bridge_socket_suffix = "opencode"

[cline.acp]
binary = "cline"
args = ["--acp"]
install_method = "npm"
download_url = "npm:cline"
bridge_socket_suffix = "cline"
```

#### install_method 与 download_url 的对应关系

| install_method | download_url 格式 | 下载命令 |
|---------------|------------------|---------|
| `npm` | `npm:<package-name>` | `npm install -g <package-name>` |
| `github_release` | `https://github.com/{owner}/{repo}/releases/download/v{version}/{asset}.tar.gz` | curl + tar |
| `cargo` | `cargo:<crate-name>` | `cargo install <crate-name>` |
| `pip` | `pip:<package-name>` | `pip3 install <package-name>` |

#### ensure-codex-acp → ensure-acp-binary 通用化

```
当前: 硬编码 codex，读 [codex].acp 字段
改为: 接受 --tool <name> 参数，循环所有 tool 或指定 tool
      从 tool-registry 读 download_url + install_method
      按 install_method 执行对应下载逻辑
      缓存到 ~/.cache/freely/acp/<tool>/<version>/<triplet>/<binary>
```

#### config.toml 路径字段

```toml
# ACP binary paths (set by freely init, read by runtime)
FREELY_ACP_CLAUDE_BIN = "/opt/homebrew/bin/claude-agent-acp"
FREELY_ACP_CODEX_BIN = "/Users/zhaoyu/.cache/freely/acp/codex-acp/0.15.0/aarch64-apple-darwin/codex-acp"
FREELY_ACP_OPENCODE_BIN = ""   # 未安装
FREELY_ACP_CLINE_BIN = ""      # 未安装
```

字段名生成规则: `FREELY_ACP_<TOOL_UPPER>_BIN`，从 registry 的 `[tool]` section name 自动生成。

#### _ensure_acp_bridge_running 改造

```bash
# 当前: 从 registry 读 binary 名 → PATH 找 或 ensure-codex-acp
# 改为:
1. 先读 config.toml: get_config "FREELY_ACP_${TOOL_UPPER}_BIN"
2. 找到且可执行 → 直接用
3. 找不到 → 读 registry acp.binary → PATH 找
4. 还找不到 → 报错 "run freely init to set up ACP tools"
```

#### Shell 注入修复

```bash
# 当前 L13868:
sock.connect('$socket')

# 改为:
sp = os.environ.get('FREELY_ACP_HEALTH_SOCKET', '')
sock.connect(sp)

# 调用方:
FREELY_ACP_HEALTH_SOCKET="$socket" python3 -c "..."
```

### 边界外（不在此 issue 做）

- 不修改 ACP SDK (agent-client-protocol Python 包) 的安装逻辑（保留 pip3 检查）
- 不修改 agent-table.toml 结构
- 不修改 ACP bridge 的 session/fork/resume 逻辑
- 不修改多 tool 同时运行的 ACP bridge 架构（那是未来需求）

### 残余风险

- npm install -g 需要 Node.js 环境（大部分开发者已有）
- github_release 下载依赖 curl + tar（系统自带）
- 网络不通时下载失败——需友好报错并给出手动安装指引
- `.freely/config.toml` 是项目级文件，binary 路径可能因机器不同而变化——需提示用户在每台机器上重新跑 `freely init`

## Candidate
- candidate_id: C-20260630T124528Z-A
- status: promoted
- milestone: M-20260630T124528Z-A
- estimated_effort: 大（涉及 5+ 文件，新增下载逻辑，registry 字段扩展，config.toml schema 扩展）
- candidate 拆分建议: 可拆为 A（registry + ensure-acp-binary 通用化）和 B（freely init 集成 + config.toml），但 B 依赖 A。建议单 candidate 推进，B2 阶段拆分 tasks。
