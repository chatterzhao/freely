# PRD: raw-20261127T085009Z
## Goal
让历史单平台 raw 通过显式来源参数开工位，并由封装命令补齐缺失平台副本。
## 实现方案
wt-create 的 replicas 前置校验在 `source_platform` 非空时跳过并打印审计；物化后调用 `issue-sync --project <fix-wt> create raw-<key>`，失败则删除新工位并非零退出。
## Dev-Loop Handoff
RED 5/5 → GREEN 10/0；不改平台 adapter，不改 raw-reconciliation 判据。
