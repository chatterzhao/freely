# Implementation Decision Note
- issue_id: I-20261104T082549Z-A
- decision: pull_raw_issue 按平台可读性选源（可显式指定），未读平台复用既有 sync-debt 记账，部分成功退出码 3 且 wt-create 继续
- why_this: 「任一平台抖动即全停」让双平台备份形同虚设；而 platform_ids / assignee / title 三个循环假定所有副本有 issue_id，降级时会 KeyError 或写入伪造身份。用户要求「优秀的 freely」，网络不确定性必须是债务而不是阻断。
- alternatives_considered: 新建独立 sync-debt 账本（双真源漂移）；把 allow_degraded 事实判定搬进 pull（与前置 gate 职责重叠）；部分成功仍返回 1（调用方无法区分硬失败与降级）；把平台写通道一起改（越界到 #4149、改动面扩散到 close/update 多调用点）；在 stdout 打印警告（破坏 wt-create 的单 JSON 解析契约）。
- boundary_non_goals: 不改 sync-debt 账本格式 / raw_reconciliation 决策 / _fill_platform_ids；不改 R2 H1 与 Q2 created_at 兼容分支 / 标题契约 / identity 校验；不夹带 R7/#4195、R11/#4149、#4194、#4201；平台写（close/update）按可用平台执行不在本 PR（issue 修复方案第 4 条的写通道部分，验收标准未覆盖，留给 R11）。
- residual_risk: ①平台写通道仍可能在部分平台不可读时静默失败（#4149 / R11 待修）。②`--platform` 目前只接受 github|gitee，新增平台时需同步扩展校验（configured_platforms 不限制，但 CLI 校验限制）。③sync-debt 的 reason 为通用文案，未携带 adapter 的具体 error；后续 reconcile 可按需补充。④顶层 `return 1` 仍待 #4201（R6.5）。
- verification: AT-001 基线 RED 9 失败 / 3 既有能力 PASS → GREEN 12 项全通过；端到端隔离 git 项目验证 CLI 退出码 3、stdout 单一 JSON、sync-debt 落账、wt-create 继续；12 个回归全 PASS；11 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；相邻现象已被 R7/#4195、R11/#4149、#4201、#4151 覆盖，未重复立项。
