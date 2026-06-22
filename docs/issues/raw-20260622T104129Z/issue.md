---
local_id: raw-20260622T104129Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T104129Z-A
platform_ids:
  github:
    issue_id: '3349'
    url: https://github.com/chatterzhao/freely/issues/3349
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T10:41:46Z'
updated_at: '2026-06-22T10:41:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

当前 `FREELY_SKIP_IBM_GATE=1` 和 `FREELY_SKIP_CREATE_GATE` 是布尔型 env var 绕过机制，不需要任何理由就能绕过门禁。这违反了"所有绕过类型必须有准确业务理由"的治理原则。

## 现状

```bash
# 无理由就能绕过
FREELY_SKIP_IBM_GATE=1 git commit ...
FREELY_SKIP_IBM_GATE=1 git push ...
FREELY_SKIP_CREATE_GATE=1 git push ...
```

## 目标

改为 reason-string 模式，必须匹配正则 `^违规绕过门禁中，理由充分，是：`：

```bash
# 必须带业务理由
FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：仅文档类变更不含实现代码，无需IBM生命周期" git commit ...
FREELY_SKIP_CREATE_GATE="违规绕过门禁中，理由充分，是：纯治理文档更新，pr-create 门禁不适用" git push ...
```

## 涉及文件

| 文件 | 改动 |
|------|------|
| `.githooks/pre-commit.sh` / `docs/system/workspace/hooks/pre-commit.sh` | `FREELY_SKIP_IBM_GATE` 检查: `== "1"` → regex 匹配 |
| `docs/system/workspace/hooks/pre-push.sh` | `FREELY_SKIP_IBM_GATE` + `FREELY_SKIP_CREATE_GATE` 检查 |
| `docs/system/workspace/hooks/pre-merge-commit.sh` | `FREELY_SKIP_IBM_GATE` 检查 |
| `docs/system/workspace/hooks/reference-transaction.sh` | `FREELY_SKIP_IBM_GATE` 检查 + GATE 消息 |

## GATE 拦截行为

当 env var 值不匹配正则时：
1. 拦截操作（阻止 commit/push/merge）
2. 输出 GATE 消息，格式与 CLI --reason gate 统一：
   ```
   [GATE] 检测到你试图通过 FREELY_SKIP_IBM_GATE 违规绕过门禁
   
   如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。
   
   只有确实有合理的业务理由（仅文档/清理/格式化变更等），才允许绕过。
   FREELY_SKIP_IBM_GATE 的值必须匹配格式:
     FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"
   
   示例: FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：仅文档类变更不含实现代码" git push
   ```

## 有效业务理由示例
- ✅ "仅文档类变更不含实现代码，无需IBM生命周期"
- ✅ "纯清理/格式化变更，无功能影响"
- ✅ "治理文档更新，pr-create 门禁不适用"

🤖 Generated with [Claude Code](https://claude.com/claude-code)
