---
name: fix-execution
description: 快速修复 bug 的工作流——用 pre 工位隔离测试，fix 工位早期创建、增量提交，治理后置。
---

# skill:fix-execution

## 核心原则

> **Fix first, govern later. Isolate test, commit early.**

- 不在 main/develop 上直接改代码测试（会阻塞其他 AI 并发工作）
- 修复决定即建 fix 工位，阶段性 cp 修改过去提交，不等最后一次性提交
- 治理文档在修复验证后才写，不走冤枉路

## 触发条件

- 运行时发现 bug（daemon crash、restart storm、超时、权限错等）
- 在 main/develop 或任意 worktree 上测试时暴露的问题
- 需要快速修复并向上合并到 develop / main

## 工作流

### 阶段 1：创建 pre 测试工位（隔离测试）

```
发现 bug（在 main / develop / 任意 worktree）
  │
  ├─ 1. 创建 fix-pre-merge 工位（hook 会自动复制 runtime 状态）
  │     ./bin/wt-create fix-pre-merge/<desc>-<YYYYMMDD> --base develop
  │
  │     为什么用 fix-pre-merge-*：
  │     - hook 复制 config.env、freely.db、tool-boundary，运行时环境完整
  │     - 与 develop/main 等效，但隔离——不阻塞其他 AI 并发工作
  │     - 测试完就删，不长期保留
  │
  ├─ 2. 初始化 pre 工位运行时
  │     ./bin/pre-init-runtime --pre-project <pre-worktree-path>
  │
  ├─ 3. 在 pre 工位上直接改源码，stop → start daemon 验证
  ├─ 4. 反复迭代，深挖根因完整链
  │
  └─ 此阶段不创建治理文档
```

### 阶段 2：早期建 fix 工位，增量提交

```
决定要 fix（此时就建 fix 工位，不等修复完成）
  │
  ├─ 1. 创建 hotfix 工位
  │     ./bin/wt-create hotfix/<desc>-<YYYYMMDD> --base develop
  │
  ├─ 2. 每次在 pre 工位验证通过一个阶段性修复，立刻 cp 到 hotfix 工位
  │     cp <pre-wt>/path/to/file <hotfix-wt>/path/to/file
  │     cd <hotfix-wt> && git add -A && git commit -m "fix: <阶段性描述>"
  │
  ├─ 3. pre 工位继续迭代下一层根因 → 验证 → cp → commit
  │
  └─ 关键：增量提交，不是最后一次性堆一个大 commit
          ├─ commit 1: fix KeyError crash
          ├─ commit 2: fix reader thread zombie
          ├─ commit 3: fix health check
          ├─ commit 4: fix lock deadlock
          └─ ...
```

### 阶段 3：补齐治理

```
hotfix 工位（修复已全部提交）
  │
  ├─ 1. 创建 raw issue: docs/issues/raw-<YYYYMMDD>-<key>/issue.md
  │     - kind: raw, status: absorbed, absorbed_into: I-<id>
  ├─ 2. 创建 candidate: docs/pre-brainstorms/<YYYYMMDD>-<key>/candidates.md
  │     - status: promoted, promoted_issue_path 指向 canonical issue
  ├─ 3. 创建 canonical issue (两处)：
  │     docs/issues/I-<id>/issue.md          (kind: linked)
  │     docs/epics/<epic>/<name>/issues/I-<id>.md
  ├─ 4. 创建 progress: docs/progress/<epic>/p-<name>.md
  ├─ 5. 创建 code-review（必须含 ## Implementation Decision Note）：
  │     - decision / why_this / alternatives_considered
  │     - boundary_non_goals / residual_risk
  ├─ 6. 更新 docs/milestones.md → committed_issues
  │
  └─ 治理文档也增量 commit，不堆在一起
```

### 阶段 4：门禁合并

```
hotfix 工位 → develop
  │
  ├─ 1. 确保 develop clean
  │     git checkout develop
  │     git merge --abort 2>/dev/null; git reset --hard HEAD; git clean -fd
  │
  ├─ 2. ./bin/merge-guarded develop hotfix/<name>
  │
  ├─ 3. 门禁失败 → 回 hotfix 工位修复 → commit → 重试（最多 2-3 轮）
  │
  ├─ 4. 通过 → 自动 push github + gitee
  │
  └─ 可选: git checkout main && ./bin/merge-guarded main hotfix/<name>
```

### 阶段 5：收尾

```
  ├─ 1. 删除 pre 工位（测试完成，不再需要）
  │     git worktree remove <pre-worktree-path>
  │     git branch -D fix-pre-merge/<desc>-<YYYYMMDD>
  │
  ├─ 2. 清理 develop 的 dirty state（如果有）
  │     git checkout -- .
  │
  ├─ 3. 可选: 创建 release 分支作为 stable 引用
  │     git checkout -b release/<YYYYMMDD>-stable main
  │     git push github origin release/<YYYYMMDD>-stable
```

## 工位类型对照

| 工位 | 用途 | 生命周期 |
|---|---|---|
| `fix-pre-merge/*` | 隔离测试环境，hook 复制 runtime | 临时，修完即删 |
| `hotfix/*` | 正规修复工位，增量提交+治理 | 合并后 retire |
| `develop` | 合并目标（只接受 merge） | 长期 |
| `main` | 发布目标（只接受 merge） | 长期 |

## 硬性规则

- **用 pre 工位隔离测试**。不在 main/develop 上直接改代码测试，避免阻塞其他 AI 并发。
- **fix 工位早期创建**。一旦决定要 fix 就建 hotfix 工位，不要等修复完成。
- **增量 cp + commit**。每个阶段性修复验证通过后，立刻 cp 到 hotfix 工位提交。不要堆到最后一次性提交。
- **pre 工位只测不改长期资产**。所有正式提交都在 hotfix 工位。
- **治理后置**。修复验证通过了再写治理文档。
- **根因深挖**。一个表面修复可能掩盖更深问题，继续 drill down。
- **不跳过门禁**。用 merge-guarded，不裸 git merge。
- **门禁失败不绕行**。补齐治理链后重试。

## 门禁常见坑速查

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section 格式 |
| `promoted_issue_path` missing | candidate 中显式声明路径 |
| `docs/issues/I-*` missing | 创建 kind: linked 的入口 issue.md |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | raw-YYYYMMDD-XXXX 目录名与 candidate date-time key 对齐 |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` 字段（非 owner_issue） |
