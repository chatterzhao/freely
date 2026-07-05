# Tasks: A2A server _restore_tasks 异步化
- issue_id: I-20260624T004524Z-A

## T1: _restore_tasks 从 __init__ 移除 ✅
- file: a2a_server.py:338
- status: done

## T2: start() 中添加后台恢复线程 ✅
- file: a2a_server.py:675
- status: done

## T3: 修正 health check 超时消息 ✅
- file: freely:8385
- status: done
