# B1 Brainstorm — raw-20261113T084729Z

## 0. 立项来源：用户强约束

「linked 到底要怎么管理要看项目的设计意图。实现必须符合整体项目的意图。不要冲突，不要矛盾，不要能力降级。」
「出现门禁问题，千万不要第一时间想着绕过……千万不能改错门禁。」

本轮恢复被 R33.8 降级的 linked 收口门禁，并收敛到项目设计的单一驱动路径；不改任何既有门禁强度。

## 1. 设计意图（已核实项目自身源码）

1. `bin/issue-sync` 头注释的 Issue model / Lifecycle：
   `raw-* kind: raw`（B1 输入）、`I-* kind: linked`（B2 输入）；
   `chat → raw proposed → B1 promotion_started (1:N children) → promotion_finalized (absorbed/open) → configured-platform close (absorbed/closed)`。
2. `bin/issue-sync.d/cmd-batch.sh` 的 `linked)` 分支是 linked 收口的**驱动者**：
   - 跳过条件 `_fm_get platform_state == closed`；
   - `cmd_update` 后仅当 `phase == completed` 才执行收口；
   - 前置还有 `_changed_since_last_sync`（内容 hash 变化）。
   即：**linked 的收口是状态驱动、由 batch 统一执行**，不是人或 AI 逐条 `close`。
3. `cmd_close` 的 strict raw effect（`_raw_effect close-platforms`）在 Phase 1 用 `raw_metadata_contract.transition(..., "platform_closed")` 做本地严格校验，非终态一律拒绝且**零平台写入**。这是门禁强度的基线。
4. `promote-finalize` 只调 `cmd_close "$raw_id"`（raw），与 linked 无关。

## 2. R33.8 实现的三处偏离（本轮要修）

1. **门禁被绕过**：`cmd-close.sh` 按 kind 分派，把 linked 交给新增的 `close-linked` effect；该 effect 只校验 `kind == linked` 与 `platform_ids` 非空，**完全没有 `phase_state` 判据**。结果 `in_dev` / `proposed` 的 linked 也能被关单，等价于把 batch 的完成门禁摘掉。
2. **第二通道与 batch 冲突**：AI 直接执行 `issue-sync close <I-id>`，绕开 `_changed_since_last_sync` 与 batch 驱动；CLI 与 batch 形成两套收口路径，判据必然漂移。
3. **第二套状态语义**：`close-linked` 回写 `status: closed`，而 batch 的判据是 `phase_state`、跳过判据是 `platform_state`。关闭后 batch 仍会把该文档视为未收口项重复处理，属自相矛盾。

## 3. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | `cmd_close` 拒绝 linked 并指向 `issue-sync batch`；batch 改用专用 `cmd_close_linked`；`close_linked` 补 `phase_state == completed` + B2 证据路径 + 双平台 id 的 Phase 1 严格校验（零平台写入）；成功后回写 `phase_state`/`platform_state` | 单一驱动路径 + 等价强度门禁，符合设计意图 ✅ |
| B | 保留 `cmd_close` 直连，只给 `close-linked` 加 phase 校验 | 仍有两套驱动路径，与 batch 语义冲突 |
| C | 放宽 raw 的 `validate()` 以兼容 linked | **改错门禁**，禁止 |
| D | 维持现状，靠人工约定「只在 completed 时 close」 | 门禁不落地，等价于能力降级 |

## 4. 能力不降级核对

- linked 依然可以关闭（由 batch 驱动），只是必须 `phase_state: completed` 且 B2 证据齐全；
- raw 的 `close-platforms` 严格契约一行未改；
- `promote-finalize` / `issue-sync create|update|comment` 不受影响；
- 不删 `issue-sync batch` 的 linked 分支，不改 `_changed_since_last_sync`。

## 5. 证伪

- 「batch 已经能关 linked，R33.8 只是补 CLI」→ 否：batch 调的是 `cmd_close`，R33.8 之前它对 linked 必然失败（strict raw 校验），所以 CLI 不是补充而是**新开的绕过通道**。
- 「phase_state 判据在 batch 里有就够了」→ 否：底层 effect 也必须自带 Phase 1 校验，否则任何调用方（含 batch 自身未来改动）都能绕过；这与 raw 的 `close_platforms` 对称。
- 「status: closed 只是展示字段」→ 否：batch 明确用 `platform_state` 跳过，写 `status` 不产生任何收口效果。
