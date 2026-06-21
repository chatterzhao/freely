---
local_id: raw-20260616T143914Z
kind: raw
phase_state: completed
platform_ids:
  github:
    issue_id: '2854'
    url: https://github.com/chatterzhao/freely/issues/2854
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T14:39:32Z'
updated_at: '2026-06-16T14:39:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

完整规范流程 `feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close` 目前只在 `three-loop-capability-lifecycle.md` 一处有完整体现。其余关键文档各自残缺：

| 文档 | 问题 |
|------|------|
| `AGENTS.md.example` | 只有 skill 路由表，无线性流程。freely init 后用户/AI 第一眼看不到从哪开始 |
| `CONSTITUTION.md` | 只有 pr-create/pr-merge 后半段，无 feedback/IBM 前半段 |
| `freely-feat-execution/SKILL.md` | 链从 B1_IBM 开始，不含 feedback 入口 |
| `freely-doc-B1_IBM-execution/SKILL.md` | 无位置标记，读者不知道自己在全链路哪一步 |
| `freely-doc-B2_IBM-execution/SKILL.md` | 同上 |
| `freely-dev-loop-execution/SKILL.md` | 同上 |
| `freely-fix-execution/SKILL.md` | 同上 |

## Requirements

### 1. AGENTS.md.example — 新增"规范流程"章节

放在 skill 路由表之前，作为用户/AI 的第一入口：

- 完整 Feat 链路：`feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close`
- Fix 变体：`wt-create → dev → test → B1 → B2 → pr-create → pr-merge → wt-close`
- Doc-only 变体：`dev → pr-create → pr-merge → wt-close`
- 每一步对应的命令/skill
- 每一步在哪个 loop（auto/doc/dev/external）中执行

### 2. 每个 skill SKILL.md — 加位置标记

在描述行或头部加入当前 skill 在全链路中的位置，格式：

```
全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close
                                                            ↑ you are here
```

涉及的 skill：
- `freely-feat-execution`（已部分描述，补全 feedback 入口）
- `freely-fix-execution`
- `freely-doc-B1_IBM-execution`
- `freely-doc-B2_IBM-execution`
- `freely-dev-loop-execution`

### 3. CONSTITUTION.md — 完整化

在分支规范处补充完整链路引用，不只有 pr-create/pr-merge 后半段。

### 4. three-loop-capability-lifecycle.md

已有完整内容，只加指向 AGENTS.md 的交叉引用。

## 不做

- 不改变任何命令/skill 的功能
- 不改变 IBM 框架本身
- 只改文档，不改脚本

## Acceptance

- [ ] `AGENTS.md.example` 有完整规范流程章节
- [ ] 5 个 skill SKILL.md 有位置标记
- [ ] CONSTITUTION.md 分支规范处有完整链路引用
- [ ] three-loop-capability-lifecycle.md 有指向 AGENTS.md 的交叉引用
- [ ] freely init 后用户项目的 AGENTS.md 包含完整流程
