---
schema_version: '1'
local_id: raw-20260725T030511Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260725T030511Z-A'
platform_ids:
  github:
    issue_id: '4074'
    url: https://github.com/chatterzhao/freely/issues/4074
    synced_at: ''
  gitee:
    issue_id: IK3X79
    url: https://gitee.com/zhaoquan/freely/issues/IK3X79
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-25T03:05:14Z'
updated_at: '2026-08-04T07:55:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-08-04T07:57:00Z'
closeout_note: ''
---

# feat: reconcile configured raw replicas before lifecycle transitions

workflow_kind: feature

## 问题

配置的平台 raw 副本目前不能作为可靠的生命周期真相：GitHub/Gitee 的发现结果可能不完整，空匹配被当作有效记录，扫描会把适配器读取失败降级为零条目。由此 `wt-create` 可能在创建临时工位后才失败，PR 和 close 流程也无法对 local B1 与全部平台副本执行同一只读一致性检查。

## 目标

建立配置驱动的只读 raw 副本发现与 canonical reconciliation gate。`wt-create` 必须在创建前比较全部已配置平台的同一 raw；后续 PR create/review/merge/close 复用同一 gate。差异只能由独立、可审计、带版本保护的 resolution 路径处理，gate 本身不得写入平台或本地元数据。

## 验收边界

- 平台枚举返回完整的 title、body、state、labels、comments、updated_at 与版本信息，并区分 empty、unknown、degraded。
- 单平台、多平台、缺副本、内容差异、分页失败和平台不可达均有确定且 fail-closed 的结果。
- 生命周期命令不复制平台比较逻辑，也不在 gate 中隐式同步。
- 扫描在 DB 或平台不可用时输出 unknown/degraded，不把失败解释为空清单或 worker 死亡。
- resolution 使用明确的 create、条件 edit 与幂等 comment，重新实时读取确认一致后才更新基线。

## 不包含

不在本项内实现 test companion 同步，也不批量关闭历史 raw；它们在本能力合入后按各自 raw 进入受控流程。
