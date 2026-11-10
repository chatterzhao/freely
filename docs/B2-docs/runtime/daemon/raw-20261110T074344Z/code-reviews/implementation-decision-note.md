# Implementation Decision Note
- issue_id: I-20261110T074344Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T074344Z/issues/I-20261110T074344Z-A.md
- decision: 逐组迁移的第一族选 cooldown-state.env，读侧走 `values` 行接口、写侧走 `--kv` argv 接口，删掉 1 处 `source`
- why_this: R23.9 交付了协议却零调用点，注入面未关闭；需要一个最小完整族把协议「用起来」，并给出可复制范式与边界数字下降。
- alternatives_considered: ①一次性替换 55 处——77 键白名单可能漏、位置格式需单独判定、无法逐族跑回归；②`to-shell` + source 中间文件——仍引入 source 与临时文件生命周期；③`eval`/命令替换解析 JSON——把外部值带回 shell 代码路径；④改键名或改下游——违反不退化边界。
- boundary_non_goals: 不改键名与语义；不动其余 54 处状态 source 与 39 处非状态 source；不改 `load_meta_env_snapshot`；不动协议既有接口语义。
- residual_risk: ①仍有 54 处状态 source，注入面按族递减但未清零；②`values` 对含换行值报错，若后续族的值可能含换行需改用 `read` JSON 接口；③每次 `_read_cooldown_state` 起一个 python 子进程，巡逻频率高时有开销（该族原本是纯 shell `source`）；④白名单 77 键来自 develop 扫描，后续族若出现新键需扩充。
- verification: AT-001 基线 RED `2 ok / 6 failed`（`marker=True` 两次，旧实现真的执行注入）→ 工位 GREEN `8 ok / 0 failed`；lint 计数 55→54；R23.9 协议 AT + 5 相关测试 + `test-all --ci` 全绿。
- self_bootstrap_findings: ①macOS 自带 bash 3.2 无 `mapfile`，用 `{ read -r a; read -r b; } < <(...)` 才跨平台；②旧实现 `unset COOLDOWN_SWITCH_*` + `source` 的下游只有 `CROSS_TOOL_SWITCH_*`，因此删掉 `COOLDOWN_SWITCH_*` 变量不会破坏其他代码；③`--kv` 用首个 `=` 切分，值内含 `=` 安全，但值以 `-` 开头会被 argparse 当选项——本族值是时间戳/索引，不构成风险。

## Implementation Decision Note
- decision: cooldown 族首个迁移，values + --kv，source 55→54
- why_this: 协议零调用点，需要可复制的逐族样板
- alternatives_considered: 一次全替 / to-shell+source / eval / 改键名
- boundary_non_goals: 键名、其余 54 处、非状态 source、meta.env、协议既有接口均不动
- residual_risk: 注入面未清零、换行值、python 子进程开销、白名单扩充
