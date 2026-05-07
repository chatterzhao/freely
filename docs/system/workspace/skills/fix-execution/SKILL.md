---
name: fix-execution
description: 快速修复 bug 的特殊高效策略——用 test-pre-merge-* 私有工位隔离快测，cp 到可写工位正式提交，不违背保护分支的本质约束。
---

# skill:fix-execution

## 定位

**fix skill 是特殊场景的高效策略，不是通用开发流程。**

常规开发走 `feature → test-pre-merge-* → develop` 完整链路，每个门禁都过。但 bug 修复有特殊性：需要快速迭代验证（改了测、测了改），如果每次改一行代码都走一遍完整门禁链路，效率极低。

本 skill 在不违背保护分支本质约束的前提下，用 `test-pre-merge-*` 作为私有快速测试沙箱，验证通过后将修改转移到可写工位，正式提交和门禁合并仍在合规分支上完成。

**不违背本质**：
- `test-pre-merge-*` 的保护约束是禁止 add/commit/push（防止未经审查的代码进入共享历史）。fix skill 在上面只产生 dirty state，不 add、不 commit、不 push。这与约束的精神完全一致——保护的是共享历史，不是阻止本地文件修改。
- 正式提交发生在可写工位（feature/hotfix），合并走 merge-guarded 合规路径。与常规开发的区别仅在于"快速测试在哪做"，提交和合并的合规性完全相同。

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

**关键**：修改只在 test-pre-merge-* 上以 dirty state 存在，验证通过后 cp 到可写工位（feature/hotfix）正式 add+commit。test-pre-merge-* 上的 dirty 修改最终被丢弃。正式提交全在可写工位，合并也走可写工位 → test-pre-merge-* → develop 的合规路径。

### test-pre-merge-* 的两层职能

`test-pre-merge-*` 在本项目中承担两层职责，fix skill 主要用第一层：

| 职能 | 说明 | fix skill 用？ |
|---|---|---|
| **运行时测试环境** | hook 复制 config.env、freely.db、tool-boundary，与 develop/main 等效。可以 stop/start daemon 做端到端验证。 | ✅ 核心用途 |
| **Merge 集成验证** | 将 feature/hotfix 分支 merge 进来，检查冲突、处理冲突、验证合并后代码可工作。这是进入 develop 前的最后一道闸。 | ✅ 可写工位走正常路径时经过 |

> fix skill 的快测阶段只用第一层（运行时环境）。第二层（merge 集成）在可写工位走 `feature → test-pre-merge-* → develop` 正常路径时自然经过——冲突在那个阶段被发现和处理。

---

## 分支规范速查（全部已有，不发明新名）

| 分支 | 可写 | 可提交 | 用途 |
|---|---|---|---|
| `main` | ❌ | ❌ | 发布目标 |
| `develop` | ❌ | ❌ | 集成目标 |
| `test-pre-merge-*` | ❌ | ❌ | 预集成验证批次 / 私有测试沙箱 |
| `fix/*` | ✅ | ✅ | bug 修复专用 |
| `feature/*` | ✅ | ✅ | 功能开发 |
| `feature/premerge-*` | ✅ | ✅ | 冲突收敛（格式: `feature/premerge-YYYYMMDDTHHMMZ--<topic>`） |
| `hotfix/*` | ✅ | ✅ | 紧急 fix，可直达 develop |

合并路径（来自 merge-guarded）:
```
fix/*             → test-pre-merge-* → develop
feature/*         → test-pre-merge-* → develop
feature/premerge-* → test-pre-merge-* → develop
hotfix/*          → test-pre-merge-* → develop  (或 hotfix/* → develop 直达)
hotfix/*          → main
```

---

## 适用场景

### 先判：原 feature worktree 还在不在

| 原 feature 工位 | 做法 |
|---|---|
| **还在** | 直接在 feature 上改 → 测 → 提交。走 feature → test-pre-merge-* → develop |
| **已退役（已合并/已删）** | 建 `test-pre-merge-*` 私有工位快测 → cp 到新建的 `fix/*` 或 `hotfix/*` |

### 再判严重程度

| 类型 | 分支 | 合并路径 |
|---|---|---|
| 普通 fix | `fix/raw-{raw-key}-{slug}` | fix → test-pre-merge-* → develop |
| 紧急 hotfix | `hotfix/<desc>-<YYYYMMDD>` | hotfix → develop（可跳过 test-pre-merge-*） |

---

## 工作流

### 场景 A：原 feature worktree 还在

```
原 feature worktree（可写）
  │
  ├─ 直接在上面改源码
  ├─ stop → start daemon → 验证
  ├─ 迭代到修复稳定
  ├─ git commit（增量提交，不等全部完成）
  └─ 走 feature → test-pre-merge-* → develop 正常路径
```

### 场景 B：原 feature 已退役

```
阶段 1 — wt-create 一次性创建两个工位
  │
  ├─ ./bin/wt-create --raw-key <key> --source <source> \
  │     --skill docs/system/workspace/skills/fix-execution/SKILL.md \
  │     --slug <slug>
  │
  │   自动创建:
  │   ├─ test-pre-merge-{raw-key}-{slug}  (基于 develop)
  │   └─ fix/raw-{raw-key}-{slug}         (基于 test-pre-merge)
  │
  ├─ 紧急 hotfix: 手动创建 hotfix 分支
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
  ├─ skill:doc-B1_IBM-execution → raw → candidate
  ├─ skill:doc-B2_IBM-execution → candidate → I-* issue → progress
  ├─ skill:dev-loop-execution → code-review（必须 ## Implementation Decision Note）+ pre-tests
  └─ milestones.md

阶段 4 — 门禁合并
  │
  ├─ 运行 ./bin/governance-merge-gate --range "develop..HEAD" 只检查本分支
  ├─ gate 失败：用对应 skill 修复分支自己的错误，预存错误不阻塞
  ├─ gate 通过：fix 基于 test-pre-merge → merge 为 fast-forward
  │     ./bin/merge-guarded test-pre-merge-<name> fix/<name>
  │         → 验证 → ./bin/merge-guarded develop test-pre-merge-<name>
  ├─ 紧急: ./bin/merge-guarded develop hotfix/<name>
  └─ 可选: git checkout main && ./bin/merge-guarded main hotfix/<name>

阶段 5 — 收尾
  │
  ├─ 丢弃 test-pre-merge-* 上的 dirty 修改（已经 cp 到可写工位）
  │     cd <test-pre-merge-wt> && git checkout -- . && git clean -fd
  ├─ 删除 test-pre-merge-* 工位
  │     git worktree remove <test-pre-merge-wt>
  └─ git branch -D test-pre-merge-<name>
```

---

## 硬性规则

- **不发明新分支名**。只用 `fix/*`、`feature/*`、`feature/premerge-*`、`hotfix/*`、`test-pre-merge-*`。
- **test-pre-merge-* 上不 commit、不 push**。只改源码快速测试，修改全部 cp 到可写工位。
- **fix 工位早期创建**，增量 cp + commit，不堆到最后。
- **原 feature 还在就直接在上面修**，不新建工位。
- **治理后置**，验证通过再写。
- **根因深挖**，不修表面症状。
- **不跳过门禁**，用 merge-guarded。

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
