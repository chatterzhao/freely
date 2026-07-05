# Candidates

## C-20260521T032154Z-A: legacy issue

- candidate_format_version: v2
- title: 修复 _on_supervisor_err 递归 ERR trap 导致的假阳性 crash 报告
- status: promoted
- decision_reason: raw-20260521T032154Z (GitHub #1523) 在 ERR trap handler 内部，`[[ "$_err_rc" -eq 0 ]]` 触发递归 ERR trap，递归展开后 `_err_cmd` 从 `BASH_COMMAND` 捕获的值不等 `[[`，导致 benign check 失败，生成假阳性 crash 报告。根因已定位，修复方案明确（提前捕获 BASH_COMMAND）。
- next_action: B2_IBM materialize（实现方案 A：提前捕获 BASH_COMMAND）
- revisit_trigger: B2_IBM 完成后进入 dev-loop
- acceptance_criteria:
  - brainstorms.md 根因分析完整（已有）
  - 修复方案已验证为最小改动（方案 A 或 B）
  - 与 C-20260517T083030Z-A (bash rc=0) 的边界清晰区分
  - 已确认修复不会影响其他 ERR trap 行为
- promotion_gate: acceptance review pass + 方案 A/B 选择决策 + 模拟测试计划
- open_questions:
  - 是否有更多 `_on_supervisor_err` 执行路径会在递归 trap 后损坏状态？
  - 方案 B（禁用 ERR trap）是否比方案 A 更安全？
  - 此前 batch1/batch2 中是否有本模式但被误归入 bash rc=0 的报告？
- acceptance_reviews:
  - reviewer: subagent
    mode: acceptance-review
    summary: |
      **a. brainstorms.md 根因分析完整** — PASS。根因定位到 `_on_supervisor_err` 函数内 `[[ "$_err_rc" -eq 0 ]]` 触发递归 ERR trap 导致 BASH_COMMAND 错位，benign check (`[[ "$_err_cmd" == "[[" ]]`) 失败。包含完整调用栈分析、变量值追踪、代码路径定位（freely:~18951）。

      **b. 修复方案已验证为最小改动** — PASS。方案 A（提前捕获 BASH_COMMAND，2 行重排）和方案 B（handler 内禁用 ERR trap）均已给出代码级验证。方案 A 改动最小、不影响已有逻辑。

      **c. 与 C-20260517T083030Z-A (bash rc=0) 边界清晰区分** — PASS。brainstorms.md 包含完整对比表：触发命令（bash vs [[）、退出码（0 vs 1）、根因（成功退出误判 vs ERR trap 递归）、代码位置（crash 检测逻辑 vs handler 内部）、修复范围（检测阈值 vs 执行顺序）。两问题独立，应各自独立 candidate。

      **d. 已确认修复不影响其他 ERR trap 行为** — PASS（minor note）。方案 A 仅将 `_err_cmd` 赋值提前，`_err_cmd` 仅用于 line 18960 的 benign check。非递归场景下 BASH_COMMAND 稳定，赋值提前不改变语义。brainstorms.md 未显式逐行验证非递归场景的零影响，但隐式涵盖。

      **Open questions** — Q1（递归 trap 后其他状态损坏）：方案 A 修复 `_err_cmd` 即足够阻断假阳性；`_err_rc` 在函数入口已缓存不受影响；其他变量在 crash report 生成路径之外。Q2（方案 B vs 方案 A）：方案 B 更稳健但需要 trap save/restore，方案 A 足够解决本 bug，推荐方案 A 进 B2_IBM。Q3（batch1/batch2 误归入 bash rc=0）：需审计历史 crash 报告，不影响当前修复。

      **Verdict**: pass — 全部 4 项 acceptance_criteria 满足，open_questions 不阻塞 promotion。推荐方案 A 进入 B2_IBM materialize。
    verdict: pass
- promoted_issue_path: "docs/issues/I-20260521T032154Z-A/issue.md"
- milestone: M-20260521T032154Z-A
- session_refs: []
