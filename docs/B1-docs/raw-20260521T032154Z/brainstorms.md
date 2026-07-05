# Brainstorm: supervisor crash — _on_supervisor_err 递归 ERR trap 导致假阳性报告

## Discovery

### 来源

- Raw issue: `raw-20260521T032154Z` (GitHub #1523)
- 创建时间: 2026-05-21T03:22:06Z
- 来源渠道: GitHub issue (platform)
- Crash: `supervisor crash: [[ at freely:18951 (rc=1)`
- `last_exit_reason_before_crash: set_e_exit_cmd=[[@freely:18951_rc_1`
- tool: cc-ds-flash-auto, adapter: acp, launch_kind: prompt

### 时效性与价值

1. **时效性高**: 同一问题模式在 supervisor crash batch1/batch2 中已被多次报告
2. **影响面广**: 每次 `[[` 条件判断 false 都可能触发一次假阳性 crash 报告，污染 issue 队列
3. **与已有候选的关系**: 与 `C-20260517T083030Z-A` (bash rc=0 假阳性) 是**不同 crash 模式**：
   - bash rc=0 是 `bash` 命令以 rc=0 退出被 ERR trap 捕获并误报
   - 本 issue 是 ERR trap handler `_on_supervisor_err` 内部逻辑缺陷导致自身产生假阳性
4. **修复边界清晰**: 代码路径已定位到 `_on_supervisor_err` 函数（freely runtime ~line 18951）

**结论**: 值得投入，与已有候选互补，应进入 brainstorm。

### 关联现有 pre-brainstorms

| 现有条目 | 关系 |
|---------|------|
| `C-20260517T083030Z-A` (supervisor bash rc=0, M-20260517T083030Z-A) | 同属 supervisor crash 假阳性类别但**不同根因**：bash rc=0 是 bash 退出码误判，本 issue 是 ERR trap handler 递归缺陷 |
| `C-20260521T012042Z-A` (stale-pid keepalive, M-20260521T012042Z-A) | 不相关：Manager keepalive 层面的 worker 生命周期问题 |

---

## Research

### 代码路径定位

Crash 发生在 `_on_supervisor_err` 函数（`docs/system/workspace/scripts/runtime/freely` ~line 18951）。ERR trap 在 line 18978 设置：

```bash
trap '_on_supervisor_err $LINENO' ERR
```

处理函数结构（line 18951-18977）：

```bash
_on_supervisor_err() {
    local _err_rc=$?                        # 18952
    if [[ "$_err_rc" -eq 0 ]]; then         # 18953 ← 可触发递归 ERR trap
        LAST_WORKCELL_EXIT_REASON="..."
        return                               # 18955
    fi
    local _err_cmd _err_line _err_reason _msg  # 18957
    _err_cmd="${BASH_COMMAND%% *}"           # 18958 ← 递归后 BASH_COMMAND 已错
    # [[ / [ rc=1 → benign
    if [[ "$_err_rc" -eq 1 ]] && [[ "$_err_cmd" == "[[" || "$_err_cmd" == "[" ]]; then  # 18960
        LAST_WORKCELL_EXIT_REASON="..."
        return                               # 18962
    fi
    # ... crash report generation (line 18964+)
}
```

### 根因分析：递归 ERR trap 导致 BASH_COMMAND 错位

**正常流程**（无递归）：
1. 外部 `[[ ... ]]` → rc=1 → ERR trap → `_on_supervisor_err LINENO`
2. `_err_rc=1`, `_err_cmd=[[` (BASH_COMMAND)
3. Line 18953: `[[ "1" -eq 0 ]]` → rc=1 → **递归 ERR trap**
4. 递归调用：`_err_rc=1`, BASH_COMMAND=当前命令 = `[[`（仍来自 18953 的 `[[`）
5. 递归调用 line 18953: 同上 → 继续递归，形成调用栈堆积
6. 栈最终展开（bash 限制递归层数后终止，或某层进入 line 18960 后被 benign check 拦截 → return）
7. 回到外层调用 line 18953 → `if` 不满足 → 继续 line 18958

**Bug 触发**：
- 经过递归展开后，回到 line 18958 `_err_cmd="${BASH_COMMAND%% *}"`
- 此时 `BASH_COMMAND` **不再是原始触发命令** `[[`，而是外层函数中正在执行的赋值命令
- `${BASH_COMMAND%% *}` 提取第一个词 → `_err_cmd`（字符串字面量）
- Line 18960: `[[ "$_err_cmd" == "[[" ]]` → `_err_cmd` = `_err_cmd` ≠ `[[` → **benign check 失败**
- Line 18964+: crash report 被错误生成

### 修复方案

#### 方案 A：提前捕获 BASH_COMMAND（推荐）

将 `_err_cmd` 的赋值移到 `[[ "$_err_rc" -eq 0 ]]` 检查之前，确保 BASH_COMMAND 在递归 trap 污染前已被保存：

```bash
_on_supervisor_err() {
    local _err_rc=$?
    local _err_cmd="${BASH_COMMAND%% *}"    # ← 提前捕获

    if [[ "$_err_rc" -eq 0 ]]; then
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi

    # [[ / [ rc=1 → benign
    if [[ "$_err_rc" -eq 1 ]] && [[ "$_err_cmd" == "[[" || "$_err_cmd" == "[" ]]; then
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi

    local _err_line _err_reason _msg
    _err_line="${1:-${LINENO}}"
    ...
}
```

优点：
- 改动最小（调整 2 行顺序）
- 不影响已有逻辑
- 不改变 ERR trap 行为

#### 方案 B：在 handler 内禁用 ERR trap

```bash
_on_supervisor_err() {
    trap '' ERR   # 禁用递归
    local _err_rc=$?
    ...
    trap '_on_supervisor_err $LINENO' ERR   # 恢复
}
```

优点：
- 完全杜绝递归
- 更安全

缺点：
- 需要记住恢复 trap
- `_on_supervisor_err` 自身的错误不会被捕获（但这也可视为优点——避免递归）

### 与 bash rc=0 假阳性的关系

| 维度 | bash rc=0 (C-20260517T083030Z-A) | 本 issue (raw-20260521T032154Z) |
|------|----------------------------------|----------------------------------|
| 触发命令 | `bash` | `[[` |
| 退出码 | 0 (成功) | 1 (条件 false) |
| 根因 | bash 成功退出被误判为 crash | ERR trap handler 递归导致 BASH_COMMAND 错位 |
| 代码位置 | supervisor bash 执行/检测逻辑 | `_on_supervisor_err` handler 内部 |
| 修复范围 | supervisor 的 crash 检测阈值 | 同一函数的执行顺序 |
| 互补性 | 研究 `rc=0` 为何能触发 ERR trap | 修复 handler 自身稳定性 |

**结论**: 两个问题独立，应各自有独立 candidate。本 issue 的修复边界更小、可操作性更高。

---

## Decision

### 决策

**新建 candidate C-raw-20260521T032154Z-A，状态 `needs_research`**。理由：

1. 根因已定位到 `_on_supervisor_err` 函数内 BASH_COMMAND 捕获顺序问题
2. 修复方案明确（方案 A 或 B），改动范围不超过 3 行
3. 与 C-20260517T083030Z-A (bash rc=0) 是不同的 crash 模式，不应合并
4. 当前是 RAW issue 阶段，先以 `needs_research` 进入 milestone，确认修复方向后再 promote

### Scope

| 项目 | 值 |
|------|-----|
| 影响文件 | `docs/system/workspace/scripts/runtime/freely` (仅 `_on_supervisor_err` 函数) |
| 修复类型 | bug fix |
| 风险 | 低（改动范围极小） |
| 测试方式 | 模拟 `[[` 条件 false 触发 ERR trap，验证 crash report 不被生成 |
| 依赖 | 无（独立的代码缺陷修复） |

### 下一跳

1. 确认 candidate acceptance → promotion gate 满足后进入 B2_IBM
2. B2_IBM 产出 PRD + pre-tests + tasks 后进入 dev-loop
3. dev-loop 实现方案 A（推荐）并验证

### 开放问题

1. 是否有更多 `_on_supervisor_err` 执行路径会在递归 trap 后损坏状态？
2. 方案 B（禁用 ERR trap）是否更安全，即使改动稍大？
3. 此前 batch1/batch2 中是否有与本 issue 模式相同但被误归入 bash rc=0 的报告？
