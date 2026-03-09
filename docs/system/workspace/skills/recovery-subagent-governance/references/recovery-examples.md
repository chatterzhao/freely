# Recovery Examples

## Resume succeeds

- `phase_state=in_dev`
- `runtime_state=resumable`
- `tool/session_id/jsonl_path` 可追溯
- 结论：优先 resume，继续原 `in_dev`

## Restart required

- `phase_state=in_dev`
- 原 session 不可续接
- `progress` 与 `issue` 仍能定位最近上下文
- 结论：写 recovery 留痕后 restart，并把恢复上下文带回 dev-loop

## Do not mark `blocked_*`

- 监控只发现 PID 消失
- AI 尚未留下业务 blocker
- 结论：先恢复定位，不把系统事件直接写成 `blocked_*`
