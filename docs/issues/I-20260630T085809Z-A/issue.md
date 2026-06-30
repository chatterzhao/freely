- issue_id: I-20260630T085809Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260630T085809Z-A
- source_candidate: docs/pre-brainstorms/20260630T085809Z--a2a-healthcheck-fix/candidates.md#C-20260630T085809Z-A
- verification_artifact_dir: docs/epics/a2a-healthcheck-fix/socket-healthcheck/code-reviews
- pre_tests_path: docs/epics/a2a-healthcheck-fix/socket-healthcheck/pre-tests.md
- canonical_issue_path: ""
- title: 修复 A2A Server 健康检查协议错误、日志轰炸、Shell 注入、超时和日志格式

# I-20260630T085809Z-A: A2A Server 健康检查修复

- source_candidate: docs/pre-brainstorms/20260630T085809Z--a2a-healthcheck-fix/candidates.md#C-20260630T085809Z-A
- verification_artifact_dir: docs/epics/a2a-healthcheck-fix/socket-healthcheck/code-reviews

## 实现
修复 5 个互联的 A2A Server 启动期 bug：

1. **健康检查协议**: `freely:8620` — 改为 socket connect 检查，不再发送 HTTP 请求
2. **h11 日志抑制**: `a2a_server.py:301` — 修复 log config 未生效
3. **Shell 注入**: `freely:8619` — 用环境变量 `FREELY_A2A_SOCKET` 替代字符串拼接
4. **启动超时**: `freely:8612` — 从 10 秒延长到 30 秒
5. **日志时间戳**: `a2a_server.py:651` — uvicorn formatter 添加 `%(asctime)s`
