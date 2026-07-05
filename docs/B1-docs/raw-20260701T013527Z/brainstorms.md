---
b1_id: B1-20260701T013527Z
phase_state: completed
source_raw: raw-20260701T013527Z27Z
source_url: https://github.com/chatterzhao/freely/issues/3674
produced_candidate: C-20260701T013527Z-A
created_at: 2026-07-01
---

# B1_IBM: get_config undefined in runtime script

## Input
- **Raw issue**: raw-20260701T013527Z27Z
- **Platform**: GitHub #3674 / Gitee IJXYY1
- **Source**: daemon startup log observation

## Problem

启动 freely daemon 时，`daemon-launch.log` 中出现：

```
line 14052: get_config: command not found
```

`docs/system/workspace/scripts/runtime/freely` 第 14052 行调用了 `get_config` 函数，但该函数在整个脚本中从未定义。代码意图是从已加载的 config.toml 环境变量中读取 ACP binary 路径（如 `FREELY_ACP_CLAUDE_BIN`），但函数不存在导致读取失败。

## Root Cause Analysis

该行位于 `_ensure_acp_bridge_running()` 函数内（约 L13979），在 daemon 启动流程中执行。此时 `load_config()` 已经通过 `source_config → toml2env` 将所有 config.toml 值导出为 shell 环境变量，可以直接通过 bash indirect expansion (`${!varname}`) 读取。但代码错误地调用了不存在的 `get_config` 函数。

影响范围：
- **非致命**：ACP bridge 仍可通过 PATH 搜索找到 binary
- **有隐患**：如果 binary 不在 PATH 中（通过 `freely init` 配置的自定义路径），ACP bridge 将完全无法启动

## Brainstorm

### Option A: 定义 `get_config` 函数，从 config.toml 文件读取

```bash
get_config() {
  local key="$1" default="${2:-}"
  local cfg="$project/.freely/config.toml"
  # read from file using regex...
}
```
- ❌ 需要重新打开和解析 config.toml 文件（重复 IO）
- ❌ 增加维护负担（需与 toml2env 保持同步）
- ❌ 在已加载配置后重复读取

### Option B: 使用 bash indirect variable expansion `${!_config_key:-}`

```bash
local _config_path; _config_path="${!_config_key:-}"
```
- ✅ 直接读取已加载的环境变量，零 IO
- ✅ 无新增函数，无维护负担
- ✅ 与 load_config 机制一致
- ✅ 已有类似用法（如 `AGENT_AI_TOOL` 的读取）

## Decision: Option B — `${!_config_key:-}`

理由：
1. load_config 已将所有配置值导出为环境变量，无需重复读取文件
2. bash indirect expansion 是标准做法，简洁可靠
3. 改动最小（一行），风险最低
4. 与脚本中其他配置读取方式一致

## Candidate

- candidate_id: C-20260701T013527Z-A
- status: promoted
- milestone: M-20260701T013527Z-A
- promoted_issue_id: I-20260701T013527Z-A
- decision_reason: bash indirect expansion 零 IO、无新增函数、与现有 load_config 机制完全一致
- next_action: B2_IBM 设计 → RED → dev 应用修复 → test 验证 → PR
