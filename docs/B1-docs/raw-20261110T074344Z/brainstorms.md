---
raw_id: raw-20261110T074344Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域

R23.9 已交付协议真源 `runtime/state_file.py` 与边界 lint（55 处 `source` 基线）。本条承接逐组迁移。实测 55 处形态：`$state_file` 22 / `workcell_state_file` 20 / `manager_worker_launch_state_file` 7 / 带 `|| true` 4 / `session_state_file` 2；另有 39 处非状态 source 不得误改；77 个状态键；部分 `printf '%s|%s'` 位置格式。

## 本轮选族：cooldown-state.env

| 维度 | 值 |
|---|---|
| 读 | `_read_cooldown_state()` 1 处 `source "$state_file"` |
| 写 | `_write_cooldown_state()` 1 处 `printf 'KEY=%s\n'` |
| 键 | `COOLDOWN_SWITCH_AT` / `COOLDOWN_SWITCH_INDEX`（2 个，都在白名单） |
| 下游 | 只使用 `CROSS_TOOL_SWITCH_AT/INDEX`，不直接引用 `COOLDOWN_SWITCH_*` |

选它的理由：最小**完整**族（读写成对、键闭合、下游依赖清晰），能一次验证「shell ↔ python 协议边界」而不牵动状态机主干。`workcell`（20 读）与 `manager_worker_launch`（7 读）应在有样板后按族推进。

## 方案方向

### 读侧：`values` 行接口

- 给 `state_file.py` 加 `values <path> <keys...>`：按行输出原始值；值含换行则**报错拒绝**（避免 bash 行读静默截断）。
- shell 侧用 `{ read -r at; read -r idx; } < <(python3 ... || true)`。**不用 `mapfile`**——macOS 自带 bash 3.2 不支持。
- 失败/缺文件回落到 0，与原实现 `${VAR:-0}` 语义一致。

### 写侧：`--kv` argv 接口

- 给 `write` 加可重复 `--kv KEY=VALUE`，值经 argv 传递，**不拼进任何脚本体**。
- 文件落成 `KEY<TAB>json.dumps(value)`，不是 shell 赋值。

### 兼容期

- reader 仍接受旧 `KEY=value`（按首个 `=` 切分、去一层引号、其余原样保留）——AT 断言旧格式 `99/3` 可读、旧格式 `$(touch marker)` **不执行**。
- 不要求人工清空 `.freely/run/`。

## 被否决

- **一次性替换全部 55 处**：77 键白名单可能漏、部分位置格式需单独判定、无法逐族跑回归。
- **`to-shell` + source 中间文件**：仍引入 source，且需临时文件生命周期管理；cooldown 只需两个标量，行读更直接。
- **`eval`/命令替换解析 JSON**：把外部值重新带回 shell 代码路径。
- **改键名或改用 `COOLDOWN_*` 下游**：违反「不改键名与语义」的不退化边界。

## fidelity 基线

- RED 必须 source **真实 `runtime/freely`** 并调用真实 `_read/_write_cooldown_state`，用 `marker=True` 证明旧实现真的执行注入。
- GREEN 必须证明：普通值往返、文件是 TAB+JSON、旧格式兼容、旧格式注入不执行、恶意值新格式逐字节且不执行、换行值被拒绝、全局 source 计数 55→54。
- 2 项 RED PASS 是守卫（普通往返、旧格式兼容），不是新功能。

## 价值判定

- 不过时：55 处仍在，cooldown 族仍用 printf+source。
- 不重叠：R23.9 只建协议未迁任何调用点；本轮是第一个真实迁移。
- 高价值：把「协议存在」变成「协议被使用」，并给出可复制的迁移范式与边界数字下降。

## 明确不纳入

其余 54 处状态 source 与对应写入点（按族逐轮推进），位置格式文件的单独判定。
