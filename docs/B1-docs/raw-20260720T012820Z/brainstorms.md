- b1_id: B1-20260720T012820Z
- phase_state: completed
- source_raw: raw-20260720T012820Z
- produced_candidate: C-20260720T012820Z-A
- created_at: 2026-07-20

# B1_IBM: cross-tool worker launch-kind new→fresh

## Input
- raw-20260720T012820Z: cross-tool ACP bridge worker launch 使用无效的 --launch-kind new
- 来源：worker crash debug log 分析

## Problem
- run-acp-prompt.py --launch-kind 仅接受: fresh, resume, fork, prompt
- Cross-tool worker 路径 (freely script L13340-13348) 使用 `_worker_launch_kind="new"`
- "new" 不在合法枚举中 → argparse error → worker 立即崩溃
- 这导致 cross-tool 配置下 Worker 永远无法启动
- debug log 确认: "run-acp-prompt.py: error: argument --launch-kind: invalid choice: 'new' (choose from fresh, resume, fork, prompt)"

## Brainstorm
### Option A: new→fresh (选用)
- 最简修复：一字改动
- fresh 语义正确：cross-tool 无法 fork（不同 base tool），需要新 session
- 行为与预期一致：启动一个新 session

### Option B: 在 run-acp-prompt.py 中添加 "new" 别名
- 侵入性更大：修改 ACP prompt launcher 本身
- 语义混淆："new" vs "fresh" vs "prompt" 界限模糊
- 驳回：修复应在调用侧，不在工具侧

## Decision: Option A — new→fresh
- 一字改动在 freely script 的 cross-tool worker launch 路径
- 与 run-acp-prompt.py 合法值对齐
- 语义正确：cross-tool session 初始化为 fresh

## Candidate
- candidate_id: C-20260720T012820Z-A
- status: promoted
- milestone: M-20260720T012820Z-A
