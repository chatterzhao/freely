# Issue: default-autonomy-activation-consent-and-tool-policy-governance

- issue_id: `I-20260401-1303-A`
- title: Default autonomy activation consent and posture truth governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `default-autonomy-activation-consent-and-tool-policy-governance`
- issue-name: `default-autonomy-activation-consent-and-tool-policy-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-1303-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/raw-20260402-0403pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-default-autonomy-activation-consent-and-tool-policy-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前的产品真相还分裂着：

1. `tools.md` 与 runtime launcher 已经把 `codex` / `cc` 的 `auto` 路径定义为免交互、自动批准。
2. 这条 owner 启动时的 reproduced split 是：`freely init` 生成的项目级 `.codex/config.toml` 原先仍写入 guarded posture，而 `tools.md` / launcher 已偏向 auto posture。
3. 产品讨论已经明确：Freely 的默认气质是 owner-grade AI autonomy，而不是把交互批准当主路。
4. 预研已经把“内部 AI 决策升级 -> security-focused reviewer / committee -> minimal risk state”定义成自治不降级的主路，但这层机制还没有稳定 owner。

这条 issue 的目标不是一次吃掉所有 security baseline，而是先冻结最核心的产品 contract：

- Freely 默认就是高自治、免交互、自动批准
- 启用时必须做强阻塞式知情同意
- safeguard 例如 sandbox / VM / 隔离设备 / 受限网络 应被强建议、强支持，但默认不是自治前置门槛
- Freely canonical policy、runtime decision ladder、tool adapter 注入、tool-local config materialization 之间必须有统一边界

## Scope

1. 冻结 Freely 的默认 autonomy posture：
   - 默认免交互
   - 默认自动批准
   - 交互批准不是主路，只是未来可配置降级
2. 定义 activation consent contract：
   - 要展示哪些风险与执行边界
   - 哪些内容必须阻塞确认
   - 哪些 safeguard 只是建议，不构成默认阻塞
3. 冻结产品级 posture truth surface：
   - `init` / 项目 `init`
   - `doctor`
   - runtime decision / escalation path
   - `baseline-status`
   - `live-status`
4. 定义工具配置分层的上位 owner 关系：
   - Freely canonical policy 是上位真源
   - tool adapter injection / tool-local config materialization 是下游物化层
5. 冻结高风险与高不确定场景下的 runtime contract：
   - 先走内部 AI 决策升级
   - 可引入一个或多个 security-focused subagent / reviewer committee
   - 仅在无法产出可信下一步时进入 minimal risk state
6. 明确把更细的 tool materialization 和当前 Codex split 收口工作切给 sibling owner `I-20260401-1303-A-2`

## Non-Goals

1. 不在本 issue 中一次 materialize 全部 security baseline domains。
2. 不在本 issue 中直接定义 reusable security skills。
3. 不在本 issue 中默认强制 sandbox、VM、隔离设备或受限网络。
4. 不在本 issue 中展开具体 supply-chain / secret / source-map 审计实现。
5. 不在本 issue 中完成具体工具配置物化、launcher 参数对齐或 `.codex/config.toml` 收口实现。
6. 不在本 issue 中把用户重新拉回运行时逐步人工审批。

## Acceptance

1. 文档明确写死：Freely 默认按免交互、自动批准运行下游工具，这是产品能力，不是异常模式。
2. activation consent 明确区分：
   - 阻塞项：用户是否已理解并接受高自治运行及当前执行边界
   - 非阻塞 safeguard：sandbox、隔离设备、VM、受限网络等建议与支持面
3. issue 明确定义 Freely canonical policy 与下游 tool materialization 之间的 owner boundary。
4. `init`、`doctor`、runtime、`baseline-status`、`live-status` 的 autonomy/safety responsibility set 被写成可继续实现的 contract。
5. 文档明确高风险/高不确定场景的主路是内部 AI 决策升级，而不是恢复用户逐步批准。
6. issue artifacts 明确写出 autonomous escalation ladder、security-focused reviewer / committee、以及 minimal risk state 作为“最后手段”的 contract。
7. sibling owner `I-20260401-1303-A-2` 被明确承接 tool adapter injection、tool-local config materialization、以及当前 Codex split 的具体收口。

## Current Follow-through

1. `I-20260401-1303-A-2` 的第一条 implementation slice 已落地：`auto` 模式的项目级 `.codex/config.toml` 现在写入 `approval_policy = "never"`。
2. 因此本 owner 保留的是产品 contract truth，而不是继续把“`.codex/config.toml` 仍然 guarded”当作当前现状。

## Current Artifact Set

- `docs/B2-docs/config/packaging/raw-20260402-0403issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403brainstorms/b-default-autonomy-activation-consent-and-tool-policy-governance.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403prd.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403pre-tests.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403tasks.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403issues/freely-tool-autonomy-policy-materialization-governance.md`

## Current Evidence

- `./bin/governance-check`
- wording review confirming:
  - default autonomy remains the canonical product posture
  - safeguard guidance is explicit but non-blocking by default
  - activation consent is blocking and distinct from runtime step approvals
  - runtime escalation and minimal-risk semantics remain autonomy-first
  - config layering is consistent with existing project-level tool config governance

## Next

- 这条 issue 已冻结默认高自治 posture、activation consent、runtime decision ladder、minimal risk semantics、和产品级 posture truth surfaces，并进入 develop-bound verification。
- tool policy materialization、launcher/config split、以及 ACP follow-up adapter seam 改由 sibling owner `I-20260401-1303-A-2` 承接。
- 更宽的 baseline domains，例如 supply chain、secret materialization、artifact exposure、security decision support，应由后续 issue 或 capability lane 继续拆分，不回灌本 issue 重新变成 umbrella。
- 待 develop 合流与 post-merge acceptance 写回后，再把本 owner 从 `in_verification` 推进到 `completed`；后续若再出现 autonomy posture / activation consent / owner boundary drift，应新开 follow-on，而不是重开本 owner。
