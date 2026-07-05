# Issue: freely-layered-architecture-and-tooling-topology

- issue_id: `I-20260326-1810`
- title: Freely layered architecture and tooling topology
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `freely-layered-architecture-and-tooling-topology`
- issue-name: `freely-layered-architecture-and-tooling-topology`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260326/candidates.md#c-20260326-1810-a`
- source_brainstorm: `docs/B1-docs/raw-20260326/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/PROJECT_INTENT.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `AGENTS.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经在多个局部真源里分别写对了部分边界，例如 `three-loop`、`tools.md`、CLI-first 与 contract/adaptor taxonomy，但仍缺一份统一的 Freely 自身产品/系统架构表达。这导致：

- `chat`、`init`、`start`、`status` family 容易和 `CLI shell / TUI shell / GUI app` 被错误并列
- 外部 AI tooling layer 缺少明确站位
- `AGENTS.md` 仍偏向“先想是不是能力”，而缺少“先判断这是 Freely 自身产品架构，还是可复用能力”的入口分流

本 issue 的目标不是扩写 `docs/system/workspace/**`，而是先把 Freely 自身架构收敛到开发期高层真源，再要求其他开发文档跟随对齐。

## Scope

1. 在 `PROJECT_INTENT` 中补齐 Freely 自身产品/系统架构总图与术语。
2. 在 `CONSTITUTION` 中冻结 Freely 产品形态的硬边界：
   - Freely core
   - canonical CLI
   - optional TUI / GUI shells
   - command / status semantics 不与 shell 并列
   - external AI tooling 不是 Freely 自身 product shell
3. 在 `LAWS` 中补齐架构改动的分类与对齐顺序。
4. 在 `AGENTS.md` 中补齐开发 Freely 时的首跳思考顺序，但不让 `AGENTS.md` 代替架构真源。

## Out Of Scope

- 不把本 issue 直接落到 `docs/system/workspace/**`
- 不把 Freely 当前产品形态直接泛化成通用能力
- 不在本 issue 内定义“未来任何应用都应采用 `core + CLI + TUI + GUI`”

## Acceptance

- `PROJECT_INTENT` 明确表达 Freely product / core / CLI shell / TUI shell / GUI app / semantic surfaces / external AI tooling layer 的关系
- `CONSTITUTION` 明确把这些关系收成硬边界，尤其 shell、command、semantic surface 不再混层
- `LAWS` 明确新讨论出现时，先判断 continuation、Freely 自身产品架构、开发治理、可复用能力，再决定落点
- `AGENTS.md` 对齐上述思考顺序，但保持“入口指引”身份，不升格为架构真源
- milestone / pre-brainstorm / issue 路径一致，不再把这条线挂在 `workspace-routing-foundation`

## Completion

- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `AGENTS.md`
- `docs/milestones.md`
- `docs/B1-docs/raw-20260326/brainstorms.md`
- `docs/B1-docs/raw-20260326/candidates.md`
- `docs/B2-docs/config/packaging/brainstorms/b-freely-layered-architecture-and-tooling-topology.md`
- `docs/B2-docs/config/packaging/prd.md`
- `docs/B2-docs/config/packaging/pre-tests.md`
- `docs/B2-docs/config/packaging/tasks.md`
- `docs/B2-docs/config/packaging/code-reviews/20260326-freely-layered-architecture-and-tooling-topology-verification.md`

## Verification

- `./bin/governance-check`
- review updated `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md` for consistent placement language

## Next

- 若后续还要抽象“通用产品形态方法”，另开独立 pre-brainstorm，不回头扩写本 issue。
