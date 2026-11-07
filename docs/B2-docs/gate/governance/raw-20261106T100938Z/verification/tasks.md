# Tasks: 补齐打包 allowlist 运行时必需文件并建立防复发检查
- issue_id: I-20261106T100938Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261106T100938Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `test-package-runtime-allowlist-parity`（static + behavior），在未修改真源上跑确认 RED；修正 ROOT_DIR 层级、静态断言收集全部结果、把守卫顺序断言改为不依赖新 hook 的独立断言，让 RED 精确反映缺陷。
- [x] T2: 实现前评审：逐条核对 17 个顶层 tracked 文件的运行时引用点，实证区分 SELF_ROOT 真源与 repo-scoped 清单（诚实修正 issue 正文）；确认 R5 checker 职责边界、输出守卫顺序、#4157 收敛意图、#4201/#4194 不夹带。
- [x] T3: `package-allowlist.txt` 显式新增 5 个运行时必需文件，3 个纯文档经评审不随包。
- [x] T4: 新增只读 `package-runtime-file-parity.py`，扫描范围排除 tests / 治理文档 / `__pycache__` / 自身；无 git 元数据时降级。
- [x] T5: `bin/freely-package` 在 R5 parity 之后、`rm -rf` 之前接入检查，脚本缺失时兼容跳过。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log；10 个回归全 PASS，9 个以未修改 develop HEAD 做基线对比零新增失败；核对输出差异仅为行号/临时路径/计时数字。
- [x] T7: 复用 `gate/governance` story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T8: 按封装命令收口：`issue-sync close` 关双平台副本 → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7, T8 | AT-001 |
