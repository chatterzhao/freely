---
local_id: raw-20260708T211928Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T211928Z-A
platform_ids:
  github:
    issue_id: '3831'
    url: https://github.com/chatterzhao/freely/issues/3831
    synced_at: ''
  gitee:
    issue_id: IJZS1F
    url: https://gitee.com/zhaoquan/freely/issues/IJZS1F
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T21:19:50Z'
updated_at: '2026-07-08T21:19:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

### 1. I-* issues 全部误判为 raw_created
20 个 I-* issues 真实状态是 in_dev/in_b2_ibm/done_b2_ibm，但 _detect_station 对 2a_non_terminal 一律返回 raw_created。I-* 和 raw issue 需要不同的 station。

### 2. 7 个 I-* issue phase_state 读为空
parse_frontmatter 对 B2-docs 路径下 I-* issue.md 的解析失败——frontmatter 明明有 phase_state 但读出来是空。

### 3. 缺少 scan_state / source_family / title 等字段
prompt builder 期望的 scan_state、scan_state_worktree、title、incomplete、children 字段 scan 没有输出。

## 修复

1. _detect_station 区分 raw vs linked (I-*) issue，各自映射到正确 station
2. parse_frontmatter 修复 B2-docs I-* issue 解析
3. 所有 item 补上 scan_state/source_family/title/incomplete 字段
4. TERMINAL_PHASES 统一：raw=absorbed/dropped/completed, linked=completed/absorbed/dropped
5. 每种 station 有精确的 [manager]/[worker] 两级 next_action

## 分类原则

无论哪种类型的修复，都走：创建 raw issue → worktree → 按 workflow skill 推进。
- raw issue 没有工位 → Manager 用 wt-create 创建工位开始 B1
- I-* issue 卡住 → Manager 创建新 raw issue → worktree → 修正 I-* 状态
- 文档状态不对齐 → 批量 sync batch（一个 raw issue 统一处理）
