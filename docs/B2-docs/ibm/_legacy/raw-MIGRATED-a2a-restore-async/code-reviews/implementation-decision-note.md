# Implementation Decision Note: _restore_tasks 异步化
- issue_id: I-20260624T004524Z-A
- issue_path: docs/issues/I-20260624T004524Z-A/issue.md
- milestone: M-20260624T004524Z-A

## Implementation Decision Note
- decision: _restore_tasks 从 A2AServer.__init__ 移至 start() 中的 daemon 线程执行
- why_this: __init__ 中的同步恢复阻塞 socket 绑定导致 health check 超时；daemon 线程让 server 先接受连接再后台恢复
- alternatives_considered: (1) asyncio.create_task — uvicorn 在 daemon 线程中运行，event loop 跨线程传递复杂 (2) 增大 timeout — 治标不治本
- boundary_non_goals: 不改变 _restore_tasks 恢复逻辑本身；不改变 health check 的 10s 超时值
- residual_risk: _restore_tasks 中的 task_store 操作是线程安全的 SQLite（WAL 模式），并发场景极少
