---
name: freely-fix-execution
description: 快速修复 bug 的特殊高效策略——用 test-pre-merge-* 私有工位隔离快测，cp 到可写工位正式提交，不违背保护分支的本质约束。
---

# skill:freely-fix-execution

> 全链路(Fix变体): wt-create → dev → test → B1 → B2 → pr-create → pr-merge → wt-close
>                                    ↑ 本 skill 自此开始（快测沙箱策略，治理后置）

## 定位

**fix skill 是特殊场景的高效策略，不是通用开发流程。**

常规开发走 `feature → test-pre-merge → pr-create-guarded → pr-merge-guarded develop` 完整链路，每个门禁都过。但 bug 修复有特殊性：需要快速迭代验证（改了测、测了改），如果每次改一行代码都走一遍完整门禁链路，效率极低。

本 skill 在不违背保护分支本质约束的前提下，用 `test-pre-merge-*` 作为私有快速测试沙箱，验证通过后将修改转移到可写工位，正式提交和门禁合并仍在合规分支上完成。

**不违背本质**：
- `test-pre-merge-*` 的保护约束是禁止 add/commit/push（防止未经审查的代码进入共享历史）。fix skill 在上面只产生 dirty state，不 add、不 commit、不 push。这与约束的精神完全一致——保护的是共享历史，不是阻止本地文件修改。
- 正式提交发生在可写工位（fix/hotfix），合并走 pr-merge-guarded 合规路径。与常规开发的区别仅在于"快速测试在哪做"，提交和合并的合规性完全相同。

## 核心原则

> **Fix first, govern later. Test in isolation, commit to writable.**

- 不在 `main`/`develop` 上直接改代码（阻塞其他 AI 并发）
- 用 `test-pre-merge-*` 私有工位快速测试（不改不提交不推送，不违背保护约束）
- 测完 cp 修改到可写工位（原 feature 还在就 cp 回去，已退役就 cp 到新 fix 工位）
- 治理文档在修复验证后才写

---

## 为什么 test-pre-merge-* 可以用于测试

`test-pre-merge-*` 的保护约束是禁止写入（add/commit）和推送（CONSTITUTION.md §2, LAWS.md §2）。fix skill 用它做的是：

```
test-pre-merge-* 上的操作:
  改源码 → ✅ 产生 dirty state（私有工位，仅自己可见）
  git add → ❌ 不做
  git commit → ❌ 不做
  git push → ❌ 不做（pre-push hook 也阻止）
  cp 修改到可写工位 → ✅ 转移修改
  清理 dirty state → ✅ git checkout -- . / git clean -fd
```

**关键**：修改只在 test-pre-merge-* 上以 dirty state 存在，验证通过后 cp 到可写工位（fix/hotfix）正式 add+commit。test-pre-merge-* 上的 dirty 修改最终被丢弃。正式提交全在可写工位，合并也走可写工位 → develop 的合规路径。

### test-pre-merge-* 作为丢弃式测试沙箱

`test-pre-merge-*` 是**丢弃的测试沙箱**，不参与任何合并链：

| 职能 | 说明 |
|---|---|
| **私有测试沙箱** | 仅在本地用于快速迭代验证，不参与任何合并链。hook 复制 config.toml、freely.db、tool-boundary，与 develop/main 等效。可以 stop/start daemon 做端到端验证，验证后丢弃。 |

---

## 分支规范速查（全部已有，不发明新名）

| 分支 | 可写 | 可提交 | 用途 |
|---|---|---|---|
| `main` | ❌ | ❌ | 发布目标 |
| `develop` | ❌ | ❌ | 集成目标 |
| `test-pre-merge-*` | ❌ | ❌ | 预集成验证批次 / 私有测试沙箱 |
| `fix/*` | ✅ | ✅ | bug 修复专用 |
| `feature/*` | ✅ | ✅ | 功能开发 |
| `fix/premerge-*` | ✅ | ✅ | 冲突收敛（格式: `fix/premerge-YYYYMMDDTHHMM[SS]Z--<topic>`） |
| `hotfix/*` | ✅ | ✅ | 紧急 fix，可直达 develop |

合并路径（来自 pr-merge-guarded）:
```
fix/*             → test-pre-merge → pr-create-guarded → pr-merge-guarded
fix/*             → test-pre-merge → pr-create-guarded → pr-merge-guarded
hotfix/*          → main + develop (pr-merge-guarded)
hotfix/*          → main
```

### 分支 base 差异

| 分支类型 | 默认 base | 说明 |
|---|---|---|
| `fix/*` | develop | bug 修复，从 develop 派生，通过 pr-merge-guarded 合并回 develop |
| `hotfix/*` | main | 紧急修复，从 main 的标签派生，通过 pr-merge-guarded 合并回 main 和 develop |

---

## 适用场景

### 先判：原 feature worktree 还在不在

| 原 feature 工位 | 做法 |
|---|---|
| **还在** | 直接在 feature 上改 → 测 → 提交。走 feature → test-pre-merge → pr-create-guarded → pr-merge-guarded develop |
| **已退役（已合并/已删）** | 建 `test-pre-merge-*` 私有工位快测 → cp 到新建的 `fix/*` 或 `hotfix/*` → `freely pr-create-guarded` 命令 → `freely pr-merge-guarded develop <branch>` 命令 → `freely wt-close` 命令 |

