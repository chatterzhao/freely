---
b1_id: B1-20260720T023136Z
phase_state: completed
source_raw: raw-20260720T023136Z
source_url: https://github.com/chatterzhao/freely/issues/4038
produced_candidate: C-20260720T023136Z-A
created_at: 2026-08-07
---

# B1_IBM: chat help 错误信息 shell 引号导致文件重定向解释

## Input
- raw-20260720T023136Z（GitHub #4038）
- 现象：`docs/system/workspace/scripts/runtime/freely` L6700 的 `log_error` 消息包含 `<描述>` / `<详细描述>`，bash 把 `<` 当作输入重定向操作符，实际渲染时输出 `line 6700: 描述: No such file or directory`，错误提示本身崩溃，用户看不到完整帮助文本。

## Problem
- 根因：字符串用双引号包裹，但消息内部又嵌套了双引号（`--title "fix|feat: <描述>"`），导致外层双引号提前闭合，`fix|feat: <描述>` 与 `<详细描述>` 落入非引号区，`<` 被 bash 解释为输入重定向。
- 这不是展示内容错误，而是 shell 语法层的引号嵌套 bug。

## Brainstorm
### Option A: 整体改单引号（选定）
- 将整个 `log_error` 参数改为单引号包裹：`log_error '[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"'`。
- 单引号内 `"` 与 `<` 全部按字面输出，无重定向解释；消息内部需展示的双引号原样保留。
- 已验证：`bash -c` 模拟输出正确且 EXIT=0，无 `No such file` 报错。

### Option B: 转义尖括号 `\<描述\>`
- 保留外层双引号，仅对 `<` `>` 加反斜杠转义。
- 可行，但可读性差；若后续再嵌套引号容易复发，且 `\` 与中文混排视觉噪音大。

### Option C: 用 printf '%s' 传参
- `printf '%s\n' '...' >&2` 形式。
- 能解决问题，但改变 log_error 调用方式，超出最小修复面，且与全脚本 log_error 用法不一致。

## Decision: Option A
- 理由：最小、语义正确，单引号内字面量完全规避重定向解释，同时保持中文提示与内层双引号可读；与 log_error 常规用法一致（只改一个字符串字面量）。
- scope：只改 L6700 一个字符串；不扫描、不改其他 log_error。

## Candidate
- candidate_id: C-20260720T023136Z-A
- status: promoted
- milestone: M-20260720T023136Z-A
