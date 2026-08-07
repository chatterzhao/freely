---
local_id: raw-20260617T043953Z53Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '2890'
    url: https://github.com/chatterzhao/freely/issues/2890
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T04:40:10Z'
updated_at: '2026-06-17T04:40:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## IBM 审计（7处缺失）

### 严重
1. AGENTS.md L22: 禁止操作总结省略 B1_IBM/B2_IBM → `wt-create → B1_IBM → B2_IBM → commit → pr-create-guarded → pr-merge-guarded`
2. AGENTS.md L166-170: Bug修复"补齐治理"用通用术语未用 B1_IBM/B2_IBM 名称

### 中等
3. three-loop-capability-lifecycle.md L147-148: 使用旧称 B1/B2 应为 B1_IBM/B2_IBM
4. freely-fix-execution SKILL.md L3: YAML description 未提 IBM（feat 提了）
5. fix-execution SKILL.md L3: 同上
6. feat-execution SKILL.md L17: 比较表 fix 流程缺 IBM 步骤 + 缺 "IBM 顺序" 行

### 低
7. three-loop-capability-lifecycle.md L6: §规范流程 锚点过时

## #2883 合规（8处未达标）

8. fix-execution: 阶段 4 未拆为 4a/4b 子阶段标签（内容已改但标签未标）
9. fix-execution + feat-execution: 硬性规则缺 "禁止原子命令绕过"
10. 所有 SKILL.md: 命令名未加 "命令" 后缀
11. feat-execution L17: 比较表 fix 流程仅 "test-pre-merge 沙箱 → cp → commit"
12. dev-loop-execution L154: 未显式命名 pr-merge-guarded
13. deploy-skills 需 --tools claude 显式指定才能部署成功

## 修复
- AGENTS.md L22, L166-170: 补 B1_IBM/B2_IBM 名称
- fix-execution SKILL.md: 阶段 4 标 4a/4b + 硬性规则 + description + "命令"后缀
- feat-execution SKILL.md: 比较表补全 + IBM顺序行 + 硬性规则 + "命令"后缀
- dev-loop-execution SKILL.md: 显式 pr-merge-guarded
- three-loop-capability-lifecycle.md: B1→B1_IBM, B2→B2_IBM, 锚点修正
