# B1 Brainstorm — raw-20261113T130925Z

## 1. 全局审计结论（详见 goal 2026-11-13 13:35Z 恢复点）

两类 issue 共用 `phase_state` 但两套状态机（raw: proposed/absorbed/dropped；linked: in_b2_ibm/done_b2_ibm/in_dev/blocked_dev/in_verification/completed）。1:N children、一个 raw 一个 worktree 均是**正确设计**。

真正的三处问题：
1. **设计不完整**：`cmd-create` 明确 linked 不声明 `platform_state`，但 `cmd-batch` 的跳过判据和 `wt-close` 的"是否已关"判断都读它 → linked 没有"平台已关"的本地投影，无法幂等判断。
2. **设计分散**：收口职责分给 `batch`（completed + hash 变化）、`wt-close`（completed|dropped + platform_state）、`issue-sync close`（拒绝 linked）三套判据。
3. **实现 bug**：`_changed_since_last_sync` 把状态判据与变更判据混用；`wt-close` 直接调 adapter（越过 issue-sync 的"唯一平台写入口"）；`wt-close` 终态枚举混用 raw 的 `dropped`。

## 2. 目标契约

- **唯一平台写入口**：`issue-sync`（头注释已声明）。
- **唯一收口判据**：linked `phase_state == completed && platform_state != closed`；raw `phase_state ∈ {absorbed, dropped} && platform_state != closed`。关闭幂等。
- **唯一投影字段**：`platform_state` 同时适用于 raw 与 linked（同一语义），不新造第二个名字。
- **入口分工**：`issue-sync batch` 是唯一写者（在工位内跑，写工位文档，随 PR 落到 develop）；`wt-close` 只做**只读的前置检查**（children 终态 + platform_state 全 closed），不写平台、不写文档。

## 3. 为什么 wt-close 改为「只检查」

- `wt-close` Phase 3 的既有注释就是「wt-close performs platform/worktree cleanup only and never writes issue files」——R33.15 让它直接调 adapter 关闭，已经偏离这句设计声明，且不回写 platform_state → 下次判据又认为未关。
- 如果 wt-close 写工位文档，工位删除后变更丢失；写 develop 又会脏。
- 因此正确的收口落盘点是 **merge 前的工位内 batch**：写工位文档 → 随 PR 进 develop → wt-close 只验证。
- 对"遗留且无工位"的 raw，用一个专门的收口工位（本 raw 的工位即第一个）跑 batch 即可。

## 4. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | linked 复用 `platform_state`（create 写 open、close 写 closed）；`batch` 解耦 close 与 hash；`wt-close` 改为只检查 | 单一判据 + 单一写入口，符合既有注释 ✅ |
| B | 给 linked 新增 `closeout_state` 字段 | 同一概念第二个名字，违反「不造第二套语义」 |
| C | 保持 wt-close 直接关 | 越过 issue-sync、不回写投影、判据仍分散 |

## 5. 证伪

- 「linked 不能有 platform_state」→ 否：`cmd-create` 注释是"避免 create 时静默加字段"，不是说该字段对 linked 无意义；raw 与 linked 都是平台 issue，都需要"平台是否已关"。
- 「batch 的 hash 门禁是必要的」→ 只对 `update` 必要（避免刷屏）；对 close 不必要（关闭幂等）。
- 「wt-close 必须自己关」→ 否：它没有 merge 前写文档的时机，回写必丢；让 batch 在 PR 内完成才是落盘点。

## 6. 边界

- 不改 raw 的 `validate()` / `close_platforms`；
- 不改 `cmd_close` 对 linked 的拒绝（直连仍走 batch）；
- 不放宽任何门禁；不手工关平台 issue；
- `scan` / `status` 的读视图问题（C-C）另立 raw。
