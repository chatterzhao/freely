# Brainstorm: raw-issue-pull git -C ROOT_DIR + worktree guard
- 来源: raw-20260508T133423Z23Z (#259)
## Discovery
raw-issue-pull `git -C "$ROOT_DIR"` 永远返回 develop，任何工位内 pull 都失败。
## Decision
去掉 -C ROOT_DIR，用当前目录；加 fix/* feature/* 显式 guard。
