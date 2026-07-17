---
issue_id: I-20260717T004620Z-A
issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/issues/I-20260717T004620Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T004620Z-A
- issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/issues/I-20260717T004620Z-A.md

## Implementation Decision Note

- decision: 在 runtime/freely 内一体修复 supervisor 生死判定四面：heartbeat stale 分支加新生宽限（可配 SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS=15）+ heartbeat 子进程上移并合并 EXIT trap + watchdog 判死改走 restart_manager_supervisor_preserving_handoff 且 kill -0 验证消亡 + ensure-manager 侧记录 supervisor 死亡进 storm window 并修正阈值口径（PEAK 10→3，COUNT 后备 4→10）
- why_this: 四缺陷同属生死判定域的输入（heartbeat 失真）/动作（kill 语义矛盾）/观测（storm 零检出）/清理（EXIT trap 覆盖），拆开修留下病理闭环；改动收敛在既有函数内，无接口变更；storm 记录放 ensure-manager 侧规避 dying process EXIT trap 内文件 I/O 的可靠性风险（acceptance review non-blocking #2）
- alternatives_considered: 只修 C1（留双 daemon 与观测盲区，否）；让 supervisor 响应裸 TERM（违反 raw-20260711T100936Z 的 operator-stop 区分设计，否）；扩大 churn 进程计数口径（与 bridge 泄漏 lane 耦合，否，取降默认值）；重构 watchdog 独立模块（Option C，改动面大，留给 watchdog-control-plane 治理线）
- boundary_non_goals: 不改 supervisor TERM 忽略语义；不改 bridge 生命周期（raw-20260717T004654Z）；不改 sse pid 校验（raw-20260717T004721Z）；不改 stall 判定（raw-20260716T114802Z）；不拆 runtime/freely 大文件
- residual_risk: teardown 失败(不可杀进程)时死亡已预记入 storm window,可能轻微高估——advisory 信号可接受,不可杀本身即值得检出的病态; cleanup_supervisor 合并进 EXIT handler 后在异常路径可能重复执行——其内部已有 supersede 检查与 rm -f 幂等操作，风险低；heartbeat 子进程上移后若 supervisor 在 doc-gate 阶段退出，子进程靠 kill -0 父进程检测自杀，无孤儿风险；PEAK 阈值降为 3 可能在极端正常重启密集期误报——signal 只升级给 manager 判断（advisory），不自动动作