### 再判严重程度

| 类型 | 分支 | 合并路径 |
|---|---|---|
| 普通 fix | `fix/raw-{raw-key}-{slug}` | fix → test-pre-merge → pr-create-guarded → pr-merge-guarded develop |
| 紧急 hotfix | `hotfix/<desc>-<YYYYMMDD>` | hotfix → pr-merge-guarded main + develop（可跳过 test-pre-merge） |

---

## 工作流

### 前置：审视 issue 价值与时效性

进入任何场景前，先审视 raw issue 是否过时、是否仍有价值、是否已被其他变更覆盖。若已无价值，不执行 fix 流程，写交接回主管说明理由。

### 场景 A：原 feature worktree 还在

```
原 feature worktree（可写）
  │
  ├─ 前置检查通过（issue 仍有价值）
  ├─ 直接在上面改源码
  ├─ stop → start daemon → 验证
  ├─ 迭代到修复稳定
  ├─ git commit（增量提交，不等全部完成）
  └─ 走 feature → test-pre-merge → pr-create-guarded → pr-merge-guarded develop 完整路径
```

### 场景 B：原 feature 已退役

```
阶段 1 — wt-create 一次性创建两个工位
  │
  ├─ 前置检查通过（issue 仍有价值）
  │
  ├─ ./bin/wt-create --raw-key <key> --source <source> \
  │     --skill docs/system/workspace/skills/freely-fix-execution/SKILL.md \
  │     --slug <slug>
  │
  │   自动创建:
  │   ├─ fix/raw-{raw-key}-{slug}         (基于 develop，永久开发工位)
  │   └─ test-pre-merge-{raw-key}-{slug}  (基于 fix，临时测试工位)
  │
  │
  ├─ 在 test-pre-merge 工位中改源码 → stop/start daemon → 验证
  ├─ 深挖根因链，反复迭代
  └─ 此阶段不 commit、不 push、不写治理文档

阶段 2 — 增量 cp 到可写工位，commit
  │
  ├─ 每个阶段性修复验证通过后 cp + commit:
  │     cp <test-pre-merge-wt>/path/to/file <fix-wt>/path/to/file
  │     cd <fix-wt> && git commit -m "fix: <阶段性描述>"
  │
  └─ 增量提交，不堆到最后

阶段 3 — 补齐治理（调用下层 skill）
  │
  ├─ skill:freely-doc-B1_IBM-execution → raw → candidate
  ├─ skill:freely-doc-B2_IBM-execution → candidate → I-* issue → progress
  ├─ skill:freely-dev-loop-execution → code-review（必须 ## Implementation Decision Note）+ pre-tests
  └─ milestones.md

阶段 4a — 提 PR
  │
  ├─ 在 fix worktree 中执行 `freely pr-create-guarded` 命令
  ├─ 自动完成：pull develop → 冲突处理 → dry-run gate → push → gh pr create
  ├─ 禁止用 gh pr create 命令替代
  │
阶段 4b — 门禁合并
  │
  ├─ 切换到 develop 分支：git checkout develop
  ├─ 在 develop 分支执行 `freely pr-merge-guarded develop fix/<name>` 命令
  ├─ 自动完成：PR gate → promotion gate → gh pr merge → 本地同步 → 推送全部 remote → issue 同步
  ├─ 禁止用 gh pr merge --admin 命令替代
  ├─ 紧急: freely pr-merge-guarded develop hotfix/<name>
  └─ 可选: git checkout main && freely pr-merge-guarded main hotfix/<name>

阶段 5 — 收尾
  │
  ├─ 丢弃 test-pre-merge-* 上的 dirty 修改（已经 cp 到可写工位）
  │     cd <test-pre-merge-wt> && git checkout -- . && git clean -fd
  ├─ 执行 `freely wt-close test-pre-merge-<name>` 命令关闭测试工位
  └─ 执行 `freely wt-close fix/<name>` 命令关闭 fix 工位和分支（PR 已合并到 develop）
```

---

## 硬性规则

- **不发明新分支名**。只用 `fix/*`、`feature/*`、`feature/premerge-*`、`hotfix/*`、`test-pre-merge-*`。
- **test-pre-merge-* 上不 commit、不 push**。只改源码快速测试，修改全部 cp 到可写工位。
- **fix 工位早期创建**，增量 cp + commit，不堆到最后。
- **原 feature 还在就直接在上面修**，不新建工位。
- **治理后置**，验证通过再写。
- **根因深挖**，不修表面症状。
- **不跳过门禁**，`freely pr-create-guarded` 命令和 `freely pr-merge-guarded` 命令是提 PR 和合并的唯一合法入口。
- **禁止用原子命令绕过**：gh pr create、gh pr merge --admin、git push --force、git merge 等原子命令不得替代 pr-create-guarded / pr-merge-guarded 命令。

## 门禁常见坑速查

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section |
| `promoted_issue_path` missing | candidate 显式声明 |
| `docs/issues/I-*` missing | 创建 kind: linked 入口 |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | 目录名对齐 candidate date-time key |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` |
| `verification_artifact_dir` missing | issue 添加此字段 |
| `phase_state: done` 被拒 | 用 `in_dev` |
