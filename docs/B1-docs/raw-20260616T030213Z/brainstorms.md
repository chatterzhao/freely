---
b1_id: B1-20260616T030213Z
phase_state: completed
source_raw: raw-20260616T030213Z13Z
source_url: https://github.com/chatterzhao/freely/issues/2795
produced_candidate: C-20260616T030213Z-A
created_at: 2026-06-16
---

# B1_IBM: Gate Scope Alignment — FREELY_SKIP_IBM_GATE 边界不一致

## Input Source

- GitHub issue #2795: https://github.com/chatterzhao/freely/issues/2795
- Raw issue: `docs/B1-docs/raw-20260616T030213Z13Z/issue.md`
- Filed by: platform (AI agent), 2026-06-16

## Problem

`LAWS.md` 规定 `FREELY_SKIP_IBM_GATE=1` 仅用于 `docs/cleanup/format`，但 `governance-merge-gate --skip-ibm-gate` 的实现将 **所有** workspace 脚本（`docs/system/workspace/scripts/runtime/`, `worktree/`, `hooks/`）都归类为 governance-only，导致运行时代码变更可以绕过 IBM 生命周期。

这意味着三条实际风险：

1. Runtime fixes 可合并而无需 B1_IBM → candidate → B2_IBM → I-* 链
2. 开发者/AI agent 可利用 `FREELY_SKIP_IBM_GATE=1` 将代码变更伪装成"治理基础设施"
3. fix-execution 的 "Fix first, govern later" 无强制约束——修复合并后治理从不补做

## Brainstorming

### Option A: 对齐 gate 到 LAWS.md（推荐，严格模式）

限制 governance-only 路径为：
- `AGENTS.md`, `CONSTITUTION.md`, `LAWS.md`, `PROJECT_INTENT.md`
- `docs/milestones.md`, `docs/B1-docs/raw-`, `docs/B2-docs/`, `docs/progress/`, `docs/B1-docs/raw-`

所有 workspace 脚本（`docs/system/workspace/scripts/runtime/`, `worktree/`, `hooks/`）**必须走 IBM 生命周期**。

优势：与现有书面规则一致；无歧义；fix-execution 的 "govern later" 成为硬性要求而非建议。

### Option B: 对齐 LAWS.md 到 gate（宽松模式）

将 `docs/cleanup/format` 扩展为包含 workspace 基础设施脚本。`FREELY_SKIP_IBM_GATE=1` 对 `docs/system/workspace/scripts/*` 生效。

风险：文字上允许更大的 bypass 面，与 Project Intent 的治理优先方向矛盾。

### Option C: 按"基础设施" vs "运行时"拆分

- RUNTIME（需 IBM）：`scripts/runtime/freely`, `scripts/worktree/wt-close`, `hooks/pre-commit.sh`
- INFRA（可跳过）：`scripts/quality/governance-merge-gate`, `scripts/runtime/acp-bridge.py`

问题：边界模糊；维护成本高；最终效果接近 Option A 但增加了分类复杂度。

## 分析与权衡

- LAWS.md 是比 gate 实现更高优先级的权威来源（CONSTITUTION 优先层级）
- 现有实现允许 runtime 代码绕过 IBM 是 bug，不是意图
- Option A 的零豁免策略最小化未来 bypass 风险
- B2_IBM 已产出 review note，确认修改范围是 `governance-merge-gate` 中的 `is_governance_only_path()`

## 结论

选定 **Option A**（Align gate to LAWS.md）。具体变更：
- 从 `is_governance_only_path()` 中移除 `hooks/`, `scripts/runtime/`, `scripts/worktree/`, `scripts/tests/`
- 修改范围仅限 `docs/system/workspace/scripts/quality/governance-merge-gate`
- meta-governance（gate 自身的 bug fix）仍保持 governance-only 豁免

对应 candidate: `C-20260616T030213Z-A`
