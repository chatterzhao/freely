## 0. 设计意图审计
### 外部锚点
- #4734 现场：GitHub 三条重复系统评论，Gitee/本地各一条；封装命令只能新增评论。
- `platform-adapter.py` 已有 `add_comment` 与 `delete_issue`，但没有 `delete_comment`。
- Gitee API v5 支持 `DELETE /repos/{owner}/{repo}/issues/comments/{id}`。
### 判定
**实现未完成**：平台写通道缺一个删除评论的封装入口，不是平台 API 缺陷。
### 冲突 / 影响面
不改评论创建、不改平台设置；新增显式命令、adapter 方法与 Gitee CLI 子命令。
## 0.1 四问
Q1 流程能力；Q2 adapter 仍是唯一平台写者；Q3 不要求额外工位；Q4 AT 直接断言身份校验与失败透传。
## 1. 决策
新增 `issue-sync comment-delete <local_id> <platform> <comment_id>`；显式平台、数字评论 ID、本地映射校验后才写；逐平台回执与可操作重试。
