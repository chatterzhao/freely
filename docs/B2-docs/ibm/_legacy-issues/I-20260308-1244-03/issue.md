---
local_id: I-20260308-1244-03
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '4'
    url: https://github.com/chatterzhao/freely/issues/4
    synced_at: '2026-04-27T11:12:05Z'
  gitee:
    issue_id: IJFO4G
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4G
    synced_at: '2026-04-27T13:13:13Z'
primary_platform: github
canonical_issue_path: docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md
last_synced_comment_at:
  github: '2026-04-27T11:12:05Z'
hash: ''
created_at: '2026-04-27T11:12:05Z'
updated_at: '2026-04-27T11:12:05Z'
platform_state: closed
---

# Issue: frontend-runtime-baseline-for-probe

- issue_id: `I-20260317-1004`
- title: Frontend Runtime Baseline for Probe
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `frontend-runtime-baseline-for-probe`
- issue-name: `frontend-runtime-baseline-for-probe`
- source_candidate: `docs/B1-docs/raw-20260317-1101/candidates.md#c-20260317-1101`
- source_brainstorm: `docs/B1-docs/raw-20260317-1101/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/pre-tests.md`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

`Frontend Probe v0` 在实现中已经暴露出一个独立基础设施缺口：缺少真实 frontend build/runtime baseline，导致后续工作无法从骨架阶段进入可运行宿主阶段。

## Scope

1. 明确 frontend 宿主入口与 React renderer 挂载基线。
2. 明确 Tauri runtime 注入路径与最小 host wiring。
3. 明确 day-1 build/test baseline 的最小约束。
4. 明确该 baseline 与 `Frontend Probe v0` 的依赖边界。

## Acceptance

- 文档明确 frontend 宿主入口、React renderer 与 runtime 注入的最小基线。
- 文档明确 build/test baseline 的最小要求，不再让 dev-loop 只停在样板代码。
- 文档明确 `Frontend Probe v0` 如何依赖该 baseline，而不是继续把它混在 Probe issue 内。

## Minimal baseline

### Host entry

- 提供统一 default entry，负责读取宿主 runtime 能力
- 提供 bootstrap / mount / host helper，避免调用方手写接线

### React renderer

- 宿主必须提供明确的 render/root 接口
- Probe app 不直接依赖外部全局 renderer 细节，而通过 host helper 统一挂载

### Tauri runtime injection

- 宿主需提供 `invoke`
- 宿主需提供 `listen`
- 两者共同驱动 adapter 的 command / event 双通道

### Minimal build/test baseline

- 至少需要一个 frontend host entry 文件
- 至少需要一个 renderer/mount 路径
- 至少需要一个可验证 adapter 注入的最小运行方式
- 若正式测试基线尚未存在，需在 issue/progress/con
