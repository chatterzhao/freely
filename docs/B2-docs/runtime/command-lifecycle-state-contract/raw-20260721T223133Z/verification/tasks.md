# Tasks — command lifecycle state contract

- issue_id: I-20260721T223133Z-A
- issue_path: docs/B2-docs/runtime/command-lifecycle-state-contract/raw-20260721T223133Z/issues/I-20260721T223133Z-A.md

## B2

- [x] T1：确认 feedback、wt-create、promotion、pr-merge 与 wt-close 历史职责。
- [x] T2：确定 strict-v1 字段全集、legacy 兼容和状态迁移表。
- [x] T3：定义多平台五态、零副作用预检与入口执行顺序。
- [x] T4：定义单元、集成、端到端和真实环境验收。

## RED

- [x] T5：证明 `wt-create` 仍包含 reopen/生命周期写入路径。
- [x] T6：证明 `pr-create-guarded` 仍在 guarded platform update 前执行 merge dry-run。
- [x] T7：证明 strict schema、promotion 原子性和 legacy 只读兼容的缺口。
- [ ] T8：记录全部 RED 输出与独立 review。

## Dev

- [x] T9：收敛 raw metadata 共享合同并接入生产者、迁移器和消费者。
- [x] T10：移除 wt-create 生命周期写入，只保留工位职责。
- [x] T11：完成 platform registry 五态观测、受控同步和 PR ensure 聚合。
- [x] T12：重排 pr-create 入口为 platform update 后 merge dry-run。
- [ ] T13：写 implementation evidence 与独立 dev review。

## GREEN / Promotion

- [x] T14：feature-local 全部 GREEN。
- [x] T15：test-pre-merge 集成、回归与命令入口 E2E 全部 GREEN。
- [ ] T16：guarded PR、六维 review、CI 与 guarded merge 完成。
- [ ] T17：在暂停的 agent-identity continuation 更新 PR #4069，记录真实多平台结果。
- [ ] T18：closeout 清理工位与平台 issue。
