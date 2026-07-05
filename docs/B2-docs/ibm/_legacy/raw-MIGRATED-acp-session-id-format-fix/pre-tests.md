# Pre-Tests: ACP Session ID 格式污染修复

## Acceptance Items

### AI-1: run-acp-prompt.py 输出两行一致性
- **Given** `LAUNCH_KIND=prompt` + `resume_target=ses_AAA`
- **When** run-acp-prompt.py 执行 session 管理
- **Then** line 1 = `ses_AAA`（clean ID），line 2 = `session id: ses_AAA (prompt)`
- **Adequacy**: assert `log_file` line 1 equals clean session ID（不含空格/label）

### AI-2: monitor-ai-acp.sh 提取 OpenCode session ID
- **Given** cycle log 含 `session id: ses_AAA (prompt)`（仅一行，模拟 Bug 1 未修复场景）
- **When** monitor-ai-acp.sh 解析 `session_id_clean` / `session_id_out`
- **Then** `session_id_clean = ses_AAA`（label 已被 `%% *` 剥离）
- **Adequacy**: assert `session_id_clean` 不含空格

### AI-3: monitor-ai-acp.sh 提取 Claude Code session ID (UUID v4)
- **Given** cycle log 含 `a1b2c3d4-e5f6-4789-abcd-ef0123456789`（line 1）和 `session id: a1b2c3d4-e5f6-4789-abcd-ef0123456789 (prompt)`（line 2）
- **When** monitor-ai-acp.sh 解析
- **Then** `session_id_clean = a1b2c3d4-e5f6-4789-abcd-ef0123456789`
- **Adequacy**: assert UUID v4 regex 匹配结果不含 label

### AI-4: is_valid_session_id 接受两种格式
- **Given** `is_valid_session_id "ses_12ef4d6cfffeWnAyWb17Uc2RdX"` 和 `is_valid_session_id "a1b2c3d4-e5f6-4789-abcd-ef0123456789"`
- **When** 调用验证
- **Then** 两者均 return 0（有效）
- **Adequacy**: assert 返回值 0

### AI-5: is_valid_uuid 向后兼容
- **Given** 旧的 `is_valid_uuid` 调用（5 处 call site）
- **When** 传入 UUID v4 或 `ses_` 格式
- **Then** 行为与 `is_valid_session_id` 一致（wrapper 委托）
- **Adequacy**: assert `is_valid_uuid` 对 `ses_` 格式返回 0（此前返回 1）

### AI-6: 污染链断裂验证
- **Given** 连续 3 次 `LAUNCH_KIND=prompt` multi-turn cycle
- **When** 观察 `session-state.env` 的 `CLAUDE_SESSION_ID_CURRENT`
- **Then** 不含 `(prompt)` / `(fresh after ...)` 等 label 后缀
- **Adequacy**: assert `CLAUDE_SESSION_ID_CURRENT` 从未包含空格

## Test Execution

这些是 code-review 级别的结构验证，需在 test-pre-merge 工作区通过 shell 测试脚本执行。端到端验证需要启动 daemon 观察 3 次以上 multi-turn cycle。

### 单元级快速验证（可脱离 daemon）

```bash
# Test AI-1: verify run-acp-prompt.py prompt branch
python3 -c "
# Simulate: launch_kind=prompt, resume_target=ses_AAA
session_id = 'ses_12ef4d6cfffeWnAyWb17Uc2RdX'
print(session_id, flush=True)                                     # line 1
print(f'session id: {session_id} (prompt)', flush=True)           # line 2
" > /tmp/test-session-output.txt
# Verify line1 is clean
line1=$(head -1 /tmp/test-session-output.txt)
if echo "$line1" | grep -q ' '; then echo "FAIL: line1 has space"; else echo "PASS: line1 clean"; fi

# Test AI-4: is_valid_session_id
source <(sed -n '/^is_valid_session_id()/,/^}/p' docs/system/workspace/scripts/runtime/freely)
is_valid_session_id "ses_12ef4d6cfffeWnAyWb17Uc2RdX" && echo "PASS: ses_ accepted" || echo "FAIL: ses_ rejected"
is_valid_session_id "a1b2c3d4-e5f6-4789-abcd-ef0123456789" && echo "PASS: UUID v4 accepted" || echo "FAIL: UUID v4 rejected"
is_valid_session_id "ses_AAA (prompt)" && echo "FAIL: contaminated accepted" || echo "PASS: contaminated rejected"
```
