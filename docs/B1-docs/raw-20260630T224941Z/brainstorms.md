---
b1_id: B1-20260630T224941Z
phase_state: completed
source_raw: raw-20260630T224941Z
source_url: https://github.com/chatterzhao/freely/issues/3669
produced_candidate: C-20260630T224941Z-A
created_at: 2026-06-30
---

# B1_IBM: config.toml.example 全面修订 + init 自动创建 config.toml

## Input
- raw issue: `docs/B1-docs/raw-20260630T224941Z/issue.md`
- 平台: GitHub #3669

## Discovery — 现状调研

### 1. config.toml.example 当前问题

**缺失字段:**
| 字段 | 代码写入位置 | example 中有？ |
|------|-------------|--------------|
| `FREELY_ACP_CLAUDE_BIN` | `_init_acp_tool_setup` L20143 | ❌ |
| `FREELY_ACP_CODEX_BIN` | `_init_acp_tool_setup` | ❌ |
| `FREELY_ACP_OPENCODE_BIN` | `_init_acp_tool_setup` | ❌ |
| `FREELY_ACP_CLINE_BIN` | `_init_acp_tool_setup` | ❌ |

**注释不准确:**
| 字段 | 当前注释 | 实际问题 |
|------|---------|---------|
| `PROJECT_ROOT` | `（必须修改）` | 没说 init 能否自动填，没说空值影响 |
| `FREELY_HOME` | `init 时自动填入实际路径` | **从未实现**——init 不填这个 |
| `AI_TOOL` | `codex \| claude \| opencode \| iflow \| kiro-cli \| cc` | 缺 `cline`，且不解释各工具差异 |
| `AI_MODEL` | `codex→gpt-5.4/gpt-5.5` | 模型名已过时 |
| `FREELY_REPO_PLATFORMS` | `例如 "github,gitee"，留空=不扫描` | 不说合法值 |
| 大多数"固定默认值"字段 | `一般无需修改` | 不说改了会怎样 |

**整体缺失:**
- 没有区分"init 自动填入" vs "用户必须手写"
- 没有"不填会how"的说明
- 新增的 init 自动 ACP 下载能力与 example 注释"必须手工配置"矛盾

### 2. 逐字段代码用法研究

#### 一、项目基础 — 必须配置

| 字段 | 代码引用 | 用法 | 空值影响 |
|------|---------|------|---------|
| `PROJECT_ROOT` | 29 处 | git 操作、config 路径、runtime 基准目录 | **空=freely 完全不可用** |
| `INTENT_FILE` | `freely_config.py` 读取 | Manager prompt 注入，约束 AI 行为 | 空=AI 缺少行为约束 |
| `CONSTITUTION_FILE` | 同上 | Manager prompt 注入，硬性边界 | 空=AI 缺少边界约束 |
| `FREELY_HOME` | 寻找自带脚本 | 定位 freely 安装目录下的模板/script | 空=部分模板功能不可用 |

init 可以自动填入的有:
- `PROJECT_ROOT`: `git rev-parse --show-toplevel`
- `INTENT_FILE`: `$PROJECT_ROOT/docs/PROJECT_INTENT.md`（约定）
- `CONSTITUTION_FILE`: `$PROJECT_ROOT/docs/CONSTITUTION.md`（约定）
- `FREELY_HOME`: 当前执行 freely 的路径

#### 二、AI 工具配置

| 字段 | 代码用法 | 合法值 |
|------|---------|--------|
| `AI_TOOL` | 172 处引用，核心调度 | `claude`, `codex`, `opencode`, `cline`, `iflow`, `kiro-cli`, `cc` |
| `AI_MODEL` | 传递给 ACP binary `--model` | 格式 `tool-model-name`，不同工具不同 |
| `AI_MODE` | 控制 autonomy/interaction/approval 三姿态 | `auto`(全自主), `step`(交互), `wait`(监听) |
| `AI_REASONING_EFFORT` | 传递给 ACP binary `--effort` | `low`, `medium`, `high` |

代码证据: L2123-2135 从 AI_MODE 推导三姿态默认值。L5251 写 AI_MODEL。L5254 写 AI_TOOL_ADAPTER。

#### 三、AI 工具适配器

| 字段 | 代码用法 |
|------|---------|
| `AI_TOOL_ADAPTER` | acp → ACP bridge 模式；direct → CLI 模式（已废弃） |
| `AI_TOOL_ADAPTER_POLICY` | direct(透传) / managed(Freely管理) |

代码证据: L3675 判断 `AI_TOOL_ADAPTER == "acp"` 决定是否启动 ACP bridge。

#### 四~十五、固定默认值字段

研究结论：这些字段的默认值在 `upsert_config_key` 调用中定义（L4258-4311），与 example 中的值一致。用户修改会影响对应行为阈值。

