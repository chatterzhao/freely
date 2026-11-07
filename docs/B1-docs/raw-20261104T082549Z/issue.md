---
schema_version: '1'
local_id: raw-20261104T082549Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T082549Z-A
platform_ids:
  github:
    issue_id: '4182'
    url: https://github.com/chatterzhao/freely/issues/4182
    synced_at: ''
  gitee:
    issue_id: IKSWR9
    url: https://gitee.com/zhaoquan/freely/issues/IKSWR9
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:25:49Z'
updated_at: '2026-11-07T07:18:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T07:15:00Z'
closeout_note: ''
---

# fix: 平台不可读时 raw-issue-pull 直接 FATAL，无法指定备用平台

workflow_kind: fix

## 根因
`raw-issue-pull` 只接受 `--raw-key` 与 `--target`，没有平台选择；`pull_raw_issue()` 要求所有已配置平台 `status == ok`，任一平台不可读即 FATAL。网络故障时即使另一个平台有同 raw key 的 issue 也无法继续。

## 证据
- `bin/raw-issue-pull` 参数解析仅 `--raw-key` / `--target`。
- `platform-adapter.py` 的 `pull_raw_issue()`：`if not replicas or any(item.get("status") != "ok" for item in replicas.values()): FATAL`。
- `platform = next(iter(replicas))`：固定取第一个平台，无优先级或可用性选择。
- `wt-create` 的 `_pull_raw_issue()` 直接调用该命令，无备用路径。

## 影响
- GitHub 网络抖动时整个工位创建/物化被阻断，即使 Gitee 完全可用。
- 双平台本应互为备份，实际退化为"任一故障即全停"。

## 修复方案
1. `raw-issue-pull` 增加 `--platform <github|gitee>`，显式指定读取源。
2. 默认行为改为「按可用性排序，取第一个 ok 的平台」；不可读平台记入 sync-debt，不阻断。
3. `wt-create` 增加 `--source-platform` 透传；未指定时按上述顺序回退。
4. 平台写（close/update）同样支持按可用平台执行，部分成功用独立退出码。

## 验收标准
- RED：屏蔽 github 网络后执行 pull，断言仍能从 gitee 物化成功；当前 FATAL。
- GREEN：`--platform gitee` 明确从 gitee 读取并写回 `platform_ids`。
- GREEN：不可读平台记入 `sync-debt list`，不阻断工位创建。
- GREEN：部分成功场景退出码为 3 而非 1。
