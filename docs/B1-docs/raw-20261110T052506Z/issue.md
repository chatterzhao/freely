---
schema_version: '1'
local_id: raw-20261110T052506Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T052506Z-A
platform_ids:
  github:
    issue_id: '4250'
    url: https://github.com/chatterzhao/freely/issues/4250
    synced_at: ''
  gitee:
    issue_id: IKU94N
    url: https://gitee.com/zhaoquan/freely/issues/IKU94N
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/issues/I-20261110T052506Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-10T05:25:06Z'
updated_at: '2026-11-10T05:42:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T052506Z-A
source_candidate: docs/B1-docs/raw-20261110T052506Z/candidates.md
completed_at: '2026-11-10T05:42:36Z'
closeout_note: ''
---

# fix: guarded PR plan 丢失平台失败原因且 fetch 无超时

workflow_kind: fix

workflow_kind: fix

## 现象（2026-11-10 R23 / #4159 收口时亲历）

`./bin/freely pr-create-guarded` Step 3 首次执行耗时 3m40s 后失败，输出：

    "plan": {
      "safe_to_execute": false,
      "platforms": {
        "github": { "branch_state": "error", "action": "fail_closed" },
        "gitee":  { "branch_state": "absent", "action": "blocked_by_aggregate" }
      }
    },
    "recovery": "同步本地分支与对应平台远端后重试；禁止 force push 或原始 push 绕过。"

真实原因是 **GitHub 侧 git 传输通道间歇性故障**（SSH `git@github-chatterzhao` 连续 3 次 ConnectTimeout；HTTPS 经代理返回 `CONNECT tunnel failed, response 502`），而 `gh api user` 同一时刻可用、Gitee SSH 1.2s 正常。按 recovery 文案去「同步本地分支」完全无效；必须人工逐层探测 4 次才定位到网络层。重试同一封装命令后 1m49s 成功（GitHub #4249 / Gitee #85）——命令本身没问题，失败信息不可诊断才是缺陷。

## 根因

1. `docs/system/workspace/scripts/sync/platform-adapter.py:1200-1205`：`fetch_branch_head()` 抛异常时把真实原因写进 `observations[platform]["error"]`（最多 300 字符），但 `plan_platform_updates()`（`scripts/sync/pr_lifecycle.py:36-70`）构造 `details[platform]` 时**只保留 `branch_state` 与 `action`**，error 详情在 plan 输出里被丢弃。上层 `guarded_pr_update` 的失败分支也只回传 `plan` + 固定 `recovery`，不回传 observations。
2. `platform-adapter.py:108-121`：`git fetch` / `git ls-remote` 的 `subprocess.run` **无 timeout**，网络半开时会无界挂起（实测 >35s 未返回），整条 guarded 命令被拖长数分钟。
3. `recovery` 文案对「环境不可用」与「分支分叉」两类完全不同的失败给同一句「同步本地分支后重试」，方向误导。

## 证据

- `pr_lifecycle.py:54` `details[platform] = {"branch_state": state, "action": action}` —— 无 error 字段。
- `platform-adapter.py:1203` `observations[platform] = {"branch_state": "error", "error": str(exc)[:300]}` —— 详情确实存在，只是在 plan 里被丢掉。
- 本轮现场：`ssh -T git@github-chatterzhao` 3/3 TIMEOUT，`git ls-remote https://github.com/...` rc=128 `CONNECT tunnel failed, response 502`，`gh api user` 返回 `chatterzhao`，`ssh -T git@gitee-zhaoquan` rc=0 1.2s。
- 与 #4136 不同：本轮 `pr-merge-guarded` 收尾仍打印 `{"status": "error", "error": "unknown: origin"}`（remote 名当 platform 名），该噪音已被 **#4136 / R47** 覆盖，本 issue 不重复处理。

## 影响

- 每轮 PR 遇到平台抖动时，运维只能看到 `branch_state: error`，无法区分「网络超时 / 认证失效 / 权限不足 / 远端不存在」，排障成本高且容易被误导去改分支。
- 无 timeout 让单平台抖动放大成整条命令数分钟挂起，与 R1 已解决的门禁性能问题同族。
- fail-closed 判定本身是**正确的**（本轮重试后完整成功），本 issue 不要求放宽它。

