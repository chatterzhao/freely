# Implementation Decision Note
- issue_id: I-20261104T075857Z-A
- issue_path: docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/issues/I-20261104T075857Z-A.md
- decision: 新增 `contracts/cross-process/`（契约 + 单页文档）、`quality/cross_process_boundary.py`（三态边界 runner）、`bin/check-cross-process-contract`（0/1/2）、AT-001；进 CORE/CI_CORE；epics-map 注册 story。**不改 `state_file.py`、不改任何 gate、不动 22 处夹具。**
- why_this: 三类跨边界失败以前不可区分（缺失→空串、类型→强转、超时→普通失败），把语义写成可执行断言比逐点改测试夹具更能降低真实风险，且零业务语义变化、可立即被 CI 守护。
- alternatives_considered: ①把 22 处 `source *.env` 全量归零——多数是测试夹具，改了不减少生产风险还拖累夹具可读性；②逐个复核 33 处 `|| echo`——需逐点判断「吞错 vs JSON 回退」，一轮内无法给出可复现 RED；③直接改 `state_file.values()` 让缺失 key 报错——会改变 runtime 行为并触发 R27 单测门禁，影响面超出本轮，留后续。
- boundary_non_goals: 不改 runtime 目录、不改 `bin/freely`/`bin/issue-sync`、不改 gate 逻辑、不动 22 处夹具、不逐点复核 33 处 `|| echo`、不校验每个消费方的调用形态。
- residual_risk: ①`values()` 缺失 key 仍返回空串，需消费方主动在 `required_keys` 登记才受保护；②lint 只校验 producer 存在与声明完整性；③契约值来自对 `state_file.py` / `pr_body.py` 的人工提取，后续若这些文件改语义需同步（c14 已交叉断言退出码，其余靠 review）；④`known_gaps` 三条开放，需后续轮次关闭。

## 为什么退出码要复用既有编号

契约声明 `3` = 契约违规，与 R27 的 `pr_body.REFUSE_EXIT = 3` 同义；`2` = 不适用/真源缺失，
与 `bin/check-skill-frontmatter`、`runtime_red_gate` 的 SKIP=2 同义。新增一套编号会让
「3 是什么意思」随文件而变，所以 AT 的 c14 把这条交叉一致性做成了断言。
