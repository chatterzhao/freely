# Tasks: #3731 ACP cleanup 遗漏修复
- issue_id: I-20260704T234812Z-A

## Phase 1: 语法错误修复
- [x] 1.1 freely_db_manager.py: h_aw_upsert_only 缩进修正
- [x] 1.2 watchdog_sse.py: 3 个 docstring 补全闭合

## Phase 2: base_tool plumbing
- [x] 2.1 acp-bridge.py: 添加 --base-tool CLI 参数；AcpBridge.__init__ 接受 base_tool
- [x] 2.2 acp-bridge.py: cmd_start/stop/status 穿透 base_tool
- [x] 2.3 freely: _ensure_acp_bridge_running pid_file 传 $base_tool
- [x] 2.4 freely: _acp_bridge_health_check 传 $base_tool
- [x] 2.5 freely: bridge start 命令传 --base-tool
- [x] 2.6 monitor-ai-acp.sh: _bridge_ensure_running 传 base_tool
- [x] 2.7 monitor-ai-acp.sh: bridge start 传 --base-tool

## Phase 3: 路径一致性
- [x] 3.1 freely: _acp_bridge_pid_file/_acp_bridge_socket 改为 conditional suffix
- [x] 3.2 monitor-ai-acp.sh: _bridge_pid_file/_bridge_socket 改为 conditional suffix

## Phase 4: 硬编码路径替换
- [x] 4.1 freely: 5 处硬编码 socket 路径替换为 _acp_bridge_socket 函数调用

## Phase 5: agent_assign 迁移
- [x] 5.1 freely: 3 处 agent_assign → acp_session_register

## Phase 6: Hook 提示改进
- [x] 6.1 pre-commit.sh: 拦截消息改为 `freely feedback` + `freely wt-create` + skill

## Phase 7: 验证
- [x] 7.1 AT-001: 全部文件语法检查通过
- [x] 7.2 AT-002: acp-bridge.py CLI 含 --base-tool
- [x] 7.3 AT-003: bash/Python 路径一致
- [x] 7.4 AT-004: hook 消息含三项关键词
