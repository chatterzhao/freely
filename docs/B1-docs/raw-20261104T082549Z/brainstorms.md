# Brainstorms: raw-20261104T082549Z

## 问题

`raw-issue-pull` 只接受 `--raw-key` / `--target`，没有平台选择；`pull_raw_issue()` 用 `if not replicas or any(status != "ok")` 要求**所有**已配置平台可读，任一网络抖动即 FATAL，并固定 `platform = next(iter(replicas))`。双平台本应互为备份，实际退化为「任一故障即全停」。

## 覆盖域与 scope

一个独立问题（pull 读源的可用性选择），一个 candidate。改动面 3 个真源：`platform-adapter.py` 的 `pull_raw_issue()` + `pull` CLI 分支、`bin/raw-issue-pull`、`wt-create` 的参数与 `_pull_raw_issue()` 退出码处理；外加新增回归测试。

## 评审中的关键发现（避免造轮子 / 夹带）

1. **sync-debt 机制已存在**：`lifecycle/sync-debt.py`（`record/list/clear`，账本在 `.freely/state/sync-debt.json`），`wt-create` 前置校验已用 `raw-reconciliation-gate --allow-degraded` + `sync-debt.py record --receipt` 记账，并打印「工位创建继续」。因此本轮**复用既有账本**，不新建 ledger、不改账本格式。
2. **前置 gate 与 pull 的职责分工**：`raw_reconciliation.reconcile()` 已判定 `unknown`（不确定性，allow_degraded 时记为 debt）与 `missing`/`diverged`（事实，仍 block）。`pull_raw_issue()` 不应重复做事实判定，只负责「选一个可读的读源」；因此任何非 ok replica 都视为 degraded，物化仍继续。
3. **`platform_ids` 的隐藏地雷**：原实现的字典推导假定每个 replica 都有 `issue_id`；非 ok replica 没有。assignee 认领循环与 title 规范化循环同样遍历全部 replicas。三处都必须只遍历可读副本，否则不是 FATAL 而是 KeyError，且会给本地 frontmatter 写入伪造身份。
4. **stdout 契约**：`wt-create` 用 `result=$(raw-issue-pull ...)` 解析**恰好一个 JSON 文档**。新增的退出码捕获、sync-debt 记账、警告必须全部走 stderr 或临时文件，不能污染 stdout。
5. **退出码 3 必须被 wt-create 当成「继续」**：否则即使 pull 成功物化，工位创建仍会被失败分支拦下，等于没修。这是本轮最容易漏的一环，已用独立隔离仓库端到端验证。

## 不退化边界（逐条评审）

1. **双平台都 ok 时行为逐字等价**：`platform = next(iter(readable))` 保持原 `next(iter(replicas))` 的顺序语义（primary 仍是第一个配置平台 github），`platform_ids` 仍含全部平台，返回字典只多两个字段（`degraded_platforms`/`partial`）。
2. **全部不可读仍 FATAL**：`if not readable: return None` 保留原 fail-closed 语义；既有 `test-raw-replica-degraded.py`（unknown != missing）全 PASS。
3. **显式指定但不可读的平台必须失败**：不能静默回退到另一个平台（用户明确指定读源时，静默换源会掩盖故障）。
4. **R2 物化 H1、Q2 created_at 兼容分支、标题契约、identity 校验**全部不动；只是把三个循环的作用域从 `replicas` 收窄为 `readable`。
5. **不夹带** R7/#4195（读通道失败静默返回空清单，属 `_safe` 与 list 通道）、R11/#4149（平台写通道静默失败）、#4194（打包触发）、#4201（顶层 return）。
6. **issue 修复方案第 4 条的边界**：「平台写（close/update）同样支持按可用平台执行」不在本 PR。理由：①验收标准 4 条全部只覆盖 pull 链路；②写通道改造是 #4149 的独立 scope，夹带会扩大到 `close_issue`/`update_issue`/`close-multi` 多个调用点，风险高；③本 PR 的「部分成功独立退出码 3」已满足验收标准第 4 条。已如实写入 IDN、GREEN 证据与 review verdict 的残余风险。

## 关键设计

- `pull_raw_issue(raw_key, target_dir, preferred_platform="")`：按 `status == "ok"` 过滤出 `readable`，`degraded` 为其余平台列表；显式指定优先且必须可读；默认取 `readable` 第一个。
- 返回 `degraded_platforms` / `partial`；adapter `pull` CLI 在 partial 时 `SystemExit(3)`，失败 `SystemExit(1)`，成功 0。
- `bin/raw-issue-pull` 新增 `--platform`（校验 github|gitee），捕获退出码，partial 时对每个降级平台调用**既有** `sync-debt.py record`，并保留 stdout 单一 JSON 文档。
- `wt-create` 新增 `--source-platform` 透传到 `raw-issue-pull --platform`；`_pull_raw_issue()` 把 3 视为「部分成功继续」，仅 1/其他码失败。

## Related findings（自举评审）

本轮未发现「现有 open issue 未覆盖」的新缺陷。相邻现象（R7/#4195 空清单、R11/#4149 写通道、#4201 顶层 return、#4151 预存红测试）均已覆盖，未重复立项。
