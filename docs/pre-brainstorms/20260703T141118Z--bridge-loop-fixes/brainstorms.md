---
b1_id: B1-20260703T141118Z
phase_state: completed
source_raw: raw-20260703T141118Z
produced_candidate: C-20260703T141118Z-A
---

# B1_IBM: bridge 重复重启 + loop_guard 缺失 + tool registry 误报

## Bug 1: ACP bridge binary changed 每 cycle

### 根因：config.toml 全路径写入文件，registry 短名用于比较，时序错位

代码顺序（`_ensure_acp_bridge_running`）：

```
14007: acp_bin = "claude-agent-acp"       (默认)
14013: acp_bin = "opencode"               (← registry acp.binary)
  ...
14069: running_bin != acp_bin ?            (← 比较发生在这里！)
        文件里: /Users/.../.opencode/bin/opencode  (上轮 config 写的全路径)
        acp_bin: opencode                         (registry 短名)
        → 不匹配 → 重启！
  ...
14098: acp_bin = "/Users/.../.opencode/bin/opencode" (← config.toml 覆盖在比较之后！)
14171: 写入文件 = "/Users/.../.opencode/bin/opencode" (全路径)
```

config.toml 的全路径覆盖在比较语句（line 14069）**之后**。
下一轮：文件 = 全路径，registry = 短名，config 覆盖也在比较之后 → 永远不匹配 → 每 cycle 重启。

### 修复

**A. `basename` 归一化比较**（稳健，不论存什么路径都对）
```bash
_running_bin_name=$(basename "$running_bin")
_acp_bin_name=$(basename "$acp_bin")
if [[ "$_running_bin_name" != "$_acp_bin_name" ]]; then
```

**B. 写短名到文件**（治本，减少路径差异）
在 config 覆盖前保存原始短名，写到文件时用短名而非全路径。

**选用 A+B**：比较用 basename + 写短名到文件。

## Bug 2: loop_guard_check_all: command not found

### 根因

`loop_guard_check_all` 定义在 freely:11562，调用在 freely:22933。
定义在前、调用在后，理论上可用。但实际报 "command not found"。

推测：调用点位于 supervisor 循环内的一个 `while true` 块。
如果该 `while` 块在某些条件下以子 shell 方式执行（如 `| while read` 管道），
则父 shell 中定义的函数在子 shell 中不可见。

或更可能：函数体内调用的 `_loop_guard_L0_check` 等子函数未定义，
导致 `loop_guard_check_all` 在定义时即失败（bash 静默跳过格式错误的函数）。

### 修复

调用前加函数存在性检查：
```bash
if declare -f loop_guard_check_all >/dev/null 2>&1; then
  loop_guard_check_all ...
fi
```

## Bug 3: tool registry 误报 "opencode 未注册"

### 根因

`start-lead-agent.sh` parse_ai_spec 中的 tool 已是 base name `opencode`
(from `AI_TOOL="${AGENT_AI_TOOL%%-*}"`)。registry 列表也有 `opencode`。
理论上应匹配。但实际不匹配。

推测：`_reg_tools` 捕获的 Python 输出有不可见字符或换行问题，
导致 for 循环迭代不完整。或 `set -euo pipefail` 导致某次迭代失败后静默退出。

### 修复

不依赖 shell for 循环匹配，改用 registry query 直接判：
```bash
_is_known=$("$_runtime_dir/tool-registry-query.py" "$_runtime_dir/tool-registry.toml" "$_case_tool" "acp.binary" >/dev/null 2>&1 && echo 1 || echo 0)
```

## Decision

三个修复归为一个 issue，同属 daemon 运行时稳定性修复。

## Candidate
- candidate_id: C-20260703T141118Z-A
- status: promoted
- milestone: M-20260703T141118Z-A
