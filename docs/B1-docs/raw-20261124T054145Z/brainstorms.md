---
b1_id: B1-20261124T054145Z
phase_state: completed
source_raw: raw-20261124T054145Z
source_url: https://github.com/chatterzhao/freely/issues/4669
produced_candidate: C-20261124T054145Z-A
created_at: 2026-11-24
---

# B1_IBM: CI 合并保护链三处失效

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文，至少两类）:
  - 门禁源码注释: `.github/workflows/pr-merge-guard.yml:1-7`「CI guard: block GitHub Merge button and enforce the correct merge workflow. 1. This workflow creates a check "governance/pr-merge-guard" (in_progress). 2. Branch protection on develop REQUIRES this check to pass. 3. Only pr-merge-guarded sets it to "success" via GitHub API. 4. Result: GitHub UI merge button is greyed out.」
  - 工作流一次性设置说明: 同文件 `:9-31`「Run this ONCE to enable branch protection on develop ... "contexts": ["governance/pr-merge-guard"] ... "enforce_admins": true ↑ THIS IS CRITICAL — prevents gh pr merge --admin bypass」
  - 既有验收测试: `docs/system/workspace/scripts/tests/test-postmerge-commit-guard.py` 一类「must reject / must block」断言，以及 `LAWS.md:52`「`main/develop` 保持 add/commit 禁止（仅接受 merge）」
  - 宪法: `CONSTITUTION.md:49`「`main` / `develop` / `test-pre-merge-*` 上，hook/gate bypass 永久禁止」
  - 实测事实（2026-11-23，已认证 gh 通道）: CI run 43827151395 guard job `POST /check-runs` → 403 `x-accepted-github-permissions: checks=write`；`gh api branches/develop/protection` → 404 `Branch not protected`；`pr-merge-guarded:296-329` 自签 success check 且 `|| true` 吞错。
- 判定（五选一，必须给证据）: **实现未完成 + 实现偏差（复合）**。设计与契约本身正确（上述 workflow 注释 + 一次性设置说明明确要求分支保护与唯一置 success 入口），但三处实现/配置未落地：① workflow 缺 `permissions` 导致第一步建 check 失败（实现未完成）；② develop 分支保护从未按注释执行一次性设置（配置未完成）；③ `pr-merge-guarded` 在 check 缺失时自行创建 success check 并吞掉 API 失败，与「Only pr-merge-guarded sets it to success」的语义表面一致、实则把「门禁通过」降级为「调用过脚本」，属于实现偏差（自签绕过）。
- 与既有断言的冲突: **有**。workflow 注释声明「Branch protection on develop REQUIRES this check」与 API 实测 404「Branch not protected」直接冲突；注释声明「Only pr-merge-guarded sets it to success」与 fallback 自行创建 success check 在语义上冲突（后者没有经过任何门禁）。谁该改：改实现/配置以符合注释契约，不改注释。
- 影响面: `.github/workflows/pr-merge-guard.yml`（权限声明）；`docs/system/workspace/scripts/worktree/pr-merge-guarded`（自签 fallback）；develop 分支保护配置（平台侧一次性设置）；相关回归测试（`tests/` 下 merge guard 族）；`docs/LAWS.md` / `CONSTITUTION.md` 的「bypass 永久禁止」条款需要可验证的执行证据支撑。

## 0.1 全局适配反思（四问）

- Q1 类别: 流程能力（合并门禁的可信度），兼治理元数据修复（分支保护配置）。
- Q2 职责边界: CI workflow 负责「建阻塞 check + 跑验证子集」，GitHub 分支保护负责「强制 check 通过才允许合并」，`pr-merge-guarded` 负责「跑完本地治理门禁后置 check 为 success」。最终判定属于 GitHub 分支保护 + check run 状态，不属于任一脚本的自我声明。三者共享「governance/pr-merge-guard」这一 check 名，必须单一语义。
- Q3 结构性冲突: 按字面「每个仓库都要手工配分支保护」会形成平台配置漂移；但本项目是单仓自举，一次性设置由 workflow 注释明确给出，属于可接受的配置前置，不是反设计。真正的反设计是自签 fallback——它让「执行者」同时成为「check 存在性的提供者」，违反「执行者不能自签验收」。
- Q4 门禁失配: 现有门禁测的是本地 governance gate（路径/身份/存在性/一致性），没有测「CI check 是否真实存在且未被自签」。本轮必须新增机器可验证的判据：check 缺失/API 失败时 `pr-merge-guarded` 非零退出，且 CI 能成功创建 check。先补判据模型，不用 `--force` 绕过任何既有门禁。

## Input
- raw key: 20261124T054145Z，GitHub #4669 / Gitee IKXKY8，severity P0。
- 来源：外部评审 + 已认证 gh 通道复核。评审指出缺 `checks: write`；复核追加发现 develop 分支未保护、pr-merge-guarded 自签 check。
- 三处现象与证据见 raw issue body 与本文件 §0。

## Problem
合并保护链有三处断点，互相掩盖：
1. CI guard job 无 `checks: write` 权限，建 check 第一步即失败 → check 从未存在。
2. develop 分支保护未配置 → 即使 check 存在，网页 Merge 也不受约束。
3. `pr-merge-guarded` 在 check 缺失时自行创建 `conclusion=success` 的同名 check，且 API 失败 `|| true` 吞掉 → 执行者可自签验收章。

净效果：项目的「禁止绕过门禁」条款在平台层面没有任何可验证的强制点。

## Brainstorm

### Option A: 只补 `permissions: checks: write`
- 优点：改动最小，修复 guard job 403。
- 缺点：develop 仍无分支保护，网页 Merge 仍可绕过；自签 fallback 仍在。修复后 CI check 存在，但没人强制它。单独做等于修了一个看不到效果的开关。否决。

### Option B: 补权限 + 配分支保护，保留自签 fallback
- 优点：覆盖前两处，网页 Merge 被拦。
- 缺点：自签 fallback 使 `pr-merge-guarded` 可在 check 缺失时自造 success check，仍是绕过通道。且 fallback 会掩盖 CI 未运行或失败的事实。否决。

### Option C: 三处一起修——补权限 + 配分支保护 + 移除自签 fallback 改为 fail-closed
- 优点：闭合整条链。CI 建 check → 分支保护强制 → 门禁通过才置 success；check 缺失/API 失败即时暴露而非被吞。
- 缺点：改动面跨 workflow / 脚本 / 平台配置三类；分支保护需要一次性平台设置（workflow 注释已给出命令，但注释本身不是执行）；移除 fallback 后若 CI 未跑，`pr-merge-guarded` 会失败，需确保 CI 在 PR 事件上先运行。
- 评审：这是唯一使「禁止绕过门禁」成为可验证事实的方案。采用。

### Option D: 换用 GitHub Ruleset / 第三方 CI
- 优点：更强保护能力。
- 缺点：引入新平台机制，超出本 raw 边界，与现有 workflow 注释契约冲突。本轮不做，写入 open_questions 供后续评估。

## Decision: Option C

三处一起修，且以「fail-closed」为统一原则：check 不存在或 API 失败必须显式报错，不允许自行创建 success check。分支保护按 workflow 注释给出的一次性设置执行，并在证据中留下 API 读取结果。

## Candidate
- candidate_id: C-20261124T054145Z-A
- status: promoted
- milestone: M-20261124T054145Z-A
