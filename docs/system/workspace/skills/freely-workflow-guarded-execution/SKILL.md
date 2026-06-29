---
name: freely-workflow-guarded-execution
description: Freely 开发工作流统一入口。feedback 之后、wt-create 之前必须加载。定义 fix 和 feature 的完整 B1→B2→RED→dev→test-GREEN→pr→merge→close 流程。fix 与 feature 的唯一语义差异在 RED 阶段：fix RED = 复现 bug，feature RED = 设计测试——功能未实现时，按测试方法测试一定是 RED，实现正确后，用实现前一样的测试方法，结论一定是 GREEN
---

# skill:freely-workflow-guarded-execution

> 全链路: [cmd] freely feedback → [skill][here] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close
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

**Freely 所有开发工作的唯一流程入口。** feedback 创建 raw issue 后、wt-create 建工位前必须加载本 skill。

fix（bug修复）和 feature（新功能/大型改动）共用同一个流程，唯一语义差异在 RED 阶段：

| 维度 | fix | feature |
|------|-----|---------|
| 分支前缀 | `fix/*` / `hotfix/*` | `feature/*` |
| wt-create | `--kind fix` | `--kind feature` |
| B1/B2/门禁 | 完全一致 | 完全一致 |
| hotfix | 合并到 main + develop | 无 |

## fix 与 feature 的唯一差异：RED 阶段

流程结构完全一致。唯一语义差异在 RED 阶段——测试方法相同，结论不同：

| | fix RED | feature RED |
|------|----------|------------|
| **测试方法** | 已有测试 / 新测试 / 手工端到端复现 | 端到端（必须）→ 集成 → 单元 |
| **RED 结论** | bug 存在时测试一定是 RED | 功能未实现时测试一定是 RED |
| **GREEN 结论** | 修复正确后，同一套测试一定是 GREEN | 实现正确后，同一套测试一定是 GREEN |
| **意外 PASS** | bug 不存在/测试写错了 → 回 B2 修 | 功能已存在/测试写错了 → 回 B2 修 |

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
| **还在** | 直接在 feature 上做完整流程 |
| **已退役（已合并/已删）** | wt-create --kind fix 创建 fix 工位 |

### 再判严重程度

| 类型 | 分支 | wt-create |
|---|---|---|
| 普通 fix | `fix/raw-{key}-{slug}` | `--kind fix` |
| 紧急 hotfix | `hotfix/<desc>-<YYYYMMDD>` | `--kind hotfix` |
| 新功能/重构 | `feature/raw-{key}-{slug}` | `--kind feature` |

---

## 工作流

### 阶段 0：判断 raw issue 是否存在

拿到任务后第一步——判断是否已有 raw issue：

**有 raw issue** → 进入「前置审视」。
**没有 raw issue** → 先用 `./bin/freely feedback` 创建 raw issue：

```
./bin/freely feedback --title "fix|feat|docs|refactor: <描述>" --kind <fix|feature> --body "<详细描述>"
```

拿到返回的 raw-{key} 后，继续用 `./bin/wt-create` 创建工位（见阶段 1）。

### 前置审视：审视 issue 价值与时效性

进入任何场景前，先审视 raw issue 是否过时、是否仍有价值、是否已被其他变更覆盖。若已无价值，不执行流程，写交接回主管说明理由。

### 阶段 1：B1_IBM 预研

```
1. ./bin/wt-create --raw-key <key> --kind <fix|feature|hotfix> --slug <slug>
2. cd 到 wt-create 输出的开发工位目录（必须，不 cd 则后续命令在 develop 上执行，直接违规）
3. skill:freely-doc-B1_IBM-execution
   → 预研收敛 → candidate 入里程碑
4. candidate promoted → 进入 B2
```

详细步骤见 `skill:freely-doc-B1_IBM-execution`。

### 阶段 2：B2_IBM

```
1. skill:freely-doc-B2_IBM-execution
   → I-* issue + pre-tests（red-green-status = pending）+ tasks + code-review
   → fix: 写清楚复现方法。feature: 端到端→集成→单元设计测试
2. phase_state = done_b2_ibm → 进入 RED
```

详细步骤见 `skill:freely-doc-B2_IBM-execution`。

### 阶段 3：RED（写代码之前。不通过 RED，不允许写实现代码）

