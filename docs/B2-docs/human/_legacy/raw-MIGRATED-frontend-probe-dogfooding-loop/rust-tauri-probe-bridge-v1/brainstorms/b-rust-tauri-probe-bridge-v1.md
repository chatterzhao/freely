# Brainstorm: rust-tauri-probe-bridge-v1

## Goal

为 `Frontend Probe v0` 提供 day-1 可接入的真实 Rust/Tauri bridge。

## Key decisions

1. day-1 工程落点优先采用根目录 `src-tauri/ + Cargo.toml`。
2. day-1 保持单 `probe_send_command` 入口，不提前拆成多条 Tauri command。
3. day-1 事件只覆盖 frontend 已消费的最小闭环，不追求完整 runtime 事件谱系。

## Open edges

1. `probe_server_event` 的 payload 是否需要完全复用 frontend manifest，还是允许后端先实现最小子集。
2. snapshot 的 terminal/run/session 字段是否需要留空占位，还是直接输出最小单实例结构。
