---
b1_id: B1-20261101T124657Z
phase_state: completed
source_raw: raw-20261101T124657Z
created_at: 2026-11-01
---

# B1_IBM: dsh-freely issue→PR E2E slice

## Input

successor raw #4115（GitHub #4115 / Gitee IKS3AV）。父 P1 已 merge：`packaging/dsh-freely` bundle/preset/白名单/bridge。父 raw 明确把完整 issue→PR 留到这里。

## Problem

P1 只证明插件能加载、建 Manager session、bridge 可调；没有证明 Manager→Worker→Reviewer→gate→PR 的完整链路。需要一条可重复、可判定的 E2E，不依赖模型自由发挥。

## Discovery

- 父 P1 已合并，`freely-manager/worker/reviewer` preset 与工具白名单可用。
- Worker session 曾在 `/tmp/freely-e2e` 真写 DONE.txt 并 commit `fa9c06e`。
- Reviewer session 可创建但未跑 verdict。
- ACP bridge 不可用；不能用 ACP reviewer，改为 DSH session 内 Reviewer + 独立人工/子 agent verdict。
- 真实平台 PR 用本 slice 自己的 Freely PR，不伪造 test repo PR。

## Decision

- 做确定性 E2E driver：Manager 由 P1 插件创建；driver 用同一 `createRoleSession` 派 Worker/Reviewer；Worker 在临时 git repo commit；Reviewer 读 diff 给 verdict；driver 跑 `pretests-gate`；结果写 JSON。
- 不做模型自由编排、不引入第二套 Router/Ticket。
- E2E 的“PR”是本 slice 的 Freely PR #（真实平台），不是临时 repo 假 PR。

## Candidate

`C-20261101T124657Z-A` → `I-20261101T124657Z-A`；milestone `M-20261101T124657Z-A`。
