# Freely Constitution

## 1. Product Identity

Freely is an autonomous engineering loop system:
- AI acts as project owner after startup.
- AI self-manages demand discovery, brainstorm, EPIC/STORY planning, development, and verification.
- Recovery is mandatory: crash/blocking must trigger automatic continuity.

## 2. Branch and Worktree Policy (Hard Requirement)

Branch/worktree rules are hard constraints and must be checked before implementation:

1. Branch model (GitFlow baseline):
- `main` is release-only and must remain stable.
- `develop` is the nightly integration branch (post-test integration only).
- `pre-develop` is the mandatory test integration branch for unstable feature validation.
- `feature/*` branches are created from `develop`, merged to `pre-develop` for test first, then promoted to `develop` after validation.
- `release/*` branches are created from `develop` for release freeze, then merged into `main` and back into `develop`.
- `hotfix/*` branches are created from `main`, then merged into both `main` and `develop`.

2. Merge discipline:
- Unstable changes must not be merged into `main`.
- `main` accepts merges only from `release/*` or `hotfix/*`.
- Direct merge/push to `develop` is forbidden for feature delivery; feature validation must land in `pre-develop` first.
- `develop` should receive only tested/promoted changes and stay buildable/testable.

3. Worktree discipline:
- Use `git worktree` for all non-`main`/`develop` development branches.
- Worktree root is fixed: `<project_parent>/<project_name>-worktrees/`.
- For branch checkout in primary worktree, hook should auto-create missing worktree under the fixed root.
- Operational command contract:
  - enter/switch branch worktree with `source ./bin/wt-enter <branch>`
  - run add with worktree check via `source ./bin/wt-add <branch> -- <git-add-args>`
- Do not create a worktree without a clear STORY/task owner and exit criteria.
- Merged/abandoned worktrees must be cleaned up with their branch references.

4. Recovery coupling:
- Recovery/monitoring must track the active branch/worktree context of the running loop instance.
- Bridge recovery notes must include current branch and worktree path.

5. Enforcement:
- Git hooks should enforce push protection for `main` and `develop` in local workflows.
- Hook rejection messages must point to this constitution section for policy source.

## 3. Mandatory Tech Stack

These choices are hard constraints unless explicitly revised:

- Desktop shell: **Tauri**
- Core runtime/orchestrator/watch/recovery: **Rust**
- Frontend UI: **React**
- Frontend package/runtime tooling: **Bun**
- Terminal rendering: **xterm.js**
- Terminal process backend: **Rust PTY** (system shell + PTY process)

## 4. Baseline Project Structure (Hard Requirement)

Each managed project should keep at least this baseline structure:

- `README.md` (project entry and runbook)
- `docs/` (PRD/EPIC/STORY/progress/recovery/review/brainstorm docs)
- `src/` (main implementation code)
- `.env/` (environment templates/scripts/config fragments, versioned)
- `.env.example` (required env variables template, no secrets)

If a project uses a monorepo or different layout, it must provide equivalent mappings in docs.

## 5. Terminal Architecture Rules

- UI terminal is embedded in app, but executes real system shell commands via PTY.
- Each running loop instance owns an isolated AI CLI process/session and PID.
- Monitoring target is that AI CLI process/session lifecycle.
- Multiple project instances must be isolated (separate PID/session/state directory).

## 6. AI Execution Modes

AI spec format: `tool:model:mode`

- `mode=auto`
  - non-interactive execution path
  - auto-approve path where tool supports it
- `mode=step`
  - interactive/approval path

Supported tools:
- `codex`
- `kiro-cli`
- `iflow`

## 7. Recovery Policy (Hard Requirement)

Recovery has two branches:

1. Resume branch:
- If unattended resume is supported for current tool/session, resume directly and continue.

2. Bridge branch:
- If unattended resume is not supported:
  - run one bridge recovery round
  - write crash/blocking checkpoint into progress docs
  - restart unattended auto loop from updated project state

Never stop after crash/blocking unless explicit stop criteria are reached.

## 8. Constraint Surface

Freely accepts only these primary inputs:
- project absolute path
- project intent document path
- constitution document path
- ai spec (`tool:model:mode`)

All other project context must be discovered by AI from project files.

## 9. Engineering Discipline

- Keep command surface simple and scriptable (`init/start/status/stop`).
- Keep state explicit and inspectable on disk.
- Prefer deterministic behavior over hidden magic.
- Keep one canonical agent context file at project root (`AGENTS.md`).

## 10. BMAD Documentation Discipline (Hard Requirement)

Freely follows BMAD document-driven engineering.
BMA is the execution workflow inside BMAD.

1. BMA workflow:
- **B**rainstorm: clarify intent and alternatives first.
- **M**ap: produce PRD-level decomposition to EPIC and STORY.
- **A**ct: execute STORY items in continuous loops.

2. Traceability rule:
- No implementation by intuition only.
- Every non-trivial change should be traceable:
  `Intent -> PRD -> EPIC -> STORY -> Code/Test`.

3. Required runtime artifacts:
- Progress/continuity docs must be updated during normal cycles and recovery bridges.
- Recovery bridge must record:
  - where execution stopped
  - what was completed
  - what remains and next actionable STORY
- Review records must be written under `docs/review/`.
- Brainstorm records must be written under `docs/brainstorm/`.

