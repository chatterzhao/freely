---
local_id: raw-20260618T040226Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T040226Z-A
platform_ids:
  github:
    issue_id: '2966'
    url: https://github.com/chatterzhao/freely/issues/2966
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T04:02:44Z'
updated_at: '2026-06-18T04:02:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

当前 `pr-create-guarded` → `pr-merge-guarded` 之间缺少独立的 review 环节。这导致：

1. **语义冲突静默通过**：ef251886（receipt fix）被 15fa666c（pull fix）覆盖，git 自动合并没有冲突提示，合并后才发现 receipt 丢失
2. **Review 证据分散**：Implementation Decision Note 在 dev-loop 产出，但没有统一的 review verdict 文档
3. **门禁检查不完整**：governance-merge-gate 只检查 IBM 文档，不检查代码级 invariant

## 行业 PR review 标准

| 平台 | Review 机制 | Review 产物 |
|---|---|---|
| GitHub | Pull Request Review (approve/comment/request changes) | Review comment + decision |
| GitLab | Merge Request Review | Approve/unapprove |
| Gerrit | Code Review +2/-2 voting | Review label |

共性：
- Review 是 merge 的独立前置步骤
- Reviewer 与 author 分离
- Review decision 可机器读取（API）
- 可设置 "Require review before merging" 分支保护

## Freely 的 pr-review-guarded 设计

### 定位

```
pr-create-guarded  →  pr-review-guarded  →  pr-merge-guarded
（创建 PR）            （独立 review）       （门禁合并）
```

### 输入

- PR 编号或 branch name
- PR diff（governance-merge-gate --range "base..HEAD"）
- 已有 code-review 文档（docs/epics/.../code-reviews/）

### Review 维度

| 维度 | 检查内容 | 方法 |
|---|---|---|
| 语义冲突 | PR 是否覆盖了已有关键逻辑（如 receipt split） | diff 分析 + invariant 检查 |
| IBM 完整 | candidate → I-* → code-review 链是否完整 | governance-merge-gate |
| Code review | Implementation Decision Note 是否存在且格式正确 | 文件存在 + 字段完整 |
| Pre-test | verification 目录下是否有 pre-tests 结果 | 文件存在 + adequacy |
| Receipt | 如果修改了 pr-merge-guarded，receipt 逻辑是否保留 | 代码模式匹配 |
| Worktree | PR 对应的 worktree 是否存在且干净 | git worktree list + git status |

### Review 产物

`docs/epics/{name}/code-reviews/pr-review-{PR#}.md`：

```markdown
# PR Review: #{PR#}
- pr_number: #{PR#}
- branch: fix/raw-{key}-{slug}
- reviewer: {AI model or human}
- review_date: {ISO timestamp}
- verdict: pass | fail | needs_changes

## Semantic Conflict Check
^- status: passed
- evidence: No overlap with known critical invariants

## IBM Completeness Check
^- status: passed
- evidence: governance-merge-gate passed

## Code Review Evidence
^- status: passed
- evidence: implementation-decision.md present, all fields complete

## Pre-test Evidence
^- status: passed
- evidence: pre-tests.md present, 3 acceptance items verified

## Receipt Integrity Check
^- status: passed
- evidence: pr-merge-guarded uses --subject/--body split

## Overall Verdict
- verdict: pass
- notes: Ready for pr-merge-guarded
```

### 门禁规则

- `verdict=pass` → pr-merge-guarded 可以执行
- `verdict=fail` → pr-merge-guarded 被阻塞，必须修复后重新 review
- `verdict=needs_changes` → 同上，但 reviewer 给出了具体修改建议

### 与现有设施的集成

- `pr-create-guarded` 成功后提示：`Next: freely pr-review-guarded <branch>`
- `pr-merge-guarded` 执行前检查 pr-review 文档是否存在且 verdict=pass
- `governance-merge-gate` 增加 pr-review 文档检查
- 可在 GitHub 上通过 `gh pr review --approve` 同步 verdict

### 实施阶段

Phase 1: pr-review-guarded 脚本 + review 文档模板
Phase 2: pr-merge-guarded 集成（检查 review verdict）
Phase 3: governance-merge-gate 集成
Phase 4: GitHub PR review API 同步（可选）
