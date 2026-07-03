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

### 触发症状

`write_workcell_state()` 使用 `source "$state_file"` 读取 `LAST_ENTRYPOINT_MODE`。
当 env 文件中含未引号多词值（如 `LAST_WORKER_CLOSEOUT_GATE_COMMAND=freely pr-create-guarded`）时，
bash 将其解释为 `VAR=val command`，导致 daemon 启动时意外执行 `pr-create-guarded` 而失败。

### 根因：workcell-state.env 的 23 个字段混入了三类职责

#### 第一类：daemon 运行时状态（6字段）—— 全局的，属于项目根目录

`DESIRED_RUNTIME_STATE` / `LAST_SUPERVISOR_STATE` / `LAST_AI_STATE` /
`LAST_EXIT_REASON` / `LAST_ENTRYPOINT_MODE` / `LAST_ROLE_HINT`

这些是 daemon 进程的运行时快照，在项目根 `.freely/run/` 下存在是合理的——不管哪个 worktree，daemon 只有一个。`write_workcell_state()` 和 `monitor-ai-cli.sh` 共同维护。

#### 第二类：Worker closeout 上下文（16字段）—— 按 raw_key 索引，应该进 agent_working 表

`LAST_WORKER_OWNER_ISSUE` / `LAST_WORKER_PRE_TESTS_PATH` /
`LAST_WORKER_CLOSEOUT_GATE` / `LAST_WORKER_CLOSEOUT_GATE_COMMAND` /
`LAST_WORKER_CLOSEOUT_TARGET_LANE` / `LAST_WORKER_CLOSEOUT_PROMOTION_GATE` / ...

这些是 manager 委派 worker 时注入的治理数据——告诉 worker 属于哪个 issue、测试路径在哪、走什么门禁。

数据流：manager → `write_worker_verification_contract_file()` → contract.env →
`write_workcell_state()` 读取写入 → `monitor-ai-cli.sh` 在每次 AI cycle 中读回保留。

问题：这是**按 raw_key 索引**的治理数据。`agent_working` 表已有 `raw_key`(PK)、
`branch`、`test_worktree`、`test_branch`，天然适合承载。放在 shell env 文件里导致
① `source` 解析不安全 ② 门禁检查困难 ③ 与运行时状态职责混淆。

#### 第三类：测试时间戳（1字段）—— 测试工位专属

`LAST_STATE_UPDATED_AT`：用于门禁对比 test 分支最新 commit 时间，判断测试是否过期。

### 之前理解的错误

1. **closeout 字段不该在 workcell-state.env** —— 应进 `agent_working` 表，随 worktree 生命周期更新
2. **门禁不应检查 closeout 字段** —— test-pre-merge 是 manager 角色，这些字段永远为空。正确做法是比较时间戳
3. **`monitor-ai-cli.sh:351` 也在用 `source`** —— 同样 unsafe，但 heredoc 已加引号，风险较小

## Scope 判定

### 本 issue 已完成的修复

1. `write_workcell_state()`: `source` → `meta_env_value`
2. `.freely/run/workcell-state.env`: `git rm --cached`
3. `pr-create-guarded`: `--worktree-path` 指向 test-pre-merge
4. `pretests-retirement-gate`: closeout 字段检查 → 时间戳比较
5. `wt-create`: test-pre-merge 创建时初始化 `not_tested` 状态
6. Skill 全链路文档: `wt-create` 后加 `cd` 提醒
7. 门禁报错文案: 用户友好的中文提示

### 需要后续 issue 跟进的重构

1. **closeout 16 字段迁移到 agent_working** —— 新增列，随 worktree 生命周期 upsert/delete
2. **`monitor-ai-cli.sh:351` 的 `source` 改安全读取**
3. **workcell-state.env 精简为 6 运行时字段 + 时间戳**
4. **测试证据文件独立** —— 在 `verification/test-evidence/` 下，门禁直接查 pre-tests.md 的 artifact_ref

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

## Decision: Option A + 附带修复（已完成）；后续 B/C 新开 issue

理由：
1. `meta_env_value` 是最小改动，复用已有安全机制
2. closeout 字段迁移（Option B）和测试证据独立（Option C）是架构重构，
   不应混在同一个 fix 里——先止血，再治本

## Candidate
- candidate_id: C-20260703T003829Z-A
- status: promoted
- milestone: M-20260703T003829Z-A
