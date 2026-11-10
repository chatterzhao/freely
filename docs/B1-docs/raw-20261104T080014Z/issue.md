---
schema_version: '1'
local_id: raw-20261104T080014Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T080014Z-A
platform_ids:
  github:
    issue_id: '4166'
    url: https://github.com/chatterzhao/freely/issues/4166
    synced_at: ''
  gitee:
    issue_id: IKSW9N
    url: https://gitee.com/zhaoquan/freely/issues/IKSW9N
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261104T080014Z/issues/I-20261104T080014Z-A.md
last_synced_comment_at:
  github: '2026-11-10T12:48:44Z'
  gitee: '2026-11-10T12:48:44Z'
hash: ''
created_at: '2026-11-04T08:00:14Z'
updated_at: '2026-11-10T12:48:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T080014Z-A
source_candidate: ''
completed_at: '2026-11-10T12:48:43Z'
closeout_note: ''
---

# refactor: 收敛双平台 issue 同步的入口与副作用

workflow_kind: feature

## 根因
GitHub 与 Gitee 双平台同步由多个入口各自实现：`issue-sync`、`platform-adapter`、`gitee-issue.py`、`cmd_feedback`，每个入口的写路径、错误处理、标签设置都不一致；`issue-sync` 本身是 `bin/` 最大脚本之一。

## 证据
- `bin/issue-sync` 是 `bin/` 中最大的脚本之一（约 800+ 行）。
- 创建路径分裂：`issue-sync create` 会剥离 frontmatter 并设标签；`cmd_feedback` 直接拼 metadata 调 `platform-adapter`，不设标签、不写本地。
- 平台写实现至少 3 套：`platform-adapter.py`、`gitee-issue.py`、`bin/issue-sync` 内联。
- 双平台状态字段 `platform_ids` 在多个脚本里各自解析。

## 影响
- 同一操作在不同入口行为不同（标签、body 格式、本地落盘）。
- 部分成功无法表达：一个平台成功、另一个失败时，调用方只能看到整体失败。
- 排障需要同时读 3 套实现。

## 修复方案
1. 平台写收口到 `platform-adapter.py` 单一实现；`issue-sync` 与 `cmd_feedback` 只做编排。
2. 统一创建契约：body 剥离 frontmatter、标签固定 `kind/raw,phase/proposed`、本地先写再同步。
3. 部分成功用独立退出码（0=全部成功、3=部分成功、1=全部失败），并回写已成功的 `platform_ids`。
4. `issue-sync` 按子命令拆分，主文件只保留参数解析与分派。

## 验收标准
- GREEN：平台写只剩 `platform-adapter.py` 一处实现，其余入口无直连 API。
- GREEN：`feedback` 与 `issue-sync create` 产出的 body/标签完全一致。
- GREEN：部分成功场景有独立退出码与已成功平台回写。
- GREEN：`bin/issue-sync` 行数下降 ≥50%，子命令各自可单测。

### comment-20261110T124844Z
- source: system
- event: promote_finalized
- children: ["I-20261104T080014Z-A"]

拆解为以下任务:
1. [I-20261104T080014Z-A](will-be-updated)
