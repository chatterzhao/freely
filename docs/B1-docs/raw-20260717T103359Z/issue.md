---
local_id: raw-20260717T103359Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T103359Z-A
platform_ids:
  github:
    issue_id: '3974'
    url: https://github.com/chatterzhao/freely/issues/3974
    synced_at: ''
  gitee:
    issue_id: IK1T69
    url: https://gitee.com/zhaoquan/freely/issues/IK1T69
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T10:34:21Z'
updated_at: '2026-07-17T10:34:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 缺陷（3 次生产实证,2026-07-17）
ACP init 超时触发 agent fallback 直启的 worker,先后:
1. 无产出移除他人工位 ×3（05:11Z 后 07-15 两工位消失、09:xx 后 084757Z/090202Z 新工位消失——均零交付、零平台动作）
2. 违规直写 develop 工作树（8 个 I-* phase_state 直改,已恢复;另 projects.tsv 落仓库根）

## 根因
Prompt 层锚约束（Worktree/Branch header）存在但非硬防护;缺三道硬防线:
- `wt-close`/worktree remove 无 owner 校验（agent_working 表有 raw_key→agent 绑定但未被校验,任何 agent 可关任何工位）
- 运行中 develop 工作树污染无检测（仅 daemon start 时检查 dirty,运行中被写无人发现）
- fallback 直启 prompt 缺「工位边界铁律」硬文案段（只写自有 Worktree;禁关非自有 key 工位;禁写 project root）

## 修复方向
(a) wt-close owner 校验:关闭目标 raw_key 的 agent_working owner 与调用方不符时硬拦（--force+reason 豁免走既有语义）
(b) supervisor 主循环周期检测 protected root dirty → `protected_root_dirty_detected` 事件升级 manager(advisory)
(c) fallback worker prompt 注入工位边界铁律段

## 关联
ACP init 超时本体（fallback 的触发源）新代码未复现,留 revisit;素材:cycle-worker-*.log timed out waiting for ACP response to initialize
