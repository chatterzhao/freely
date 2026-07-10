---
kind: raw
local_id: raw-20260517T071929Z29Z
priority: P2
source: chat-inbox
created_at: '2026-05-17T07:19:29Z'
title: freely-package 版本号缺少时分，同天多次打包会覆盖
phase_state: absorbed
platform_ids:
  github:
    issue_id: '447'
    url: https://github.com/chatterzhao/freely/issues/447
    synced_at: '2026-05-17T07:19:35Z'
updated_at: '2026-06-17T00:25:16Z'
primary_platform: github
platform_state: closed
absorbed_into: raw-20260710T005219Z---

## 问题

`freely-package --version` 当前格式为 `YYYY.MM.DD-stable`（如 `2026.05.17-stable`），不含小时分钟。同一天多次打包时，后一次会覆盖前一次。

## 期望格式

`YYYY.MM.DD.HHMM-stable`（如 `2026.05.17.2130-stable`），精确到分钟。

## 范围

`bin/freely-package`：版本号生成逻辑 + usage 示例。
