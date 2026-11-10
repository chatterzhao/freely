---
raw_id: raw-20261110T081029Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（develop `9038a2547` 真源普查）

R23.9 交付协议真源、R23.11 迁了第一族 cooldown-state.env（55 → 54）。本条承接剩余 54 处。先按「形态」和「状态文件」两个维度重新普查，避免照抄 issue 的旧行号：

| 形态 | 数量 | 行号 |
|---|---|---|
| `source "$state_file"` | 21 | 1895,1914,2116,2218,2645,8256,8473,8629,8655,9257,9268,9517,9564,9726,9853,13252,15098,15824,17824,21956,26787 |
| `source "$(workcell_state_file "$project")"` | 20 | 2033,2148,3696,5695,… |
| `source "$(manager_worker_launch_state_file "$project")"` | 7 | 11574,11605,11742,13804,25983,26354,26819 |
| `source "$state_file" 2>/dev/null \|\| true` | 4 | 11838,11888,11926,24431 |
| `source "$(session_state_file "$project")"` | 2 | 18382,19190 |

按状态文件归类后另有：`manager_worker_launch_state_file` 还有 7 处走变量形式 `source "$state_file"`（2218/9517/9564/13252/15098/15824/21956），合计 14 处读；`workcell_state_file` 另有 6 处。

## scope 收敛：本轮选 execution-network-recovery.env

恢复点建议先迁 `manager_worker_launch` 族（7 读、回归护栏多）。**前置评审否掉了这个建议**：

- 该族写入用 11 键 heredoc，**11 个键全部不在 `ALLOWED_KEYS` 白名单**（见下）—— 一迁就会 `unknown state key`；
- 55 个测试直接 `cat >manager-worker-launch-state.env <<EOF` 构造旧格式，多个还用 `grep -q '^KEY="value"$'` 断言写入格式、甚至 `source` 该文件；
- 一轮改完 14 读 + 11 键 + 55 测试，「行为不变」无法验证。

改选最小且真实活跃的族 `execution-network-recovery.env`：

| 维度 | 值 |
|---|---|
| 写 | `persist_execution_network_state()` 1 处 heredoc，4 键 |
| 读 | `runtime_network_failure_reason_from_log()` 与 `execution_network_launch_block_active()` 共 2 处 `source` |
| 键 | `EXECUTION_NETWORK_REASON` / `FAILURE_COUNT` / `NEXT_RETRY_EPOCH` / `LAST_FAILURE_EPOCH`，**4 个全在白名单** |
| 耦合测试 | 仅 1 个 `test-freely-execution-network-failure-classification`（3 处 grep 格式断言） |
| 注入面 | `reason` 是日志派生字符串，写进 heredoc 后被 `source` 读回 —— 与 R22 分支名注入同族 |

`tool_availability` 族更小（1 读 1 写、零测试耦合），但 `tool_load_availability_state` **没有任何调用方**，迁移它无法证明协议「被使用」，故选 execution-network。

## 方案方向

### 写侧：`write --kv`

- `persist_execution_network_state` 去掉 heredoc，改 `python3 "$STATE_FILE_PY" write <path> --kv KEY=VALUE`（4 次），值经 argv 传递、不拼进脚本体。
- 落盘 `KEY<TAB>json.dumps(value)`。`write_state` 自己 `mkdir(parents=True)`，原 `mkdir -p` 可删。

### 读侧：`values` 行接口

- 两处 `source` 全删。单键读者用命令替换 `next_retry_epoch="$(python3 ... values ... || true)"`；双键读者用 `{ read -r a || true; read -r b || true; } < <(python3 ... values ... || true)`。
- **不用 `mapfile`**（macOS bash 3.2 无）。`read` 加 `|| true` 是为了兼容「文件损坏 / 键缺失」时不让 `set -e` 终止 daemon；默认值语义（0）保持不变。

### 耦合测试改为格式无关

- 3 处 `grep -q '^KEY="value"$' "$STATE_FILE"` 改为 `[[ "$(read_state_value KEY)" == "value" ]]`，`read_state_value` 走 `state_file.py values`。
- **语义不变**（仍断言 reason 与 failure_count 写对），只是不再绑定文件格式；否则格式一改测试就假红。

### 逐族 AT 的计数断言改为单调守卫

- R23.11 的 AT 把 lint 计数写死 `== 54`，本轮降到 52 后它变红。这是**多轮迁移的固有缺陷**：每迁一族都会让上一族 AT 假红。
- 两处都改为 `0 < got < 上限`（上一族 `< 55`、本族 `< 54`），保留「严格低于上一轮基线」的语义且可持续；本族真正的守卫是静态断言（该族不再 `source`）。

## 被否决

- **先迁 manager_worker_launch**（恢复点建议）：11 键不在白名单 + 55 测试耦合，前置评审否掉，改 #4264 先补白名单再迁。
- **一轮迁完 54 处**：77 键白名单可能漏、位置格式需单独判定、无法逐族跑回归。
- **`to-shell` + source 中间文件**：仍引入 source 与临时文件生命周期；本族只需 1–2 个标量，行读更直接。
- **保留 grep 格式断言**：格式一改就假红，属于把实现细节当契约。
- **把绝对计数断言继续写死**：多轮迁移会反复假红。

## fidelity 基线

- RED 必须 source **真实 `runtime/freely`** 并调用真实 `persist_execution_network_state` / `execution_network_launch_block_active`，用 `marker=True` 证明旧实现真的执行注入。
- GREEN 必须证明：普通值往返且 block 判定成立、文件是 TAB+JSON、旧格式兼容、旧格式注入不执行、恶意值新格式逐字节且不执行、换行值被拒绝、全局 source 计数 54→52、耦合测试改为协议断言。
- 4 项 RED PASS 是守卫（普通往返、旧格式可读、协议模块本身的恶意值/换行行为），不是新功能。

## 价值判定

- 不过时：54 处状态 source 实测仍在，该族仍用 heredoc + `source`。
- 不重叠：R23.9 只建协议、R23.11 只迁 cooldown；#4264 补白名单；本轮是第二族真实迁移。
- 高价值：注入面来自日志派生字符串，属延迟触发；且给出「耦合测试如何随协议演进」与「逐族 AT 如何不互相拖红」两个可复制范式。

## 本轮自举发现（已独立立项 #4264）

`ALLOWED_KEYS` 注释声称「全量扫描」，实测漏 **21 个** heredoc/printf 写入键。后果不是「写不了新格式」，而是**兼容读取承诺失效**：`read_state` 对每一行（含 legacy `KEY=value`）都调 `_check_key`，任何含未登记键的存量状态文件一被协议读取就整份抛错，`values` 的失败在 shell 侧被 `|| true` 吞掉 → 值静默回落默认值。会阻塞后续 manager_worker_launch / loop_guard / test-gate 族。已用 `feedback` 立 `raw-20261110T084522Z` / GitHub #4264（P1），排进 goal。
