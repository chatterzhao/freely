# 预研头脑风暴：all-tools-unified-slot-contract-governance

## 背景

`I-20260331T184000Z-A` 已经把 Freely 从 `kiro-cli -> codex` 的硬编码桥接推进到 ordered cross-tool fallback，但 current implementation 仍然保留一个根本缺口：

- runtime 把 `AI_TOOL` 当作 current tool truth
- `codex` 有成熟的 same-tool slot watchdog truth
- 其他工具至多参与 weak readiness cross-tool fallback
- `ai-cli login/save/list/switch/whoami/status` 的 slot 真相几乎仍是 codex 专属

这导致 Freely 还没有真正拥有统一状态机：

1. 当前工具不可用时，先在当前工具内部穷尽 slot family
2. 当前工具所有 slot 都不可用后，再按 `AI_FALLBACK_TOOLS` 从最左侧开始进入下一个工具
3. 每进入一个工具，都继续先扫该工具自己的 slot family
4. 所有工具都穷尽后，显式进入 waiting / all-tools-unavailable，并锁定最早恢复的 tool+slot

## 要冻结的新 contract

### 1. 所有工具都必须进入统一 slot 抽象

- `slot` 是 Freely 的统一账户容器，不是某个工具内部实现细节
- 即使某个工具暂时没有成熟多账号切换，也至少应能表示为一个 slot
- canonical inventory 继续放在 `~/.ai-auth/<tool>-<slot>/`

### 2. 当前指针必须统一命名

- `AI_TOOL` 继续承担 current tool persisted truth
- runtime / control-plane 应新增并消费 `current_slot` 真相，而不是继续混用只带历史语气的 `LAST_ACTIVE_SLOT`
- `last_*` 只用于观测历史，不再承担“下一步从哪里继续试”的语义

### 3. 能力矩阵要与 inventory 分开

所有工具都应有 slot inventory，但不能因为目录存在就假装能力等价。至少要区分：

- `slot_inventory`
- `slot_switch`
- `slot_probe`
- `earliest_reset_hint`
- `same_tool_watchdog_recovery`

### 4. 调度顺序必须统一

- current tool 先扫 own slot family
- exhausted 后再按 `AI_FALLBACK_TOOLS` 最左侧进入下一个 tool
- 每个 tool 都先 slot-first，再 tool-fallback
- all-tools-unavailable 时保留 no-launch，并 pin earliest-recovery target

## 非目标

1. 本轮不承诺所有工具立刻拥有和 `codex` 等价的 probe 质量
2. 本轮不把跨工具 resume 语义恢复回来；继续保持 `fresh_with_handoff`
3. 本轮不改动 `tools.md` 的任务路由优先级定位

## 预期 materialization

需要新 owner 单独承接：

- 旧 `I-20260331T184000Z-A` 收窄为 v1：ordered fallback + codex parity
- 新 owner 负责 all-tools unified slot contract、naming truth、generic inventory API、以及 slot-first global scheduler
