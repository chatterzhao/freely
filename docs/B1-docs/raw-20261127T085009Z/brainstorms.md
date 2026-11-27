## 0. 设计意图审计
### 广搜与分层
- 关键词：source-platform / raw replicas / raw-issue-pull / issue-sync create。命中 `worktree/wt-create:389,1023`、`bin/raw-issue-pull:80`、`commands.md:89`。
- 现状：`--source-platform` 已解析并传给 raw-issue-pull，但全副本前置校验仍无条件执行；R59 现场互锁。
- 历史文档：R16 只交付 install-state 一致性检查，未覆盖单平台 legacy raw。
### 外部锚点
- wt-create 回执：`configured raw replicas are inconsistent or unavailable`（observations 仅 gitee）。
- raw-issue-pull 回执：只能在包含 raw-key 的工位分支执行。
### 判定
**实现未完成**：显式参数已存在但未接入判据；不是设计错误。
### 冲突 / 影响面
无门禁断言冲突；改 wt-create 判据 + 物化后由 issue-sync create 补副本。
## 0.1 四问
Q1 流程能力；Q2 平台写仍由 issue-sync 独占；Q3 不要求额外工位；Q4 门禁失配：一致性前置校验无法表达「显式单平台来源」意图，直接补判据。
## 1. 决策
显式 `--source-platform` 跳过全副本前置校验并打印审计说明；物化后调用 `issue-sync create` 补齐缺失副本，失败即拒绝创建工位。
