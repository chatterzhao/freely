# 预研头脑风暴：slot-switch-lock-startup-governance

## 背景

2026-04-04 在 root `develop` 监督 `freely start --project /Users/zhaoyu/Downloads/code/my-freely/freely` 时，曾经出现启动失败且需要手工删除 `~/.codex/slot-switch.lock` 才能恢复的现场。当前再次复核后，最新失败主因已经不是 live lock，而是 `auth_failure`：

- `~/.codex/slot-switch.lock` 当前不存在
- `.freely/logs/runtime-events.log` 最新两轮 `ai_cycle_finished` 都记录 `slot_switch_reason=auth_failure` 且 `exit_reason=auth_failure`
- `freely live-status --project ...` 当前也不是在报告一个仍然存在的 shared lock

因此，当前 root 失败不是“现在有 lock 卡住”；但 stale shared lock 曾经真实阻塞过启动，并且目前仍主要依赖操作者手工清理，这说明 `freely start` / `doctor` / status surface 的治理还缺一条更窄的 owner。

## 已确认事实

### 1. 这不是 `C-20260404T154500Z-A` 的同一问题

- `C-20260404T154500Z-A` 关注的是 websocket permission-denied、prompt 可刷新但 intake claim / continuity 不前进的 blocked supervision contract。
- shared slot-switch lock 在那条 lane 里只是叠加信号，不是其主 owner 的边界。
- 若把启动前 stale/active/ambiguous lock 预检继续塞进 `1545`，会把 blocked-intake supervision 和 startup preflight 混层。

### 2. 这也不是 reopen 已完成 owner 的理由

- `I-20260318T163000Z` 已完成，承担的是 global AI account watchdog / manager bootstrap / slot sweep / launch gate 的既有 canonical owner；新缺口应新开 lifecycle，而不是静默回写 completed owner。
- `I-20260327T200600Z-A` 已把 project command semantics 冻结成单独 owner，并明确 shared lock 不应再被 project command 语义层重吸收。

### 3. 底层 launch path 已有一部分 shared lock 保护，但启动治理仍不闭环

当前代码里，`tool-launchers.sh` / `ai-cli` 已具备：

- stale cleanup only when owner pid missing or dead
- live lock bounded wait before launch
- lock acquire / release helpers

但外层仍缺少统一 contract：

- `freely start` 没有把 lock truth 显式作为 startup preflight surface
- `doctor` / `live-status` / `baseline-status` 还没有稳定暴露 current lock truth
- `state.env` 缺失或 race 时，现场仍可能退化成原始 stderr 噪音，例如历史 `sed: .../state.env: No such file or directory`

## 初步边界判断

这条问题最窄且可执行的定义是：

1. `freely start` 在启动前识别 shared codex slot-switch lock 的 `idle` / `active` / `stale` / `ambiguous` 状态
2. 仅在 `owner_pid` 缺失或已死时允许自动清理 stale lock
3. live shared lock 只能 bounded wait / defer / fail clearly，不能 project-local force remove
4. `doctor` / `live-status` / 等价状态面必须暴露结构化 lock truth，而不是只留下 launch stderr
5. `state.env` 缺失、损坏、不可读时必须给出治理化 reason，不能继续裸漏 `sed` 噪音

## 当前判断

这应作为 `source_class=continuation` 下的 `new_candidate_same_family_follow_on` 处理：

- 不 reopen `I-20260318T163000Z`
- 不 reopen `I-20260327T200600Z-A`
- 不并入 `C-20260404T154500Z-A`
- 先在 pre-brainstorm 冻结 owner 边界，再决定是否 materialize 成新的 runtime startup issue

## 后续重开条件

1. 再次在 current `develop` 复现 stale 或 ambiguous shared lock 阻塞 `freely start`
2. `start` / `doctor` / status surface 任一处开始吸收这条 contract，需要升级为正式 issue owner
3. 证明当前 lock truth 已被其他现有 owner 明确吸收，否则不能让这条 candidate 静默消失
