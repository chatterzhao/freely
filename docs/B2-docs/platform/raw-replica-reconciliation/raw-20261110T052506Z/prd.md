# PRD: guarded PR plan 可诊断 + git 传输超时守卫
- issue_id: I-20261110T052506Z-A
- source_raw: raw-20261110T052506Z
- milestone: M-20261110T052506Z-A

## 问题
平台观测失败时，guarded PR 的 plan 丢掉真实异常，只给 `branch_state: error` 与固定「同步分支」文案；`fetch_branch_head` 无 timeout 导致整条命令挂起数分钟。

## 目标
1. 每个失败平台带真实原因（截断 300 字符）。
2. recovery 按「分支分叉」与「环境不可用」分类。
3. 三处 git 调用共用单一超时常量，超时归一为带 platform/remote 的诊断。
4. 不改变 all-or-nothing 聚合、状态判定、fail-closed 结果。

## 非目标
平台自动 failover、自动重试、放宽 fail-closed、修 #4136 噪音。

## 验收
见 verification/pre-tests.md 的 AT-001。
