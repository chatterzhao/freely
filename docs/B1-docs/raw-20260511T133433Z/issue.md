---
local_id: raw-20260511T133433Z33Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
priority: high
source: platform
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '302'
    owner: chatterzhao
    repo: freely
created_at: '2026-05-11T13:34:33Z'
title: 'fix: .githooks/* wrappers bash 3.2 precedence bug blocks all ref updates'
platform_state: closed
---

## 问题

macOS 自带 bash 3.2 的 `set -e` 行为与 bash 4.x/5.x 不同：`X=$(failing_cmd)` 即使失败命令在 `&&` 列表里，也会导致脚本退出。

配合 `.githooks/*` 4 个 wrapper 第 4 行的 bash 优先级问题（`&&`/`||` 同级左结合）：

```bash
ROOT_DIR="$(git rev-parse --show-toplevel || cd ... && pwd -P)"
# bash 解析为 (A || B) && C → pwd -P 总会执行 → ROOT_DIR 含换行符
```

## 修复

每个 wrapper 加 `{ ; }` 显式分组：

```diff
-ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || cd ... && pwd -P)"
+ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || { cd ... && pwd -P; })"
```

## 绕过说明

此 bug 本身会拦截修复自己的合并，需 `FREELY_SKIP_IBM_GATE=1` 绕过。
