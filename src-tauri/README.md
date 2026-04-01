# Rust/Tauri Probe Bridge

## Purpose

This directory hosts the day-1 Rust/Tauri backend bridge for `freely.probe.v1`.

## Current bridge surface

- `probe_request_snapshot`
- `probe_send_command`
- `probe_server_event`

## Local preflight

Run these from the repository root:

```bash
bun run rust:preflight
bun run rust:preflight:test
bun run cargo:check:probe
bun run tauri:preflight:probe
bun run tauri:dev:probe
```

`rust:preflight` verifies that `cargo`, `rustc`, and `rustup` are available.
If any of them are missing, the script prints the exact missing commands plus the next suggested install/retry steps.
Preferred bootstrap path is `skill:rust-tauri-toolchain-bootstrap`, which uses `rsproxy` instead of the default rustup host.

`rust:preflight:test` verifies that the preflight guidance itself still covers the missing-command summary, install hint, shell reload hint, and retry commands.

`cargo:check:probe` runs the preflight first, then executes:

```bash
cargo check -p freely-probe-bridge
```

`tauri:preflight:probe` extends the Rust preflight with host-validation dependencies:

- `bun`
- `node_modules`
- `cargo tauri`

`tauri:dev:probe` runs that host preflight first, then starts the real Tauri dev host from `src-tauri/`.

## Host validation contract

- Vite dev host is fixed to `127.0.0.1:4173`.
- `src-tauri/tauri.conf.json` uses the same `devUrl`.
- Real host validation must use `bun run tauri:dev:probe`, not ad-hoc `bun run dev`.
