---
schema_version: '1'
local_id: raw-20261108T134701Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  gitee:
    issue_id: IKTSRS
    url: https://gitee.com/zhaoquan/freely/issues/IKTSRS
    synced_at: ''
  github:
    issue_id: '4746'
    url: https://github.com/chatterzhao/freely/issues/4746
    synced_at: '2026-11-27T13:59:35Z'
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-08T13:47:01Z'
updated_at: '2026-11-27T13:59:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P2
---

# fix: bin/freely 注释承诺 freely install 与 @freely-dev-path 标记，但命令从未实现

workflow_kind: fix

workflow_kind: fix

## 根因

`bin/freely` 的头部注释承诺了一套并不存在的安装机制：

- `bin/freely:10` `prod mode: installed via 'freely install' to a system path.`
- `bin/freely:23-27` 要求把 `# @freely-dev-path` 标记行加进 `~/.zshrc`，并声明 `freely install` 会「自动移除」该行。
- 但 `docs/system/workspace/scripts/runtime/freely` 里既没有 `install)` 分派，也没有 `cmd_install()`；全仓检索不到任何安装命令实现或安装包脚本。
- 用户本机 `~/.zshrc:75` 确实保留着 `# @freely-dev-path — 安装 freely 时自动移除` 这一行，是「注释/文档与实现脱节」的活证据。

## 来源与不夹带说明

这是 #4194（R16，已合并 `c2a55934e`）修复方案第 3 项。R16 只实现了方案 1/2/4（一致性检查、合并后受控重打包、hash 清单），并在 IDN 的 `boundary_non_goals` / `residual_risk` 明确把第 3 项列为**本轮不做**；#4194 关闭后该缺口会随 issue 一起消失，故按自举约定独立立项，不夹带进 R16 的 PR。

## 证伪（现有 open issue 均未覆盖）

- 现网 45 条 open issue 标题中无 install / dev-path / zshrc / 安装态文档相关项（`gh issue list --state open --jq` 过滤确认）。
- #4205（R5.5，已关闭）修的是打包 allowlist 遗漏，与「install 命令与 zshrc 标记」无关。
- #4194 本身即本轮 issue，正文第 3 项只提出方向、验收标准未包含它，R16 的 AT-001 也未覆盖。
- #4169（入口文档链路）针对首跳阅读量，不涉及命令注释与 shell 标记的一致性。

## 修复方案（二选一，倾向 B）

- A：实现 `freely install`，包含安装态切换与 `@freely-dev-path` 标记的增删；与 R16 已上线的 `freely-package --version auto --activate` 存在职责重叠，易产生第二份安装真相源。
- B（推荐）：删除 `bin/freely` 注释中对 `freely install` 的承诺，把说明改为真实存在的 `freely-package --activate`；清理 `~/.zshrc` 的 `@freely-dev-path` 标记（或改为描述开发态 PATH 前置），并让 usage / AGENTS / 文档投影同步。

## 验收标准

- RED：静态断言当前 `bin/freely` 仍引用不存在的 `freely install`，且 runtime 无实现；`usage` 或文档投影仍承诺该命令。
- GREEN：代码、usage、文档投影中不再出现任何未实现的命令名；`freely doctor` 与打包入口被正确描述。
- GREEN：新增「命令名必须在 dispatcher 中存在」的静态契约检查，防止同类脱线再次发生。
- GREEN：既有 doctor / package / dispatch 相关回归 worktree 与 develop 基线退出码一致。
