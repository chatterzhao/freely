## 0. 设计意图审计（先于方案）
### 广搜与分层
- 关键词：delete-branch / repo_path_branch / Gitee API v5 / git/refs。命中 `runtime/gitee-issue.py:164,174`、`wt-close` 的 fallback 路径、raw #4137 现场记录。
- 当前生效：`repo_path_branch()` 仍构造 GitHub 风格 ref 路径；fallback `git push --delete` 掩盖失败。
- 历史记录 #4136/#4137 曾按「同簇 4149」归档，但 triage 复核证明 4149 未覆盖该函数。
### 外部锚点
- Gitee API v5 分支删除端点：`DELETE /repos/{owner}/{repo}/branches/{branch}`。
- raw #4137 实证：4/4 分支 404，fallback 成功。
### 判定
**实现偏差（bug）**：端点构造错误，不是设计问题。
### 冲突 / 影响面
无门禁冲突；只改 `repo_path_branch()` 与 AT。
## 0.1 四问
Q1 平台适配 bug；Q2 与 wt-close 的 fallback 共享职责但 fallback 保留；Q3 不要求额外工位；Q4 门禁测 API 路径，AT 直接断言路径。
## 1. 决策
改为 Gitee canonical 分支端点；AT 断言无 git-ref 残留、DELETE 路径/鉴权/回执正确。
