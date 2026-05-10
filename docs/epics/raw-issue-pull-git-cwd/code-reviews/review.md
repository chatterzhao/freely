# Code Review: raw-issue-pull git CWD fix
- issue_id: I-20260508T133423Z-A
## Implementation Decision Note
- decision: 使用 git rev-parse 替代硬编码 ROOT_DIR，排除 .scan-state
- why_this: 工位即可执行，不依赖项目根目录
