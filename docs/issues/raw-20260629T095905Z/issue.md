---
local_id: raw-20260629T095905Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3620'
    url: https://github.com/chatterzhao/freely/issues/3620
    synced_at: ''
  gitee:
    issue_id: IJXN4K
    url: https://gitee.com/zhaoquan/freely/issues/IJXN4K
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T09:59:27Z'
updated_at: '2026-06-29T09:59:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260629T095905Z-A
---
\n\n## 问题

freely-workflow-guarded-execution 有三个缺口导致 AI 不自举：

### 1. 缺少阶段 0：创建 raw issue
skill 定位是 feedback 之后加载，但没有覆盖发现问题但无 raw issue 的场景。AI 拿到 bug/需求后不知道该先 feedback。

### 2. 缺少 cd 到开发工位
wt-create 跑完后，skill 没有说下一步要 cd 到开发工位目录。不 cd 的话后续命令都在 develop 上跑，直接违规。

### 3. CLAUDE.md 链不够强制性
礼貌地说完整治理规则请见 AGENTS.md，AI 可能不跟。需要明确命令：启动后第一步必须读 AGENTS.md，然后加载 workflow skill。

## 改动范围

### A. freely-workflow-guarded-execution SKILL.md
- 在工作流标题后、阶段 1 前，增加阶段 0：创建 raw issue（如不存在）
- 阶段 1 wt-create 步骤后，增加 cd 到开发工位目录
- 阶段 0 中说明 feedback 的完整用法和 --kind 参数

### B. CLAUDE.md
- 启动必读段：执行任何操作前必须先读 AGENTS.md
- 工作流执行段：明确用 Skill 工具加载 workflow skill

### C. AGENTS.md
- wt-create 命令行统一使用 --kind 参数
