---
kind: raw
priority: P1
phase_state: absorbed
absorbed_into: I-20260514T103532Z-A
status: closed
source: chat-inbox
created_at: '2026-05-15T12:56:10Z'
title: freely 启动时自动检测安装路径并写入项目配置
platform_ids:
  github:
    issue_id: '345'
    url: https://github.com/chatterzhao/freely/issues/345
    synced_at: '2026-05-15T12:56:16Z'
updated_at: '2026-05-15T12:56:16Z'
primary_platform: github
platform_state: open
---

## 问题
`workspace_root_for_project` 和 `runtime_script_for_project` 返回项目路径（`$project/docs/system/workspace`），导致安装版启动后 Worker 从项目仓库加载旧 freely 脚本而非安装版。

## 实际修复方案
不需要新增配置项。`SELF_ROOT` 已能从 `${BASH_SOURCE[0]}` 自动检测启动位置——安装版指向 `~/.freely/versions/...`，仓库版指向 repo 根目录，工位版指向 worktree 路径。两处修改：

1. `workspace_root_for_project`：简化为直接返回 `$SELF_ROOT/docs/system/workspace`
2. `runtime_script_for_project`：`$project/docs/.../freely` → `$SELF_ROOT/docs/.../freely`

## 关闭理由
根因已修复，方案比原期望更简单——不需要新增配置字段，利用已有的 SELF_ROOT 自动检测。提交 38903ab8 和 3554b7b6。
