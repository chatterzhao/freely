# Brainstorm: supervisor crash batch2 — bash rc=0 假阳性续报

## 背景

第二波 supervisor bash rc=0 crash 报告，与第一波（2026-05-17）完全同模式。

已有根因候选 `C-20260517T083030Z-A` (M-20260517T083030Z-A) 在处理此问题，状态 `needs_research`。

## 本批次 raw issues

| raw key | GitHub # | 时间 | 代码位置 |
|---------|----------|------|---------|
| raw-20260519T011323Z | #598 | 01:13:23Z | freely:18846 |
| raw-20260519T091827Z | #647 | 09:18:27Z | freely:18910 |
| raw-20260519T094157Z | #648 | 09:41:57Z | freely:18923 |
| raw-20260519T102151Z | #651 | 10:21:51Z | freely:18923 |
| raw-20260519T113307Z | #653 | 11:33:07Z | freely:18923 |
| raw-20260519T130500Z | #654 | 13:05:00Z | freely:18894 |
| raw-20260519T145453Z | #656 | 14:54:53Z | freely:18897 |

## 决策

**全部吸收到 `C-20260517T083030Z-A`**。理由：

1. 同模式：bash rc=0（成功退出）被标记为 crash
2. 工具一致：7/7 使用 `oc-acp-ds-flash-auto`（仅最后一个 #656 使用 `cc-ds-flash-auto`）
3. adapter 一致：全部使用 ACP adapter
4. launch_kind 一致：全部是 `resume`
5. 已有 consolidator 在处理 — 第一波已吸收 5 条（#500, #501, #502, #503, #504），此 7 条为续报
6. 不单独创建候选 — 占用 B1 资源不如推动 consolidator 进入 B2

## 后续动作

- 吸收这些 raw issue 后，consolidator C-20260517T083030Z-A 的 scope 更新为覆盖全部 12 条 supervisor bash rc=0 crash
- 推动 C-20260517T083030Z-A 从 `needs_research` 进入 B2（已经吸收了足够多证据）
- 在 milestone 中记录每条 raw 的 absorb 状态
