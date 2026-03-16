# Candidates - 20260312-0011--architecture-synthesis-and-api-boundary

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260312-0011-A
- title: Backend Service Contract and Adapter Taxonomy
- problem: 当前文档已经接受 `ClientCommand`、`ServerEvent`、`Snapshot` 与 `tauri_adapter/ws_adapter` 的方向，但还没有一份更高层的正式产物说明 backend service contract 本体、adapter 分类以及它们各自的兼容义务。
- why_now: 如果不先冻结这一层，后续 Frontend Probe、transport 选择、第三方 runtime 接入都会继续在“协议语义”和“承载方式”之间混层。
- acceptance_hint: 明确 backend service contract 的职责边界；定义 adapter taxonomy；说明 `tauri_adapter`、`ws_adapter`、`local_process_adapter`、`openclaw_adapter/profile` 的角色差异；规定 adapter 只做承载与映射，不改业务语义。
- priority: P0
- status: proposed
- decision_reason: 这是把现有分散架构研究收敛成单一中间层真源的前置问题。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 1

### C-20260312-0011-B
- title: Frontend Manifest Boundary and Runtime Capability Layering
- problem: 当前技术栈已经在规范中冻结，但前端 manifest、后端 manifest、协议层真源以及 agent tooling capability 的边界尚未正式收敛，后续实现时容易把产品依赖、开发依赖和外部工具能力混写。
- why_now: Freely 即将从研究进一步进入实现阶段，如果不先明确 manifest 分层，后续 `package.json`、`Cargo.toml` 与可选 agent tooling 会很快失去边界。
- acceptance_hint: 明确 frontend `package.json` 只承载 Tauri shell / React UI 依赖；backend 依赖只落 Rust manifest；协议对象不埋进任一端私有依赖表；agent tooling 进入独立 capability 层与门禁。
- priority: P0
- status: proposed
- decision_reason: 这是技术栈长期可维护的基础，也能避免“产品运行时依赖”和“AI 执行环境工具”混层。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 2
- depends_on:
  - C-20260312-0011-A

### C-20260312-0011-C
- title: Runtime Independence with OpenClaw Profile as Optional Adapter
- problem: 现有研究已经证明 OpenClaw 可作为阶段性借力 runtime，但还没有把“Freely 产品独立成立”与“OpenClaw 只是 adapter/profile”这层主从关系正式固定下来。
- why_now: 如果不把这层关系说清，后续架构讨论会不断在“是否依赖 OpenClaw”上反复摇摆，影响后端 contract 和前端边界收敛。
- acceptance_hint: 明确 Freely 的产品 contract、治理规则和状态词典不依赖 OpenClaw；定义 OpenClaw profile 的接入方式、可映射能力、不可等价语义，以及后续替换/退出边界。
- priority: P1
- status: proposed
- decision_reason: 它能把“借力现有 runtime”变成可治理的实现策略，而不是新的架构中心。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 3
- depends_on:
  - C-20260312-0011-A

### C-20260312-0011-D
- title: Event Log and Snapshot Reconstruction Contract
- problem: 当前文档已经多次提到 `ServerEvent`、`Snapshot`、恢复和 team visibility，但还没有把“哪些事实必须事件化、哪些可以快照化、快照如何从后端状态重建”单独收敛成正式问题。
- why_now: 这直接影响 Frontend Probe、恢复治理、AI 团队态势 UI 和后续多 transport 适配的正确性。
- acceptance_hint: 明确事件单调追加原则、最小事件字段、快照重建来源、UI 首屏恢复语义，以及 event log / snapshot 对 recovery 与 visibility 的支撑关系。
- priority: P1
- status: proposed
- decision_reason: 它是把 backend contract 真正落成可观测控制面的关键补充。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 4
- depends_on:
  - C-20260312-0011-A

