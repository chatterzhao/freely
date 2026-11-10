# Implementation Decision Note
- issue_id: I-20261110T081029Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T081029Z/issues/I-20261110T081029Z-A.md
- decision: 第二族选 execution-network-recovery.env（否掉恢复点建议的 manager_worker_launch）；写侧 `write --kv`、两读者 `values`、耦合测试改协议断言、逐族 AT 计数断言改单调守卫
- why_this: 恢复点建议的族经前置评审发现 11 键全不在白名单 + 55 个测试直接构造/source 旧格式，硬迁会让「行为不变」无法验证且协议直接抛错。改选最小真实活跃族（4 键全在白名单、1 个耦合测试、reason 为日志派生字符串），并顺手修掉「每迁一族就把上一族 AT 拖红」的流程缺陷。
- alternatives_considered: ①先迁 manager_worker_launch——白名单缺键 + 55 测试耦合，否掉，改 #4264 先补白名单；②一轮迁完 54 处——无法逐族跑回归；③`to-shell` + source 中间文件——仍引入 source 与临时文件生命周期；④保留 grep 格式断言——格式一改就假红，把实现细节当契约；⑤绝对计数断言继续写死——多轮迁移反复假红。
- boundary_non_goals: 不改键名与语义；不动其余 52 处状态 source 与 39 处非状态 source；不改 `load_meta_env_snapshot`；不改协议既有接口与白名单（那是 #4264）；不删除既有状态文件。
- residual_risk: ①全局仍有 52 处状态 source，注入面按族递减但未清零；②`values` 对含换行值报错，后续族若值含换行须改用 JSON `read`；③每次读状态起一个 python 子进程，巡逻频率高时有开销；④本族 `--kv` 值若以 `-` 开头会被 argparse 当选项，但 4 个值分别是枚举字符串与整数，不构成风险；⑤#4264 未修前，含未登记键的存量文件一旦被协议读取会抛错（本族不含这些键，故未触发）。
- verification: AT-001 基线 RED `4 ok / 7 failed`（`marker=True`，旧实现真的执行注入）→ 工位 GREEN `11 ok / 0 failed`；lint 计数 54→52；耦合回归 + 两族 AT + 5 个相关测试 + `test-all --ci` 全绿。
- self_bootstrap_findings: ①`ALLOWED_KEYS` 注释声称「全量扫描」却漏 21 个 heredoc/printf 键，导致「兼容读取旧格式」承诺在后续族失效——已独立立项 #4264，不夹带；②55 个测试直接构造并 `source` 状态文件，说明 manager_worker_launch 族的迁移成本远高于 issue 估计（7 读 → 实测 14 读）；③上一族 AT 写死绝对计数，本轮迁移即变红——改为单调守卫；④`tool_availability` 族的读函数无任何调用方，迁移它无法证明协议被使用。

## Implementation Decision Note
- decision: execution-network 族迁移 + 逐族 AT 单调守卫 + 耦合测试格式无关
- why_this: 建议族不可迁，需选最小可验证族并修流程缺陷
- alternatives_considered: 建议族 / 一轮全替 / to-shell+source / 保留 grep / 绝对计数
- boundary_non_goals: 键名、其余 52 处、非状态 source、meta.env、协议接口、既有状态文件均不动
- residual_risk: 注入面未清零、换行值、python 子进程、argv 前导 -、#4264 未修
