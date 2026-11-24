# PRD: session restore 退出码
- issue_id: I-20261124T054241Z-A

## Goal
Runtime 重启恢复 ACP session 时，让外部调用者能依据退出码与结构化汇总准确判断恢复健康，不再把部分失败误判整体成功。

## 实现方案
1. `agent_session_restore.main()`：统计 outcomes 中 resumed / failed / slot_unavailable 三类计数并打印结构化 summary（JSON line）。
2. 有 `failed` outcome → 非零退出（如 1）；全部 resumed/slot_unavailable → 0（slot_unavailable 属可恢复的待重试态，不当场失败）。
3. 保留逐条 outcome 打印（顺序不变）与 usage 退出码 2。
4. 不改 `resume_persisted_sessions()` 返回结构。

## 不退化边界
- 全 resumed 时输出与退出码（0）不变；逐条 outcome JSON 行格式不变。
- 不改 session/resume 调用本身、不改 DB/A2A 交互。

## Dev-Loop Handoff
见 pre-tests.md。RED：基线 mock failed outcome 仍退出 0；GREEN：非零 + 汇总。