### C-20260312-0011-E
- title: AI Team Control Surface and Multi-Worktree Visibility
- problem: 当前文档已明确需要 human correction、agent roster、team timeline 和 embedded terminal，但还没有一份正式问题专门收敛 Freely 应用的整体信息架构，尤其是如何让人同时观察多个 worktree、多个 AI 和多个 subagent 的推进状态。
- why_now: 如果不尽早冻结控制面方向，Frontend Probe 很容易退化成“聊天窗 + 单终端”，最终失去 Freely 作为自治工程控制面的产品识别度。
- acceptance_hint: 定义面向不同操作系统用户的 Freely App 信息架构；明确 chat、team timeline、agent roster、worktree lanes、embedded terminal、status panels 的相对地位；说明 day-1 probe 如何做到“薄但方向正确”。
- priority: P0
- status: proposed
- decision_reason: 这直接决定 Freely 的产品体验是否服务于多 agent / 多 worktree / 多 subagent 的真实使用场景。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 3
- depends_on:
  - C-20260312-0011-A

### C-20260312-0011-F
- title: Skill-first Capability Exposure with OpenClaw Workspace Projection
- problem: 现有研究已经分别讨论了 Freely skills 和 OpenClaw workspace 可扩展性，但还没有正式收敛“Freely 先以 skill 暴露能力，再把这些能力映射到 OpenClaw workspace/profile”的统一方案。
- why_now: 如果不先明确这层能力投影关系，后续第三方接入要么会污染 Freely 内核边界，要么会把 OpenClaw 错抬为主架构。
- acceptance_hint: 明确 Freely 哪些核心能力以 skill 暴露；定义这些能力如何通过 adapter/profile 投影到 OpenClaw workspace 自定义、memory、hooks、skills；说明哪些能力可映射，哪些语义不能等价替代。
- priority: P1
- status: proposed
- decision_reason: 这能把 OpenClaw 的优势用起来，同时不损害 Freely 的产品独立性和治理主权。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 5
- depends_on:
  - C-20260312-0011-A
  - C-20260312-0011-C

### C-20260312-0011-G
- title: Standalone Runtime Baseline Without OpenClaw
- problem: 当前仓库已经存在 `freely` supervisor、lead-agent prompt 组装、AI CLI 监控和 recovery skill，但还没有一份正式架构产物明确说明“Freely 在完全不对接 OpenClaw 时，依靠哪些组件独立工作”。
- why_now: 如果不把 standalone baseline 单独冻结，后续关于 memory、skills、runtime、UI 和第三方集成的讨论会持续把 OpenClaw 当成隐式前提，削弱 Freely 的产品独立性。
- acceptance_hint: 说明 standalone mode 的最小组件：governance inputs、runtime supervisor、external AI CLI adapters、skills、workspace governance、state evidence；明确哪些连续性由 Freely 自身文档和 `.freely/` 状态承担，哪些能力接入 OpenClaw 后才是增强项。
- priority: P0
- status: proposed
- decision_reason: 这是把“Freely 必须先独立成立”从口头判断提升为技术架构承诺的关键一步。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 4

### C-20260312-0011-H
- title: Human Intervention Transport Across Auto-Run CLIs
- problem: 当前产品方向已经明确 human chat input 是高优先级 side-channel，协议层也已有 `SendChatIntervention`，但还没有正式收敛“在 auto-run CLI 场景下，人类输入如何可靠进入当前会话”的统一 transport 方案。
- why_now: 如果不先冻结这层控制链，Frontend Probe 的 chat intervention panel、backend arbitration、以及 `codex/iflow/kiro-cli` 的 resume/attach 差异会各自演化，最终难以形成稳定的人类纠偏能力。
- acceptance_hint: 定义 `SendChatIntervention` 的统一 contract；明确 day-1 主实现为 `resume_with_intervention`；说明 `tool/session_id/resume_hint` 的最小依赖；把 `direct_interrupt` 明确为未来保留能力，而不是当前主依赖。
- priority: P0
- status: proposed
- decision_reason: 这是把“人类在环侧观察并偶尔高优先级介入”从产品意图落成技术控制链的关键一步。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- sequencing_rank: 5
- depends_on:
  - C-20260312-0011-A
  - C-20260312-0011-G
