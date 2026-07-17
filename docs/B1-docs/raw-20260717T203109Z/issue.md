---
local_id: raw-20260717T203109Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T203109Z-A
platform_ids:
  github:
    issue_id: '3983'
    url: https://github.com/chatterzhao/freely/issues/3983
    synced_at: ''
  gitee:
    issue_id: IK1VC4
    url: https://gitee.com/zhaoquan/freely/issues/IK1VC4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T20:31:37Z'
updated_at: '2026-07-17T20:31:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 两项遗留（PR #3980 autonomous gate 已合入,gate 核心判定在位,两个技术点需补）

### 1. agent_working 查询段为 STUB
_gate 函数内查询 agent_working 表的 python3 -c 段因 f-string 中的单引号在 bash 双引号上下文中被吃,当前为 STUB。修复:改用独立 heredoc (<<'PYAW') 传参,环境变量 PROJECT_ROOT 和 _AW_RAW_KEY 传参,避开引号冲突。

### 2. gate 内 _has_merge 检测在 subshell 中未命中
git log 在终端直调确认命中 merge commit,但在 gate 函数 exec bash 的 subshell 上下文中未命中。修复:git log 前显式 git -C "$PROJECT_ROOT" 确保在项目根查询,消除 subshell 环境差异。

### 3. usage/help 同步
autonomous gate 引入后 --force 语义变化,usage() 中 --force 描述需同步更新。
