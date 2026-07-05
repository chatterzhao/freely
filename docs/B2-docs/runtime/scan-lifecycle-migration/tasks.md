# Tasks — scan lifecycle migration

- issue_id: `I-20260503-0200-A`

## task-1: switch TASK_SOURCE_SCAN_SCRIPT
- status: done
- summary: 将 freely runtime 中的 scan 脚本引用从 task-source-scan.py 切换到 task-lifecycle-scan.py

## task-2: rewrite prompt builder
- status: done
- summary: 重写 append_task_source_patrol_seed_if_needed 为 lifecycle-aware 输出

## task-3: add chain trace
- status: done
- summary: 实现 _trace_chain 函数，按 raw-xxx key 追踪完整生命周期站

## task-4: add chat inbox scan
- status: done
- summary: 实现 scan_chat_inbox 从 freely.db 扫描 unconsumed chats

## task-5: fix AF_UNIX socket path
- status: done
- summary: acp-bridge.py 用 hash-based /tmp 路径替代 worktree 内长路径

## task-6: enforce branch naming
- status: done
- summary: governance scan + pre-push hook 强制分支名包含 issue key
