---
raw_id: raw-20261110T060553Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（develop `ea9f5b38c` 实测）

| issue 证据 | 实测 | 结论 |
|---|---|---|
| 状态文件被 `source` | `grep 'source ".*state' freely` 命中 **55 处**（原报 20） | 更严重 |
| 状态写入点 | `cat >"$state_file" <<EOF` / `printf 'KEY=%s\n'` 至少 15 处 | 成立 |
| 正面先例 `load_meta_env_snapshot` | 定义在 `freely:6694`，白名单 awk 解析 | 成立 |
| 键集合 | 全量扫出 **77 个**状态键 | 可作为显式白名单 |
| 位置格式 | `printf '%s|%s\n'` 等不按 KEY=value，需单独判定 | 增加迁移复杂度 |

55 处读的形态：`source "$state_file"` 22、`source "$(workcell_state_file ...)"` 20、`manager_worker_launch_state_file` 7、带 `|| true` 4、`session_state_file` 2；另有 **39 处非状态 source**（库加载、identity 文件）绝不能误改。

## scope 收敛：本轮只做第一阶段

issue 自己写的是「逐组迁移，每组单独提交并跑对应回归」。一轮改完 55 读 + 15 写会让「行为不变」无法验证（77 个键、部分位置格式、20+ 下游读取依赖）。按项目既有收敛模式（R22 四面做两面、R23.5 拆状态文件协议），本轮做**可独立验证的基础设施**：

1. `runtime/state_file.py` —— 安全协议单一所有者
2. `bin/check-state-file-sources` —— 冻结边界（55 处只降不升 + 禁止 eval/exec）
3. AT-001 —— 注入 PoC + round-trip + 未知键 + 兼容不展开 + to-shell 惰性

**逐组迁移 55 读 / 15 写** 拆出 `raw-20261110T074344Z`（P1），已排进 goal。

## 方案方向

### 协议格式

- 新：`KEY<TAB>json.dumps(value)` 单行。值含 tab/换行/`"`/`$()`/反引号都只是 JSON 字符串，不是 shell。
- 兼容旧：`KEY=value` / `KEY="value"`，按第一个 `=` 切分、去一层引号、**其余原样保留**（不展开 `$`、不 eval）。这是滚动升级的关键：迁移期间旧状态文件必须可读，不得要求人工清空 `.freely/run/`。
- 白名单：`ALLOWED_KEYS`（77 键，来自 develop 全量扫描）。未知键读写都抛 `StateFileError`——新增状态键必须登记，把状态键变成契约。
- `to-shell`：输出 `KEY=<shlex.quote(value)>`，供第二阶段 `runtime_state_load` 生成惰性赋值；即便值含 `$(...)`，被引用后也不会执行。

### 被否决

- **一轮把 55 处 source 全替成 helper**：白名单可能有遗漏键、部分文件是位置格式，且 `source` 安全中间文件仍需评审；应逐组迁移并各跑回归。
- **`printf %q` 后继续写 shell 赋值**：写入侧仍是 shell 代码，无法排除未来新值触发注入。
- **拒绝读旧格式**：会要求人工清空 `.freely/run/`，违反 issue 的不退化边界。
- **无白名单、接受任意 KEY**：等于没有状态键契约，拼写错误会静默产生新状态。

## fidelity 基线

- RED 必须有**可执行 PoC**：`LAST_EXIT_REASON="$(touch marker)"` 经 `source` 真的创建文件；若 PoC 不执行，测试只是 grep。
- GREEN 必须由新 reader/writer 证明「含 `"`、换行、tab、`$()`、反引号的值逐字节相等且不执行」。
- 兼容断言必须是「读回 `$HOME $(id)` 原样字符串」，不是「没报错」。

## 价值判定

- 不过时：55 处 source、15 处写实测仍在。
- 不被覆盖：#4156 只修 argv/sed；#4246 只修 TSV + lint；#4239 是 pkill；#4254 是派发/SSE；均不涉及状态文件协议。
- 高价值：AI 生成的摘要/reason/分支名会写进状态文件，下一轮巡逻读回时执行——与 R22 的分支名注入同族，只是延迟触发。
