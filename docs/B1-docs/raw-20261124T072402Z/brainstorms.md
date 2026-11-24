---
b1_id: B1-20261124T072402Z
phase_state: completed
source_raw: raw-20261124T072402Z
source_url: https://github.com/chatterzhao/freely/issues/4675
produced_candidate: C-20261124T072402Z-A
created_at: 2026-11-24
---

# B1_IBM: governance check 置 success 接线审视

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文，至少两类）:
  - workflow 注释（本轮前已存在）`.github/workflows/pr-merge-guard.yml:1-7`「1. This workflow creates a check "governance/pr-merge-guard" (in_progress). 2. Branch protection on develop REQUIRES this check to pass. 3. Only pr-merge-guarded sets it to "success" via GitHub API. 4. Result: GitHub UI merge button is greyed out.」
  - 同文件 `:33-35`「Correct merge workflow: ./bin/pr-merge-guarded develop <source-branch> (NEVER the GitHub Merge button)」
  - 实现源码 `scripts/worktree/pr-merge-guarded:748-793`「gh pr merge --merge --body does NOT work. Use local merge.」+ `git push "$remote" develop`
  - 实测：CI run 45346477702（新 workflow）guard job=success、check `governance/pr-merge-guard`=in_progress；`gh api branches/develop/protection` 配置后 contexts=[governance/pr-merge-guard], enforce_admins=true, protected=true
  - 宪法 `CONSTITUTION.md:49`「hook/gate bypass 永久禁止」
- 判定（五选一，必须给证据）: **设计正确、实现正确、但文档断言错误**。设计目标「网页 Merge 按钮变灰，合并只能走 pr-merge-guarded」已完全达成：check 保持 in_progress + 分支保护要求该 check → 网页按钮被拦；本地 merge+push 不查 check status → 治理链路照常工作。注释第 3 条「Only pr-merge-guarded sets it to success」从未实现（全仓 grep 无调用点），且**不需要实现**——置 success 反而会让网页按钮可用，违背第 4 条与「NEVER the GitHub Merge button」。
- 与既有断言的冲突: 有。注释第 3 条与第 4 条/「NEVER merge button」自相矛盾：若 check 被置 success，分支保护放行，网页按钮不再灰——正好破坏它自己声明的目标。谁该改：改文档断言（删/更正第 3 条），不改实现。
- 影响面: `.github/workflows/pr-merge-guard.yml` 注释；本 raw 的问题定性（从 P0 功能缺陷降为文档修正）；R60 恢复点里"分支保护陷阱"的记录需更正为"保护本可安全启用，回退是误判"。

## 0.1 全局适配反思（四问）

- Q1 类别: 治理元数据修复（文档断言与实现对齐），非流程能力变更。
- Q2 职责边界: check run 的最终判定属于 GitHub 分支保护 + CI，不属于任何脚本的自我声明；`pr-merge-guarded` 的职责是本地治理门禁 + 本地 merge + push，不需要也不应该去操作 check status。
- Q3 结构性冲突: 若按字面实现「pr-merge-guarded 置 success」，会产生「执行者自签验收」的反设计，且与「NEVER merge button」冲突。因此问题定错在「实现缺失」，正确定义是「文档断言错误」。
- Q4 门禁失配: 现有门禁测的是本地 governance gate 与双平台同步，没有测文档注释与实现一致性——属可接受的文档债，不构成门禁失配；本轮用 AT 静态断言覆盖注释与代码的一致性即可，不动门禁判据。

## Input
- raw key: 20261124T072402Z，GitHub #4675 / Gitee IKXMQR，severity P0（基于误判）。
- 来源：R60 轮中，因误判「配分支保护会卡死所有 PR」而回退保护后立项。

## Problem（原始断言，已被证伪）
- 原断言：`governance/pr-merge-guard` 无人置 success → 分支保护无法安全启用 → 需接线解决时序死锁。
- 证伪：分支保护已于本轮重新启用并 verified（protected=true, contexts 含该 check, enforce_admins=true）；`pr-merge-guarded` 的本地 merge+push 链路不依赖 check status，未被拦截。所谓「时序死锁」不存在——check 保持 in_progress 正是网页按钮该有的拦截态。

## Brainstorm

### Option A: 在 pr-merge-guarded 里接线置 success
- 优点：让注释第 3 条变成事实。
- 缺点：置 success 会让网页按钮可用，直接违背注释第 4 条与「NEVER the GitHub Merge button」；且 merge 前的窗口里执行者自签验收，引入绕过通道。**否决**。

### Option B: 删除/更正注释第 3 条，明确 check 恒 in_progress 是设计态
- 优点：文档与实现一致；保留网页拦截这一真实达成的目标；零运行时风险。
- 缺点：需同步更正 R60 恢复点里的误判记录。
- 评审：最小、正确、无副作用。**采用**。

### Option C: 保持现状，什么都不改
- 优点：零改动。
- 缺点：注释继续误导后来者（包括 AI）再去「修」这个不存在的缺陷，R60.4 这类误判会重复。**否决**。

## Decision: Option B

将 raw 从「P0 功能缺陷」降为「文档断言修正」：更正 workflow 注释中错误的第 3 条，写明 check 恒 in_progress 是拦截网页合并的设计态，success 无需也不应设置。用静态 AT 锁定「注释不再声称会置 success」与「无自签调用」两条契约。

## Candidate
- candidate_id: C-20261124T072402Z-A
- status: promoted
- milestone: M-20261124T072402Z-A
