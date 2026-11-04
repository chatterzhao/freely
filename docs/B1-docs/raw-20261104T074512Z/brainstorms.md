---
b1_id: B1-20261104T074512Z
phase_state: completed
source_raw: raw-20261104T074512Z
source_url: https://github.com/chatterzhao/freely/issues/4158
produced_candidate: C-20261104T074512Z-A
created_at: 2026-11-04
---

# B1_IBM: freely-package --output 无路径守卫，可删除仓库外内容

## Input
- `bin/freely-package:68` 在任何校验前执行 `rm -rf "$OUTPUT"`；`--output` 在 `:46-52` 直接赋值，无路径检查。
- `--output /`、`--output ~`、`--output ..` 会把删除目标指向仓库外。
- `--output ""` 已由 `:57-59` 兜底为默认目录，不构成风险，不作为本 issue 范围。
- 该命令通常由发布流程以较高权限执行，误触概率不低。

## Option A: 仅在文档中提示不要传危险路径（否决）
- 不能阻止误触；CI 与脚本调用方仍可传入任意值。

## Option B: 解析后拒绝危险目标 + 目录白名单（选定）
- 拒绝字面 `/`、`.`、`..`、`$HOME`，以及解析后落在 `/` 或 `$HOME` 的目标。
- 默认要求输出位于 `$HOME/.freely/versions/` 下；外部目录需显式 `FREELY_PACKAGE_ALLOW_OUTSIDE=1`。
- 守卫在 `rm -rf` 之前执行，失败即退出。

## Option C: 交互确认（否决）
- CLI 必须支持非交互模式，交互确认会阻塞自动化调用。

## Decision: Option B
- 边界：不改变默认输出路径、不改变 allowlist、不改变安全路径的打包行为；只增加删除前拒绝。

## Candidate
- candidate_id: C-20261104T074512Z-A；milestone: M-20261104T074512Z-A
