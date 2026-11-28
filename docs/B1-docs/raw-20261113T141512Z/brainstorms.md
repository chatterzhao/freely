## 0. 设计意图审计
### B0 前置广搜
- 关键词族：`agent_working empty — fail-closed` → `runtime/freely:4537`；`owner-lane claim skipped` → `owner_lane.py:127`；`Changed issues since last sync` → `bin/issue-sync.d/cmd-scan.sh`；`_already_on_platform` → `lib-state.sh`（#4699 已改平台判据）。
- 三类分层：当前生效实现 = `load_config()` 的 agent-table 解析 + `_already_on_platform` 平台取证；历史局部文档 = raw 对 scan 的原始描述（写于 #4699 之前）；权威恢复点 = #4699/#4707 的副本对账设计。
- 矛盾清单：raw 说 scan 把 never 当变更；当前 `_already_on_platform` 已按平台判定，raw 现象在 raw 分支部分过时。需实证区分。
- 二元决策：继续——修 status 只读视图；scan 部分先实证，只修仍存在的缺陷。
### 外部锚点
- `runtime/freely:4535-4538`：空 agent_working 直接 `return 1`。
- `owner_lane.py:127`：`rows_unreadable` 是 claim 能力，不是只读视图判据。
- #4699 实证：`_already_on_platform` 改按平台判定，scan 的 raw CREATE 噪声已消除。
- 判定：实现偏差（只读视图误用写入路径的 fail-closed 策略）。
- 影响面：status/live/fleet/baseline 四个只读入口；不改写入/委派路径的 fail-closed。
## 0.1 四问
Q1 只读视图语义；Q2 与 owner-lane/agent-table 共享身份判据，但只读面不拥有最终身份判定；Q3 不为只读新增工位；Q4 AT 断言空表 rc=0 且输出 issue 段，真读失败仍 fail-closed。
## 1. 决策
引入只读视图标记：status 系列入口在 load_config 前声明；load_config 在空 agent_working 时降级为 info，不改写入路径。scan 以 #4699 平台判据为准，补负向控制 AT。
