# Candidates - 20260405-1615--feature-owned-test-pre-merge-family

### C-20260405-1615-A

- candidate_format_version: `v2`
- title: Feature-owned test-pre-merge family promotion model
- problem: 现有 canonical 语义仍允许 `feature/*` 直接 merge 到 `develop`，而 `test-pre-merge-*` 只被当成 shadow batch 和 replay 证据面。这让“每个 feature 先在 develop-like 环境完成预集成测试再进入 develop”无法真正闭环，也让多个待测 feature 只能靠串行污染 `develop` 或反复切 branch 来争用测试环境。
- why_now:
  - 本轮已经明确需要把 `test-pre-merge-*` 提升为真实的 develop 前预集成 lane，而不是可有可无的旁路
  - 用户已明确提出 `develop` 不应再接受直接 `feature/*` promote，否则“忘记测试”会继续成为制度漏洞
  - 多个 feature 并行测试需要独立 worktree 批次，不能再靠单树切换 branch 伪装集成环境
  - 当前 `CONSTITUTION` / `LAWS` / branch-management reference 仍写着 replay-only 旧模型，若不先冻结新设计，后续 hook/gate 修改会失去 issue-guided 边界
- acceptance_criteria:
  - 明确 canonical 命名前缀只保留 `test-pre-merge-*`，不再引入新的 `test-pre-multi-merge-*`
  - 明确 `test-pre-merge` 与 feature 的关系是 renewable family，而不是永久固定一对一对象
  - 明确 `develop` 的正常 promote source 是否切换为 `test-pre-merge-*` family，而不是 `feature/*`
  - 明确 single-feature lane 是否为 develop-bound feature 的默认必经 gate
  - 明确 multi bundle 是否允许直接 promote 到 `develop`，以及它与 single-feature lane 的闭环关系
  - 明确 multi bundle 的最小 manifest contract，至少包含 `base_develop_sha`、成员 feature 列表、成员 sha、merge 顺序
  - 明确 stale / rebuild / cleanup 的判定边界，尤其是 single family 与 multi bundle 的区别
  - 明确哪些内容必须由 `pr-merge-guarded` / hook / `governance-check` / runtime status machine-enforce，不能只留在文档
- promotion_gate:
  - 证明当前问题不是单纯命名或 skill 文案问题，而是 develop promotion model 本身的治理缺口
  - 证明 single-feature promote 与显式 multi bundle promote 的边界足够清晰，不会形成第二种前缀或第二套平行治理
  - 证明后续可拆分为至少一个“治理真源 issue”和一个“gate enforcement issue”，避免预研直接膨胀成大一统改造
  - 在本 candidate promoted 前，不直接修改 `CONSTITUTION` / `LAWS` / protected-branch gate 实现
- open_questions:
  - single-feature lane 是否必须在 feature 创建后立刻 eager materialize，还是进入 promote/integration 阶段时 lazy materialize
  - multi bundle 直接 promote 时，成员 feature 是否仍要求已有独立 single-lane receipt，还是 bundle receipt 即构成该轮唯一 promote evidence
  - multi bundle 的 manifest 应落在 merge receipt、artifact file，还是两者都要
  - stale detection 应先落在 `pr-merge-guarded`，还是先由 runtime/status 暴露再由 gate 阻断
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 旧 replay-only 模型解决不了“develop 只接收已测树”这个目标，必须先冻结新的 promote 模型。
  - reviewer: `subagent-enforcement-review`
    verdict: `mixed`
    note: 两路评审主张 multi 只作验证证据，一路主张 multi 直接 promote；已收敛为“默认 single-feature promote + 显式 bundle promote 路径待 issue 中最终冻结”。
- decision_reason:
  - 先冻结 promote model，再动宪法/法律/gate，才能符合 issue-guided 治理要求
  - 命名统一、lane lifecycle、bundle 语义、stale 规则和 gate enforcement 是同一个设计面，不能分散成口头规则
  - 需要先把默认路径和 bundle 例外路径拆清，否则后续 hook/gate 会要么过宽、要么不可实现
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260405-1615/brainstorms.md`
- promoted_issue_id: `I-20260405-1615-A`
- promoted_issue_path: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260405-1615-A`
  - keep the owner scoped to freezing the promote model and single/multi semantics before any constitutional or gate implementation changes
  - route later execution into separate enforcement and lifecycle owners instead of widening this owner
- revisit_trigger:
  - 再次出现“feature 直接 merge 到 develop 也算合规”的讨论
  - 再次引入 `test-pre-multi-merge-*` 之类第二前缀
  - 在没有 batch manifest 的前提下讨论 multi 直接 promote