## 修复方案

1. `plan_platform_updates()` 在 `details[platform]` 保留观测中的 `error`（截断后），使 plan 输出自带逐平台失败原因；`guarded_pr_update` 失败分支把 observations 或等价诊断一并回传。
2. `fetch_branch_head()` 的 `git fetch` / `git ls-remote` / `rev-parse` 加显式 timeout（建议沿用项目既有平台调用超时口径），超时归一为「环境不可用」并带 platform + 远端名，不改变 fail-closed 结果。
3. `recovery` 按失败类型分两类文案：`branch_state in {ahead,diverged}` → 同步分支；`error/unsupported` → 探测平台可达性与认证状态后重试，并打印对应探测命令。
4. 保持 all-or-nothing 聚合：**不得**改成「一个平台失败就只推另一个」，那会制造双平台 PR 状态不一致，与 R14.5 的副本幂等语义冲突。

## 验收标准

- RED：注入一个 `fetch_branch_head` 抛 `RuntimeError("ssh: connect timed out")` 的夹具跑 plan，断言输出中**不含**该原因、`recovery` 仍指向同步分支（当前行为）。
- RED：注入一个永不返回的 fetch 子进程，断言 guarded plan 在时限内返回「环境不可用」而不是挂起（当前无 timeout）。
- GREEN：同一夹具输出中每个失败平台都带 `error` 且含原始原因摘要；`recovery` 为环境类文案并含探测命令。
- GREEN：`ahead`/`diverged` 夹具的 recovery 仍是分支同步类文案；`safe_to_execute=false` 与 `actions=[]` 保持不变；现有 `test-command-lifecycle-pr-update.py` 全绿。
- GREEN：真机重跑一次 `pr-create-guarded` 健康路径，双平台仍 created/reused。

## 不退化边界

- 不改 `classify_branch()` 的五种状态判定，不改 `SAFE_BRANCH_STATES` / `BLOCKED_BRANCH_STATES` 集合。
- 不改 all-or-nothing 聚合（`blocked_by_aggregate` 保留），不引入单平台部分推送。
- 不改 `push_branch` / `ensure_pr` 的成功路径与重试语义。
- 不放宽任何 fail-closed 判定；只增加诊断信息与超时守卫。
- 不把 timeout 值写死在多个调用点，抽成单一常量（#4154 契约收口时登记）。

## 明确不纳入

- 平台自动 failover（单平台不可用时改用另一平台 push）——会破坏 PR 双平台一致性。
- 自动重试网络调用——重试策略应由调用方决定，本 issue 只保证失败可诊断。
- 修 #4136 的 `unknown: origin` 噪音——已由既有 issue 覆盖。
- 修 `gh api` 与 git 传输通道的代理差异——属本机网络环境，不是 Freely 代码。

## 证伪（现有 open / 已合并 issue 均不覆盖）

- **#4149 / R11（已合并）**：修 `detect()` 四类原因与 `create_issue` 写通道，作用在 issue 创建路径，不涉及 `guarded_pr_update` 的 plan 阶段输出。
- **#4157 / R25（open）**：8 条分项是 watchdog、cycle、append_runtime_event、日志轮转、凭据、打包守卫、Python 版本前置、.env.example；5 条验收标准无一条指向 PR plan 的 error 详情或 fetch 超时。
- **#4166 / R26（open）**：双平台写入口收敛与部分成功退出码，作用在 issue 同步写结果，不是分支观测计划。
- **#4154 / R24（open）**：契约常量与 raw key 多副本收口，虽含「错误模型 4 套」，但未点名 plan 诊断字段丢失，且本缺陷可独立修复。
- **#4136 / R47（open）**：merge 收尾 remote 名当 platform 名，不同函数、不同阶段。
- **R1 性能优化（已合并）**：只改门禁读取与评论扫描，未触碰 `fetch_branch_head` 的 subprocess 超时。
