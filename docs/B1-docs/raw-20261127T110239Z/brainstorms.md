## 0. 设计意图审计
### 广搜与分层
- 关键词：comment / issue_comment / promote_finalized / 401。命中 `gitee-issue.py:api_request`、`bin/issue-sync.d/cmd-comment.sh:24-55`、`cmd-promote-finalize.sh:38-54`、`GET /api/v5/repos/zhaoquan/freely`。
- 现状：`cmd_comment` 不检查平台状态；`promote-finalize` 重跑无条件推评论；`api_request` 转发裸 401。
### 外部锚点
- Gitee 仓库设置：`can_comment=true`、`issue_comment=false`（不允许 closed Issue 评论）。
- #4734 现场：正常评论在 close 前 14 秒成功；重试在 close 后被 401 拒绝。
### 判定
**实现不完整**：封装命令缺少状态判据与语义化错误翻译，不是平台 API 错误。
### 冲突 / 影响面
不改平台设置、不删已有评论；改三个封装层与 AT。
## 0.1 四问
Q1 诊断可操作性；Q2 平台写仍由 adapter/CLI 独占；Q3 不要求额外工位；Q4 AT 直接断言错误文本与重跑次数。
## 1. 决策
评论前读 Gitee Issue 状态；closed 时跳过并打印可操作原因；401 语义翻译；`promote-finalize` 用 `last_synced_comment_at` 做重跑幂等。
