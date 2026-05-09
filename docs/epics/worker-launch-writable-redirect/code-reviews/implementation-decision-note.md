# Implementation Decision Note

## Decision

`worker_prompt_launchable_for_manager_project()` 在已提取 `target_branch` 后增加 shell `case` prefix 检查：仅 `fix/*` 和 `feature/*` 允许通过，其他 branch 返回 1（not launchable）。

## Why this

这是对根因链最精确的修复：
- 第 2+3 层（runtime 不验证 → worker 启动后在保护分支被 hook 拦截）
- 改动仅限于一个函数（L9695-9717），不影响其他功能
- 已有 `WORKER_PROMPTS_NOT_LAUNCHABLE` 处理路径（L13177）直接复用
- 符合最小作用域原则：不做自动重定向、不改 prompt 格式、不改 resolved_worktree

## Alternatives considered

| 方案 | 问题 |
|------|------|
| 自动重定向到配对工位 | 主管可能选错工位，runtime 猜测不可靠；brainstorm 已否决 |
| 在 prompt 生成时检查 | 需要改提示词生成逻辑，影响更大 |
| 在 hook 层面加友好提示 | hook 已经是第二道防线，第一道必须在 launch 时阻断 |

## Boundary / non-goals

- 不改 `worker_prompt_resolved_worktree`——worktree 路径解析和 branch 验证是两层职责
- 不改 AI prompt 格式——主管侧修正 worktree 路径就能通过
- 不改 hotfix/release 判断——当前场景不涉及

## Residual risk

- 若将来出现合法非 fix/feature 的 worker target（如 release/* 的临时维护），此检查会误拒
  - 缓解：放行 `hotfix/*` 作为扩展点，其他新情况按需加 prefix 进 case
  - 空 branch 值已放行，避免 `worker_prompt_target_branch` 新格式解析失败时阻塞
- 被拒后的 storm 风险：runtime 已有 `WORKER_PROMPTS_NOT_LAUNCHABLE` → `resume_invalid` 路径，不会无限重启
