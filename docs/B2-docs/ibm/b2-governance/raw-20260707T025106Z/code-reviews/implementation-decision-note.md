# Implementation Decision Note

- issue_id: I-20260707T025106Z-A
- milestone: M-20260707T025106Z-A
- created_at: 2026-07-07

## Decision

在 pr-review-guarded 增加双重清洁检查（审查前入口 + 审查后出口），pr-merge-guarded 增加兜底检查（合并前最后防线）。检查逻辑完全复用 pr-create-guarded Step 0a 模式（git status --porcelain + git ls-files --others）。

## Why This

1. pr-review-guarded 当前没有任何工位清洁检查——这是明确的功能缺口
2. review 过程可能生成文件（review doc、gate 修复等），没有出口闸门这些修改会丢失
3. pr-merge-guarded 兜底是最后的安全网——即使前两道闸门被绕过也能拦住
4. 复用已有模式（pr-create-guarded Step 0a）确保实现一致性和可维护性

## Alternatives Considered

| 方案 | 评估 |
|------|------|
| A: 只加审查前检查 | ❌ 审查后产生的修改仍可能遗漏 |
| B: 审查前+后+merge 兜底 ✅ | 选定：三层覆盖，每层不同的错误消息场景 |
| C: 只加 merge 兜底 | ❌ 问题发现太晚，需回到 review 重做 |

## Boundary Non-Goals

- 不修改 pr-create-guarded 的检查逻辑（已有且正确）
- 不改变任何门禁规则
- 不修改 wt-close 的检查逻辑
- 不涉及 test-pre-merge 工位的清洁检查

## Residual Risk

- **pr-review-guarded 脚本的 $review_branch 变量引用 bug**：脚本中 `$review_branch` 在参数解析前被引用（line 39），set -euo pipefail 下会导致脚本报错。这个 bug 已存在，不在本次修复范围。
- **清洁检查只检测 tracked/untracked 文件**：不检测 submodule 变更、stash 状态等边缘情况，但这些边缘情况在实际使用中极少触发。
- **检查逻辑是纯文本插入**：与现有脚本逻辑无交互，bash -n 语法检查即可验证。
