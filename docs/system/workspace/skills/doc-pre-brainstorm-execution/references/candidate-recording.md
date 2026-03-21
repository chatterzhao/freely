# Candidate Recording

## `brainstorms.md`

至少记录：

- 来源
- 当前为什么不能直接进入 IBM / dev
- 当前问题边界
- 推荐下一跳

## `candidates.md`

至少记录：

- `title`
- `status`
- `decision_reason`
- `next_action`
- `revisit_trigger`
- `promoted_issue_path`
- `milestone`
- `session_refs`

若 candidate 当前还不能收口：

- 使用 `needs_research`、`blocked` 或等价的未收口状态词
- 明确写出为什么本轮不能进入 IBM / dev-loop
- 保持它继续出现在 `docs/milestones.md#candidate_issues`
- 不允许因为“本轮没继续做”就静默跳过

## `session_refs`

- 最小结构：`tool/session_id/jsonl_path/role`
- 若 jsonl 路径不可见，使用 `unavailable://<reason>`

## `docs/milestones.md`

必须原子同步：

- 建立 candidate 映射
- 放入 `candidate_issues`
- 写清下一动作
- 若未收口，补 `revisit_trigger` 或同等的下一次重启条件

## Derived worktree fields

若 candidate 依赖未合并父分支，补充：

- `execution_base`
- `integration_target`
- `depends_on`
