# 预头脑风暴工作区

预头脑风暴记录的规范结构：

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
