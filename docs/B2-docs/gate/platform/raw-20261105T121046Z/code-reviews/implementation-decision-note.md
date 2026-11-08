# Implementation Decision Note
- issue_id: I-20261105T121046Z-A
- decision: 安装态身份收口到唯一真源 `quality/install_state.py`（hash 清单 + 一致性检查 + 原子激活）；`freely-package` 写清单并支持 `--version auto --activate`；develop 合并 followthrough 幂等重打包；`freely doctor` 输出结论
- why_this: 合并 develop 后安装态不重新打包，且没有任何检查能发现落后/悬空；实测 `latest` 的 `FREELY_PACKAGED_FROM=444985f50` 落后于 develop `c1949aa24`，PATH 可能静默命中旧版 runtime 与旧门禁，已修缺陷在新会话「复活」。
- alternatives_considered: ①只在 doctor 打印提示不落 hash 清单（无法机器证明文件一致）；②每次调用 freely 都自动打包（副作用不可控）；③软链项目树替代安装态（打包产物失去独立可复现性）；④无条件清空 `~/.freely/versions/*`（违反个人目录安全边界、破坏回滚）；⑤激活时覆盖健康链接（会破坏 R5.5 的开发态规避）。
- boundary_non_goals: 默认打包（不带 --activate）行为不变；门禁判定、raw 生命周期、平台写语义不动；不实现 `freely install`（issue 修复方案第 3 项的文档缺口另见残余风险）；不修改任何平台 issue。
- residual_risk: ①followthrough 的打包源取 `${PROJECT_ROOT:-git rev-parse --show-toplevel}`，可能是调用它的工位而非主仓；已用 `FREELY_PACKAGE_FROM=<develop HEAD>` 显式标记版本来源，且 doctor 的 hash 清单会检出内容不一致 —— 但「打包了工位内容」本身仍可能包含未提交改动，故 followthrough 前若有未提交文件应先提交（本轮流程已满足）。②打包失败只告警不阻塞合并（合并已提交、不可回滚），需由 `freely doctor` 或下次合并发现；不会静默，会打印修复指令。③`KEY_FILES` 固定 6 个入口文件，新增关键真源需同步扩展，否则该文件漂移不会被检出（目录内容由入口间接覆盖）。④`~/.local/bin/freely` 若已健康指向项目真源则不重建，安装态版本目录本身不挂到 PATH —— 这是刻意保留开发态，不是遗漏。⑤`bin/freely` 注释承诺的 `freely install` 与 `~/.zshrc` 的 `@freely-dev-path` 标记仍未实现/清理，属 issue 修复方案第 3 项，需另立 raw 单独评审（不夹带本 PR）。
- verification: AT-001 develop 基线快照 RED `2 ok / 21 failed` → 工位 GREEN `23 ok / 0 failed`；21 个相关回归 worktree/baseline 退出码全 MATCH（2 项首轮 DIFF 已证实为基线快照缺文件，补齐后 MATCH）；真机合并后 followthrough 自举刷新安装态。
- self_bootstrap_findings: ①开工前只读检查复现症状（落后 + 无清单）；②发现 `git archive -- bin docs` 快照不含 3 个 allowlist 路径，导致 2 个打包测试假 DIFF —— 已补齐快照复验，并写入回归日志 NOTE；③发现 followthrough 从工位调用会写错 `FREELY_PACKAGED_FROM`，已加 `FREELY_PACKAGE_FROM` 通道。另发现「`freely install` 文档与实现脱节」仍是 open 缺口，按约定**不夹带**，用 feedback 另立 raw 排进 goal（见 v4 队列新增项）。

## Implementation Decision Note
- decision: 唯一真源 install_state + hash 清单 + 原子激活 + 合并幂等重打包 + doctor 结论
- why_this: 安装态落后一个 merge 且无任何检查，PATH 可能命中旧版
- alternatives_considered: 只打印提示 / 每次调用都打包 / 软链项目树 / 清空安装目录 / 覆盖健康链接
- boundary_non_goals: 默认打包、门禁、生命周期、平台写语义均不动
- residual_risk: 打包源可能是工位、打包失败只告警、KEY_FILES 固定 6 个、健康链接不重建、freely install 文档缺口另立 raw
