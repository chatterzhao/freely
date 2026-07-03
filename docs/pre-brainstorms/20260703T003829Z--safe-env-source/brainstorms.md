---
b1_id: B1-20260703T003829Z
phase_state: completed
source_raw: raw-20260703T003829Z
source_url: https://github.com/chatterzhao/freely/issues/3699
produced_candidate: C-20260703T003829Z-A
created_at: 2026-07-03
---

# B1_IBM: workcell-state.env unsafe source 导致 daemon 启动时命令注入

## Input
- 来源: `docs/issues/raw-20260703T003829Z/issue.md`
- 平台: GitHub #3699, Gitee IJYGUQ
- 严重程度: P1 — daemon 无法启动

## Problem

`write_workcell_state()` 在 `docs/system/workspace/scripts/runtime/freely:8426` 使用
`source "$state_file"` 读取 `LAST_ENTRYPOINT_MODE`。

当 `workcell-state.env` 中包含未加引号的多词值（如
`LAST_WORKER_CLOSEOUT_GATE_COMMAND=freely pr-create-guarded`）时，
bash 将其解释为 `VAR=val command` 语法——设置变量后执行命令。
导致 `pr-create-guarded` 在 daemon 启动期间被意外执行，在 develop
分支上因分支保护检查而失败。

此外，`.freely/run/workcell-state.env` 被错误地提交到了 git
（尽管 `.gitignore` 已有 `.freely/` 规则），每次 checkout 都会
恢复含未引用值的损坏版本。

## Scope 判定

这是一个独立的 bug，范围明确：
- 影响模块：`write_workcell_state()` 函数
- 影响文件：`docs/system/workspace/scripts/runtime/freely`
- 附带清理：`.freely/run/workcell-state.env` 从 git 跟踪中移除
- 不涉及其他模块或架构变更

## Brainstorm

### Option A: 用 meta_env_value 替换 source（推荐）

`meta_env_value` 是项目中已有的安全 env 值读取函数，使用
`awk -F '"'` 按双引号分割取值，不会执行 shell 命令。

改动：将 `write_workcell_state()` 中的 4 行 `source` 逻辑替换为
1 行 `meta_env_value` 调用。

优点：
- 最小改动（删除 4 行，增加 1 行）
- 复用已有安全机制，一致性高
- 不影响其他调用方
- `meta_env_value` 已被项目中多处使用（verification contract 读取等）

缺点：
- 依赖 `meta_env_value` 的双引号解析约定（`KEY="value"` 格式）

### Option B: 写入前对值做 shell 转义

在 `cat > "$state_file" <<EOF` 生成 env 文件时，对每个值调用
`printf '%q'` 做 shell 转义。

优点：
- 从写入端防止问题

缺点：
- 改动面大（需要改所有 write_workcell_state 调用方）
- `printf '%q'` 在不同 bash 版本中行为不一致（macOS vs Linux）
- 生成的 env 文件对人类不友好（转义后的格式）
- 治标不治本——如果文件被外部工具修改仍然会出问题

### Option C: 用 grep + cut 手动提取值

用 `grep "^LAST_ENTRYPOINT_MODE=" "$state_file" | cut -d= -f2-` 提取值。

优点：
- 不依赖双引号格式

缺点：
- 引入新的值提取模式，与已有的 `meta_env_value` 不一致
- 对于包含 `=` 的值处理不正确
- 增加维护负担

## Decision: Option A — 用 meta_env_value 替换 source

理由：
1. `meta_env_value` 是项目已有的标准安全读取方式
2. 改动最小、最安全
3. 整个 `write_workcell_state()` 的 heredoc 模板已经用双引号格式
   （`KEY="value"`），与 `meta_env_value` 的解析约定一致
4. 附带修复：从 git 跟踪中移除 `.freely/run/workcell-state.env`
   （`.gitignore` 已有 `.freely/` 规则，该文件不应被跟踪）

## Candidate
- candidate_id: C-20260703T003829Z-A
- status: promoted
- milestone: M-20260703T003829Z-A
