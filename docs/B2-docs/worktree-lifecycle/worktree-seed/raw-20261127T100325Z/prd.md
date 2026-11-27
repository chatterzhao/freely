# PRD: raw-20261127T100325Z
## Goal
保证 shell 失败回执不因全角标点变量边界而掩盖真实平台写失败。
## 实现方案
`wt-create` 回执改 `${raw_key}`；新增 AT 扫描 `$var` 后紧跟全角标点，并以 stub issue-sync rc=1 断言 stderr 无 unbound variable 且有可操作拒绝文本。
## Dev-Loop Handoff
RED 4/2 → GREEN 6/0；不改平台写通道。
