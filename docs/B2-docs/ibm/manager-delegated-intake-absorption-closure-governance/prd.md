# PRD

## Goal

让 manager-owned delegated continuation 在成功产出新的 manager continuity 后，能把 intake lifecycle 从 `delegated` 正式收为 `absorbed`，不再让历史 interruption 永久挂在 backlog 元数据里。

## Requirements

1. consumed evidence 与 lifecycle absorbed 必须分层：
   - prompt consumed 继续由 session-state / live-status 表示
   - lifecycle closure 由 intake `meta.env` 表示
2. 只有成功 continuity round 才能关闭 lifecycle。
3. 失败轮必须保留 delegated，供 recovery / reentry 使用。
4. closure 后的 linked artifact / absorption target 必须回指真实 manager continuity / followthrough artifact。

## Non-Goals

- 不改 dispatcher 只处理 `new` 的设计
- 不扩到 worker-side lifecycle closure
- 不新增复杂 intake schema
