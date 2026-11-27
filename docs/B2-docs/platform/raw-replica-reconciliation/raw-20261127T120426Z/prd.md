# PRD: raw-20261127T120426Z
## Goal
用唯一封装入口清理平台侧重复评论，保持平台写审计与副本对账可信。
## 实现方案
`issue-sync` 新增 `comment-delete` 动作；adapter 新增 `delete_comment()` 与两平台 handler 方法；Gitee CLI 新增 `delete-comment` 子命令；显式 platform/comment-id、本地映射校验、失败透传。
## Dev-Loop Handoff
RED 1/14 → GREEN 15/0；runtime unit 覆盖三处契约。
