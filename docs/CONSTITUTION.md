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
- `develop` is the nightly integration branch.
- `feature/*` branches are created from `develop` and merged back into `develop`.
- `release/*` branches are created from `develop` for release freeze, then merged into `main` and back into `develop`.
- `hotfix/*` branches are created from `main`, then merged into both `main` and `develop`.

2. Merge discipline:
- Unstable changes must not be merged into `main`.
- `main` accepts merges only from `release/*` or `hotfix/*`.
- `develop` may contain in-progress changes, but should stay buildable/testable.

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
- Git hooks should enforce `main` protection for local workflows (at least block direct push to `main`).
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
