# PRD：角色级 harness 选择（I-D）

## Goal

三角色分别选 harness，校验后原子写 `agent-table.toml`，并让 `harness-status` 按角色输出能力/满足度。

## 设计

### 读取

`RoleHarnessConfig` 从 agent-table 归一化：role/tool/slot/adapter/model/source/capabilities/health。tool 从 slot 前缀推断；adapter 取全局 `AGENT_AI_TOOL_ADAPTER`。

### requirements

| role | 必需 | 可选/降级 |
| --- | --- | --- |
| manager | resume, tools, skills | fork |
| worker | session_new, tools, skills | fork, resume |
| reviewer | resume, tools, skills | fork |

`degraded` 记录 `fork=degraded` 等；`satisfied=false` 当必需能力缺失/unknown。

### validate

- role/tool/slot 必填；slot 必须存在；tool 必须能从 slot 推断。
- binary 必须 ok（strict 时 direct-only 也失败）。
- 必需能力缺失 → fail；degraded 允许但返回 warnings。
- 不改文件。

### apply

- 先 validate；失败不落盘。
- 备份 `agent-table.toml`；只改对应 `{role}_slot`；写后重新读取校验；原子替换。
- 返回 diff、requires_restart、audit_id。
- 运行中 session 不重启。

### CLI

```
harness-select show [--json]
harness-select list --role reviewer
harness-select validate --role reviewer --slot cline-...
harness-select apply --role reviewer --slot cline-...
```

### --role

`harness-status --role` 只输出该角色；未知角色返回 2 + 错误。

## 非目标

- 不做 UI/TUI；不实现 `{role}_adapter`；不改 prompt/session。
- 不做自动重启。

## 验收

- `--role` 过滤正确，未知 role 失败。
- requirements/satisfied/degraded 正确，reviewer fork degraded。
- apply 失败不落盘；成功只改一个 slot；diff/audit 可读。
- 原子写/备份/重读校验。
