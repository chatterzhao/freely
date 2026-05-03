# Code Review — Scan Lifecycle Migration

- issue_id: `I-20260503-0200-A`
- review_date: 2026-05-03
- reviewer: ai
- verdict: approved

## Changes Reviewed
- `task-lifecycle-scan.py`: +600 lines, full lifecycle chain trace
- `freely`: prompt builder rewritten for lifecycle-aware output
- `acp-bridge.py`: hash-based socket path
- `wt-create`: fixed issue key regex, test-pre-merge support
- `pre-push.sh`: branch naming convention gate
- `.githooks/post-checkout`: auto pre-init-runtime for test-pre-merge

## Implementation Decision Note
- 选择 chain trace 替代旧 flat scan：每个 raw-xxx key 追踪14站
- mandatory 站点阻塞进度，optional 站点仅报告
- 分支命名不再豁免旧分支，全部按规范整改
- socket 路径用 SHA256 hash 避免 AF_UNIX 104字节限制
