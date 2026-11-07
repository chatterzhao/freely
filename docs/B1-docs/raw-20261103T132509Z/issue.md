---
schema_version: '1'
local_id: raw-20261103T132509Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132509Z-A
platform_ids:
  github:
    issue_id: '4147'
    url: https://github.com/chatterzhao/freely/issues/4147
    synced_at: ''
  gitee:
    issue_id: IKSPQ1
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ1
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:25:09Z'
updated_at: '2026-11-07T09:19:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T09:15:00Z'
closeout_note: ''
---

# fix: 接通 commit-msg 门禁或删除孤儿实现

workflow_kind: fix

## 根因
承载 receipt「提交期阻断」的 `commit-msg` hook 有完整实现，却没有任何 shim / 安装器 / 文档 / 测试引用它，是孤儿代码；trailer 校验因此退化为写入方自己复查。

## 证据
- 实现在 `docs/system/workspace/hooks/commit-msg.sh`（130 行）：trailer 解析 `:83-85`、拒绝文案 `:89,98,107,116,125`、允许值 `pr-merge-guarded|pr-merge-guarded-complete` `:95-99`。
- `.githooks/` 内无 `commit-msg` 条目（`ls -a .githooks/` 实测）。
- 该文件在 git 中为 `100644`（`git ls-files -s` 实测）；即便补 shim，`.githooks/pre-commit:7` 的 `-x` 判断也会跳过。
- 全仓（`bin/` + `scripts/` + `hooks/` + `*.md`）grep `commit-msg` 零命中，无安装器、无文档、无测试引用。
- trailer 由 `bin/pr-merge-guarded:303-305` 写入 `Freely-Merge-Path / Freely-Bypass-Mode / Freely-Source-Branch`，再在 `:763-766` 自己 `git log` 复查 → 手工 `git merge` 后自填 trailer 即可让 merge commit 在结构上「看起来合规」。
- 与本仓文档冲突：`docs/system/workspace/hooks/README.md:41` 宣称治理依赖「hook 时机阻断 + pr-merge-guarded 受控 receipt + governance-check post-merge audit」三层，实际第一层缺席，只剩事后审计（`governance-check` 仅 `freely:26727` 手工触发）。

## 影响
绕过路径（手工 `git merge` 后自填 trailer、`gh pr merge --admin`）在提交期零拦截；文档宣称的强制力比实际强一层，据此高估护栏的人会做出错误的风险判断。同时 130 行实现无人执行，属于「看起来有、实际不跑」的假安全感。

## 修复方案
二选一，不要停留在「看起来有、实际不跑」：
1. **接线**：新增 `.githooks/commit-msg` shim（模板用 `${HOOK_NAME}.sh` 拼路径，天然找到 `commit-msg.sh`，无需改拼装逻辑）；同时把 shim 的 `[[ -x ... ]]` 改 `[[ -f ... ]]`（与 #4146 第 1 项同一处改动），使 `100644` 不再阻断。补一条测试：受保护分支上缺 trailer 的 commit 必须被拒。
2. **放弃**：删除 `commit-msg.sh`，同步把 `hooks/README.md:41` 的三层表述改为「事后审计」，并在 `pr-merge-guarded` 侧增加对「无 receipt 的 merge commit」的显式拒绝。

## 验收标准
- 选 1：RED→GREEN：在 `develop` 上 `git commit -m "chore: x"`（无 `Freely-Merge-Path`），当前成功；接线后必须失败并打印 `commit-msg.sh:89-125` 中的拒绝原因之一。
- 选 1：`git ls-files -s .githooks/commit-msg` 存在，且执行不依赖文件 mode（因 shim 用 `-f`）。
- 选 2：全仓 grep `commit-msg` 只剩历史记录；`hooks/README.md:41` 不再宣称提交期阻断。
- 两路共同：`pr-merge-guarded:763-766` 的自复查不再是唯一校验点，绕过路径有独立测试覆盖。
- RED：手工 `git merge` 后自填 `Freely-Merge-Path: pr-merge-guarded`，断言在选定方案下仍被拒或在审计中被显式标出；当前完全不可见。
