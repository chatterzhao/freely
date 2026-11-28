## 0. 设计意图审计
### B0 前置：关键词广搜 + 多文档交叉
- 关键词族：`closing ... PRs via platform-adapter` / `close-pr` → `scripts/worktree/pr-merge-guarded:490-508`、`scripts/sync/platform-adapter.py:1540,2017`；`configured_platforms` → `platform-adapter.py:916`；`unknown: origin` → raw 正文与 R59 merge 回执。
- 怀疑多份文档：是。adapter 真源在 platform-adapter.py；shell 侧收尾循环是历史实现；不能只读 raw 原文。
- 三类分层：当前生效实现 = adapter `configured_platforms()` + `_handler_for()`；历史局部文档 = pr-merge 的 `git remote` 循环；权威恢复点 = raw-20261103T063354Z 的根因描述 + 两次 merge 实证。
- 矛盾清单：`git remote` 名（github/origin/all）与 adapter 平台名（github/gitee）不是同一概念；现有循环把二者混用。
- 二元决策：继续——改收尾循环用 adapter 暴露的配置平台名。
### 外部锚点（引用原文）
- 既有门禁源码: `platform-adapter.close_pr()`「unknown: {platform}」只对未配置平台返回。
- 既有同类实现: `platform-adapter.configured_platforms()` 是唯一配置来源。
- 实证: R59 merge `8c55a9e09`、#4749 merge `a1a0281` 均输出 `{"status":"error","error":"unknown: origin"}`。
- 判定：实现偏差（概念混用），不是 adapter 设计错误。
- 影响面：pr-merge 收尾循环、adapter CLI（新增只读 platform 列表动作）、AT/单测。
## 0.1 四问
Q1 流程能力；Q2 adapter 拥有平台身份判定，shell 只消费；Q3 不要求额外工位；Q4 门禁需断言传给 adapter 的 platform 属于配置集合。
## 1. 决策
adapter 新增 `configured-platforms` 只读动作；pr-merge 收尾循环改用它，过滤 github，逐平台输出结构化回执，失败给可操作告警。
## 2. Candidate
C-20261103T063354Z-A promoted → M-20261103T063354Z-A。
