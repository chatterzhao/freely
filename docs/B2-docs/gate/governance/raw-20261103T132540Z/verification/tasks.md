# Tasks: 合并门禁读 verdict，评审判定不再默认通过
- issue_id: I-20261103T132540Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261103T132540Z/verification/pre-tests.md

## 任务分解

- [x] T1: 逐行复核三处消费者与写侧默认值，普查 401 份真实 review 文档的 verdict 写法分布，确定历史兼容边界。
- [x] T2: 编写 AT-001（19 项静态断言 + 10 个行为场景 + 401 份语料普查），在基线快照上确认 RED。
- [x] T3: 建单一 verdict 真源 `review_verdict.py` + `review-verdict.sh`（解析 + 合并决策）。
- [x] T4: 改读侧 `pr-merge-guarded` 为读内容→共享判定→非 pass 阻断；判定函数缺失时 fail-closed。
- [x] T5: 改写侧 `bin/pr-review-guarded`：默认 `needs_changes`、覆盖三值校验 + 强制 reason + reason 落痕、manual 模式拒绝覆盖。
- [x] T6: 改审计侧 `governance-merge-gate`：`completed` 不再裸 continue，要求绑定 review 产物 + verdict=pass，显式非 pass 不可翻盘。
- [x] T7: 跑 GREEN、回归基线对比零新增失败、真实工位反向探针与真实受控合并。
- [x] T8: 补齐 B1/B2 治理文档、milestone、IDN；按封装命令收口（`pr-create-guarded` → 独立 review → `pr-merge-guarded` → `wt-close` → 打包 → 更新 goal/memory）。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5, T6 | AT-001 |
| T7, T8 | AT-001 |
