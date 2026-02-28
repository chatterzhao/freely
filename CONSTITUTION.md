# Freely Constitution

## 1. Product Identity

Freely is an autonomous engineering loop system:
- AI acts as project owner after startup.
- AI self-manages demand discovery, brainstorm, EPIC/STORY planning, development, and verification.
- Recovery is mandatory: crash/blocking must trigger automatic continuity.

## 2. Mandatory Tech Stack

These choices are hard constraints unless explicitly revised:

- Desktop shell: **Tauri**
- Core runtime/orchestrator/watch/recovery: **Rust**
- Frontend UI: **React**
- Frontend package/runtime tooling: **Bun**
- Terminal rendering: **xterm.js**
- Terminal process backend: **Rust PTY** (system shell + PTY process)

## 3. Terminal Architecture Rules

- UI terminal is embedded in app, but executes real system shell commands via PTY.
- Each running loop instance owns an isolated AI CLI process/session and PID.
- Monitoring target is that AI CLI process/session lifecycle.
- Multiple project instances must be isolated (separate PID/session/state directory).

## 4. AI Execution Modes

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

## 5. Recovery Policy (Hard Requirement)

Recovery has two branches:

1. Resume branch:
- If unattended resume is supported for current tool/session, resume directly and continue.

2. Bridge branch:
- If unattended resume is not supported:
  - run one bridge recovery round
  - write crash/blocking checkpoint into progress docs
  - restart unattended auto loop from updated project state

Never stop after crash/blocking unless explicit stop criteria are reached.

## 6. Constraint Surface

Freely accepts only these primary inputs:
- project absolute path
- project intent document path
- constitution document path
- ai spec (`tool:model:mode`)

All other project context must be discovered by AI from project files.

## 7. Engineering Discipline

- Keep command surface simple and scriptable (`init/start/status/stop`).
- Keep state explicit and inspectable on disk.
- Prefer deterministic behavior over hidden magic.
- Add compatibility bridges for renamed paths and legacy state.

