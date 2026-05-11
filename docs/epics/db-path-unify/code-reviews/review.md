# Code Review: DB path unification
- issue_id: I-20260511T0245Z-A
## Implementation Decision Note
- decision: project_db_path() 统一入口，默认用 PROJECT_ROOT，可指定 project
- why_this: 安装版和非安装版都能用，维护只改一处
