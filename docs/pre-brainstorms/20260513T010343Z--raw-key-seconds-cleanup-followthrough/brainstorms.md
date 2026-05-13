# 研究：秒级 raw key 格式清理跟进

## 背景

I-20260507T143545Z-A（timestamp-seconds-upgrade）曾宣称完成 `\d{4} → \d{4,6}` 全局替换，
但实际 14 处遗漏（4 处 regex bug + 10+ 处文档）。

本 pre-brainstorm 承接该遗漏，完成全量清理。

## 来源

- GitHub issue: #326
- 前置 issue: I-20260507T143545Z-A（timestamp-seconds-upgrade）
