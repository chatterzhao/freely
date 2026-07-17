---
b1_id: B1-20260717T103359Z
phase_state: completed
source_raw: raw-20260717T103359Z
produced_candidate: C-20260717T103359Z-A
created_at: 2026-07-17
---

# B1_IBM: 工位所有权硬防护缺失

## Input
3 次生产实证（2026-07-17）：fallback worker 无产出移除工位（05:11Z 两例=派驻者放弃自删；09:xx 一例=删他人新工位）+ 违规直写 develop（8 个 I-* 直改）。

## Problem
Prompt 层锚约束存在但非硬防护；缺三道硬防线（wt-close 无未完成/异主校验；运行中 protected root 无污染检测；fallback prompt 无边界铁律段）。

## Brainstorm
### 事故模式拆解
- 异主型（09:xx）：worker key≠目标 key → 异主校验可拦
- 弃单型（05:11）：派驻者零交付即删自有工位 → owner 校验无效；「未完成拦截」可拦（无 develop merge 证据的 key 默认禁 close，--force+reason 走既有豁免语义）
- 直写型：无法文件系统级阻止 → 运行中检测+事件升级（advisory,恢复决策归 manager）

### Option A（选定）：三道防线
1. bin/wt-close 前置 guard：(i) 未完成拦截——目标 key 在 develop 无 merge 证据且非 dropped → 需 --force；(ii) 异主拦截——FREELY_AGENT_RAW_KEY 已设且≠目标 key → 需 --force（fallback launch 路径导出该变量）
2. supervisor 主循环轻量检测 protected root dirty → `protected_root_dirty_detected` 事件（指纹去抖）
3. fallback 直启前对 prompt 文件幂等 prepend「工位边界铁律」段
### Option B：只做 prompt 层加固
- 非硬防护,已被实证击穿,否
### Option C：文件系统 ACL
- 平台耦合重,否

## Decision: Option A

## 边界
- wt-close 的 --platform-only 不受影响（不动工位）；人类直接操作（无 FREELY_AGENT_RAW_KEY）只受未完成拦截约束（--force 可走）
- 不修 ACP init 超时本体（fallback 触发源,新代码未复现,revisit_trigger 记录）
- 不做自动恢复 develop 污染（advisory 事件,决策归 manager）

## Candidate
- candidate_id: C-20260717T103359Z-A
- status: promoted
- milestone: M-20260717T103359Z-A