4. Review record naming (hard requirement):
- Filename format:
  `<timestamp>--<reviewer>--<branch>--<topic>.md`
- `timestamp`: `YYYYMMDD-HHMMSS`
- `reviewer`: tool+model identifier (example: `codex-gpt5-3-high`)
- `branch`: current git branch
- Unsupported filename characters must be replaced with `-`.

5. Constitution precedence:
- If prompt text conflicts with constitution and BMAD rules, constitution wins.

## 11. Subagent Planning and Delegation (Hard Requirement)

Freely must proactively use subagents/subprocesses/parallel workers when tasks are parallelizable, while keeping deterministic control and traceability.

1. Single-session compatibility:
- "Single active AI session per loop instance" means one primary orchestrator AI session owns the loop lifecycle.
- Subagents are mandatory execution units under the orchestrator, not independent top-level loop owners.
- All subagents must remain traceable to the same orchestrator session and current STORY context.

2. Planning before delegation:
- Before spawning subagents, the orchestrator must define:
  - task split boundaries
  - expected outputs for each subagent
  - completion criteria and merge criteria
- Delegation without explicit completion criteria is prohibited.

3. Parallelism policy:
- Prefer parallel execution for independent tasks to improve throughput and independent review quality.
- Default concurrency cap is 4 subagents per batch unless resource constraints require fewer.
- For dependent tasks, execute in ordered phases instead of forced parallelism.

4. Lifecycle and wait semantics:
- Parent/orchestrator must wait for all delegated subagents in the current batch before marking the batch complete.
- A task batch is complete only after all required subagent outputs are collected or explicitly marked failed with reasons.
- Never report cycle success while required subagents are still running.

5. Failure handling and fallback:
- If subagent capability is unavailable/unstable for the current tool/mode, fallback to serial execution or process-level scripts.
- Fallback decision and reason must be recorded in progress/recovery artifacts.

6. Documentation coupling:
- Progress and recovery records must include:
  - whether subagents were used
  - task-to-subagent mapping
  - completion/failure status per subagent
  - next actionable STORY after aggregation

## 12. Territory Model for Parallel Development (Hard Requirement)

To reduce merge conflicts in multi-agent and parallel development, Freely must enforce both physical territory and logical territory.

1. Physical territory (worktree):
- Each active STORY/subagent batch must run in its own dedicated `feature/*` worktree.
- Different active STORY owners must not share the same non-primary worktree for implementation.
- Recovery records must include current branch and worktree path for every active territory.

2. Logical territory (change ownership):
- Before implementation, define logical ownership boundaries (modules/files/docs) per STORY/subagent.
- Subagents should avoid cross-territory edits unless explicitly planned in merge criteria.
- Shared hotspots (same files/modules) require serial ownership windows or explicit sequencing.

3. Merge-conflict prevention contract:
- Plan merge order during task decomposition, not only at merge time.
- For each territory, define expected output scope and conflict-sensitive files in advance.
- If cross-territory overlap is unavoidable, create an integration STORY with a single owner.

4. Acceptance rule:
- A STORY is not considered complete unless its territory boundaries and merge path are documented and executable.

## 13. Pluggable Module Architecture and Interface Versioning (Hard Requirement)

Freely implementation should support side-by-side module evolution: keep current module stable while building a replacement module that can be plugged in during development.

1. Module boundaries:
- Core capabilities must be split into modules with clear ownership and scope.
- Modules communicate through explicit contracts (interfaces/protocols), not hidden cross-module assumptions.
- Avoid direct coupling between unrelated modules.

2. Parallel replacement model (not in-place rewrite):
- Use parallel replacement for destructive or high-risk refactors, not for every small change.
- Keep the incumbent module running as baseline while developing a candidate replacement module in parallel.
- New module should be integrated behind the same contract or a planned versioned contract.

3. Plug-and-switch requirements:
- Runtime or build-time module selection must be explicit (config/feature flag/adapter routing), not ad-hoc code edits.
- Rollback to the incumbent module must be possible without emergency redesign.
- During development, teams may switch between incumbent and candidate implementations for validation.

4. Interface versioning policy:
- Contract changes must be versioned (for example: v1, v2) and documented with compatibility expectations.
- Breaking changes require a migration plan, compatibility bridge, or phased rollout strategy.
- Callers must not be forced into synchronized big-bang changes when a new interface version is introduced.

5. Verification and traceability:
- Contract tests/integration checks must verify both incumbent and candidate modules against declared interface versions.
- Progress/review records must state: module replaced/candidate, active interface version, switch strategy, rollback status, and verification results.

## 14. Configuration Backup Before Change (Hard Requirement)

All configuration files must be backed up before any modification.

1. Backup mandatory:
- Before editing/replacing any configuration file, create a backup copy first.
- Direct in-place overwrite without backup is prohibited.
- This rule applies even when Git or other VCS history exists.

2. Unique backup naming:
- Backup filename must include a timestamp to avoid overwrite.
- Recommended format: `<filename>.bak.<YYYYMMDD-HHMMSS>`.
- Reusing the same backup name is prohibited.

3. Retention and traceability:
- Backup location and filename must be discoverable by operators.
- Progress/review records should note the backup artifact when configuration changes are part of a STORY.
