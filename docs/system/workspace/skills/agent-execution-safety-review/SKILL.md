---
name: agent-execution-safety-review
description: 在 Freely workspace 中执行 execution-boundary review，并在高风险或高不确定时输出 reviewer-backed security decision support。用于 security review capability 需要给 runtime / issue / verification 提供 advisory evidence 时。
---

# skill:agent-execution-safety-review

## 职责

- 对齐 project-local config、launch-time injection、tool flags 和 observed posture。
- 在不把用户拉回逐步审批的前提下，组织 reviewer-backed security guidance。
- 输出可写回 issue / progress / verification 的 advisory evidence。

## 不负责

- 不直接改写 launch blockers、approval posture 或 fallback policy。
- 不把 safeguard recommendation 自动升级成 runtime stop。
- 不替代 product-facing activation consent owner。

## 最短步骤

1. 读取当前 project config truth：
   - `FREELY_SECURITY_REVIEW_POLICY`
   - `FREELY_SECURITY_REVIEW_SCOPE`
   - `AI_TOOL` / `AI_MODE` / `AI_TOOL_ADAPTER`
2. 比对 execution boundary：
   - tool flags
   - project-local config
   - launch-time injected posture
   - observed runtime posture
3. 当风险高或不确定性高时，形成 reviewer-backed summary：
   - risk summary
   - disagreement or uncertainty
   - suggested next-safe continuation
4. 写回 evidence 时明确：
   - advisory-only
   - does_not_replace_user_consent
   - does_not_block_runtime_by_default

## Evidence Outputs

- execution-boundary summary
- reviewer-backed decision support summary
- recommended policy or routing adjustments
- follow-on owner recommendation when the issue exceeds advisory scope
