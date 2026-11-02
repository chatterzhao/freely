---
candidate_id: C-20261102T113816Z-A
status: promoted
source_raw: raw-20261102T113816Z
created_at: 2026-11-02
milestone: M-20261102T113816Z-A
---

# Candidates

## C-20261102T113816Z-A: 副本观测三态化（unknown ≠ missing）+ 有界重试 + 可选降级与债账本

- candidate_format_version: v2
- title: 把 raw 副本门禁的读取抖动从“不可用事实”降级为可对账的 unknown
- status: promoted
- decision_reason: 同一 raw 同一内容三次运行结果不同（通过/失败/通过），`gh` 读取实测失败 3/10，原因是出口代理间歇 502。现有 adapter 把 transport 异常直接写成 `status=error`，`reconcile` 又把任何非 `ok` 当阻塞事实，于是网络抖动等价于内容违规。门禁在内容合规时也报红，只会训练操作者重跑到绿，这比放宽门禁更危险。
- next_action: B2 物化 `I-20261102T113816Z-A`；先写 RED 用例证明 unknown 被记成 error、且无重试，再改 adapter 与 reconcile。
- revisit_trigger: 若连续两个里程碑内 `sync-debt` 龄期超过 24h 的条目为 0，且门禁无因读取失败的报红，可复核是否仍需保留 `allow_degraded` 通道。
- acceptance_criteria:
  - `discover_raw_replicas` 对 transport 异常先重试，仍失败记 `status=unknown` 并带 `reason`；`missing` 只在“搜索成功且 0 命中”时出现
  - `reconcile` 默认语义不变（unknown/error 仍阻塞，既有用例全绿）；新增 `allow_degraded` 才放行
  - receipt 提供 `decision`（allow / allow_degraded / block）与 `debt`（platform + reason）
  - `missing` / `ambiguous` / `diverged` 在任何开关下都阻塞
  - 所有平台都读不到（`baseline is None`）时阻塞
  - `wt-create` 以 `allow_degraded` 调用，并把债写入 `.freely/state/sync-debt.json`
- promotion_gate: RED→GREEN + `test-raw-reconciliation.py` 全绿 + `governance-merge-gate --range develop..HEAD` 通过
- open_questions:
  - 债账本的清理入口放在 `issue-sync reconcile` 还是独立 `freely sync-debt`（本轮只做 record/list，对账留给 C-B）
  - `pull_raw_issue`（materialize）是否也应接受 degraded（当前保持严格，因为无本地可核对）
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 `platform-adapter.py:770`（无重试、异常直接 error）、`raw_reconciliation.py`（任何非 ok 即阻塞）、`wt-create:273`（只取退出码）；三次实跑与 10 次 `gh` 探测构成可复现证据
  - verdict: pass
- promoted_issue_id: I-20261102T113816Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/issues/I-20261102T113816Z-A.md
- milestone: M-20261102T113816Z-A
- session_refs: []

## C-20261102T113816Z-B: 平台对账命令（reconcile）+ 债偿还

- candidate_format_version: v2
- title: `issue-sync reconcile <raw-key|--all>`：按账本把缺失/落后的副本补齐并清债
- status: needs_research
- decision_reason: 本轮只把“未知”变成可记账的债，没有偿还入口。没有偿还，债就是新的静默失败。
- next_action: 待 C-A 合并后单独立 raw；先设计幂等语义（missing → create、state 落后 → close/update、内容分歧 → 阻塞不动）。
- revisit_trigger: `sync-debt list` 出现龄期 > 6h 的条目
- acceptance_criteria:
  - 对每个平台只做幂等动作；分歧内容不自动覆盖，只报告
  - 成功偿还后从账本移除，receipt 重新生成
  - 仍为 unknown 的条目保留并累加 attempts
- promotion_gate: 独立 B2 + RED/GREEN
- open_questions:
  - 谁触发：scan 每轮、还是 `freely status` 提示后人工触发
- acceptance_reviews: []
- promoted_issue_id: ''
- promoted_issue_path: ''
- milestone: M-20261102T113816Z-A
- session_refs: []
