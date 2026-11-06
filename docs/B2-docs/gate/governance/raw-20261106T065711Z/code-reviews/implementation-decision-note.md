# Implementation Decision Note
- issue_id: I-20261106T065711Z-A
- decision: 只做两项零语义变化性能优化，用单一真源 `RepoView` 与 `comment-resolution-scan.py` 去掉本地 N+1 子进程
- why_this: 实测 `pr-create-guarded` 347s 中 243s 是本地进程扇出（Step 2e 188s + governance-merge-gate 55s），而该门禁在 pre-commit / pre-push / pre-merge-commit / pr-create / pr-merge 都会跑，一条 issue 链路累计浪费 5–7 分钟；1000 轮自动化下这是首要杠杆。用户明确要求「功能逻辑不要误修改，比如精确搜索是否真的符合需求」，因此只改执行方式，不改任何判定规则。
- alternatives_considered: title-only 精确搜索（证伪：GitHub 已分别 in:title/in:body 两次搜索，Gitee 无服务端搜索需全量分页，803/803 body 含 local_id，截断会破坏 ambiguous 判定）；削减 `_retry_read` 重试（削弱 fail-closed）；跨写操作缓存 remote head（读到陈旧值）；一次性预读所有路径（canonical_issue_path 运行时解析，无法预枚举）；把优化与 Q2 标题达标逻辑合并（越界且易退化）；放宽性能阈值掩盖 I/O 环境开销（改为分离测量算法与 I/O）。
- boundary_non_goals: 不改 `search_raw_issue` 搜索字段 / `--state all` / 分页 / `--limit 20` / 客户端二次校验；不改 `_retry_read` 3 次重试与 fail-closed；不跨写操作缓存 remote head；不改 staged > range > disk 视图优先级与 `FileNotFoundError` 文案；不改 `issue-sync` / `pull_raw_issue` 标题达标逻辑与门禁判定规则。
- residual_risk: ①本机 IDE `brokered-bin` shim 使每次 `open()` 约 4.4ms，804 份文件完整扫描仍需 3.487s（相对 188s 为 53.9×）；若未来语料再增一个数量级，可考虑按内容哈希或 mmap 做增量扫描，但那会引入状态，需另立 issue。②`RepoView` 的长驻进程只在非 blob 响应时重建；真实治理文档全是 blob，回退路径未被触发，但已在 unit 测试中覆盖 header 解析与缺失 spec。③双平台串行 fetch、重复 fetch develop、`discover_raw_replicas` 全量分页枚举仍有 20–45s 网络开销，因绑定 fail-closed 语义未纳入本 issue。
- verification: AT-001 RED → GREEN（11 项检查）；6 种 gate 调用模式 verdict byte-identical；4,363 份真实治理文档 × 2 函数 × 双视图 0 差异；build_issue_index git 子进程 3423 → 8；7 个相关回归测试基线对比 0 新增失败；`bin/check-epics-map` 对齐。
- self_bootstrap_findings: 3 个 `test-merge-guarded*` 与另外 4 个门禁测试在 develop 基线同码失败，属「测试与实现漂移 / 测试永久无人执行」家族，已被 #4151 覆盖，未重复创建 raw issue；证据见 B1 brainstorms §Related findings 与 AT-001-GREEN.log。
