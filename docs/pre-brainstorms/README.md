# 预研头脑风暴工作区

预研头脑风暴记录的规范结构：

```text
docs/pre-brainstorms/
  INDEX.md
  <YYYYMMDD-HHMM--topic>/
    brainstorms.md
    candidates.md
```

`<id>` 命名规则：
- 使用 `YYYYMMDD-HHMM--<topic>` 格式（24 小时制，零填充）。
- `<topic>` 保持简洁，使用 kebab-case。
- 确保同一天的条目按时间自然排序。

## 状态

- 迁移已完成。
- 本目录是 pre-brainstorm 记录的活跃来源。

## Candidates 字段约定

`candidates.md` 中以下字段必须显式填写，不留空值：
- `promoted_issue_path`：未落位前使用 `pending://issue-materialization`
- `milestone`：未绑定前使用 `pending://milestone-binding`
- `session_refs`：无会话证据时使用 `[]`

`session_refs` 一旦存在，最小结构为：
- `tool`
- `session_id`
- `jsonl_path`
- `role`

若当前 AI 工具无法暴露 jsonl 文件路径，允许 `jsonl_path=unavailable://<reason>`，但不得省略 `session_id`

## Candidate 产物定位

`candidates.md` 只承载 pre-brainstorm 阶段的前置收敛状态，不承载执行态。

建议状态只使用：

- `proposed`
- `needs_research`
- `promoted`
- `dropped`

说明：

- `promoted` 表示该 candidate 已被 milestone 接纳，后续从 milestone / issue 继续推进
- `in_progress`、`blocked`、`completed` 这类执行态应写在 milestone / issue / progress 产物中，而不是写回 candidate
