- issue_id: I-20261102T113816Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/issues/I-20261102T113816Z-A.md

## Implementation Decision Note

- issue: I-20261102T113816Z-A
- candidate: C-20261102T113816Z-A
- decision: accept
- scope: adapter 观测层、reconcile 判定、gate 开关、wt-create 记账、sync-debt 账本
- out_of_scope: 债的偿还（issue-sync reconcile）、materialize 降级、close 语义

### 为什么改

同一 raw、同一内容，gate 三次运行给出 通过/失败/通过；`gh repo view` 连测 10 次失败 3 次（出口代理间歇 502）。原实现把 transport 异常直接写成 `status=error`，`reconcile` 又把任何非 `ok` 当阻塞事实，于是网络抖动等价于内容违规。门禁在内容合规时报红，只会训练操作者重跑到绿——这比放宽门禁更危险。

### 改了什么

1. `discover_raw_replicas`
   - 平台并发读取；每个平台 3 次有界重试，退避 0.5s / 1.5s 并加抖动。
   - 终止性错误（authentication / not found / 404）不重试，避免掩盖真实原因。
   - 只有“搜索成功且 0 命中”才是 `missing`；其余异常一律 `unknown` 并带 `reason`。
2. `reconcile`
   - `unknown` / `error` 进 `degraded`，默认仍阻塞（规范不变）。
   - 新增 `allow_degraded`；放行时输出 `decision=allow_degraded` 与 `debt`。
   - 新增“全平台不可读 → 无 baseline → block”，避免凭一无所知放行。
3. `raw-reconciliation-gate.py`：新增 `--allow-degraded`；gate 仍只读。
4. `sync-debt.py`：`.freely/state/sync-debt.json` 的 record / list / clear；条目含 raw_key、platform、reason、since、last_seen、attempts。
5. `wt-create`：以 `--allow-degraded` 调用；有债时写账本并打印提示，工位继续创建。
6. `worktree-common.sh`：PR / 合并 / 收口共用同一入口，保持严格语义，但对“非事实类失败”最多重试 3 次；判定读 `diagnostics` 数组而不是正文——正文里出现 missing 这个词不代表诊断。

### 对既有断言的处理

`test-raw-reconciliation.py::test_blocks_missing_or_unreachable_configured_replica` 原先断言 `diagnostics[0].code == "error"`。状态名从 `error` 改为 `unknown` 后该断言失效。新断言为：

- `ok is False`
- `decision == "block"`
- `degraded` 精确包含 `gitee`
- `observations` 不含 `gitee`

这是收紧而不是放宽：它同时证明“仍然阻塞”和“未被误当成内容事实”。

### 残余风险

- `allow_degraded` 让 `wt-create` 的严格性下降一格：从“所有配置平台可读”降为“至少一个可读且本地可核对”。补偿手段是账本 + 后续对账；在 C-20261102T113816Z-B（`issue-sync reconcile`）落地前，债只能靠 `sync-debt list` 人工发现。
- 账本在 `.freely/state/`（gitignored），只代表本机视角，不跨机器。
- 重试上限 3 次、退避合计 ≤ 1.65s：代理重启若超过约 3 秒，仍会落到 degraded。

### Reviewer 备注

本改动由作者自审（owner lane，无委派 worker 会话），人工按四层（需求/设计/实现/证据）走查；执行证据见 `verification/test-evidence/`。
