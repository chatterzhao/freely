---
raw_id: raw-20261110T052506Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 来源：本轮自举亲历（不是推测）

R23（#4159）首次 `pr-create-guarded` 耗时 3m40s 后失败，plan 输出只有 `github: {branch_state: error, action: fail_closed}` 与固定文案「同步本地分支与对应平台远端后重试」。逐层实测：`ssh -T git@github-chatterzhao` 3/3 TIMEOUT、`git ls-remote https://github.com/...` rc=128 `CONNECT tunnel failed, response 502`、`gh api user` 正常、`ssh -T git@gitee-zhaoquan` rc=0 1.2s。**重试同一封装命令 1m49s 即成功**（PR #4249 / Gitee #85）。命令逻辑没错，失败信息不可诊断才是缺陷。

## 覆盖域（issue 4 条修复面）

| # | 面 | develop 实测 | 本轮 |
|---|---|---|---|
| 1 | plan 保留逐平台 error 详情 | `pr_lifecycle.py:54` 只写 `branch_state`/`action`，`observations[platform]["error"]`（真实异常）被丢弃 | ✅ 修 |
| 2 | `fetch_branch_head` 加 timeout | `platform-adapter.py:108-121` 三处 `subprocess.run` 均无 timeout；实测 >35s 挂起 | ✅ 修 |
| 3 | recovery 按失败类型分类 | 固定一句「同步本地分支」，对网络故障方向误导 | ✅ 修 |
| 4 | 保持 all-or-nothing / fail-closed | 现状正确 | ✅ 逐字节守住 |

## 方案方向

- **单一真源**：`recovery_for_plan(plan)` 放在 `pr_lifecycle.py`（plan 的语义所有者），adapter 只调用，不再内联字面量。两张文案都定义为常量。
- **error 透传**：`plan_platform_updates()` 把 `observation["error"]` 截断 300 字符后放进 `details[platform]`，与生产侧 `str(exc)[:300]` 的界一致；健康平台不伪造 error。
- **timeout 收敛**：`GIT_FETCH_TIMEOUT_SECS = 30`（与项目既有 `gh issue list` 的 30s 口径一致），三处 git 调用统一走一个 `run_git()` helper；`TimeoutExpired` 归一为带 platform/remote/branch 的 `RuntimeError`，让 plan 拿到可读原因。
- **不改成部分推送**：`blocked_by_aggregate` 保留。一个平台不可读就只推另一个会制造双平台 PR 状态不一致，与 R14.5 副本幂等语义冲突。

## fidelity 基线

- AT-001 必须有对照组在 RED 时 PASS：`classify_branch` 五状态矩阵、`SAFE/BLOCKED` 集合、all-or-nothing 聚合、健康平台不伪造 error、既有 `test-command-lifecycle-pr-update.py` 全绿。
- 零退化用 **8 状态 × 2 平台 = 64 组全矩阵**逐项对比 develop 基线 plan，除新增 `error` 键外必须 0 差异；`aggregate_results` 另跑 9 组。
- 行为断言要真的注入异常与 `TimeoutExpired`，不能只 grep 源码。

## 价值判定

- 不过时：本轮亲历，且每轮 PR 都可能遇平台抖动（R6/R14 已有 GitHub 降级记录）。
- 不重叠：见下方证伪。
- P1：不丢数据，但把分钟级排障变成 1 次重试，属吃狗粮链路高频痛点。

## 被否决

- **平台自动 failover**：单平台不可用时改用另一平台 push → 破坏双平台一致性。
- **自动重试网络调用**：重试策略应由调用方决定；本轮只保证失败可诊断。
- **放宽 fail-closed**：本轮基线 fail-closed 判定是**正确**的，把它改软会引入真实风险。
- **在三处 git 调用各写一个 timeout 字面量**：改成单一常量 + 单一 helper，避免 #4154 同族漂移。
- **顺带修 #4136 的 `unknown: origin` 噪音**：本轮 merge 又复现，但已由既有 issue 覆盖，不夹带。

## 证伪（逐条）

- #4149 / R11（已合并）：`detect()` 四类原因 + `create_issue` 写通道，不涉及 `guarded_pr_update` 的 plan 输出。
- #4157 / R25（open）：8 分项为 watchdog / cycle / append_runtime_event / 日志轮转 / 凭据 / 打包守卫 / Python 版本前置 / .env.example，5 条验收无一条指向 PR plan 的 error 详情或 fetch 超时。
- #4166 / R26（open）：双平台**写入口**收敛与部分成功退出码，作用在 issue 同步写结果，不是分支观测计划。
- #4154 / R24（open）：契约常量与 raw key 多副本，虽含「错误模型 4 套」但未点名 plan 诊断字段丢失；本缺陷可独立修复。
- #4136 / R47（open）：merge 收尾 remote 名当 platform 名，不同函数不同阶段。
- R1（已合并）：只改门禁批量读取与评论扫描，未触碰 `fetch_branch_head` 的 subprocess 超时。
