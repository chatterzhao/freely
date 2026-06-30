# Tasks: A2A Server 健康检查修复
- issue_id: I-20260630T085809Z-A

## Task 1: 修复健康检查协议 (freely 脚本)
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: `ensure_a2a_server_running()` 函数 (~line 8608-8640)
  - 将 HTTP GET 健康检查改为 socket connect 检查
  - 用 `os.path.exists(socket_path) + socket.connect()` 替代 `sendall(GET /tasks)`
- 依赖: 无

## Task 2: 修复 Shell 注入 (freely 脚本)
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: 健康检查 Python -c 代码块
  - 用 `os.environ.get('FREELY_A2A_SOCKET')` 替代 `'$a2a_socket'` 字符串拼接
  - 调用前 `export FREELY_A2A_SOCKET="$a2a_socket"`
- 依赖: Task 1

## Task 3: 延长启动超时 (freely 脚本)
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: line 8612
  - `_health_waited -lt 20` → `_health_waited -lt 30`
  - `sleep 0.5` → `sleep 1`（减少轮询频率）
- 依赖: Task 1

## Task 4: 修复 h11 日志抑制 (a2a_server.py)
- 文件: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
- 改动: `_a2a_uvicorn_log_config()` 
  - 添加 `"disable_existing_loggers": True` 强制覆盖
  - 或改用 `uvicorn.Config(log_level="warning")` 字符串形式
- 依赖: 无

## Task 5: 添加日志时间戳 (a2a_server.py)
- 文件: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
- 改动: `_a2a_uvicorn_log_config()` 或 uvicorn.Config
  - formatter 添加 `%(asctime)s` 或设置 `datefmt`
- 依赖: 无

## Task 6: 验证
- 在 test-pre-merge 工位执行 pre-tests.md 全部 acceptance items
- 确认 AT-001 ~ AT-005 全部 GREEN
- 依赖: Task 1-5