```
1. skill:freely-test-RED-execution
   → fix: 用同一套测试复现 bug，确认 RED
   → feature: 用设计的测试确认功能未实现，确认 RED
2. 全部 red-green-status = red → 进入 dev
```

详细步骤（含意外 PASS 处理）见 `skill:freely-test-RED-execution`。

### 阶段 4：Dev 实现

```
1. skill:freely-dev-loop-execution
   → 测试先行，代码后行。不碰 pre-tests.md。
   → 写 code-review + Implementation Decision Note
```

详细步骤见 `skill:freely-dev-loop-execution`。

### 阶段 5：test-GREEN（测试工位最终验证）

```
1. skill:freely-test-execution
   → 在与开发工位 raw key 相同的 test-* 测试工位执行
   → 先 cherry-pick 同步全部 dev 提交，再跑全量测试
   → 全部 green → in_verification → pr-create
   → 不 green → 回阶段 4 修复 → 重新同步 → 重跑
```

GREEN 判定标准和详细步骤见 `skill:freely-test-execution`。

### 阶段 6：pr-create-guarded 提 PR

```
1. 在开发工位执行 ./bin/pr-create-guarded
2. 自动完成：pull develop → 冲突处理 → dry-run gate → push → platform-adapter
```

### 阶段 7：pr-review-guarded 独立 review

```
1. ./bin/pr-review-guarded <branch>
2. 6 维 review → verdict 文档
```

### 阶段 8：pr-merge-guarded 门禁合并

```
1. 切换到 develop 分支: git checkout develop
2. ./bin/pr-merge-guarded develop <branch>
3. PR gate → promotion gate → merge → develop-push → platform-adapter close
```

### 阶段 9：wt-close 收口

```
1. ./bin/wt-close test-pre-merge-<key>-<slug>  # 先关测试工位
2. ./bin/wt-close <branch>                      # 再关开发工位
```

---

## Gate 处理

- 合并前必须运行 `./bin/governance-merge-gate --range "develop..HEAD"`
- `--range` 只检查本分支的变更，不受 develop 预存错误干扰
- 分支自己的 gate 错误：用对应 skill 修复
- 预存错误（非本分支引入）：报告但不阻塞
- gate 失败 ≥3 次：回传 `worker_blocked` + 具体的 gate 输出

## 硬性规则

- **流程顺序不可变**。B1 → B2 → RED → dev → test-GREEN → pr，fix 和 feature 一致。
- **不发明新分支名**。只用 `fix/*`、`feature/*`、`hotfix/*`、`test-pre-merge-*`。
- **test 工位是纯验证沙箱**，禁止在上面直接开发。代码在开发工位写，cherry-pick 到测试工位验证。
- **B1 必须有根因分析**，不修表面症状。
- **B2 必须有 pre-tests**，覆盖全部改动面的测试方案，端到端优先。
- **RED 不可跳过**。不通过 RED 不允许写实现代码。
- **原 feature 还在就直接在上面修**，不新建工位。
- `freely pr-create-guarded` 和 `freely pr-merge-guarded` 是提 PR 和合并的唯一合法入口。
- `freely pr-merge-guarded` 必须在 develop 分支执行。
- **禁止用原子命令绕过**：gh pr create、gh pr merge --admin、git push --force、git merge。

## 门禁常见坑速查

> 完整 IBM 治理坑速查见:
> - `skill:freely-doc-B1_IBM-execution` §门禁常见坑速查 (candidate/source_candidate/milestone)
> - `skill:freely-doc-B2_IBM-execution` §门禁常见坑速查 (I-* issue/verification/code-review)

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section |
| `promoted_issue_path` missing | candidate 显式声明 |
| `docs/epics/**/issues/I-*` missing | 创建 kind: linked 入口 |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | 目录名对齐 candidate date-time key |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` |
| `verification_artifact_dir` missing | issue 添加此字段 |
| B1 brainstorms 缺失 | 必须写完整的根因分析和方案评估 |
| B2 pre-tests 缺失 | 必须有覆盖全部改动面的 pre-tests，端到端优先 |
| RED 未通过就进了 dev | 回退，先跑 skill:freely-test-RED-execution |
| red-green-status 不是 green 就提 PR | 完成 RED→dev→GREEN 循环 |
