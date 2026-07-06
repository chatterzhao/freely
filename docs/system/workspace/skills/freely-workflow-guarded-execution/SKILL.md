---
name: freely-workflow-guarded-execution
description: >-
  Freely 项目所有开发工作的唯一流程入口。编排从 `freely feedback` 命令到
  `freely wt-close` 命令的完整生命周期。底层是 raw → candidate（C-{key}-A）
  → milestone（M-{key}-A）→ I-* issue（I-{key}-A）四节点链路，上层是 B1 预研 →
  B2 设计 → RED 测试先行 → dev 实现 → test-GREEN 验证 → PR 门禁合并 → 收口。
  fix 和 feature 共用同一流程。

  Use when: starting any development task, fixing a bug, implementing
  a feature, creating a worktree, or when the user mentions "修 bug",
  "开工位", "开发流程", "怎么开始", "反馈", "提 PR" without specifying
  which skill to use. Also use when the user describes a task without
  a clear workflow — this skill provides the canonical process.
---

# skill:freely-workflow-guarded-execution

> 全链路: [skill][here] freely-workflow-guarded-execution → [cmd] freely feedback → [cmd] freely wt-create（创建工位后cd到工位进行工作） → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close
>
> 文档中可能用简称指代上述节点。对应关系:
>
> | 简称 | 全称 | 类型 |
> |------|------|------|
> | feedback / feedback 命令 | `freely feedback` | [cmd] |
> | workflow / workflow skill | `freely-workflow-guarded-execution` | [skill] |
> | wt-create | `freely wt-create` | [cmd] |
> | B1 / B1 skill / B1_IBM | `freely-doc-B1_IBM-execution` | [skill] |
> | B2 / B2 skill / B2_IBM | `freely-doc-B2_IBM-execution` | [skill] |
> | RED / RED skill | `freely-test-RED-execution` | [skill] |
> | dev / dev-loop | `freely-dev-loop-execution` | [skill] |
> | test / test-GREEN / test skill | `freely-test-execution` | [skill] |
> | pr-create | `freely pr-create-guarded` | [cmd] |
> | pr-review | `freely pr-review-guarded` | [cmd] |
> | pr-merge | `freely pr-merge-guarded` | [cmd] |
> | wt-close | `freely wt-close` | [cmd] |

## 定位

**Freely 所有开发工作的唯一流程入口。** 在任何开发工作开始之前（即 `freely feedback` 命令之前），必须先加载本 `freely-workflow-guarded-execution` skill。它判定是否需要创建 raw issue、是否需要复用已有工位。

fix（bug修复）和 feature（新功能/大型改动）共用同一个流程，唯一语义差异在 `freely-test-RED-execution` skill 阶段：

| 维度 | fix | feature |
|------|-----|---------|
| 分支前缀 | `fix/*` / `hotfix/*` | `feature/*` |
| `freely wt-create` 命令 | `--kind fix` | `--kind feature` |
| `freely-doc-B1_IBM-execution` / `freely-doc-B2_IBM-execution` / 门禁 | 完全一致 | 完全一致 |
| hotfix | 合并到 main + develop | 无 |

## fix 与 feature 的唯一差异：`freely-test-RED-execution` skill 阶段

流程结构完全一致。唯一语义差异在 `freely-test-RED-execution` skill 阶段——测试方法相同，结论不同：

| | fix RED | feature RED |
|------|----------|------------|
| **测试方法** | 已有测试 / 新测试 / 手工端到端复现 | 端到端（必须）→ 集成 → 单元 |
| **RED 结论** | bug 存在时测试一定是 RED | 功能未实现时测试一定是 RED |
| **GREEN 结论** | 修复正确后，同一套测试一定是 GREEN | 实现正确后，同一套测试一定是 GREEN |
| **意外 PASS** | bug 不存在/测试写错了 → 用 `freely-doc-B2_IBM-execution` skill 修正测试设计 | 功能已存在/测试写错了 → 用 `freely-doc-B2_IBM-execution` skill 修正测试设计 |

