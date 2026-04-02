# Runtime Status Time Display Audit

- 日期：2026-04-02 03:08 UTC

## 背景

- 前一轮已经把 frontend probe Recent Activity、`freely ai`、watchdog 的 human-readable cooldown 时间统一到了宿主系统时区渲染。
- 但仓库里仍有 `freely` runtime 的 status surfaces 直接把 ISO/UTC 真相值回显给人看，造成同一产品内显示层时间风格继续分裂。

## 这轮审计聚焦什么

- 只看“面向人读”的 runtime / CLI 状态输出。
- 不改事件真相、持久化时间、备份命名。
- 不把 doc loop / progress / pre-brainstorm 里的治理时间戳误当成 UI 本地化目标。

## 当前发现的展示层遗留

### 1. `freely live-status` 仍直接回显 intake `created_at`

- `docs/system/workspace/scripts/runtime/freely` 的 `intake_snapshot_for_project()` 读取 `CREATED_AT` 后直接输出 `created_at=<iso-z>`。
- 这是给人看的状态摘要，不是机器真相面；继续裸回显 UTC 会和 frontend/ai/watchdog 的本地渲染冲突。

### 2. `freely live-status` / `fleet-status` 仍直接回显 runtime state 更新时间

- `last_state_updated_at`
- `develop_push_followthrough_defer_updated_at`

这些字段都出现在 status surface 中，属于用户理解当前 runtime 新鲜度的展示面。

### 3. `activation_consent_recorded_at` 也属于同类问题

- `freely init`
- `freely baseline-status`
- `freely live-status`

目前共用同一个 helper，但 helper 只是直接打印配置里的原始值，没有做显示层格式化。

## 不应改动的 UTC / 标准化真相面

- `.bak.<YYYYMMDD-HHMMSS>` 备份命名
- RFC3339 / ISO `created_at`、`claimed_at`、`occurredAt` 的落盘值
- epoch cooldown / `reset_at` / manifest timestamp / history filename

## 结论

- 继续沿用上一轮边界：
  - naming truth: UTC
  - storage truth: epoch / RFC3339 / ISO
  - display truth: host system local time with timezone label
- `freely` runtime 需要补一个共享的“ISO/UTC truth -> 本地展示时间” helper，并在所有 status surfaces 复用。
