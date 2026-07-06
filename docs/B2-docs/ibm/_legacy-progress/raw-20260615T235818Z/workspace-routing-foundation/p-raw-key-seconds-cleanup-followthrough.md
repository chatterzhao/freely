# Progress — 秒级 raw key 格式清理跟进

- issue_id: `I-20260513T010343Z-A`
- phase_state: `completed`
- updated_at: `2026-05-13T01:03:43Z`

## Status

14 处遗漏已全部修复：
- 4 处 freely regex `[0-9]{6}` → `[0-9]{4,6}`
- 6 处 wt-create 帮助/错误消息 + legacy regex `[0-9]{4}` → `[0-9]{4,6}`
- 4+ 处 governance-merge-gate / ibm-framework / CONSTITUTION / pre-push 格式文字
- 6+ 处 3 个 skill 文件格式文字

## Next

Merge to develop.