详细执行步骤见 `skill:freely-test-RED-execution`。workflow skill 不重复描述——编排交给本 skill，执行交给子 skill。

## 分支规范速查

| 分支 | 可写 | 可提交 | 用途 |
|---|---|---|---|
| `main` | ❌ | ❌ | 发布目标 |
| `develop` | ❌ | ❌ | 集成目标 |
| `test-pre-merge-*` | ❌ | ❌ | 丢弃式测试沙箱 |
| `fix/*` | ✅ | ✅ | bug 修复 |
| `feature/*` | ✅ | ✅ | 功能开发 |
| `hotfix/*` | ✅ | ✅ | 紧急修复，合并到 main + develop |

合并路径（来自 pr-merge-guarded）:
```
fix/*             → develop
feature/*         → develop
hotfix/*          → main + develop
```

## 适用场景

### 先判：原 feature worktree 还在不在

| 原 feature 工位 | 做法 |
|---|---|
| **还在** | 直接在 feature 工位上走完整流程：`freely-doc-B1_IBM-execution` skill → `freely-doc-B2_IBM-execution` skill → `freely-test-RED-execution` skill → `freely-dev-loop-execution` skill → `freely-test-execution` skill |
| **已退役（已合并/已删）** | 用 `freely wt-create --kind fix` 命令创建 fix 工位 |

### 再判严重程度

| 类型 | 分支 | `freely wt-create` 命令 |
|---|---|---|
| 普通 fix | `fix/raw-{key}-{slug}` | `--kind fix` |
| 紧急 hotfix | `hotfix/<desc>-<YYYYMMDD>` | `--kind hotfix` |
| 新功能/重构 | `feature/raw-{key}-{slug}` | `--kind feature` |

---

## 工作流

### 阶段 0：判题 — 搜索相似 raw issue + 决定创建还是复用

拿到任务后，第一步不是用`freely feedback`命令创建 raw issue，也不是直接用`freely wt-create`命令创建工位，然后就按`freely-doc-B1_IBM-execution`skill 开始工作。先做两件事：

#### 0a. 思考 + 搜索相似 raw issue

把问题想清楚，然后搜索是否已有类似 raw issue：
- 搜 `docs/B1-docs/raw-*/issue.md` 的标题和正文
- 搜平台（GitHub/Gitee）上的 open issue
- 搜 `docs/milestones.md` 看看是否已被某个 candidate/issue 覆盖

#### 0b. 根据搜索结果决策

**找到相似的 raw issue：**

| 你的状态 | 做法 |
|---------|------|
| 还没有 raw issue | 不创建新的。用 `freely comment --issue raw-{key} "..."` 命令把新发现追加到已有 raw issue |
| 已有 raw issue，和已有的重复 | 用 `freely wt-close <branch> --platform-only` 命令关掉自己这个的平台 issue，用 `freely comment` 命令追加到已有的 |

**没找到相似的 raw issue：**

| 你的状态 | 做法 |
|---------|------|
| 还没有 raw issue | `freely feedback --title "fix\|feat\|docs\|refactor: <描述>" --kind <fix\|feature> --body "<详细描述>"` 命令 |
| 已有 raw issue | 进入「前置审视」 |

**已有 raw issue 但描述不准确需要改：**

用 `freely feedback edit` 命令：
```
freely feedback edit --raw-key <key> --title "..." --body "..."
```

拿到 raw-{key} 后，继续用 `freely wt-create` 命令创建工位（见阶段 1）。

### 前置审视：剖析 raw issue — B1 起手式

加载 `freely-doc-B1_IBM-execution` skill 之前，必须对 raw issue 做结构化剖析。这不是简单读一遍——而是要拆开看它到底在说什么，为 brainstorms 搭好骨架。

#### 1. 画覆盖域

raw issue 提到了哪些模块、哪些文件、哪些功能点？列出来。每个点 `freely-doc-B1_IBM-execution` skill 都必须分析到。raw 里写了但 brainstorms 没涉及的 → 遗漏。brainstorms 里凭空出现的 → 偏离。

#### 2. 判 scope

