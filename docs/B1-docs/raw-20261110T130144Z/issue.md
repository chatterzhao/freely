---
schema_version: '1'
local_id: raw-20261110T130144Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T130144Z-A
platform_ids:
  github:
    issue_id: '4286'
    url: https://github.com/chatterzhao/freely/issues/4286
    synced_at: ''
  gitee:
    issue_id: IKUEWL
    url: https://gitee.com/zhaoquan/freely/issues/IKUEWL
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/issues/I-20261110T130144Z-A.md
last_synced_comment_at:
  github: '2026-11-10T13:32:19Z'
  gitee: '2026-11-10T13:32:19Z'
hash: ''
created_at: '2026-11-10T13:01:44Z'
updated_at: '2026-11-10T14:03:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T130144Z-A
source_candidate: ''
completed_at: '2026-11-10T13:32:18Z'
closeout_note: ''
severity: P2
---

# refactor: 拆分 issue-sync 并统一 feedback 创建契约

workflow_kind: feature

从 #4166（raw-20261104T080014Z）拆分。R26 已完成「平台写收口到 platform-adapter.py」：issue-sync 的 GitHub 四类写改经 issue-write-one，Gitee 仍走 adapter 底层 gitee-issue.py；部分成功 0/3/1 退出码经核对已由 adapter 的 create-issue 与 issue-sync close 实现。本 issue 承接剩余三项。

## 根因

1. bin/issue-sync 仍是约 1300 行单文件，子命令无法独立单测，任何改动都要读整份脚本。
2. feedback 与 issue-sync create 的 body/标签虽已基本一致（都经 adapter 或剥离 frontmatter），但没有逐字对齐的断言，标签缺省值仍分散在两处。
3. bin/issue-sync-bootstrap 仍直连 gh issue delete，是平台写入口的唯一例外，未登记契约。

## 影响

子命令不可单测导致每次改 issue-sync 都只能端到端验证；body/标签的「基本一致」在下一个入口出现时会再次分叉；delete 例外没有文档化，排查时会被当成漏网直连。

## 修复方案

1. 按子命令拆分 bin/issue-sync：参数解析与分派留在主文件，create/update/comment/close/promote/promote-finalize/status/batch/scan 各自成为可 source 的函数模块（如 bin/issue-sync.d/*.sh），主文件行数下降 ≥50%。
2. 统一创建契约：adapter 的 create_issue 与 issue-sync 的 create 共用同一个 body 剥离函数与标签清单常量；新增断言对比两条路径产出的 body/标签完全一致。
3. 把 bootstrap 的 gh issue delete 迁到 adapter（新增 delete_issue 可选方法）或登记为显式例外并在代码注释与命令文档中标注。

## 验收标准

- RED：issue-sync 行数仍 >1000、无子命令模块；两条 create 路径的标签清单存在重复常量；bootstrap 直连 delete 未登记。
- GREEN：issue-sync 主文件行数下降 ≥50%，每个子命令可 source 后单独测试；body/标签一致性断言通过；delete 迁到 adapter 或例外登记有测试/文档守护。
- 不退化：不改 issue-write-one 契约、不改 0/3/1 退出码、不改 promote/close 的既有行为。

### comment-20261110T133219Z
- source: system
- event: promote_finalized
- children: ["I-20261110T130144Z-A"]

拆解为以下任务:
1. [I-20261110T130144Z-A](will-be-updated)
