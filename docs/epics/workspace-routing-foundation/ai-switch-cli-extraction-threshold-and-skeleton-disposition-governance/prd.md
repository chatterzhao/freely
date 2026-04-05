# PRD: ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance

## Goal

冻结 standalone `ai-switch-cli` backend 的 extraction threshold，以及现有本地 switch skeleton 的 canonical disposition，使 Freely 后续能在明确边界下启动独立 backend owner，而不是继续依赖口头判断。

## Why Now

当前状态已经进入一个容易失控的窗口：

- Codex-first contract 已经足够强，说明 backend 方向不是空想
- 但第二工具还没有 verified parity，说明现在直接整体迁出会制造双份不稳定真相
- 本机又已经有一个未提交、旧命名的 skeleton repo，容易被误当成“其实拆分已经开始了”

因此现在必须冻结：

1. 什么叫“达标到可以拆”
2. 什么叫“还没达标，不要拆”
3. 那个本地 skeleton 到底是过渡占位，还是未来正式仓库的起点

## Product Surface

- current Freely owner:
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/file-backup.sh`
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- future backend:
  - `ai-switch-cli`
- local skeleton under discussion:
  - `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch`

## Non-Goals

- implementing standalone packaging or installer flow
- moving live code out of Freely in this owner
- adding new tool-specific save/switch/probe parity
- deciding final backend implementation language before the CLI contract is stable

## Extraction Threshold

Standalone extraction may start only after all of the following are true:

1. command surface is frozen for:
   - `list`
   - `current`
   - `login`
   - `save`
   - `switch`
   - `delete`
   - `probe`
   - `best`
   - `status`
2. JSON envelope is frozen and Freely can consume it without relying on extra stdout heuristics.
3. at least one tool, currently Codex, has verified:
   - save truth
   - switch truth
   - probe truth
   - mutation safety for home-level config
4. generic helper surfaces that are not tool-specific are already separated from one-off inline logic.
5. this IBM package is frozen and available as the extraction-start handoff:
   - `issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
   - `brainstorms/b-ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
   - `pre-tests.md`
   - `tasks.md`
6. the follow-on owner can point to a concrete first move without reopening threshold research:
   - choose `rename-in-place` or `fresh-repo`
   - preserve Freely as canonical until the first backend commit lands
   - move only backend-owned surfaces first, not Freely orchestration policy

## Required Generic Helper Surfaces Before Split

The backend should not be born from copying raw inline script fragments. At minimum, extraction should start only after these helpers are identifiable as backend-worthy or Freely-only:

1. file-backup helper for write-before-mutation of untracked config files
2. generic slot inventory conventions (`~/.ai-auth/<tool>-<slot>/`)
3. active-slot pointer semantics
4. generic manifest vocabulary
5. backend JSON envelope formatter

Anything still tightly coupled to Freely orchestration should remain in Freely until the extraction owner explicitly moves it.

## Control Plane vs Backend Boundary

### Freely control plane owns

1. project-level tool priority ordering
2. watchdog retry / cooldown / bounded recovery policy
3. when to ask backend for `probe`, `best`, `switch`
4. project-local UX such as init-time backend detection and priority-list insertion prompts
5. orchestration decisions across tools

### ai-switch-cli backend owns

1. tool-native login flow
2. slot save/delete/switch implementation
3. tool-specific live config mutation
4. tool-specific probe execution
5. JSON machine-readable output consumed by Freely

### Explicitly not allowed

1. Freely re-embedding new backend-only file mutation rules after extraction starts
2. backend silently deciding project-level fallback ordering
3. prompt-only undocumented backend semantics

## Local Skeleton Disposition

Observed local skeleton:

- path: `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch`
- current state:
  - local git repo exists
  - no commits yet
  - README/product naming still says `codex-account-switch`
  - current contents are mostly repo skeleton / governance scaffolding

Canonical interpretation:

- this is not yet a canonical backend repo
- it is only disposable local scaffolding

Allowed future paths:

### Path A: rename in place

Allowed only when extraction has formally started. Before the first real commit:

1. rename repo to `ai-switch-cli`
2. rewrite `README.md`
3. rewrite `AGENTS.md`
4. rewrite `PROJECT_INTENT.md`
5. remove stale `codex-account-switch` naming from canonical docs

### Path B: discard and create fresh repo

Preferred if the skeleton contains no meaningful truth beyond boilerplate or if the old naming leaves too much cleanup risk.

Rule:

- no later owner may claim the old skeleton is canonical simply because it existed first

## Extraction-Start Checklist

The first standalone extraction owner may begin only when it can answer all of the following with canonical repo evidence:

1. `threshold_met`
   - Codex remains the verified strong tool contract for save/switch/probe/materialization
   - no required generic helper is still only implicit in tool-local inline code
2. `boundary_frozen`
   - Freely still owns priority ordering, watchdog policy, recovery policy, and project UX
   - backend owns login/save/delete/switch/probe and tool-specific config mutation
3. `repo_path_selected`
   - either `rename_in_place` or `fresh_repo` is explicitly chosen
   - the reason is written before the first backend commit
4. `naming_cleanup_ready`
   - any surviving repo path can drop `codex-account-switch` naming before its first real commit
5. `first_move_scoped`
   - the first extraction slice only moves backend-owned surfaces
   - Freely continues consuming a CLI/JSON boundary rather than re-embedding new private mutation rules

## Stage Plan

### Stage A: finish Codex-first proof in Freely

Use current owners to keep:

1. Codex slot bundle contract
2. provider-aware probe contract
3. shared helper extraction such as file-backup

### Stage B: materialize extraction owner

The follow-on owner must:

1. choose rename-in-place vs fresh-repo path
2. define migration sequence
3. decide what code actually moves first

### Stage C: start standalone repo

Only then may implementation-bearing backend work start outside Freely.

## Acceptance Summary

This owner is complete only when the docs make all three statements unambiguous:

1. `ai-switch-cli` is the preferred long-term backend direction
2. current Freely code remains canonical until extraction threshold is met
3. the existing `codex-account-switch` skeleton is not yet canonical and must either be renamed under an explicit owner or discarded
