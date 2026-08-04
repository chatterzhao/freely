---
local_id: raw-20260721T223133Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '4070'
    url: https://github.com/chatterzhao/freely/issues/4070
    synced_at: ''
  gitee:
    issue_id: IK2WN2
    url: https://gitee.com/zhaoquan/freely/issues/IK2WN2
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/command-lifecycle-state-contract/raw-20260721T223133Z/issues/I-20260721T223133Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-21T22:31:56Z'
updated_at: '2026-07-21T22:57:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

生命周期命令存在两类相互关联的状态一致性缺陷：

1. `pr-create-guarded` 更新已有 PR 时，先执行要求本地 HEAD 等于远端 PR head 的 merge dry-run，再执行受控 push，导致 reviewer 修复提交无法通过封装命令更新已有 PR。
2. `wt-create` 拉取新 raw issue 后无条件把 `phase_state` 从 `proposed` 改为 `absorbed`，但此时尚无 `absorbed_into` 和 `canonical_issue_path`，形成非法状态。raw 元数据字段由多个命令零散增删，scan/gate 部分逻辑还以字段存在性而不是字段值和组合做判断。

## 目标

- `pr-create-guarded` 动态发现所有配置平台，按 absent/behind/equal/ahead/diverged 分类；仅 absent/behind 通过 adapter 受控 push；创建、更新或复用各平台 PR；ahead/diverged fail closed，并给出 Freely/adapter 恢复指令；聚合全部平台结果。
- 新 raw issue 从 `feedback` 阶段形成完整、固定顺序的扁平 metadata 字段集和初始值；后续命令只更新字段值，不增删字段、不改顺序。
- `wt-create` 只填写工位相关值，不得把 `proposed` 提前变为 `absorbed`。只有形成 canonical I-* issue 时才能原子写入 `phase_state: absorbed`、`absorbed_into`、`canonical_issue_path` 等配套值。
- scan、gate、sync、PR、closeout 等消费者按字段值及跨字段合法组合判断；字段存在但值为空不得视为状态成立；非法组合 fail closed。
- 现有历史 raw 文件不批量迁移；消费者兼容旧格式，新建 raw 严格使用完整 schema。

## 验收

1. 已有 PR 在本地新增 reviewer 修复提交后，可直接重跑 `freely pr-create-guarded`，由所有配置平台 adapter 完成受控更新。
2. 新 feedback 创建的 raw issue 物化后字段全集、顺序和显式空值稳定。
3. wt-create 后 raw 仍为 `proposed`；未形成 canonical issue时不得出现有效 absorbed 状态。
4. `absorbed` 缺少吸收目标或 canonical 路径、平台字段只有键没有有效值等组合被 scan/gate 拒绝。
5. RED/GREEN 覆盖创建、拉取、工位、scan、PR 更新、多平台聚合及旧格式兼容。

## 治理边界

已由 Freely 封装的 issue/worktree/push/PR/merge/closeout 生命周期操作必须使用 Freely；本地观察、可写工位提交及 test-pre-merge 本地同步不属于平台生命周期绕过。force、no-verify、禁用 hooks、受保护分支直接提交永久禁止。