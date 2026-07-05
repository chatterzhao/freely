# Code Review — Scan Lifecycle Migration

- issue_id: `I-20260503-0200-A`
- issue_path: `docs/B2-docs/runtime/scan-lifecycle-migration/issues/I-20260503-0200-A.md`
- review_date: `2026-05-03`
- reviewer: `ai`
- verdict: `approved`

## Changes Reviewed
- `task-lifecycle-scan.py`: chain trace, chat inbox, governance
- `freely`: prompt builder rewritten
- `acp-bridge.py`: hash-based socket path
- `wt-create`: fixed regex, test-pre-merge support
- `pre-push.sh`: branch naming gate
- `.githooks/post-checkout`: auto pre-init-runtime

## Implementation Decision Note

- decision: `切换到 task-lifecycle-scan v2，用 chain trace 替代旧 flat scan，分支命名不再豁免`
- why_this: `旧 scan 输出 147 条噪声且已废弃，新 scan 已有实现但未接入。chain trace 按 raw-xxx key 追踪完整生命周期，每条有精确的 current/next/blokers`
- alternatives_considered: `(1) 修旧 scan — 治标不治本，旧架构无法支持链条追踪；(2) 完全重写 — 成本高，task-lifecycle-scan.py 已有完整基础`
- boundary_non_goals: `不覆盖外部平台同步（issue-sync），不替代 pr-merge-guarded 门禁`
- residual_risk: `chat inbox 依赖 freely.db 的 chats 表（pre-init-runtime 拷贝时可能锁表导致0字节），SKIP_PLATFORM_CHECK 跳过平台关闭检查`
