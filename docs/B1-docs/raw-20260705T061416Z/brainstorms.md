---
b1_id: B1-20260705T061416Z
phase_state: completed
source_raw: raw-20260705T061416Z
source_url: https://github.com/chatterzhao/freely/issues/3742
produced_candidate: C-20260705T061416Z-A
created_at: 2026-07-05
---

# B1_IBM: fix __manager__ slot empty + dirty 提示 backtick 被执行

## Input
- GitHub issue #3742
- Raw key: raw-20260705T061416Z
- Kind: fix

## Discovery

### value_check
- Bug 2 仍有价值：backtick 在 dirty 检查时被 bash 当作命令替换，触发 `command not found` 错误
- Bug 1 已被 M-20260703T080443Z-A 独立修复，无需再处理
- 本 candidate scope 收窄为仅 Bug 2

### scope_check
- 单行修复，scope 极小
- 影响面：仅 `docs/system/workspace/scripts/runtime/freely:21982`，一条 log_error 消息

## Problem

1. ~~Bug 1: daemon 启动时 `__manager__` 行用 `agent_assign` 无 slot → slot 列永远为空~~
   - **已于 M-20260703T080443Z-A 修复**，已改用 `acp_session_register` + `slot='${AGENT_AI_TOOL:-}'`

2. **Bug 2: dirty 提示中反引号被 bash 当命令执行**（待修复）
   - 文件：`docs/system/workspace/scripts/runtime/freely:21982`
   - 当前内容：`log_error "    详细流程见 skill \\\`freely-workflow-guarded-execution\\\`"`
   - 根因：双引号字符串中 `\\` 被转义为字面 `\`，随后裸反引号 `` ` `` 触发命令替换
   - `log_error()` 定义为 `echo "$*"`，参数在传递给函数前已被 bash 展开
   - 效果：bash 尝试执行 `freely-workflow-guarded-execution` 命令，必报 `command not found`

## Brainstorm

### Option A: 去掉反引号，改为纯文本
- 将 `\\\`freely-workflow-guarded-execution\\\`` 改为 `freely-workflow-guarded-execution`
- 优点：最简单、bash 不会触发命令替换、纯文本语义不变
- 缺点：无

### Option B: 用单引号替代反引号
- 将反引号改为单引号：`'freely-workflow-guarded-execution'`
- 优点：有视觉区分
- 缺点：不必要的替代，单引号本身在此无特殊含义

### Option C: 在反引号前加真正的转义
- 改为 `\`freely-workflow-guarded-execution\``（每个反引号前一个反斜杠）
- 优点：保留反引号视觉效果
- 缺点：`\\\`` → `\`\`` 在双引号中仍是 `\`` → 命令替换依然触发，转义链脆弱

## Decision: Option A — 去掉反引号

- 双引号中的反引号换任何转义都需经过两层处理（bash 参数展开 + echo），非常脆弱
- 纯文本是最直接、最安全的方案
- 该字符串仅作为用户可见的提示信息，不构成任何格式约定

## Candidate
- candidate_id: C-20260705T061416Z-A
- status: promoted
- milestone: M-20260705T061416Z-A
