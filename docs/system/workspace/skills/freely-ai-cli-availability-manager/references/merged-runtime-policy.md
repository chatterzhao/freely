# Runtime Policy

## 命名语义

- 顶层执行器：`cc`
- 内部 capability：`codex-cli`

不要把 `codex-cli` 塞进 `tool:model:mode` 三段式。

## 自动批准映射

### Freely `auto`

- Claude:

```text
--permission-mode bypassPermissions
```

- Codex MCP:

```text
approval-policy=never
```

### Freely `step`

- Claude: 默认 permission mode
- Codex MCP:

```text
approval-policy=on-request
```

## `codex` / `codex-reply` 路由

1. 首次进入新任务 / 新 issue / 无 continuity thread
- 调用 `mcp__codex-cli__codex`

2. 同一 issue 持续推进且已有 continuity thread
- 调用 `mcp__codex-cli__codex-reply`

3. 上下文不健康或应轮换
- 再次调用 `mcp__codex-cli__codex`
- 更新记录的 `threadId`

## 需要被 runtime 保存的状态

- `provider_backend`
- `tool_capabilities`
- `capability_continuity.threadId`
