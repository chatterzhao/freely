---
name: fix-execution
description: 快速修复 bug 的工作流——先判场景选工位类型，用现有 test-pre-merge 隔离测试，决定 fix 即建工位、增量提交，治理后置。
---

# skill:fix-execution

## 核心原则

> **Fix first, govern later. Isolate test, commit early.**

- 不在 main/develop 上直接改代码测试
- 修复决定即建工位，阶段性 cp 修改过去提交
- 治理文档在修复验证后才写

---

## 适用场景（先判再动）

### 按"在哪发现"分类

| 发现位置 | 原 feature 工位 | 做法 |
|---|---|---|
| feature worktree 还在 | 存在 | **直接在 feature 上修**，走正常 feature → test-pre-merge → develop。不需要新建工位。 |
| feature 已合并、worktree 已删 | 不存在 | 新建工位（见下方"按严重程度"），在 test-pre-merge 上隔离测试 |
| develop / main 测试时发现 | 不存在 | 新建工位 + test-pre-merge 隔离测试。**不能在 protected branch 上直接改。** |
| test-pre-merge 测试时发现 | 可能存在 | 回 source feature 修；若 feature 已删，新建 feature 工位修 |

### 按"严重程度"选择工位类型

| 类型 | 分支命名 | 合并路径 | 适用场景 |
|---|---|---|---|
| **普通 fix** | `feature/<desc>-<YYYYMMDD>` | feature → test-pre-merge → develop | 常规 bug，不走捷径 |
| **紧急 hotfix** | `hotfix/<desc>-<YYYYMMDD>` | hotfix → develop（可再到 main） | 运行时 crash、daemon 不可用等阻断性问题 |

> `hotfix/*` 在 merge-guarded 中允许直接到 develop（跳过 test-pre-merge），但治理门禁仍然完整。普通 fix 用 `feature/*`，走完整的 test-pre-merge 验证链路。

### 为什么不做"从下往上修再合并"

```
反模式（慢）:
  在 develop 发现 bug → 建 feature → 修 → test-pre-merge → develop
  每个门禁都走一遍，改一行代码可能花几十分钟过门禁

fix skill 方式（快）:
  在 develop 发现 bug → 建 test-pre-merge 隔离测试 → 直接在上面改、测
  → 确定修复后建 feature/hotfix 工位 → cp 过去 → 走一次门禁
```

---

## 工作流

### 阶段 1：创建 test-pre-merge 隔离测试

```
发现 bug（main / develop / 任意位置）
  │
  ├─ 1. 如果原 feature worktree 还在，跳过此步——直接在 feature 上改
  │
  ├─ 2. 否则创建 test-pre-merge 工位隔离测试
  │     ./bin/wt-create test-pre-merge/<desc>-<YYYYMMDD> --base develop
  │
  │     test-pre-merge 的 hook 自动复制 config.env、freely.db、tool-boundary
  │     运行时环境与 develop 等效，但不阻塞其他 AI 在 develop 上的并发工作
  │
  ├─ 3. 初始化运行时
  │     ./bin/pre-init-runtime --pre-project <pre-worktree-path>
  │
  ├─ 4. 直接在 test-pre-merge 上改源码
  │     stop → start daemon → 验证 → 迭代
  │
  ├─ 5. 深挖根因链，不要止于表面症状
  │
  └─ 此阶段不创建治理文档
```

### 阶段 2：决定 fix 即建工位，增量提交

