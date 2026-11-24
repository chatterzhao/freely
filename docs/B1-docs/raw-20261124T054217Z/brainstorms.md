---
b1_id: B1-20261124T054217Z
phase_state: completed
source_raw: raw-20261124T054217Z
produced_candidate: C-20261124T054217Z-A
created_at: 2026-11-24
---

# B1_IBM: issue-sync update 失败传播

## 0. 设计意图审计
- 外部锚点:
  - `bin/issue-sync.d/cmd-update.sh:32`「_gitee_update ... || echo "[issue-sync] Gitee: update FAILED" >&2」+ 第 35 行 `echo update complete` 使函数返回 0。
  - 宪法 `CONSTITUTION.md` / 项目长期记忆：平台写只能走 adapter；禁止部分成功伪装整体成功；fail-closed。
  - 实测：`cmd-update` 的 `_gh_update` 同样未检查返回值（第 26 行）。
- 判定: **实现缺陷**。设计（双平台一致 + fail-closed）正确，实现吞掉写失败。
- 与既有断言冲突: 无；不改变成功路径。
- 影响面: cmd-update.sh；上层 Runtime 依赖平台状态一致性；F2 其它平台写命令（create/close/comment）不在本 raw scope。

## 0.1 全局适配反思
- Q1 类别: 流程能力（平台写结果可信）。
- Q2 职责边界: issue-sync 拥有平台写结果判定；Runtime 消费结果，不应自己猜测。
- Q3 结构性冲突: 若要求「任何平台失败都整体重试」会引入重复写；正确语义是「失败即非零 + 可重试幂等」。
- Q4 门禁失配: 现有门禁测本地状态不测平台写结果；本轮用 AT 覆盖，不动门禁判据。

## Input / Problem
GitHub 更新成功、Gitee 更新失败时，命令仍打印 `update complete` 并返回 0，上层误以为双平台同步完成。长期无人值守下产生静默漂移。与 #4136（Gitee PR 关闭路径）边界不同：本题是 update 路径。

## Brainstorm
- Option A: 只修 Gitee 分支返回码 — 最小但 GitHub 失败仍吞，否决。
- Option B: 汇总两平台结果，任一失败非零退出 + 打印 per-platform 摘要 — 采用。
- Option C: 引入自动重试 — 超出 scope，幂等/去重复杂，否决。

## Decision: Option B
双平台写均检查返回值；汇总 `github: success/failure` / `gitee: success/failure` / `overall`；任一 failure 非零退出。

## Candidate
- candidate_id: C-20261124T054217Z-A
- status: promoted
- milestone: M-20261124T054217Z-A
