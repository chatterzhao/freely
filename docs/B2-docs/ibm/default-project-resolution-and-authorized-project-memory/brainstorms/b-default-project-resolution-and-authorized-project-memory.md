# Brainstorm: default-project-resolution-and-authorized-project-memory

- source: `docs/B1-docs/raw-20260320-0018/brainstorms.md`
- status: `materialized`

## Summary

Freely 的 CLI-first 路径应该默认解析当前项目，而不是要求 `--project` 成为常态输入。

## Guardrails

- `--project` 只作为 override。
- 解析优先级必须稳定。
- 全局已授权项目记忆只做轻量索引，不做第二套配置真源。