**有明确默认值且 init 会自动写入的字段**（L4258-4311）:
- 所有的"十五、自治与安全姿态"
- `AUTO_SWITCH_SLOT`, `AUTO_SWITCH_TOOL`, `AUTO_SETUP_FREELY_PROXY`
- `CONTEXT_WARN_RATIO`, `CONTEXT_ROTATE_RATIO`
- `RESTART_STORM_WINDOW_SECS`, `RESTART_STORM_COUNT`
- `FREELY_NETWORK_PROXY_MODE`

**不在 init 自动写入但 runtime 有 fallback 的字段**:
- `CHECK_INTERVAL`: `"${CHECK_INTERVAL:-10}"` (L15841) — 默认 10 秒
- `AI_FALLBACK_TOOLS`: `"${AI_FALLBACK_TOOLS:-}"` (L4955) — 默认空，不 fallback

### 3. init 创建 config.toml 流程设计

**当前行为:**
- init 只释放 `config.toml.example` 到 `.freely/`，不创建 `config.toml`
- 提示用户手工 `cp` 和编辑

**应改为:**

```
freely init --ai claude:sonnet:auto [--auto] [--reset]
  │
  ├─ 判断 .freely/config.toml 是否存在
  │
  ├─ 不存在:
  │   ├─ 从 templates/config.toml.example 复制
  │   ├─ 自动填入: PROJECT_ROOT, INTENT_FILE, CONSTITUTION_FILE, FREELY_HOME
  │   ├─ 打印: "config.toml 已创建，请编辑 .freely/config.toml"
  │   └─ 继续 ACP 工具准备
  │
  ├─ 存在，无 --reset:
  │   ├─ 读取现有值
  │   ├─ 只补缺失的 FREELY_ACP_*_BIN 字段
  │   └─ 已有字段不动
  │
  └─ 存在，--reset:
      ├─ 有 --auto: 自动确认，直接重置
      ├─ 无 --auto: 交互 [y/N]，30s 超时默认 N
      ├─ 备份: mv config.toml → config.toml.YYYYMMDDTHHMMSSZ.bak
      ├─ 从 example 复制 → 填值（同"不存在"分支）
      └─ 继续 ACP 工具准备
```

### 4. merge lock 死锁检测

**当前行为:**
```bash
while ! mkdir "$lock_dir"; do
    if waited >= 300s: "merge lock timeout (another merge in progress?)"
    sleep 2
done
```

**问题:** 不区分真实并发 vs 死锁。死锁时静默等 300 秒。

**应改为:**
```bash
while ! mkdir "$lock_dir"; do
    if [[ -d "$lock_dir" ]]; then
        lock_pid=$(cat "$lock_dir/pid" 2>/dev/null)
        if kill -0 "$lock_pid" 2>/dev/null; then
            echo "另一个 merge 正在进行 (PID: $lock_pid)，请稍后再试"
        else
            echo "⚠️ 疑似死锁 — lock 目录存在但进程 $lock_pid 已不存在"
            echo "   确认无其他 merge 进程后可清理: rm -rf $lock_dir"
        fi
    fi
    ...
done
# 获取锁时写 PID
echo $$ > "$lock_dir/pid"
```

### 5. config.toml.example 注释改进原则

每条字段注释必须包含：

1. **这是什么** — 一句话说明用途
2. **合法值** — 固定值字段列出全部选项+各自含义
3. **不填会怎样** — 留空/删掉的影响
4. **init 行为** — init 是否自动填，填什么值
5. **谁填** — `[init自动]` / `[用户必填]` / `[可选]`

## Decision

### 方案: 全面修订 config.toml.example + 实现 init 创建/重置逻辑 + merge lock 诊断

**理由:**
1. config.toml.example 是用户配置的唯一入口，注释不准确会误导
2. 新增的 FREELY_ACP_*_BIN 字段必须出现在 example 中
3. init 现在能做更多事（ACP 下载），不应还让用户手工 cp
4. merge lock 死锁问题已两次导致我们的合并卡住，必须修

**改动范围:**
1. `templates/config.toml.example`: 修订注释，新增第十六节 FREELY_ACP_*_BIN
2. `docs/system/workspace/scripts/runtime/freely` cmd_init(): 
   - 实现 config.toml 自动创建
   - 实现 --reset 逻辑（备份+覆盖）
   - 交互式确认 30s 超时
3. `docs/system/workspace/scripts/worktree/pr-merge-guarded`:
   - merge lock 写 PID
   - 死锁检测+清晰提示

**拆分建议:**
- Candidate A: config.toml.example 修订（纯文档，可先合）
- Candidate B: init 创建/重置逻辑（代码，依赖 A）
- Candidate C: merge lock 死锁诊断（独立，不依赖）

## Candidate
- candidate_id: C-20260630T224941Z-A
- status: promoted
- milestone: M-20260630T224941Z-A
