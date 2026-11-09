# Implementation Decision Note
- issue_id: I-20261103T132548Z-A
- decision: 测试证据格式与校验收口到 `quality/test-evidence.py`（8 字段 + sha256 + HEAD 绑定）；只有 `freely test-gate run` 的真实执行能产出可信结论；门禁 fail-closed；新增 `bin/test-all` 聚合入口并替换两个 CI 桩
- why_this: 手写三行 `test-gate.env` 即可让 `pretests-retirement-gate` 返回 0（本轮隔离夹具实测 rc=0）；唯一 Gitee CI 打印固定成功行且 `fix/*` 不触发，GitHub workflow 无任何 `run:`；R12.5 只解决了「谁写」，没解决「写的是不是真的」。
- alternatives_considered: ①继续信任 `record --status completed`（仍是自述）；②一次跑全部 575+ 测试（预存红让 CI 永久红、信号归零）；③把证据写进提交信息（跨工位不可解析）；④上 PKI 签名（本机无 PKI，hash+HEAD 绑定已足够防手写）。
- boundary_non_goals: 不改 `test-gate record` 的写入语义与 dispatcher 兼容；不改 `pretests-retirement-gate` 的 closeout / issue 解析；不批量执行未 onboarding 的 575 个测试；不修改任何平台 issue 生命周期语义；**`pretests-gate` 从「artifact_ref 本地存在」升级为「在 PR diff 中且 hash 匹配」未纳入本轮验收标准**（见 residual_risk）。
- residual_risk: ①`EVIDENCE_FILE` 记录的是 test 工位内的绝对路径，跨机器/跨工位不可移植；本仓门禁都在同一台机器的工位上运行，可接受，若引入远端 runner 需改为相对 worktree 的路径。②`freely evidence add` 只做 `git add -f` + 本地 manifest，`pretests-gate` 仍未校验「证据文件是否真的在当前 PR diff 中且 hash 匹配」——issue 修复方案第 4 项的后半段，需另开轮次收口。③`bin/test-all` 白名单只有 9 个（CI 5 个），575 个未 onboarding 测试仍是债务，需渐进 triage。④`test-gate run` 用 `bash -c <command>`，命令内容由调用方提供；若调用方故意跑 `true` 仍能自证，但至少退出码与证据文件是真实进程产物，比三行手写强一个量级；后续可把 `--command` 收口到 pre-tests.md 声明的测试集。⑤`record` 现在写出的是 legacy 3 字段格式，门禁会拒绝；所有后续轮次必须改用 `test-gate run`（已写入 goal 恢复点）。
- verification: AT-001 develop 基线快照 RED `4 ok / 16 failed` → 工位 GREEN `20 ok / 0 failed`；17 个相关回归 16 项 MATCH + 1 项已解释的活跃平台状态 DIFF（`20261108T134701Z` Gitee-only，R59 待补）；`bin/test-all --ci` 退出 0；真机：本轮收口用 `freely test-gate run` 写合法证据后门禁放行。
- self_bootstrap_findings: ①用隔离 git 夹具真实驱动门禁，复现手写三行 env 放行；②实现过程中发现 macOS bash 3.2 无 `mapfile`，已改为可移植写法；③发现 `.gitee-ci.yml` 注释若保留固定成功行字符串会让静态断言误判，已改写注释。未发现其他未被 open issue 覆盖的新缺陷。

## Implementation Decision Note
- decision: 单一真源证据格式 + 真实 runner + 门禁 fail-closed + 聚合 runner + 真实 CI
- why_this: 手写三行即可通过门禁，CI 从不执行测试
- alternatives_considered: 信任自述 / 全量跑 / 写进提交信息 / PKI
- boundary_non_goals: record 语义、closeout、批量 onboarding、pretests-gate diff 校验均不动
- residual_risk: 绝对路径证据、pretests-gate diff 校验未做、575 个 known-broken、command 仍由调用方提供、后续轮次必须用 test-gate run
