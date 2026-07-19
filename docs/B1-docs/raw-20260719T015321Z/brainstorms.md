---
b1_id: B1-20260719T015321Z
phase_state: completed
source_raw: raw-20260719T015321Z
source_url: https://github.com/chatterzhao/freely/issues/3994
produced_candidate: C-20260719T015321Z-A
created_at: '2026-07-19'
---

# B1_IBM: 清理 lead-agent.md 悬空引用 + 修复 governance-check 落后 skill 路径

## Input

- raw issue: raw-20260719T015321Z
- 症状: `freely governance-check` 因 `lead-agent.md` 缺失而 FAIL，阻塞所有 raw issue 推进
- 根因: 2026-05-15 commit `1c505bf63` 删除了 `lead-agent.md`，声明后续清理 scope，但后续从未发生

## Problem

两层问题叠加导致 governance-check 无法通过：

### 问题 A: lead-agent.md 悬空引用

`lead-agent.md` 已于 2026-05-15 删除（commit `1c505bf63`），但 5 处仍有引用：

1. `governance-check` — `three_loop_reference_targets` 检查 lead-agent.md 存在性
2. `start-lead-agent.sh` — `initial_read_targets` 包含 lead-agent.md
3. `auto-loop-orchestrator/SKILL.md` — 主链描述含 lead-agent 层
4. `context-source-skill/SKILL.md` — "为 lead-agent 产出"
5. `project-agents-contract.md` — "Runtime and lead-agent flows"

### 问题 B（dev 阶段发现）: governance-check skill 路径指向不存在的目录

develop HEAD（465d793b3）的 governance-check 将 skill 路径从 `freely-doc-B1_IBM-execution`、`freely-doc-B2_IBM-execution` 改为了 `doc-ibm-execution`、`doc-pre-brainstorm-execution`，但对应目录从未创建，旧 skill 目录仍然存在。门禁引用了不存在的路径→ FAIL。

同样是 commit `1c505bf63` 不完整 rename 的后遗症。

## Brainstorm

### Option A: 恢复 lead-agent.md（回退）

重新创建 lead-agent.md 文件，恢复旧引用。

→ **否决**：lead-agent.md 的角色职责已被 manager-agent.md 吸收，不应恢复。

### Option B: 清理所有悬空引用 + 修复 skill 路径（前进）

1. governance-check：删除 lead-agent.md 引用，将 skill 路径修复回实际存在的目录
2. start-lead-agent.sh：删除 lead-agent.md 引用，更新 lead-agent→manager
3. auto-loop-orchestrator/SKILL.md：主链和角色引用更新
4. context-source-skill/SKILL.md：描述更新
5. project-agents-contract.md：术语更新
6. 配套：4 个测试文件中删除 fake lead-agent.md 创建
7. 配套：scripts/README.md、tools.md、freely runtime 中 lead-agent 引用更新

→ **采纳**：完成 2026-05-15 未完成的 cleanup，解除所有 raw issue 阻塞
