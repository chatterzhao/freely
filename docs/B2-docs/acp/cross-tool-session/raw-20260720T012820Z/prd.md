# PRD: cross-tool worker launch-kind new→fresh
- issue_id: I-20260720T012820Z-A

## Goal
修复 cross-tool worker 启动时因无效 launch-kind "new" 导致的 argparse crash，使 worker 能正常启动。

## Problem
- run-acp-prompt.py --launch-kind 仅接受: fresh, resume, fork, prompt
- freely script cross-tool worker 路径使用 "new"
- "new" 不在合法枚举中 → argparse error → worker 立即崩溃
- 影响: cross-tool 配置下 Worker 永远无法启动

## Implementation
- 文件: docs/system/workspace/scripts/runtime/freely
- 位置: L13347
- 改动: `_worker_launch_kind="new"` → `_worker_launch_kind="fresh"`
- 语义: fresh 表示新 session，cross-tool 无法 fork（不同 base tool），语义正确

## Dev-Loop Handoff
- 改动范围: 一字
- 测试: merge 后 clear DB → restart freely → 观察 worker debug log 确认 --launch-kind fresh 无 argparse error
- 回滚: 如 fresh 导致其他问题，恢复 "new" 并改为在 run-acp-prompt.py 添加 "new" 别名
