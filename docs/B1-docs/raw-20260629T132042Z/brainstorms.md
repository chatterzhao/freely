---
b1_id: B1-20260629T132042Z
phase_state: completed
source_raw: raw-20260629T132042Z42Z
source_url: https://github.com/chatterzhao/freely/issues/3624
produced_candidate: C-20260629T132042Z-A
created_at: 2026-06-29
---

# B1_IBM: replace ./bin/ with freely in hook scripts and start-lead-agent

## Input
- 来源：GitHub issue #3624 ([RAW-20260629T132042Z])
- 平台：github （主）/ gitee（辅）
- kind：fix

## Discovery

### 背景
`./bin/` → `freely` 替换在 216 个文件中已执行，但以下 6 个 .sh 文件被 gate 判定为代码而撤销了修改：

1. `.githooks/pre-commit.sh`
2. `docs/system/workspace/hooks/pre-commit.sh`（前者的正式真源）
3. `docs/system/workspace/hooks/pre-merge-commit.sh`
4. `docs/system/workspace/hooks/pre-push.sh`
5. `docs/system/workspace/hooks/reference-transaction.sh`
6. `docs/system/workspace/scripts/start-lead-agent.sh`

### 时效性判断
- 问题与 #3622（命令规范化 — 全链路 [cmd] 节点统一为 freely 子命令）紧密相关，属同一轮规范化行动
- 216 个文件已成功替换，仅剩这 6 个 .sh 文件因 gate 判定撤回
- 不实施会导致命令引用不一致：大部分文件用 `freely xxx`，这些文件仍用 `./bin/xxx`
- **结论**：值得投入，时效性高

### 当前状态
每个文件中仍存在大量 `./bin/` 引用模式，包括：
- `./bin/freely xxx` → 应替换为 `freely xxx`
- `./bin/pr-create-guarded`、`./bin/pr-merge-guarded` → 应替换为 `freely pr-create-guarded`、`freely pr-merge-guarded`
- `./bin/wt-create`、`./bin/wt-close` → 应替换为 `freely wt-create`、`freely wt-close`
- `./bin/governance-merge-gate`、`./bin/governance-promotion-gate` → 应替换为 `freely governance-merge-gate`、`freely governance-promotion-gate`
- `./bin/checkpoint-guard`、`./bin/pretests-gate` → 应替换为 `freely checkpoint-guard`、`freely pretests-gate`

以及文件存在性/可执行性检查：
- `[[ -f "./bin/..." ]]` / `[[ -x "./bin/..." ]]` → 需改为 `which freely` 或等效检查

## Problem

核心问题：6 个 shell 脚本文件中仍使用 `./bin/xxx` 格式引用命令，与其他 216 个已规范化文件不一致。hook 脚本尤其关键——它们是在 commit/merge/push 时执行的，若 `./bin/` 下的实际二进制不完整或路径不对齐，会导致钩子静默失效或错误提示路径混淆。

## Brainstorm

### Option A: 全文机械替换（与 216 文件一致）
将所有 `./bin/<command> <args>` 替换为 `freely <command> <args>`，包括：
- 命令执行行（`./bin/freely xxx` → `freely xxx`）
- 存在性检查（`[[ -x "./bin/governance-merge-gate" ]]` → `which freely` 或 `freely` 存在性检查）
- source 行（`source ./bin/worktree-common.sh`）保留不变（这属于库引用，不是 CLI 命令）

**优点**：与 216 个文件的处理方式完全一致，一次性完成
**缺点**：需要仔细区分 source 行和命令执行行，避免误改

### Option B: 仅替换命令执行行
只替换实际执行 `./bin/xxx` 命令的行，保留所有 `[[ -x ]]` / `[[ -f ]]` 检查和 `source` 行。

**优点**：保守，风险最小，不会意外破坏门禁逻辑
**缺点**：存在性检查仍指向旧路径，与 `freely` 命令体系不完全对齐

### Option C: 分文件逐个处理
对每个 .sh 文件单独评估替换策略，不搞一刀切。

**优点**：精细控制
**缺点**：增加不一致性风险，且与 216 个文件的方式脱节

## Decision: Option A（全文机械替换）

### 理由
1. 216 个文件的替换已验证该策略正确有效
2. 门禁撤回这 6 个文件是因为识别为"代码文件"走 gate 检查，不是替换策略有问题
3. 统一替换保持全仓一致性
4. gate 的存在性检查需要同步适配——如果命令已迁移到 `freely` 子命令体系，检查 `./bin/` 路径已无意义

### 替换规则
| 原始模式 | 替换后 | 说明 |
|----------|--------|------|
| `./bin/freely xxx` | `freely xxx` | CLI 命令调用 |
| `./bin/pr-xxx` | `freely pr-xxx` | PR 相关子命令 |
| `./bin/wt-xxx` | `freely wt-xxx` | worktree 相关子命令 |
| `./bin/governance-xxx` | `freely governance-xxx` | 治理门禁子命令 |
| `./bin/checkpoint-guard` | `freely checkpoint-guard` | checkpoint 子命令 |
| `./bin/pretests-gate` | `freely pretests-gate` | pretests 子命令 |
| `[[ -x "./bin/worktree-common.sh" ]]` | 保留 `[[ -f "./bin/worktree-common.sh" ]]` | 库文件存在性检查，非 CLI 命令 |
| `source ./bin/worktree-common.sh` | 保留 | 库引用，非 CLI 命令 |
| `[[ -x "./bin/governance-merge-gate" ]]` | `which freely >/dev/null 2>&1` | CLI 可用性检查 |
| `[[ -x "./bin/checkpoint-guard" ]]` | `which freely >/dev/null 2>&1` | CLI 可用性检查 |
| `[[ -x "./bin/pretests-gate" ]]` | `which freely >/dev/null 2>&1` | CLI 可用性检查 |

### 边界
- `source ./bin/worktree-common.sh` 和 `[[ -f "./bin/worktree-common.sh" ]]` 涉及库文件 `worktree-common.sh`，不属于 CLI 命令迁移范围，保留原样
- 面向用户的提示/错误消息中的 `./bin/xxx` 路径引用也一并更新为 `freely xxx`

## Candidate
- candidate_id: C-20260629T132042Z-A
- status: promoted
- milestone: M-20260629T132042Z-A
