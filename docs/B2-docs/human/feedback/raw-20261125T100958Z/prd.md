# PRD: raw-20261125T100958Z
## Goal
feedback edit 与 wt-create 解耦：缺本地文档时按 raw key 从平台发现 issue ids 并调 adapter update-issue。
## 实现方案
cmd_feedback edit 分支：本地文件存在→既有路径；不存在→`python3 platform-adapter.py search <raw_key>` 解析双平台 issue_number 组装 platform_ids，kind 默认 raw；body 用显式 --body 原样（无 metadata 前缀）；标题走 canonical_raw_title；update-issue 已汇总双平台结果。
## Dev-Loop Handoff
RED：无本地文件场景 rc=1；GREEN：成功且本地无文件。回归既有 edit 兼容。
