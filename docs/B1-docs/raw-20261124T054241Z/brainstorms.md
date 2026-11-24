---
b1_id: B1-20261124T054241Z
phase_state: completed
source_raw: raw-20261124T054241Z
produced_candidate: C-20261124T054241Z-A
created_at: 2026-11-24
---

# B1_IBM: session restore 退出码

## 0. 设计意图审计
- 外部锚点:
  - `agent_session_restore.py:73-80`「main() 逐条 print outcome ... return 0」——无论 resumed/failed/slot_unavailable 恒 0。
  - 项目 fail-closed 原则（长期记忆）；Runtime 重启后应暴露真实恢复状态。
  - 全仓搜索无内部调用者——该 CLI 退出码是给外部消费的契约。
- 判定: **实现缺陷**。设计（持久化恢复 + 状态分类）正确，退出码未反映失败。
- 与既有断言冲突: 无；成功路径仍返回 0。
- 影响面: agent_session_restore.main()；外部调用者依据退出码判断健康；不改 resume_persisted_sessions 返回结构。

## 0.1 全局适配反思
- Q1 类别: 流程能力（恢复结果可信）。
- Q2 职责边界: CLI 负责如实报告结果；Runtime 消费退出码。
- Q3 结构性冲突: 若失败就异常退出会丢已恢复的 session 信息；正确做法是打印全部结果 + 汇总 + 非零码。
- Q4 门禁失配: 无门禁测退出码；本轮用 AT 覆盖，不动门禁判据。

## Input / Problem
Runtime 重启后部分 Worker/Reviewer 的 `session/resume` 失败时，进程退出码仍是 0，外部只看退出码会把部分恢复失败误判整体成功。

## Brainstorm
- Option A: 任一失败 raise — 丢汇总信息，否决。
- Option B: 打印结构化汇总（resumed/failed/slot_unavailable 计数 + health），有 failed 即非零退出 — 采用。
- Option C: 只打印不改码 — 外部仍误判，否决。

## Decision: Option B
main() 汇总三类 outcome 计数并打印；failed>0 或关键 Agent 未恢复 → 非零退出；resume_persisted_sessions 返回结构不变。

## Candidate
- candidate_id: C-20261124T054241Z-A
- status: promoted
- milestone: M-20261124T054241Z-A
