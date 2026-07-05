# Brainstorm — macOS bash 3.2 兼容性修复

## 背景

`freely daemon start` 在 macOS 上执行时，daemon 无法正常启动。通过 `bash -x` 逐行 trace 定位到两个 bash 3.2 兼容性 bug。

## 问题分析

### Bug 1：daemon 进程自检测自杀

`resolve_active_supervisor_pid_for_start` 中 `current_runtime_discovery_excluded_pids_csv` 依赖 `BASHPID` 变量。macOS 默认 bash 3.2 不支持 `BASHPID`（bash 4.0+），导致 `discover_supervisor_pid` 在 subshell 中无法正确排除当前进程 PID。daemon-run 通过 pgrep 发现"另一个"daemon（其实是自己），执行 `terminate_pid_with_graceful_wait` 自杀。

### Bug 2：ls 空 glob + pipefail 崩溃

`select_launch_kind` ACP resume detection 路径中：
```bash
recent_log=$(ls -t "$logs_dir"/cycle-*.log 2>/dev/null | head -1)
```
首次运行时没有 `cycle-*.log` 文件，`ls` 返回 exit code 2。`set -o pipefail` 让整个管道失败，bash 3.2 上触发立即 shell 退出（`set -e`），跳过后续 `LAUNCH_KIND_SELECTED="fresh"` 赋值。

## 决策

### 修复 1

在 `resolve_active_supervisor_pid_for_start` 中显式追加 `$$` 到 excluded_pids，并对 `supervisor.pid` 指向自身的情况跳过处理。

### 修复 2

用 `shopt -s nullglob` + 数组检查代替裸 `ls` 管道，仅在 glob 匹配到文件时才执行 `ls`。

## 替代方案评估

- 要求用户升级 bash 到 4.0+：不现实，macOS 默认安装 bash 3.2
- 修改 shebang 为 `#!/usr/bin/env zsh`：影响面太大，不可控
- 在脚本开头检查 bash 版本并报错：用户体验差，且阻止了其他可能正常工作的功能

## 结论

两个修复都是最小化的防御性改动。不影响核心逻辑，不改变架构，不引入新的依赖。
