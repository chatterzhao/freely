# Implementation Decision Note
- issue_id: I-20261104T082603Z-A
- decision: 关闭路径改为「校验 → 执行 → 回写 → 退出码」四段式；终态校验用纯 `transition` 预演（平台零调用即 fail-closed）；平台关闭统一 0/3/1 记账；非严格路径禁止在任一平台失败时写 `platform_state=closed`
- why_this: 平台关闭不可逆，而旧实现「先关平台、后校验本地契约」使「平台已关、本地未关」成为常态结果，调用方只看到 rc=1；非严格路径又在任一平台失败后无条件自证 `platform_state=closed`，让 batch 扫描永久跳过未同步对象；adapter 两态退出码让「关掉一半」与「一个都没关」不可区分，重试策略无从下手。
- alternatives_considered: ① bash 侧重复实现终态判断（第二份真源，会重犯 #4154）；② 平台关闭失败后伪回滚（issue 重开会留下状态历史，Gitee 还需额外 API）；③ 非终态也允许关闭并只把退出码改 3（把不可判变可判，但仍会关掉不该关的对象）；④ 顺手把 `update-issue`/`comment` 通道也改成 0/3/1（属 #4166，扩大回归面）。
- boundary_non_goals: 不改 `create`/`update`/`comment` 通道与读通道；不改 `pr-merge-guarded` 与 `.githooks/`；不改 `wt-close`（其 `if cmd; then` 语义下 3 与 1 都走 else 分支，行为不变）；不动 `search_raw_issue` 身份解析。
- residual_risk: ①真实平台关闭仍只在测试夹具的 stub 边界外发生；本轮靠「本条 issue 自身 wt-close」做真机执行证据，未额外制造平台写。②`close_platforms` 额外要求「adapter rc=0 时必须逐平台报告 closed」，这是对 adapter 输出契约的收紧；既有 `test-command-lifecycle-raw-metadata.py` 的 stub adapter 已同步为「打印逐平台 JSON」，该改动是契约收紧的必要夹具修正，已在 GREEN 证据与回归对比中记录。③`wt-close` 的 `test-command-lifecycle-wt-close.py` 仍有 1 项预存红（`is ambiguous: 2 matches` 与断言 `uniquely` 文案不符），基线同样失败、非本轮引入，归 #4151 证据链范围。④一旦引入第三平台，`_close_exit_code` 的「全 closed 才 0」语义仍需复核（无平台白名单硬编码，按 configured_platforms 动态记账）。
- verification: AT-001 develop 基线快照（`git archive develop -- bin docs`）RED `SUMMARY: 16 ok, 11 failed` → 工位 GREEN `SUMMARY: 27 ok, 0 failed`；6 个相关回归基线对比退出码全 MATCH（1 项预存红基线一致）。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；关闭路径顺序归本条、entry-level 双平台收口归 #4166、常量收口归 #4154，均证伪后排除。R12.5（test-gate 无 agent 可用写入命令）已在上一轮立项（`raw-20261107T120208Z` / #4216 / IKTNYG），非本轮发现。

## Implementation Decision Note
- decision: 先校验后关平台、关闭记账 0/3/1、非严格路径禁止自证
- why_this: 关闭不可逆，先关后校验让「平台已关本地未关」成为常态，且部分成功被自证为全关
- alternatives_considered: bash 重复终态判断；伪回滚；非终态放行改码；夹带 update/comment 与 #4166 入口收口
- boundary_non_goals: create/update/comment、读通道、pr-merge-guarded、.githooks/、wt-close 均不动
- residual_risk: 真实平台写由本轮 wt-close 闭环；adapter 输出契约收紧（夹具已同步）；wt-close 1 项预存红归 #4151；第三平台需复核全 closed 语义
