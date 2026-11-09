---
local_id: raw-20260629T025659Z59Z
kind: feature
phase_state: absorbed
absorbed_into: I-20260629T025659Z-A
platform_ids:
  github:
    issue_id: '3616'
    url: https://github.com/chatterzhao/freely/issues/3616
    synced_at: ''
  gitee:
    issue_id: IJXH20
    url: https://gitee.com/zhaoquan/freely/issues/IJXH20
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T03:43:35Z'
updated_at: '2026-06-29T03:43:35Z'
intake_id: ''
author: zhaoquan
channel: freely-feature-execution
session_refs: []
platform_state: closed
---
# refactor: 统一 fix skill 与 feature skill 的治理顺序 — B1→B2→dev→test

## 问题

当前 fix skill 和 feature skill 的流程顺序不一致：
- **feature**: `feedback → wt-create → B1 → B2 → dev → test → pr`
- **fix**: `feedback → wt-create → dev → test → B1 → B2 → pr`

fix 采用"Fix first, govern later"导致：
1. pre-tests 形同虚设（代码写完才补测试计划）
2. TDD 无法落地（RED-GREEN 需要 pre-tests 先于代码）
3. B1 brainstorms 无意义（修复已完成再补根因分析）
4. code-review 缺少决策记录（没有 B2 的 Implementation Decision Note）
5. test-pre-merge cherry-pick 机制复杂且不必要

## 目标

统一为：`wt-create → B1 → B2 → dev → test → pr`

## 波及文件

- `~/.claude/skills/freely-fix-execution/SKILL.md` — 重写
- `~/.claude/skills/freely-test-execution/SKILL.md` — 流程序列
- `~/.claude/skills/freely-feature-execution/SKILL.md` — 分工表
- `docs/system/workspace/three-loop-capability-lifecycle.md` — Fix 变体路径
- `AGENTS.md` — 流程序列 + Bug修复章节
- 项目级 skill 副本同步更新

## 验收标准

1. fix skill 的 IBM 顺序与 feature 一致：B1 → B2 → dev → test
2. 去掉 test-pre-merge cherry-pick 机制
3. fix 的 B1 保留根因分析要求
4. fix 的 B2 必须有 pre-tests
5. three-loop 真源文档同步更新
6. AGENTS.md 同步更新
