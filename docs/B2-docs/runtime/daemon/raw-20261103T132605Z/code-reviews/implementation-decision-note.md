# Implementation Decision Note
- issue_id: I-20261103T132605Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132605Z/issues/I-20261103T132605Z-A.md
- decision: 用 `_FREELY_IS_SOURCED` 区分执行/被 source；sourced 时不设 `-euo pipefail`、缺库返回 `FREELY_LIB_LOAD_ERROR` + `return 1`；直接执行保持原行为（`set -e` + `false` 以 1 退出）；`stop_project_runtime` 改返回码
- why_this: 4 个控制面脚本 source 本库；缺一个库文件 → watchdog/dispatcher/promotion gate/supervisor 同时退出，supervisor 30 秒后拉停 daemon；且 sourcing 会把 `-euo pipefail` 强加给调用方。
- alternatives_considered: ①只把 `exit 1` 换 `return 1`——顶层 return 在直接执行时非法，且不改 `set -e` 仍会杀掉调用方；②彻底移除 `set -euo pipefail`——直接执行失去严格模式；③子 shell 加载库——函数进不了调用方；④本轮顺带搬 skills 库、拆 lib——issue 明确非目标，且会让「行为不变」不可验证。
- boundary_non_goals: 不拆 26,823 行单体；不迁 Rust；不改 551 个测试语义；不搬 skills 库；不动 `main` 的 `BASH_SOURCE` 守卫。
- residual_risk: ①sourced 时不再有 `set -e`，库函数内部的失败要靠显式返回码兜住——已有 `|| return 1` 的点覆盖，但未逐函数审计；②`false` 依赖「直接执行时 `set -e` 已生效」，若将来改成默认不开 `-e` 则缺库会静默继续；③`_FREELY_IS_SOURCED` 是文件级快照，若库被嵌套 source 需重新评估。
- verification: AT-001 基线 RED `1 ok / 5 failed`（`(34,'exit 1')`、`(41,'exit 1')`、happy-path source 无输出）→ 工位 GREEN `6 ok / 0 failed`（`OPTIONS_UNCHANGED`、`SURVIVED rc=1`）；`bin/test-all --ci` 与 4 个相关测试全绿。
- self_bootstrap_findings: ①基线在隔离夹具里连 `source` 都成功不了（输出为空），说明「source 即死」比 issue 描述的更直接；②issue 要求「库加载段 0 处 exit」与「直接执行仍 exit 1」在字面上冲突，用 `set -e` + `false` 同时满足两者；③把 `-euo pipefail` 也纳入 sourced 豁免是必须的——否则调用方仍会被 `-e` 杀掉，「不终止调用方」不成立。

## Implementation Decision Note
- decision: `_FREELY_IS_SOURCED` 分支 + 错误变量/返回码 + 库函数返回码
- why_this: source 即副作用/即死，会连带拉停 daemon
- alternatives_considered: 只换 return / 移除 set -e / 子 shell / 顺带拆 lib
- boundary_non_goals: 单体拆分、Rust 迁移、测试语义、skills 库、main 守卫均不动
- residual_risk: sourced 无 -e 需显式返回码、false 依赖 -e、sourced 快照
