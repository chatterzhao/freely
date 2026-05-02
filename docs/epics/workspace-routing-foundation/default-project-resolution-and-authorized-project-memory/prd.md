# PRD: default-project-resolution-and-authorized-project-memory

## Objective

把 Freely 的 CLI-first 人类入口收束到“默认解析当前项目”，降低 `--project` 在常见场景中的重复负担。

## User Story

用户已经在某个 Freely 项目目录中工作时，希望直接运行 `freely chat`、`freely tui`、`freely baseline-status`、`freely intake status`，而不是每次都补绝对路径。

## Non-Goals

- 不把全局记忆升级成第二套项目配置真源。
- 不把任意外部目录静默当成项目。
