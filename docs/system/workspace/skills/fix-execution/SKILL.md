---
name: fix-execution
description: 快速修复 bug 的工作流——用 test-pre-merge-* 私有工位隔离快测，cp 到可写工位正式提交，不违背保护分支约束。
---

# skill:fix-execution

## 核心原则

> **Fix first, govern later. Test in isolation, commit to writable.**

- 不在 `main`/`develop` 上直接改代码（阻塞其他 AI 并发）
- 用 `test-pre-merge-*` 私有工位快速测试（不改不提交不推送，不违背保护约束）
- 测完 cp 修改到可写工位（原 feature 还在就 cp 回去，已退役就 cp 到新 fix 工位）
- 治理文档在修复验证后才写

---

## 为什么 test-pre-merge-* 可以用于测试

`test-pre-merge-*` 受保护分支的约束是：禁止写入、提交、推送（CONSTITUTION.md §2）。但 fix skill 用它做的是：

| 动作 | 在 test-pre-merge-* 上做？ | 违背约束？ |
|---|---|---|
| 改源码验证修复 | ✅ 是（私有工位，仅自己可见） | 否——不提交，不影响其他 AI |
| git commit | ❌ 否 | — |
| git push | ❌ 否（pre-push hook 本身就阻止） | — |
| 正式提交流程 | ❌ 在可写工位（feature/hotfix）上做 | — |

**本质上**: test-pre-merge-* 作为私有测试工位，等同于临时沙箱。修改通过 cp 转移到可写工位，正式提交发生在合规分支上。不阻塞 develop，不影响其他 AI 的并发工作。

---

## 分支规范速查（全部已有，不发明新名）

| 分支 | 可写 | 可提交 | 用途 |
|---|---|---|---|
| `main` | ❌ | ❌ | 发布目标 |
| `develop` | ❌ | ❌ | 集成目标 |
| `test-pre-merge-*` | ❌ | ❌ | 预集成验证批次 / 私有测试沙箱 |
| `feature/*` | ✅ | ✅ | 功能开发 / 普通 fix |
| `feature/premerge-*` | ✅ | ✅ | 冲突收敛（格式: `feature/premerge-YYYYMMDD-HHMM--<topic>`） |
| `hotfix/*` | ✅ | ✅ | 紧急 fix，可直达 develop |

合并路径（来自 merge-guarded）:
```
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
| **已退役（已合并/已删）** | 建 `test-pre-merge-*` 私有工位快测 → cp 到新建的 `feature/*` 或 `hotfix/*` |

### 再判严重程度

| 类型 | 分支 | 合并路径 |
|---|---|---|
| 普通 fix | `feature/<desc>-<YYYYMMDD>` | feature → test-pre-merge-* → develop |
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
阶段 1 — 建 test-pre-merge-* 私有工位快测
  │
  ├─ ./bin/wt-create test-pre-merge-<desc>-<YYYYMMDD> --base develop
  ├─ ./bin/pre-init-runtime --pre-project <path>  # 复制 runtime 状态
  ├─ 直接改源码 → stop/start daemon → 验证
  ├─ 深挖根因链，反复迭代
  └─ 此阶段不 commit、不 push、不写治理文档

阶段 2 — 决定 fix 即建可写工位，增量 cp
  │
  ├─ 普通: ./bin/wt-create feature/<desc>-<YYYYMMDD> --base develop
  │   紧急: ./bin/wt-create hotfix/<desc>-<YYYYMMDD> --base develop
  │
  ├─ 每个阶段性修复验证通过后立刻 cp + commit:
  │     cp <test-pre-merge-wt>/path/to/file <fix-wt>/path/to/file
  │     cd <fix-wt> && git commit -m "fix: <阶段性描述>"
  │
  └─ 增量提交，不堆到最后

阶段 3 — 补齐治理
  │
  ├─ raw issue → candidate → canonical issue → progress
  ├─ code-review（必须 ## Implementation Decision Note）
  └─ milestones.md

阶段 4 — 门禁合并
  │
  ├─ 普通: ./bin/merge-guarded test-pre-merge-<name> feature/<name>
  │         → 验证 → ./bin/merge-guarded develop test-pre-merge-<name>
  ├─ 紧急: ./bin/merge-guarded develop hotfix/<name>
  └─ 可选: git checkout main && ./bin/merge-guarded main hotfix/<name>

阶段 5 — 收尾
  │
  ├─ git worktree remove <test-pre-merge-wt>
  └─ git branch -D test-pre-merge-<name>
```

---

## 硬性规则

- **不发明新分支名**。只用 `feature/*`、`feature/premerge-*`、`hotfix/*`、`test-pre-merge-*`。
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
