# PRD: raw-20261124T131119Z
## Goal
提供唯一封装入口关闭 local_id 的全部平台真实副本（含 stale linked 孤儿），保持双平台原子性回执。
## 实现方案
`bin/issue-sync` 新增 `close-orphans` 动作；`cmd-close.sh` 定义 `cmd_close_orphans`，读取 doc 的 platform_ids 作为提示后委托 `platform-adapter.py close-local-id`，原样打印结果并透传 rc；失败输出重试命令。
## Dev-Loop Handoff
RED 2/11 → GREEN 13/0（stub adapter 覆盖 0/3/1）；不改 adapter 与 batch 判据。
