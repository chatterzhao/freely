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
```

`rust:preflight` verifies that `cargo`, `rustc`, and `rustup` are available.
If any of them are missing, the script prints the exact missing commands plus the next suggested install/retry steps.
Preferred bootstrap path is `skill:rust-tauri-toolchain-bootstrap`, which uses `rsproxy` instead of the default rustup host.

`rust:preflight:test` verifies that the preflight guidance itself still covers the missing-command summary, install hint, shell reload hint, and retry commands.

`cargo:check:probe` runs the preflight first, then executes:

```bash
cargo check -p freely-probe-bridge
```

## Current blocker

At the moment this workspace does not have `cargo`, `rustc`, or `rustup`, so Rust-side compilation cannot yet be verified locally.
Use the preflight output as the canonical install/retry guidance before attempting real Tauri bridge checks.
