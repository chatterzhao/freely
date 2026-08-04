# PRD — command lifecycle state contract

- issue_id: I-20260721T223133Z-A

## Goal

让 raw metadata 与 existing-PR 更新都通过显式状态合同执行，消除命令按键存在性、错误阶段副作用或远端旧 head 作出决策的情况。

## 用户可见结果

1. 新 raw 在平台创建时就具有完整 v1 schema；拉入工位后字段集合与顺序不变。
2. `wt-create` 不 reopen、不 absorbed、不补生命周期字段。
3. promotion 只有在 canonical child 有效时才形成完整 absorption；closeout 不修补历史状态。
4. 已有 PR 存在 reviewer fix 时，重跑 `freely pr-create-guarded` 会先通过各平台 adapter 同步 source branch，再执行 merge dry-run。
5. 任一配置平台不安全或失败时，整体失败且不建议 raw git/gh 恢复动作。

## 模块关系

```text
raw_metadata_contract
  → feedback payload
  → raw-issue-pull materialization
  → promotion transition adapter
  → normalized consumer view

pr_lifecycle
  → platform registry observations
  → all-platform transition plan
  → adapter-controlled effects
  → aggregate result

pr-create-guarded
  → governance preflight
  → guarded platform update
  → synchronized-head merge dry-run
```

## 数据合同

- strict v1：字段全集、顺序、类型、枚举和跨字段组合全部校验。
- legacy：只产生 normalized view；读取不重写。
- metadata 写入：先生成候选状态并校验，再同目录原子替换。
- 多平台：先全量观测；存在 unsafe state 时零副作用。

## 非目标

- 不批量迁移历史 raw。
- 不改变 `feedback` 的 platform-only 边界。
- 不让 `wt-close` 成为 metadata 修复器。
- 不降低真正 merge 的 source-head equality 门禁。
- 不在 runtime 超大单体中新增业务规则；入口只编排独立模块。

## Dev-Loop Handoff

1. 先运行入口顺序、wt-create 副作用、schema/transition 与五态聚合 RED。
2. 只在 RED 证据成立后修正入口编排和各生命周期 adapter。
3. metadata 与 PR 生命周期分别实现、分别测试，通过命令入口集成测试合流。
4. GREEN 后在 test-pre-merge 工位运行回归，再通过真实 paused agent-identity PR 更新完成 post-merge dogfood。
