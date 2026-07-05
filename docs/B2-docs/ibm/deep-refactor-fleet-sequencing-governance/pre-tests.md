# Pre-Tests: deep-refactor-fleet-sequencing-governance

## Acceptance Structure

### Pre-merge focused regression / smoke

1. 单独阅读 `AGENTS.md` 时，能明确看出 broad/deep refactor 前要先做 fleet sequencing audit，而不是直接开新 implementation lane。
2. 新 gate 单独阅读时，能看出：
   - 要同时看 `git worktree list`、`wt-fleet-status`、`freely live-status`、`freely fleet-status`
   - 要把结果与 `milestones` / `progress` 对齐
   - 要优先收束 `dirty`、`desired=running`、或仍持有 owner judgement 的工位
3. 新 wording 单独阅读时，不会把这条规则误读成 `docs/system/**` 的运行期能力 contract。

### Post-merge integration acceptance

1. 在 canonical `develop` 上准备下一轮 broad/deep refactor 时，先按 `AGENTS.md` 执行 fleet sequencing audit，确认排序与 gate 能直接指导下一步工位选择。
2. environment:
   - `develop`
   - feature worktree used for merge prep / refactor kickoff
3. evidence:
   - audit 输出与 `milestones` / `progress` 能对齐出高风险 owner 和上游治理前置顺序
4. failure signal:
   - 仍然在未检查 fleet 的情况下直接开新 refactor worktree
5. failure handling / replay expectation:
   - 若失败，回到来源 feature worktree 修正文案或再补充 gating evidence，然后重新从 `develop` replay audit

### Post-merge application-native real-environment acceptance

1. 在真实 Freely 开发流程中再次准备 broad/deep refactor 时，manager 或人工引导都能先识别 dirty/running/owner 工位，再决定是否开新 lane。
2. environment:
   - live Freely development workflow on `develop`
3. evidence:
   - fleet audit、worktree选择与后续 merge prep 顺序符合 gate
4. failure signal:
   - runtime 或人工流程仍把 clean/stopped 非阻塞树当第一优先，或忽略 dirty closeout owner
5. failure handling / replay expectation:
   - 若失败，新开 dedicated governance worktree 修正开发期 gate，再重新执行 audit

### Post-merge end-to-end dogfood acceptance

1. 用一次真实“准备大重构”的 dogfood 场景，检查开发者或 manager 是否先执行 sequencing audit，再决定哪个 worktree 先完成、哪个上游树先吸收。
2. environment:
   - `freely chat` against canonical development workflow or direct development session following `AGENTS.md`
3. evidence:
   - 最终选择的 worktree 顺序与 gate 一致
4. failure signal:
   - 团队重新掉回“看到一个新大想法就直接开重构工位”
5. failure handling / replay expectation:
   - 若失败，回到本 issue 或新的 follow-up governance issue 继续修正规则

### Non-goals

1. 不要求本 issue 自动化执行 sequencing judgement。
2. 不要求本 issue retire 所有 clean/stopped 历史 worktree。
