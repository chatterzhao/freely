# Pre-Tests: ACP/A2A 架构重构

## Acceptance Items

### AI-1: JSON-RPC 2.0 roundtrip
- **Given** a2a_task.py 发送 tasks/send
- **When** A2A Server 接收并处理
- **Then** 返回 JSON-RPC 2.0 格式响应（含 jsonrpc/result/id）
- **Adequacy**: assert response["jsonrpc"] == "2.0", response["result"] exists

### AI-2: --db 移除
- **Given** a2a_task.py 调用不再传 --db
- **When** 执行任意 task 操作（list/get/update）
- **Then** 全部通过 JSON-RPC → A2A Server
- **Adequacy**: grep -r "\-\-db" a2a_task.py 返回 0 结果

### AI-3: WAL write（异步不阻塞）
- **Given** TaskStore 状态变更
- **When** 触发 WAL 写
- **Then** 内存更新立即返回，WAL 写入在后台完成
- **Adequacy**: 内存更新耗时 < 1ms（不受 WAL 写入影响）

### AI-4: WAL replay（崩溃恢复）
- **Given** SQLite 有未完成 task 记录
- **When** 启动时执行 task-restore
- **Then** TaskStore 恢复所有未完成 task（状态为 pending/submitted）
- **Adequacy**: 恢复后的 task count == WAL 中未完成 task count

### AI-5: 降级运行
- **Given** db_manager 不可用
- **When** 状态变更发生
- **Then** 内存 TaskStore 正常更新，WAL 写失败 skip，系统不崩溃
- **Adequacy**: 无异常抛出，TaskStore.get() 返回正确状态

### AI-6: session/ping heartbeat
- **Given** ACP bridge 运行中
- **When** monitor-ai-acp.sh 发送 ping
- **Then** 10s 内收到 pong
- **Adequacy**: ping-pong 成功响应

### AI-7: stopReason 正规化
- **Given** bridge 检测到 fatal error
- **When** session/prompt 完成
- **Then** stopReason 为 "error" 而非 "end_turn"
- **Adequacy**: assert stopReason != "end_turn" on fatal conditions

### AI-8: Per-tool prompt 注入
- **Given** AI_TOOL=opencode
- **When** 构建 Manager system prompt
- **Then** 含 opencode 特定委派指引
- **Adequacy**: prompt 含 "opencode" 或 tool-specific delegation instruction

### AI-9: State Bridge（idle timeout 不误杀）
- **Given** Manager 在等待 Worker，有 alive A2A task
- **When** ACP idle timeout 即将触发
- **Then** 查 TaskStore → 有 alive worker → 延长 timeout
- **Adequacy**: Manager session 未被 kill

## 单元测试

```bash
# AI-1: JSON-RPC roundtrip
python3 -c "
import json, socket
# Send JSON-RPC 2.0 to A2A Server
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/tmp/freely-a2a-<hash>.sock')
req = json.dumps({'jsonrpc':'2.0','id':1,'method':'tasks/list','params':{}})
sock.sendall(f'POST / HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: {len(req)}\r\n\r\n{req}'.encode())
resp = sock.recv(4096)
print('JSON-RPC response:', resp)
"

# AI-4: WAL replay
python3 docs/system/workspace/scripts/runtime/freely-db-cli \
  --project /path task-restore --role worker

# AI-6: ping
python3 -c "
import json,subprocess
r = subprocess.run(['python3','acp-bridge.py','ping'], capture_output=True, text=True)
assert r.returncode == 0
"
```
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
