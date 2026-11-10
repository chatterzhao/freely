# Implementation Decision Note
- issue_id: I-20261103T132614Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132614Z/issues/I-20261103T132614Z-A.md
- decision: 新增 `runtime/paths.sh` 作为 tool-registry 路径唯一所有者并让缺失 fail-closed；`raw_key_canon.py` 增加 legacy 规范化与 CLI，`wt-create` 入口改调它；本轮只做 #4154 的面 1+2
- why_this: `bin/deploy-skills:72` 与 `runtime/freely::_init_acp_tool_setup` 各拼了一份不存在的 `scripts/runtime/tool-registry.toml`，且都静默降级（fallback claude / warn+return 0）；`wt-create:279-284` 接受 legacy raw key 只告警，分支名变成 `raw-20261103-1326`，下游全部 `T...Z` 提取器得到空 raw_key，daemon 据此 fail-closed。两类都是「同一值多副本」，不编译失败、不测试失败，只表现为「工具莫名不部署」「工位建了但 daemon 拒启动」。
- alternatives_considered: ①只在两个错误点写回正确字面量——仍是两份，下一处新增调用点会再漂移；②在 wt-create 内联第二套正则——正是本条要消除的成本；③直接拒绝 legacy 格式——破坏历史工位/分支，成本转给用户；④拆新 raw 承接面 3–6——队列已有 #4179/#4166/#4161，重复排期且用户明确不要无限拆；⑤改 `worktree-common.sh` 第三套正则——超出入口规范化的必要范围。
- boundary_non_goals: 不改 `raw_key_canon` 的 opaque key 语义；不改 `worktree-common.sh`；不改 `platform-adapter.py`、Rust/TS 契约、错误模型；`--tools` 与 `--dry-run` 语义不变；不创建真实工位/不写工具目录/不访问平台。
- residual_risk: ①`paths.sh` 成为 `runtime/freely` 的 source 依赖，安装态旧包若未带该文件会走 `_freely_lib_missing`（fail-closed，可诊断）；②注册表存在但无已安装工具时 `deploy-skills` 打印说明并 `exit 0`，属合法空集而非猜 claude，但调用方若依赖「总是部署 claude」需显式 `--tools`；③legacy 4 位时分补 `00` 秒，可能与真实秒级时间有 59 秒内偏差——raw key 只用于身份，不用于排序；④`wt-create` 新增 canon 依赖，任何复制脚本的隔离夹具必须一并复制（本轮已补两个既有夹具）；⑤local `test-all` 既有 `test-github-label-autocreate.py` 失败未处理。
- verification: AT-001 基线 RED `1 ok / 12 failed` → 工位 GREEN `13 ok / 0 failed`；首轮 3 项失败由行为断言暴露（注释误命中、present rc 假设错误、分支名 legacy 需二次提取），修正后全绿；13 项回归 + 2 lint + `test-all --ci` 全绿。
- self_bootstrap_findings: ①正文的 5 个面里有两个已过时/被他 issue 覆盖，开工前重新普查避免做重复工；②`deploy-skills` present 场景不能用 rc=0 做断言——注册表里有未支持的 `cline`，脚本本来就 rc=1；改成「输出里出现 cline」才能区分「真的读了注册表」与「fallback claude」；③负向静态扫描会把注释里的旧路径算作命中，修复说明里不要写完整错误路径；④新增依赖必须同步更新隔离夹具，否则回归会把「夹具缺文件」误报成产品回归（与 R18 同类）。

## Implementation Decision Note
- decision: paths.sh 单一所有者 + canon 入口规范化，只做面 1+2
- why_this: 两处静默降级 + raw key 空值导致 daemon 拒启动
- alternatives_considered: 写回字面量 / 内联第二套正则 / 拒绝 legacy / 拆新 raw / 动第三套正则
- boundary_non_goals: opaque key、worktree-common、platform-adapter、Rust/TS、错误模型均不动
- residual_risk: paths.sh 依赖、空集 exit 0、legacy 秒补零、夹具依赖、既有 known-broken
