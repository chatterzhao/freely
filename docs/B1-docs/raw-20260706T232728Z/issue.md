---
local_id: raw-20260706T232728Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3787'
    url: https://github.com/chatterzhao/freely/issues/3787
    synced_at: ''
  gitee:
    issue_id: IJZ839
    url: https://gitee.com/zhaoquan/freely/issues/IJZ839
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T23:27:49Z'
updated_at: '2026-07-07T00:33:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

当前项目文档中，封装命令的使用要求散落在 AGENTS.md 的速查表、workflow skill 的铁律区域、以及 `.githooks/bin/gh` wrapper 的拦截消息中。但缺少一个系统性的说明，解释：

1. **为什么**必须用封装命令（因为封装了完整流程）
2. **什么场景**用什么命令（意图→命令的完整映射）
3. **不用会怎样**（跳过流程的后果）

导致 AI agent 和开发者在被 hook 拦截后不知道正确命令是什么，或者只是在被拦截后才被动查找。

## 需要添加的文档位置

### 1. AGENTS.md 命令速查表（已有，需要增强）

当前 AGENTS.md 有一个速查表，但只列了命令和禁止项。需要增强：

- 每个命令旁边加 **"为什么用这个"** 一列——解释该命令封装了什么流程
- 加 **"意图 → 命令"** 映射表——从开发者意图出发，告诉他用哪个命令

示例表述：

> | 你想做什么 | 用这个命令 | 它封装了什么 |
> |-----------|-----------|-------------|
> | 报告一个 bug 或提需求 | `freely feedback --title "..." --kind fix|feature --body "..."` | 创建 raw issue → 双平台同步（GitHub + Gitee）→ 纳入扫描发现 |
> | 开始修 bug/做功能 | `freely wt-create --raw-key <key> --source platform --kind fix|feature --slug <slug>` | 创建 dev worktree + test-pre-merge 工位 → 同步 tooling → cd 到工位 |
> | 提 PR | `freely pr-create-guarded` | pull develop → 冲突处理 → dry-run gate → push → 双平台创建 PR |
> | 评审 PR | `freely pr-review-guarded <branch>` | 6 维独立 review → verdict 文档 |
> | 合并 PR | `freely pr-merge-guarded develop <branch>` | PR gate → promotion gate → merge → develop-push → 双平台同步 |
> | 收工关 issue | `freely wt-close --raw-key <key>` | 关闭 test + dev worktree → 双平台 close issue → 清理分支 |
> | 同步到远程 | `freely develop-push attempt` | 受控的 develop push，有审计日志 |

### 2. freely-workflow-guarded-execution SKILL.md（已有的铁律区域，需要补充意图映射）

当前 SKILL.md 已有铁律区域（禁止绕过），但缺少 **正向引导**——告诉开发者应该怎么做的意图映射表。

需要在铁律区域 **之前** 加入 "意图→命令" 章节：

```markdown
## 意图→命令速查

开发 Freely 时，从你的意图出发选择命令，不要直接操作 git/gh：

| 你的意图 | ✅ 正确做法 | ❌ 错误做法 | 原因 |
|---------|------------|-----------|------|
| 报告问题 | `freely feedback --title "..." --kind fix --body "..."` | 直接 commit 修 | 必须先有 raw issue，才能创建工位 |
| 开工干活 | `freely wt-create --raw-key <key> --source platform --kind fix --slug <slug>` | `git worktree add`, `git checkout -b` | wt-create 自动创建 test 工位、同步 tooling |
| 代码写完了想提交 | `freely pr-create-guarded` | `gh pr create`, `git push` | pr-create-guarded 先 pull develop、跑 dry-run gate |
| 请人 review | `freely pr-review-guarded <branch>` | — | 6 维独立 review + verdict |
| review 通过想合并 | `freely pr-merge-guarded develop <branch>` | `gh pr merge`, `git merge` | pr-merge-guarded 跑全部门禁 + 双平台同步 |
| 合并完了收工 | `freely wt-close --raw-key <key>` | `git worktree remove`, `git branch -D` | wt-close 同时关 test + dev 工位 + 双平台 close issue |

**每条封装命令都封装了多个步骤**。直接用 git/gh 命令 = 跳过流程 = 门禁拦截。
```

### 3. .githooks/bin/gh wrapper 拦截消息（已有，需要补"你应该用什么"）

当前 gh wrapper 拦截消息已经告诉了用户正确命令，但可以加强"为什么"：

当前：
```
[BLOCKED] gh pr create is not allowed directly.
  Use the canonical command: freely pr-create-guarded
```

建议增强：
```
[BLOCKED] gh pr create 不允许直接使用。
  直接用 gh pr create = 跳过 pull develop、dry-run gate、push 门禁。

  ✅ 使用封装命令: freely pr-create-guarded
     它封装了: pull develop → 冲突处理 → dry-run gate → push → 双平台创建 PR
```

### 4. .githooks/pre-commit.sh 和 pre-push.sh（已有点，需增强"意图→命令"）

当前 hook 拦截后会列出 orphaned branches 并提示 `freely wt-close`。但拦截消息中没有告诉用户：
- 当前被拦截，应该回到哪个命令重新走流程
- 当前的意图（commit/push）对应什么封装命令

建议在 hook 拦截消息末尾加一行：

```
[freely] 你刚才想做的是 git commit → 对应封装命令是 freely pr-create-guarded
[freely] 完整流程: feedback → wt-create → B1 → B2 → RED → dev → GREEN → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
[freely] 被拦截了？从你当前阶段对应的命令重新开始。
```

### 5. 新文件：docs/system/workspace/commands.md（建议新建）

创建一个命令索引文件，作为所有封装命令的权威参考：

```markdown
# Freely 封装命令参考

## 为什么用封装命令

Freely 的每条封装命令内部执行多个步骤，直接用 git/gh 命令会跳过关键流程：

| 封装命令 | 封装了哪些步骤 |
|---------|--------------|
| `freely feedback` | 创建 raw issue → 双平台同步（GitHub + Gitee） |
| `freely wt-create` | 创建 dev worktree + test-pre-merge 工位 → sync-tooling → cd |
| `freely pr-create-guarded` | pull develop → 冲突处理 → dry-run gate → push → 双平台 PR |
| `freely pr-review-guarded` | 6 维独立 review → verdict 文档 |
| `freely pr-merge-guarded` | PR gate → promotion gate → merge → develop-push → 双平台同步 |
| `freely wt-close` | 关 test + dev 工位 → 关双平台 issue → 清理分支 |
| `freely develop-push attempt` | 受控 develop push → 审计日志 |

跳过任何一步 = 门禁拦截 = 必须 revert 重来。
```

## 实现要求

1. **AGENTS.md**：增强现有速查表，加"意图"列和"封装了什么"列
2. **freely-workflow-guarded-execution SKILL.md**：在铁律区域前加"意图→命令速查"章节
3. **.githooks/bin/gh**：每个拦截消息加"为什么"解释
4. **.githooks/pre-commit.sh**：拦截末尾加流程提示
5. **.githooks/pre-push.sh**：同上
6. **新建 docs/system/workspace/commands.md**：封装命令权威参考

## 设计原则

- **从意图出发**：不要让人去查命令手册——告诉他想做什么，给他对应命令
- **每个命令说清楚封装了什么**：让人理解这不是无意义的包裹，而是流程的编码
- **被拦截时给出正向引导**：不只是说"你错了"，而是说"你应该用什么"
- **一致性**：所有位置的表述保持一致，AGENTS.md ↔ SKILL.md ↔ hook 消息 ↔ commands.md
