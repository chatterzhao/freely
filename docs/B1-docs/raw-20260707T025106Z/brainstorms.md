---
b1_id: B1-20260707T025106Z
phase_state: completed
source_raw: raw-20260707T025106Z
source_url: https://github.com/chatterzhao/freely/issues/3790
produced_candidate: C-20260707T025106Z-A
created_at: 2026-07-07
---

# B1: pr-review-guarded 增加工位清洁检查

## Input
- raw-20260707T025106Z: pr-review-guarded 缺少工位清洁检查
- GitHub issue #3790
- Kind: fix

## Discovery

### value_check: 当前状态
1. **pr-create-guarded** 有完整的工位清洁检查（Step 0a），检查 tracked modifications + untracked files，并给出 3 种修复方案（commit/stash/gitignore） ✅
2. **freely-review** 有基本清洁检查（worker caller），但消息太简略只说 "dirty, commit first" ⚠️
3. **pr-review-guarded** 完全缺少工位清洁检查 ❌ — 这是本次修复的核心
4. **pr-merge-guarded** 无独立清洁检查 ❌ — 依赖 pr-review-guarded 的保护失效时出现 gap
5. **wt-close** 有 dev↔test 一致性检查，但只在收口阶段报 ❌ — 太晚了

### scope_check: 改动范围
- `bin/pr-review-guarded`: 增加审查前+审查后工位清洁检查
- `bin/pr-merge-guarded`: 增加合并前兜底清洁检查

全部为单一脚本修改，无运行时架构变更。

## Problem

review 过程中可能产生文件修改（review 文档写回、gate 修复等），如果这些修改未被提交，会直接丢失。pr-create-guarded 有检查但 pr-review-guarded 没有——这中间形成了一个"清洁检查真空区"。

## Brainstorm

### Option A: 只在 pr-review-guarded 审查前加检查
- 优点：改动最小
- 缺点：审查后如果 review 生成了文件（如 review doc），这些修改仍可能遗漏

### Option B: pr-review-guarded 审查前 + 审查后都加检查 ✅
- 审查前检查：拒绝 dirty 工位，要求先提交再审查
- 审查后检查：如果 review 产生了修改，强制 git add + git commit
- pr-merge-guarded 合并前再加一次兜底检查
- 优点：全覆盖，任何阶段的遗漏都能被捕获
- 缺点：改动 2 个文件

### Option C: 只在 pr-merge-guarded 合并前加兜底检查
- 优点：改动最小（一个检查点）
- 缺点：问题发现太晚——merge 阶段才发现 review 遗漏，需要回到 review 重做

## Decision: Option B — pr-review-guarded 审查前+后 + pr-merge-guarded 兜底

理由:
1. 审查前检查是"入口闸门"——不带着脏工位做审查
2. 审查后检查是"出口闸门"——审查产生的所有修改必须提交
3. pr-merge-guarded 兜底是"最后防线"——即使前两道闸门被绕过，合并前也能拦住
4. 错误消息必须参考 pr-create-guarded 的设计：说清问题 + 给出具体修复命令 + 不丢弃数据

错误消息设计原则:
- **说清问题**: 列出具体哪些文件 dirty/untracked
- **正向引导**: 告诉用户应该怎么做（git add + git commit / git stash / .gitignore）
- **关联上下文**: 告诉用户当前在哪个阶段的哪个检查点被拦住了
- **不丢弃数据**: 绝不建议 `git reset --hard` 或 `git clean -f` 等丢弃操作

## Candidate
- candidate_id: C-20260707T025106Z-A
- status: promoted
- milestone: M-20260707T025106Z-A
