---
b1_id: B1-20261102T130603Z
phase_state: completed
source_raw: raw-20261102T130603Z
source_url: https://github.com/chatterzhao/freely/issues/4125
produced_candidate: C-20261102T130603Z-A
created_at: 2026-11-03
---

# B1_IBM: 平台 handler 探活依赖网络且无 None 守卫

## Input
- raw-20261102T130603Z（GitHub #4125 / Gitee IKSF6N）
- 现象：PR 创建/更新入口推送 review 提交时报 `AttributeError: 'NoneType' object has no attribute 'push_branch'`；重跑一次即成功。
- 根因：`_handler_for(platform)` 每次都执行 `h.detect()`（GitHub detect = 一次 `gh repo view` 网络调用，本机约 1.1s，抖动时 3/10 失败）；失败返回 None。`guarded_pr_update` 在 plan 阶段与 execute 阶段各取一次 handler，execute 阶段若抖动则直接解引用 None。

## Brainstorm
### Option A: 探活结果进程内记忆 + 探活重试 + execute 阶段结构化失败（选定）
- 成功探活缓存到进程级 dict；失败不缓存（保留恢复机会）。
- 探活走现有 `_retry_read` 有界重试，单次抖动不再判死。
- 执行阶段新增 `_ensure_handler`：None 时返回 `{'status':'error','stage':'execute','error':'platform handler unavailable: <name>'}`，调用方转成平台级 error，不再抛异常。
- 优点：一次 PR 流程内零重复网络开销；失败可恢复且错误可执行；改动集中在 adapter。

### Option B: 只看平台配置（`configured_platforms`）不探活
- 否决：配置存在不等于凭据/网络可用；会把"不可用"误判成"可用"，失败后移到更晚的 push 阶段。

### Option C: 调用方各自重试
- 否决：`_handler_for` 被 18 处消费，重试与错误语义会重复漂移；应收敛在探活入口。

## Decision: Option A
- 探活是高成本、可抖动的网络动作 → 缓存成功结果；执行阶段必须 fail-closed 为结构化 error。
- 不改 `configured_platforms()` 语义，不改平台注册表。

## 边界
- 只改 platform-adapter 的 handler 探活/执行守卫；不改各平台 handler 自身逻辑。
- 不改变 PR 流程 gate 语义；失败仍然阻断，只是错误形态可执行。

## Candidate
- candidate_id: C-20261102T130603Z-A
- status: promoted
- milestone: M-20261102T130603Z-A
