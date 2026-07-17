---
local_id: raw-20260617T035314Z14Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T121608Z-A
platform_ids:
  github:
    issue_id: '2883'
    url: https://github.com/chatterzhao/freely/issues/2883
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T03:53:32Z'
updated_at: '2026-06-29T13:43:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 审计结论

全文有两类表述问题：结构缺失（阶段流程）和用语不标准（未标明"命令"）。

---

## 一、结构缺失

### 1. fix skill 阶段 4 缺少 pr-create-guarded 步骤
L158-164 从 governance-gate 直接跳到 pr-merge-guarded，对比 feat skill L84-98 正确拆分为两步。

### 2. fix skill + feat skill 未标注 pr-merge-guarded 需在 develop 执行
pr-merge-guarded L393 `check_branch_context "$target"` 强制要求当前在 develop。

### 3. 三个 skill 硬性规则无"禁止原子命令绕过"
当前只写"用 pr-create-guarded / pr-merge-guarded"，没有"禁止 gh pr create / gh pr merge --admin / git push --force 替代"。

参考 LAWS.md L304-306 已有的禁令表述：
> `--no-verify`、`git commit --no-verify`、`git merge --no-verify` 或任何等价手动绕过手段永久禁止。

---

## 二、用语不标准 — 命令名未标注"命令"

全文大量使用封装命令名称作为流程步骤，但未标明它们是**可执行命令**。AI 可能把它们理解为抽象概念而非必须执行的 CLI 命令。

### AGENTS.md

| 行 | 当前表述 | 应改为 |
|----|---------|--------|
| L22 | `wt-create → worktree → commit → pr-create-guarded → pr-merge-guarded` 流程 | `freely wt-create` 命令 → `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L90 | pr-merge-guarded develop <feature-branch> 合并 | `freely pr-merge-guarded` 命令 |
| L131 | 创建 raw issue（freely feedback / chat --new-issue） | `freely feedback` 命令 |
| L132 | 创建工位（wt-create --raw-key） | `freely wt-create` 命令 |
| L137 | 提 PR（pr-create-guarded → pull develop → ...） | `freely pr-create-guarded` 命令 |
| L139 | 门禁合并（pr-merge-guarded → PR gate → ...） | `freely pr-merge-guarded` 命令 |
| L140 | 收口（wt-close） | `freely wt-close` 命令 |
| L166 | pr-create-guarded → pr-merge-guarded → develop | `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L168 | test-pre-merge-* → pr-create-guarded → pr-merge-guarded → develop | 同上 |

### fix-execution SKILL.md

| 行 | 当前表述 | 应改为 |
|----|---------|--------|
| L12 | `pr-create-guarded → pr-merge-guarded develop` 完整链路 | `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L14 | 正式提交和门禁合并仍在合规分支上完成 | 正式提交后通过 `freely pr-create-guarded` 命令提 PR，再通过 `freely pr-merge-guarded` 命令合并 |
| L18 | 合并走 pr-merge-guarded 合规路径 | 合并走 `freely pr-merge-guarded` 命令 |
| L45 | 合并也走可写工位 → develop 的合规路径 | 通过 `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L93 | 建 test-pre-merge-* 私有工位快测 → cp 到 fix/* | 建 test-pre-merge-* 私有工位快测 → cp 到 fix/* → `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 → `freely wt-close` 命令 |
| L99 | pr-create-guarded → pr-merge-guarded develop | `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L120 | pr-create-guarded → pr-merge-guarded develop 完整路径 | 同上 |
| L158 | 阶段 4 — 门禁合并 | 阶段 4a — `freely pr-create-guarded` 命令提 PR / 阶段 4b — `freely pr-merge-guarded` 命令合并 |
| L162 | freely pr-merge-guarded develop fix/<name> | `freely pr-merge-guarded` 命令 |
| L170-172 | 关闭 test-pre-merge-* 工位 | `freely wt-close` 命令 |
| L183 | 原 feature 还在就直接在上面修 | 原 feature 还在就直接在上面修，修完走 `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L186 | 用 pr-create-guarded / pr-merge-guarded | 用 `freely pr-create-guarded` 命令 / `freely pr-merge-guarded` 命令 |

### feat-execution SKILL.md

| 行 | 当前表述 | 应改为 |
|----|---------|--------|
| L17 | wt-create→B1_IBM→B2_IBM→dev→test-pre-merge→pr-create-guarded→pr-merge-guarded→wt-close | 每步加上 `./bin/` 前缀和"命令" |
| L33 | pr-create-guarded → pr-merge-guarded develop 完整链路 | `freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 |
| L41 | freely wt-create --raw-key <key> —source ... | 已有 `./bin/`，追加 "命令" |
| L84 | 阶段 5：提 PR | 阶段 5：`freely pr-create-guarded` 命令提 PR |
| L87 | 运行 `freely pr-create-guarded` | 运行 `freely pr-create-guarded` 命令 |
| L91 | 阶段 6：门禁合并 | 阶段 6：`freely pr-merge-guarded` 命令门禁合并 |
| L93 | 运行 `freely pr-merge-guarded develop <pr-branch>` | 运行 `freely pr-merge-guarded` 命令（在 develop 分支执行） |
| L100 | 阶段 7：收口 | 阶段 7：`freely wt-close` 命令收口 |
| L110 | 运行 `./bin/governance-merge-gate` | 已有 `./bin/`，追加 "命令" |
| L118 | 不要跳过...pr-create-guarded→pr-merge-guarded→wt-close 任一阶段 | 不要跳过...`freely pr-create-guarded` 命令 → `freely pr-merge-guarded` 命令 → `freely wt-close` 命令任一阶段 |

### dev-loop SKILL.md

| 行 | 当前表述 | 应改为 |
|----|---------|--------|
| L154 | 通过 pr-create-guarded 提 PR | 通过 `freely pr-create-guarded` 命令提 PR |

---

## 三、硬性规则增加"禁止原子命令绕过"

三个 skill 的硬性规则统一增加：
```
- `freely pr-create-guarded` 命令和 `freely pr-merge-guarded` 命令是提 PR 和合并的唯一合法入口。
  禁止用 gh pr create、gh pr merge --admin、git push --force、git merge 等原子命令替代。
- `freely pr-merge-guarded` 命令必须在 develop 分支执行。
```

---

## Acceptance Criteria
- [ ] 所有命令名统一加 `./bin/` 前缀 + "命令"后缀（约 35 处）
- [ ] fix skill L158-164 拆分为 4a (pr-create-guarded) + 4b (pr-merge-guarded)
- [ ] pr-merge-guarded 标注"在 develop 分支执行"
- [ ] 三个 skill 硬性规则增加"禁止原子命令绕过"
- [ ] deploy-skills 执行


## State Reconcile Note (2026-07-17, raw-20260715T122119Z batch)

- 平台 issue 已 CLOSED、实现已进 develop（前 I-* 物化时代 lane，无 canonical I-* 锚，跟随 raw-20260501 absorbed 惯例收敛）
