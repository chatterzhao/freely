---
local_id: raw-20260719T015321Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T015321Z-A
platform_ids:
  github:
    issue_id: '3994'
    url: https://github.com/chatterzhao/freely/issues/3994
    synced_at: ''
  gitee:
    issue_id: IK1ZV4
    url: https://gitee.com/zhaoquan/freely/issues/IK1ZV4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T01:53:44Z'
updated_at: '2026-07-19T01:53:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

2026-05-15 提交 1c505bf63 删除了 lead-agent.md，声明 scope 仅限 agents/ + skills/README.md，runtime scripts 和 skill content 故意留到后续跟进，但后续跟进从未发生。

## 影响

governance-check 第24行要求 lead-agent.md 存在，导致拦截。start-lead-agent.sh、auto-loop-orchestrator、context-source-skill、project-agents-contract.md 均有悬空引用。

## 修复方案

清理5处悬空引用：
1. start-lead-agent.sh：worker路径 initial_read_targets 删除 lead-agent.md 引用
2. auto-loop-orchestrator/SKILL.md：主链描述去掉 lead-agent 层
3. context-source-skill/SKILL.md：frontmatter 删除'为 lead-agent 产出'描述
4. project-agents-contract.md：删除 lead-agent 引用
5. governance-check：删除第24行文件存在检查