这是一个独立问题，还是多个独立子问题的拼盘？
- 一个独立问题 → 一个 candidate
- 多个独立子问题 → 拆成多个 candidate，每个有独立边界
- scope 过大或过小，现在就想清楚理由

#### 3. 想方案方向

这个问题大概有哪些解法方向？不是现在就做决策，而是让 `freely-doc-B1_IBM-execution` skill 执行时不要只盯着一个方案走。每个方向要有具体论据，不能只有一句"这个最好"。

#### 4. 定 fidelity 基线

candidate 的验收条件必须能从 brainstorms 的 Decision 推导出来。promotion gate 必须反映边界分析和依赖关系。现在就想：brainstorms 写出来后，candidate 应该长什么样才算忠实消化？

#### 5. 判价值

这条最优先——raw issue 是否过时？是否已被其他 issue/candidate 覆盖？当前项目阶段是否还相关？
- 若无价值 → 标记 dropped，写理由，不执行后续流程
- 若部分有价值 → 明确缩小 scope，说明放弃的部分及理由

### 阶段 1：`freely-doc-B1_IBM-execution` skill 预研

```
1. freely wt-create --raw-key <key> --kind <fix|feature|hotfix> --slug <slug>
2. cd 到 freely wt-create 命令输出的开发工位目录（必须，不 cd 则后续命令在 develop 上执行，直接违规）
3. 加载 skill:freely-doc-B1_IBM-execution
   → 预研收敛 → candidate 入里程碑
4. candidate promoted → 进入阶段 2
```

详细步骤见 `skill:freely-doc-B1_IBM-execution`。

### 阶段 2：`freely-doc-B2_IBM-execution` skill 设计

```
1. 加载 skill:freely-doc-B2_IBM-execution
   → B 阶段：实现分析 brainstorms → 替代方案评估
   → M 阶段：物化 I-* issue 完整文档 + pre-tests（red-green-status = pending）+ tasks + code-review
   → fix: 写清楚复现方法。feature: 端到端→集成→单元设计测试
2. phase_state = done_b2_ibm → 进入阶段 3
```

详细步骤见 `skill:freely-doc-B2_IBM-execution`。

### 阶段 3：`freely-test-RED-execution` skill — 写代码之前，不通过 RED 不允许写实现代码

```
1. 加载 skill:freely-test-RED-execution
   → fix: 用同一套测试复现 bug，确认 RED
   → feature: 用设计的测试确认功能未实现，确认 RED
2. 全部 red-green-status = red → 进入阶段 4
```

详细步骤（含意外 PASS 处理）见 `skill:freely-test-RED-execution`。

### 阶段 4：`freely-dev-loop-execution` skill 实现

```
1. 加载 skill:freely-dev-loop-execution
   → 测试先行，代码后行。不碰 pre-tests.md。
   → 写 code-review + Implementation Decision Note
```

详细步骤见 `skill:freely-dev-loop-execution`。

### 阶段 5：`freely-test-execution` skill — 测试工位最终验证，全量 GREEN

```
1. 加载 skill:freely-test-execution
   → 在与开发工位 raw key 相同的 test-* 测试工位执行
   → 先 merge（首选）或 git cherry-pick 同步全部 dev 提交到测试工位，再跑全量测试
   → 全部 green → in_verification → 进入阶段 6
   → 不 green → 回阶段 4 用 `freely-dev-loop-execution` skill 修复 → 重新 merge（首选）或 cherry-pick 同步 → 重跑
```

GREEN 判定标准和详细步骤见 `skill:freely-test-execution`。

### 阶段 6：`freely pr-create-guarded` 命令提 PR

```
1. 在开发工位执行 freely pr-create-guarded 命令（禁止在 develop 分支上执行）
2. 自动完成：pull develop → 冲突处理 → dry-run gate → push → platform-adapter
```

### 阶段 7：`freely pr-review-guarded` 命令独立 review

```
1. freely pr-review-guarded <branch>
2. 6 维 review → verdict 文档
```

### 阶段 8：`freely pr-merge-guarded` 命令门禁合并

