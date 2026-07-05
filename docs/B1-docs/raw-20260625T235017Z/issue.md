---
local_id: raw-20260625T235017Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3521'
    url: https://github.com/chatterzhao/freely/issues/3521
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T23:50:36Z'
updated_at: '2026-06-25T23:50:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T235017Z-A
pre_tests_path: docs/epics/feat-to-feature/verification/pre-tests.md
absorbed_into: I-20260625T235017Z-A
source_candidate: docs/B1-docs/raw-20260625T235017Z/candidates.md#C-20260625T235017Z-A
---

## 问题

`freely-feature-execution` 用缩写 `feat` 作为 `feature` 的简写，容易和 `fix` 混淆（都是三个字母），`feat` 在代码库里不直观。

## 改动

### 重命名
- `docs/system/workspace/skills/freely-feature-execution/` → `docs/system/workspace/skills/freely-feature-execution/`
- `~/.claude/skills/freely-feature-execution/` → `~/.claude/skills/freely-feature-execution/`
- `~/.claude/skills/feature-execution/` → 删除（旧版本）
- SKILL.md 内 `name: freely-feature-execution` → `name: freely-feature-execution`

### 替换所有引用（约 65+ 文件）
- 所有 .sh 脚本: `freely-feature-execution` → `freely-feature-execution`
- 所有 .py 文件: 同上
- 所有 .md 文档: 同上
- 所有 config/说明中 `feat` 指 feature 的地方: 改用 `feature`

### 不改
- `feat` 作为 git conventional commit prefix（`feat: new feature`）不改
- `feature` 单词本身不改
- `feat` 是其他单词一部分的不改（`defeat` 等）

### 验证
```bash
# 改完后不应有残留
grep -r "freely-feature-execution" docs/ bin/ ~/.claude/skills/ --include="*.sh" --include="*.py" --include="*.md"
# 应返回空
```
