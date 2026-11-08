# Implementation Decision Note
- issue_id: I-20261108T134853Z-A
- decision: `GitHubHandler` 只在 `gh issue create` 报 label-not-found 时调用 `ensure_github_labels()` 补齐缺失标签并重试一次；错误判定必须同时含 `not found` 与 `label`；其他错误原样返回
- why_this: R15 让 feedback 传 `severity/Pn` 标签，但 GitHub 仓库从未预置 severity 标签，`gh issue create --label` 不会自动建标签 → 整单失败、feedback PARTIAL、raw 只剩 Gitee 副本，直接阻塞自举立项。真机证据：13:47Z 的 `could not add label: 'severity/P2' not found`。
- alternatives_considered: ①建单后用 `gh issue edit --add-label` 补（仍要标签存在，且留半成品单）；②每次无条件预建标签（健康路径多 N 次 API）；③文档要求人工预建（换机复发）；④在 feedback 层去掉标签重试（会让优先级重新丢失，违反 R15 验收）。
- boundary_non_goals: Gitee handler 不动；R15 severity 数据链、4 参 `create_issue` 与 CLI 第 5 参兼容、平台关闭/更新/评论语义均不改；不补建 `raw-20261108T134701Z` 的 GitHub 副本（见 residual_risk）。
- residual_risk: ①**延后项**：`raw-20261108T134701Z`（本缺陷修复前的 PARTIAL 产物）在 Gitee 有 IKTSRS、GitHub 无单，`test-platform-open-parity.py` 因此在真实工位报 1 项差异。`raw-issue-pull` 只允许在「分支名含该 raw-key」的工位内物化，跨轮次补建需另开工位；用户要求本轮后暂停，故排进 v4 队列 **R59**，届时用 `issue-sync create` 补齐。该测试全仓无门禁引用，不阻塞 PR/merge。②失败判定依赖 GitHub CLI 的英文错误文本（`not found` + `label`）；若 gh 改版换措辞可能漏判，revisit 时可改为先 `gh label list` 核对。③`gh label create` 对已存在标签的报错被忽略（幂等），但如果返回的是权限错误也会静默跳过，随后重试仍失败并如实返回 error —— 不会吞错。④标签颜色/描述固定，未按标签族区分。
- verification: AT-001 develop 基线快照 RED `7 ok / 12 failed` → 工位 GREEN `19 ok / 0 failed`；首轮 16 个回归 15 项 MATCH + 1 项已解释的平台状态 DIFF；同轮前置修复后复跑 12 项关键回归全 MATCH；真机：补标签后 `feedback create` 双平台 created（#4230 / IKTSSM）。

- same_round_prerequisites: 本轮 PR 首次 `pr-create-guarded` 被副本一致性门禁挡下（`content_diverged`）：平台副本有 `kind/raw,phase/proposed,severity/p0` 三个标签，而 `lifecycle/raw-reconciliation-gate.py::_local_record` 硬编码 `"labels": []`。这是 R15 标签链在「本地投影」上的第三处遗漏，且**不修就无法创建当前 PR**（鸡生蛋），故按 R13 先例在本轮收口：①`_local_record` 从 frontmatter 推导文档可判定的 `kind/*`（`labels` 字段显式声明时优先）；②`raw_reconciliation.canonical_projection` 对两侧都排除 `phase/*`（创建时快照，平台不随生命周期更新）与 `severity/*`（目前只存在于平台标签，物化不落该字段）——保留 `kind/*` 的真实差异检出能力，并由 AT-001 新增 5 项断言（含「kind/linked 差异仍被检出」的反向守护）。修复后 `raw-reconciliation-gate.py --require-local` 返回 `ok: True / decision: allow`；既有 `test-raw-reconciliation.py`（3 tests）与 `test-raw-replica-degraded.py`（10 tests）全绿。**由此暴露的独立缺口**（物化不落 severity 字段）已按约定用 `feedback` 另立 raw，排进 goal v4（R60），未夹带实现。
- self_bootstrap_findings: 本条即 R16 收口时用 feedback 立项时自举发现（feedback 因自身缺陷 PARTIAL）。同轮还确认「补建标签」只是本机止血，机制修复才是本 PR；未发现其他未被 open issue 覆盖的新缺陷。

## Implementation Decision Note
- decision: label-not-found 后补齐标签 + 有限重试，健康路径零开销
- why_this: 缺 severity 标签让所有 feedback 在 GitHub 整单失败
- alternatives_considered: 建单后补标签 / 无条件预建 / 人工预建 / feedback 层去标签
- boundary_non_goals: Gitee、severity 链、兼容调用面均不动
- residual_risk: R59 补建副本延后、错误文本依赖、label create 报错被忽略、标签样式固定