```
1. 切换到 develop 分支: git checkout develop
2. freely pr-merge-guarded develop <branch>
3. PR gate → promotion gate → merge → develop-push → platform-adapter close
```

### 阶段 9：`freely wt-close` 命令收口

```
1. freely wt-close test-pre-merge-<key>-<slug>  # 先关测试工位
2. freely wt-close <branch>                      # 再关开发工位
```

---

## Gate 处理

- 合并前必须运行 `freely pr-merge-guarded --dry-run develop <branch>`（等价于 `governance-merge-gate --range "develop..HEAD"`）
- `--range` 只检查本分支的变更，不受 develop 预存错误干扰
- 分支自己的 gate 错误：用对应 skill 修复
- 预存错误（非本分支引入）：报告但不阻塞
- gate 失败 ≥3 次：回传 `worker_blocked` + 具体的 gate 输出


## 铁律: 禁止绕过门禁

以下行为违反工作流纪律，任何情况下不得使用:

| 禁止 | 原因 |
|------|------|
| `git push --no-verify` | 跳过 pre-push hook，门禁不执行 |
| `git commit --no-verify` | 跳过 pre-commit hook，pretests-gate 不执行 |
| `gh pr merge --admin` | 跳过 CI PR Merge Guard，即使 red X 也能合并 |
| `git push --force` | 强制覆盖远程历史，丢失他人提交 |
| 手工在 develop 上 git add/commit | 违反 protected branch 原则 |

**唯一的 bypass**: `freely develop-push attempt` — 受控的平台同步，有审计日志。

违反上述铁律的提交，即使在本地通过，CI 硬拦截也会阻止合并。

## 硬性规则

- **流程顺序不可变**。`freely-doc-B1_IBM-execution` → `freely-doc-B2_IBM-execution` → `freely-test-RED-execution` → `freely-dev-loop-execution` → `freely-test-execution` → `freely pr-create-guarded`，fix 和 feature 一致。
- **不发明新分支名**。只用 `fix/*`、`feature/*`、`hotfix/*`、`test-pre-merge-*`。
- **test-pre-merge-* 工位是纯验证沙箱**，禁止在上面直接开发（禁止手动 add+commit 原创）。代码在开发工位（fix/* 或 feature/*）写，用 merge（首选）或 `git cherry-pick` 同步到测试工位验证。
- **`freely-doc-B1_IBM-execution` skill 必须有根因分析**，不修表面症状。
- **`freely-doc-B2_IBM-execution` skill 必须有 pre-tests**，覆盖全部改动面的测试方案，端到端优先。
- **`freely-test-RED-execution` skill 不可跳过**。不通过 RED 不允许写实现代码。
- **原 feature 工位还在就直接在上面修**，不新建工位。
- `freely pr-create-guarded` 命令和 `freely pr-merge-guarded` 命令是提 PR 和合并的唯一合法入口。
- `freely pr-merge-guarded` 命令必须在 develop 分支执行。
- **禁止用原子命令绕过**：`gh pr create`、`gh pr merge --admin`、`git push --force`、`git merge`。

## 门禁常见坑速查

> 完整 IBM 治理坑速查见:
> - `skill:freely-doc-B1_IBM-execution` §门禁常见坑速查 (candidate/source_candidate/milestone)
> - `skill:freely-doc-B2_IBM-execution` §门禁常见坑速查 (I-* issue/verification/code-review)

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section |
| `promoted_issue_path` missing | candidate 显式声明 |
| `docs/B2-docs/**/issues/I-*` missing | 创建 kind: linked 入口 |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | 目录名对齐 candidate date-time key |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` |
| `verification_artifact_dir` missing | issue 添加此字段 |
| B1 brainstorms 缺失 | 必须写完整的根因分析和方案评估 |
| B2 pre-tests 缺失 | 必须有覆盖全部改动面的 pre-tests，端到端优先 |
| RED 未通过就进了 dev | 回退，先跑 skill:freely-test-RED-execution |
| red-green-status 不是 green 就提 PR | 完成 RED→dev→GREEN 循环 |
