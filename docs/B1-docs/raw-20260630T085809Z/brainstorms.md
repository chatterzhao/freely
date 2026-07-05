---
b1_id: B1-20260630T085809Z
phase_state: completed
source_raw: raw-20260630T085809Z
source_url: https://github.com/chatterzhao/freely/issues/3647
produced_candidate: C-20260630T085809Z-A
created_at: 2026-06-30
---

# B1_IBM: A2A Server 健康检查协议错误导致日志轰炸和启动超时

## Input
- raw issue: `docs/B1-docs/raw-20260630T085809Z/issue.md`
- 平台: GitHub #3647, Gitee #IJXVF2
- 发现方式: `freely start --task-mode auto` 启动时观测

## Discovery — 问题验证

### 观测事实
1. A2A Server 日志 45,870 行中 44,835 行 (97.7%) 是 "Invalid HTTP request received"
2. A2A Server 累计启动 122 次，0 次优雅关闭 — 服务器频繁崩溃重启
3. `freely start` 报告 "A2A server start timed out after 10s" 但服务器实际启动成功（PID 70117）
4. `task_mode degraded to WAIT: DB query failed after 3 retries` — 在 DB daemon 就绪前查询
5. A2A Server 日志无时间戳，无法追踪问题时间线
6. ASGI Exception: `JSONDecodeError` — JSON-RPC endpoint 收到非法请求
7. `FileNotFoundError: /tmp/freely-a2a-*.sock` — 多进程竞态条件

### 时效性判断
- 问题当前仍在发生（今天启动复现）
- 直接影响 Freely 运行时稳定性
- **结论: 值得投入修复**

## Problem — 根因分析

### 根因 1: 健康检查协议不匹配
`docs/system/workspace/scripts/runtime/freely:8620`:
```python
s.sendall(b'GET /tasks HTTP/1.1\r\nHost: localhost\r\n\r\n')
```
- 发送原始 HTTP GET 到 Unix socket
- A2A Server 的 `/_tasks_endpoint` 虽然接受 GET，但 h11 在服务器启动瞬间（socket 存在但 ASGI app 未完全初始化）将这些字节识别为无效 HTTP
- 正确做法: ① 用 `/.well-known/agent.json` 端点（REST，始终可用且轻量）；② 或用 socket 文件存在性 + PID 存活作为健康信号

### 根因 2: h11 日志抑制未生效
`docs/system/workspace/scripts/runtime/a2a/a2a_server.py:301-309`:
```python
def _a2a_uvicorn_log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "h11": {"level": "ERROR"},
            "uvicorn": {"level": "INFO"},
        },
    }
```
- `"h11"` 是包级 logger name，但 h11 实际使用的 logger 是 `h11._connection`、`h11._readers` 等子模块
- 虽然 Python logging 层级继承应该生效，但 uvicorn 在应用 log_config 之前已经配置了 root logger
- `"disable_existing_loggers": False` 导致已有 logger 不被覆盖
- 修复: 用 `"h11"` 包级抑制 + uvicorn 的 `--log-level` 参数双重保障，或直接在 uvicorn config 中用字符串 log-level 控制

### 根因 3: Shell 注入
`docs/system/workspace/scripts/runtime/freely:8619`:
```python
s.connect('$a2a_socket')
```
- `$a2a_socket` 直接拼接到 Python `-c` 字符串
- 攻击面: socket 路径包含 `'` 字符时可逃逸 Python 字符串
- 修复: 与环境变量 `FREELY_HEALTH_SOCKET` 传递，与之前修复的 freely-cycle 同类问题

### 根因 4: 启动超时 10 秒过短
- `_restore_tasks()` 在后台线程恢复历史 task，需要遍历 a2a_tasks 表、检查 PID 存活、worktree 存在性
- 当前项目中 a2a_tasks 有一定历史数据，恢复过程需要 5-15 秒
- 修复: 延长超时到 30 秒，或用指数退避代替固定间隔

### 根因 5: A2A Server 日志无时间戳
- uvicorn 默认使用 `logging.Formatter("%(levelprefix)s %(message)s")` — 无时间戳
- 修复: 在 `_a2a_uvicorn_log_config()` 中配置 formatter 添加时间戳

## Brainstorm — 方案评估

### Option A: 改造健康检查为 socket 存在性检查（最小改动）
- 移除 HTTP 请求发送，改为:
  1. 检查 socket 文件存在 (`os.path.exists`)
  2. 连接测试 (`socket.connect` 成功即认为就绪)
  3. 不发送任何数据，不期待响应
- 优点: 改动最小，彻底消除 "Invalid HTTP" 日志，无协议依赖
- 缺点: socket 存在不等于 server 能处理请求（但 connect 成功 + socket 文件存在已足够证明 uvicorn 在监听）
- **选此方案** — 最简洁、最可靠

### Option B: 改用 `/.well-known/agent.json` 端点
- `GET /.well-known/agent.json` — Starlette REST 端点，返回 JSON
- 优点: 真正的 HTTP 层验证
- 缺点: 仍需要发送 HTTP 请求，h11 在启动瞬间仍可能报错；agent-card 响应体较大

### Option C: 只改日志抑制 + 修复 shell 注入 + 延长超时
- 保留现有健康检查机制，只修复副作用
- 优点: 不改变健康检查语义
- 缺点: 根本问题（协议不匹配）未解决

## Decision: Option A

**理由:**
1. Unix socket 健康检查的语义是 "服务器是否在监听"，socket 文件存在 + connect 成功足以证明
2. HTTP 层验证可以在启动后通过 `freely daemon status` 独立验证，不应混入启动流程
3. 彻底消除 "Invalid HTTP request" 日志来源
4. 零协议依赖，不会因 A2A 协议升级而失效

**附加修复 (与 Option A 并行):**
- Fix h11 log suppression: 改 `"h11": {"level": "ERROR"}` + 在 uvicorn config 中使用 `log_level="warning"` 降低全局日志级别
- Fix shell injection: 用 `FREELY_A2A_SOCKET` 环境变量
- Fix timeout: 30 秒，间隔 1 秒（30 次重试）
- Fix timestamps: uvicorn formatter 添加 `%(asctime)s`

## Candidate
- candidate_id: C-20260630T085809Z-A
- status: promoted
- milestone: M-20260630T085809Z-A
- acceptance_criteria:
  - 健康检查改为 socket 存在性检查（connect 成功 = 就绪），不再发送 HTTP 请求
  - Shell 注入修复：socket 路径通过环境变量 `FREELY_A2A_SOCKET` 传递
  - h11 日志抑制生效：`"h11"` logger 设为 ERROR 级别
  - A2A 启动超时从 10 秒延长到 30 秒
  - A2A Server 日志包含时间戳
- promotion_gate: 修改 freely 脚本 + a2a_server.py，语法验证通过，启动测试无 "Invalid HTTP" 日志
