# Brainstorms: 降级 pull 后 create 重复建 raw 副本致 identity ambiguous

- raw_key: 20261108T092758Z
- GitHub: #4225 / Gitee: IKTR2N
- workflow_kind: fix
- 来源：R14 收口时自举发现（本轮亲历、直接阻断过 PR/收口），P1

## 问题复述
R6(#4182) 的降级 pull 只把可读平台写入本地 `platform_ids` 并记 sync-debt。随后 `bin/raw-issue-pull:130-134` 无条件调 `issue-sync create <local_id>` 做标题归一化，而 `cmd_create` 用 `_already_on_platform()`（只读本地 `platform_ids`，`bin/issue-sync:181`）判断平台是否已有副本 → 把「本地缺 id」误判成「平台无副本」→ 新建重复副本。同一平台出现 2 条 `[RAW-key]` canonical-title 副本后，`_resolve_raw_identity` 返回 `ambiguous`（`platform-adapter.py:875`），`raw-reconciliation-gate` 直接 block。另一面：`issue-sync close` 的 strict `close_platforms` 用同一份 partial `platform_ids` 组 `close-multi`，只关已登记平台，另一个平台残留 open。

## 现场证据（R14 真实发生）
- `wt-create --source-platform gitee`（GitHub 当时 `search_unreadable`）→ 物化 `platform_ids` 只有 gitee IKSPQ7。
- GitHub 恢复后重跑 `raw-issue-pull` → `issue-sync create` 输出 `[issue-sync] GitHub: creating issue... #4224`，真实 #4152 早已存在。
- `raw-reconciliation-gate --require-local` → `ok:false / decision:block / [ambiguous] 2 canonical title matches`。
- GitHub `search_raw_issue` 用 `--state all`（`:315`），**仅 close #4224 不解 ambiguous**（实测），只能删除重复副本恢复 `ok:true/allow`（封装 `bin/issue-sync-bootstrap --delete`）。
- `discover-raw` 在 GitHub 恢复后返回 `{github:{status:ok,issue_id:4152,url:...}, gitee:{status:ok,...}}` —— 平台侧事实一直可得，缺的是 create/close 没有去问。

## 被否决 / 收窄的方案（证伪，不写成 candidate）
1. **在 `platform-adapter.py search_raw_issue` 里收窄 `--state all` / 减分页 / 改 title-only**：R1 已明令证伪（Gitee 无服务端 raw-key 搜索、必须全量分页枚举；`--limit 20`/20 页服务于 ambiguous 判定），且会让 closed 副本漏检、破坏 identity resolution → 本轮绝不动搜索层。
2. **发现 ambiguous 时自动删重复副本**：删库是不可逆动作，且无法证明哪条是「错的」；应由人工/收口判定，不自动化。
3. **改 `raw-issue-pull` 让 partial(rc3) 不调 create**：能挡住 R14 那条触发链，但 `issue-sync create` 仍是「直接运行 / wt-create 恢复 / 手动调用」时的裸缺陷；合同问题在 create 自身（信任缓存），应在 create 修，pull 只作为顺带减噪（本轮不夹带，记入 revisit）。
4. **每次 create 都无条件 discover-raw**：会在健康路径（platform_ids 已含全部平台）增加一个平台往返，违反「健康路径零语义变化」。收窄为：仅当某配置平台本地缺 id 时才查询。
5. **`present` 时改走 update 做标题归一化**：issue 方案 1 提到，但本轮聚焦「不重复建单」；标题达标已由 Q2 `_platform_title()` / R2 H1 保证，update 会扩大改动面，不做。

## Related findings（已被现有 open issue 覆盖，不新建/不夹带）
- #4166（双平台同步入口收敛）、#4154（契约常量多副本）是相邻重构，但不含「create 按平台侧发现做幂等」这一具体正确性缺陷，见 candidates 证伪段。
- `issue-sync close` 的 0/3/1 退出码、四段式（R12/#4184）保持不动；本轮只在 strict close 前补一次「平台侧发现回填」，不改 close_platforms 真源。
- 2 条 linked `I-*` 平台残留（R13/R13.5 promote 产生）是另一收口问题，归队列收尾判定，非本缺陷。

## 决策
单一 promoted candidate：以 `platform-adapter.discover_raw_replicas` 的平台侧事实为身份判定源，`replica_guard.py` 做纯判定，`issue-sync` 的 create（幂等/失败关闭）与 close（回填）共用。健康路径零 I/O、零行为变化。见 candidates.md。
