# PRD: ACP Bridge 启动链路修复

- issue_id: I-20260704T004227Z-A
- epic: agent-acp
- story: agent-table-driven

## Goal

确保 agent-table.toml 中每个 agent role 配置的 slot 能正确映射到对应的 ACP binary 和模型，消除隐式的 Claude Code 回退和模型错误。

## 现状

```
agent-table.toml
  → opencode-apikey-ds-flash-auto
    → base_tool: opencode
      → tool-registry: acp.binary=opencode, acp.args=acp
        → config.toml: FREELY_ACP_OPENCODE_BIN=/Users/.../opencode/bin/opencode
          ✅ freely _ensure_acp_bridge_running 正确走完整链路
          ❌ monitor-ai-acp.sh _bridge_ensure_running 完全跳过 → 默认 claude-agent-acp
```

两个独立的 bridge 启动路径（freely + monitor-ai-acp.sh）只在 freely 侧正确实现。monitor-ai-acp.sh 侧有 tool name 比较误杀、不传 --acp-bin、不写 .bin 文件三个问题。叠加父进程环境变量污染，导致最终使用了完全错误的 binary 和模型。

## 实现方案

### Phase 1: monitor-ai-acp.sh `_bridge_ensure_running` 对齐 freely

修复 tool name 对比（都提取 base_tool 再比），增加与 `_ensure_acp_bridge_running` 相同的三层 ACP binary 解析，写 `.bin` 文件。

三层回退:
1. tool-registry.toml → `acp.binary` + `acp.args` (如 opencode + acp)
2. .freely/config.toml → `FREELY_ACP_{TOOL}_BIN` (安装路径，优先)
3. command -v / PATH (最后回退)

### Phase 2: 环境变量清理

在两个 bridge 启动函数中，启动前 unset:
- `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`
- `ANTHROPIC_DEFAULT_OPUS/SONNET/HAIKU_MODEL`
- `CLAUDE_CODE_*` (AUTO_COMPACT_WINDOW/ENTRYPOINT/EXECPATH/SESSION_ID/CHILD_SESSION/SUBAGENT_MODEL)
- `AI_AGENT`

保留: `CLAUDE_CODE_PERMISSION_MODE` (由 `ai_cli_tool_with_auth_assemble` 从 slot config 显式提取)

### Phase 3: agent-id grep 精确匹配

`grep -F "$(pwd)"` → `grep -F "$(pwd)="`，利用 agent-id.env 中路径后紧跟 `=` 的特点锚定行尾。

### Phase 4: 诊断日志

| 日志点 | 内容 |
|--------|------|
| bridge 启动 | `base_tool`, `acp_bin` (完整路径), `acp_args`, `slot`, `config_path` |
| env 清理 | 清理变量数 + 类型, 保留的 slot-specific vars |
| session 创建 | `session_id`, `agent_role`, `actual_binary`, `actual_model`, `actual_provider` |

## 设计决策

| 决策 | 理由 |
|------|------|
| monitor-ai-acp.sh 不 source freely，改用 awk 直接读 config.toml | monitor-ai-acp.sh 是独立 subprocess，不能访问 freely 函数 |
| base_tool 对比而非全名对比 | 两边格式不一致 (自由侧写全名，传参传 base)，统一到 base_tool |
| env 清理在 bridge 启动前而非 acp-bridge.py 内部 | 在入口清理，覆盖所有 ACP binary（claude/opencode/codex/cline） |
| .bin 文件存全路径而非 registry 短名 | 全路径更精确，basename 比较仍可用于跨 format 兼容 |
| agent-id grep 加 `=` 而非 `"` 锚定 | agent-id.env 格式是 `path=worker=worker_01`，`=` 是唯一分隔符 |

## Dev-Loop Handoff

- 实现顺序: Fix 1a+1b+1c → Fix 2a+2b → Fix 3 → Fix 4
- 涉及文件: monitor-ai-acp.sh, freely (runtime)
- 不涉及 config 变更，纯代码修改
- 修改完成后用 test cases 验证: test-acp-binary-matches-agent-table-slot, test-acp-bridge-env-sanitization, test-acp-bridge-start-records, test-acp-session-model-matches-config