```
决定要 fix（此时就建工位，不等修复完成）
  │
  ├─ 1. 按严重程度选工位类型
  │     普通: ./bin/wt-create feature/<desc>-<YYYYMMDD> --base develop
  │     紧急: ./bin/wt-create hotfix/<desc>-<YYYYMMDD> --base develop
  │
  ├─ 2. 每次在 test-pre-merge（或 feature）验证通过一个阶段性修复
  │     立刻 cp 到 fix 工位提交：
  │     cp <test-wt>/path/to/file <fix-wt>/path/to/file
  │     cd <fix-wt> && git add -A && git commit -m "fix: <阶段性描述>"
  │
  ├─ 3. 测试工位继续迭代下一层根因 → 验证 → cp → commit
  │
  └─ 增量提交，commit 干净整洁：
        ├─ commit 1: fix KeyError crash
        ├─ commit 2: fix reader thread zombie exit
        ├─ commit 3: add bridge health check
        ├─ commit 4: fix session/set_mode after resume
        ├─ commit 5: split stdin_write_lock from server_lock
        └─ ...
```

### 阶段 3：补齐治理

```
fix 工位（修复已全部提交）
  │
  ├─ 1. raw issue: docs/issues/raw-<YYYYMMDD>-<key>/issue.md
  │     kind: raw, status: absorbed, absorbed_into: I-<id>
  ├─ 2. candidate: docs/pre-brainstorms/<YYYYMMDD>-<key>/candidates.md
  │     status: promoted, promoted_issue_path 指向 canonical issue
  ├─ 3. canonical issue（两处）:
  │     docs/issues/I-<id>/issue.md           (kind: linked)
  │     docs/epics/<epic>/<name>/issues/I-<id>.md
  │     必须包含: phase_state=in_dev, verification_artifact_dir
  ├─ 4. progress: docs/progress/<epic>/p-<name>.md
  ├─ 5. code-review（必须含 ## Implementation Decision Note）:
  │     - decision / why_this / alternatives_considered
  │     - boundary_non_goals / residual_risk
  ├─ 6. 更新 docs/milestones.md → committed_issues
  │
  └─ 治理文档也增量 commit
```

### 阶段 4：门禁合并

```
普通 fix (feature/*):
  feature → test-pre-merge → develop
  │
  ├─ ./bin/merge-guarded test-pre-merge/<name> feature/<name>
  ├─ 在 test-pre-merge 上验证
  └─ ./bin/merge-guarded develop test-pre-merge/<name>

紧急 hotfix (hotfix/*):
  hotfix → develop（可跳过 test-pre-merge）
  │
  └─ ./bin/merge-guarded develop hotfix/<name>

可选: git checkout main && ./bin/merge-guarded main hotfix/<name>
```

### 阶段 5：收尾

```
  ├─ 1. 删除 test-pre-merge 工位
  │     git worktree remove <pre-wt> && git branch -D test-pre-merge/<name>
  ├─ 2. 清理测试工位的 dirty state
  └─ 3. 可选: release 分支作为 stable 引用
```

---

## 工位类型速查

| 工位 | 用途 | 生命周期 |
|---|---|---|
| `test-pre-merge/*` | 隔离测试，hook 复制 runtime（**已有机制**） | 临时，修完即删 |
| `feature/*` | 普通 fix 的正规提交工位 | 合并后 retire |
| `hotfix/*` | 紧急 fix，可直达 develop | 合并后 retire |

---

## 硬性规则

- **先判场景**。原 feature worktree 还在就直接在上面修；不存在才新建。
- **用现有 test-pre-merge 隔离测试**。不在 main/develop 上直接改代码。
- **fix 工位早期创建**。决定 fix 就建，不等到修复完成。
- **增量 cp + commit**。每个阶段验证通过就 cp 提交。
- **治理后置**。修复验证过了再写治理文档。
- **根因深挖**。一个表面修复可能掩盖更深问题。
- **不跳过门禁**。用 merge-guarded，不裸 git merge。

## 门禁常见坑速查

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section 格式 |
| `promoted_issue_path` missing | candidate 里显式声明 |
| `docs/issues/I-*` missing | 创建 kind: linked 入口 |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | 目录名对齐 candidate date-time key |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` |
| `verification_artifact_dir` missing | issue 里添加此字段 |
| `phase_state: done` 被拒 | develop merge 用 `in_dev` |
