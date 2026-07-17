---
issue_id: I-20260717T103359Z-A
issue_path: docs/B2-docs/gate/governance/raw-20260717T103359Z/issues/I-20260717T103359Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T103359Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20260717T103359Z/issues/I-20260717T103359Z-A.md

## Implementation Decision Note

- decision: wt-close 未完成/异主双拦截 + fallback FREELY_AGENT_RAW_KEY 导出与 prompt 铁律幂等注入 + supervisor 周期 protected root dirty 检测（指纹去抖）
- why_this: 三事故模式一一对应;复用 --force+reason 既有豁免语义不新增旁路;检测 advisory 化守 watchdog 契约
- alternatives_considered: 仅 prompt 加固（已被击穿,否）;文件系统 ACL（平台耦合,否）;agent_working owner 精确校验（弃单型拦不住,并入异主环境变量方案）
- boundary_non_goals: 不修 ACP init 超时本体;不自动恢复污染;--platform-only 不受影响
- residual_risk: 人类操作员关未完成工位需 --force（摩擦换安全,提示语给足指引）;FREELY_AGENT_RAW_KEY 依赖 launch 路径导出,非 fallback 路径的 worker(bridge session 型)不经 shell 执行 wt-close 时该变量缺失→退化为仅未完成拦截,可接受
