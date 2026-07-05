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
- 来源: `docs/B1-docs/raw-20260703T003829Z/issue.md`
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

#### 第二类：Worker closeout 上下文（16字段）—— 冗余副本，权威源已在别处

这些 16 个字段是 `worker-verification-contract.env` 的缓存副本，
`write_workcell_state()` 从 contract 读出再写入 workcell-state.env，
然后 `monitor-ai-cli.sh` 原样保留。但它们的真实数据已经在其他地方有权威源：

| 冗余字段 | 权威源 | 如何获取 |
|---------|--------|---------|
| `LAST_WORKER_OWNER_ISSUE` | agent_working.raw_key → I-* issue | raw_key 就是 issue key |
| `LAST_WORKER_PRE_TESTS_PATH` | I-* issue `pre_tests_path` 字段 | 读 I-* issue 文档 |
| `LAST_WORKER_VERIFICATION_ARTIFACT_DIR` | I-* issue `verification_artifact_dir` | 同上 |
| `LAST_WORKER_CLOSEOUT_GATE_COMMAND` | **常量** — `freely pr-create-guarded` | 写死在门禁逻辑里 |
| `LAST_WORKER_CLOSEOUT_TARGET_LANE` | **分支类型决定** — test-pre-merge → `premerge-integration` | 从分支名推导 |
| `LAST_WORKER_CLOSEOUT_PROMOTION_GATE` | **分支类型决定** — fix/feature → `develop_merge` | 同上 |
| `LAST_WORKER_REQUIRED_TEST_LANES_CSV` | B2 pre-tests.md 中定义 | 从治理文档读取 |
| 其他 closeout 字段 | 同上模式 | 同上 |

**正确做法不是"把 16 个字段搬到 agent_working"，而是：**
1. 需要这些值时，从权威源读取——I-* issue 文档、分支名、agent_working 表
2. workcell-state.env 里删掉这 16 个冗余缓存
3. 能推导的推导（如 closeout_gate_command 是常量），不存副本

#### 第三类：测试证据 —— 独立文件，仅在测试工位

`LAST_STATE_UPDATED_AT` 的职责是让门禁判断"测试跑过了没有"。
这个职责不应该混在 workcell-state.env（运行时状态文件）里，
应该独立为 **test-gate.env**，由 wt-create 在测试工位创建。

### 文件分布设计

```
项目根目录 (develop/fix/feature)         测试工位 (test-pre-merge-*)
├── .freely/run/                         ├── .freely/run/
│   └── workcell-state.env               │   ├── workcell-state.env    ← daemon 运行时状态，全局一致
│       (6 运行时字段 + 时间戳)            │   └── test-gate.env    ← 测试证据，仅此工位有
│                                         │       wt-create 创建
│                                         │       daemon 启动/停止时更新
│                                         │       门禁检查这个文件
```

**workcell-state.env**（精简后，所有工位都有）：
```
DESIRED_RUNTIME_STATE="stopped"
LAST_SUPERVISOR_STATE="down"
LAST_AI_STATE="down"
LAST_EXIT_REASON="operator_stop"
LAST_ENTRYPOINT_MODE="daemon"
LAST_ROLE_HINT="manager"
LAST_STATE_UPDATED_AT="2026-07-03T02:01:59Z"
```

**test-gate.env**（仅 test-pre-merge 工位有，wt-create 创建）：
```
TEST_STATUS="not_tested"           # not_tested → testing → completed
LAST_TESTED_AT="1970-01-01T00:00:00Z"
LAST_TESTED_COMMIT=""              # 测试时 HEAD 的 commit hash
```

### 生命周期

1. **wt-create**：创建 test-pre-merge 时写入 test-gate.env，初始 `not_tested`
2. **daemon 启动**：将 `TEST_STATUS` 更新为 `testing`，`LAST_TESTED_AT` 更新
3. **daemon 停止**：将 `TEST_STATUS` 更新为 `completed`，记录 `LAST_TESTED_COMMIT`
4. **门禁**：对比 `LAST_TESTED_COMMIT` vs HEAD；`LAST_TESTED_AT` 作为兜底时间戳
5. **test-pre-merge 删除**：文件随工位一起删除

### 门禁检查逻辑

```
if test-gate.env 不存在:
    → "请先在测试工位运行 daemon"
if LAST_TESTED_COMMIT != HEAD:
    → "测试工位有新提交未重新测试"
if TEST_STATUS == "not_tested":
    → "测试工位还没有运行过 daemon"
else:
    → 通过
```
门禁直接查 SQL 即可，不需要在 env 文件里再存一份。

### 之前理解的错误

1. **closeout 字段不该在 workcell-state.env** —— 它们是 worker-verification-contract.env 的冗余缓存。应该删除，需要时从权威源读：I-* issue frontmatter、分支名推导、agent_working 表
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

1. **删掉 workcell-state.env 中 16 个 LAST_WORKER_* 字段** —— 冗余缓存
2. **门禁从权威源读值** —— 不依赖 closeout 副本
3. **`monitor-ai-cli.sh:351` 的 `source` 改安全读取**
4. **其他 `source` workcell-state.env 的调用点全部改安全读取**

## 全量消费者分析与重构方向

### 消费者 1：`write_workcell_state()` (line 8424)

```bash
entrypoint_mode="$(meta_env_value "$state_file" "LAST_ENTRYPOINT_MODE")"
```
- 读什么：`LAST_ENTRYPOINT_MODE`
- 权威源：`WORKCELL_ENTRYPOINT_MODE_OVERRIDE` 环境变量 > state file
- 状态：**已修复**（source → meta_env_value）
- 重构方向：不改。entrypoint_mode 是 daemon 进程级配置，env var 兜底合理

### 消费者 2：`monitor-ai-cli.sh` (line 324-397)

大量 `source "$state_file"` 然后读全部 23 个字段，更新运行时字段后全部写回。
closeout 字段在此是纯透传——读出来，什么也不改，原样写回。

- 读什么：23 个字段全部
- 运行时 6 字段的权威源：**daemon 进程自身**（它是 AI cycle 的写者）
- closeout 16 字段的权威源：**worker-verification-contract.env**
- 重构方向：
  1. `source` → `meta_env_value` 逐字段安全读取（只读需要的）
  2. 运行时字段继续从 workcell-state.env 读
  3. **closeout 字段改为直接从 worker-verification-contract.env 读**——不经过 workcell-state.env 中转
  4. 写回时只写运行时字段 + 时间戳，不再写 closeout

### 消费者 3：`start-lead-agent.sh` prompt_role_for_project() (line 142-164)

`prompt_role_for_project()` 用 source 读 `LAST_ROLE_HINT`。
closeout 字段已经通过 `worker_verification_contract_launchable()` 从 contract 文件直读——不从 workcell-state.env 读。

- 读什么：仅 `LAST_ROLE_HINT`（closeout 已从 contract 读）
- 权威源：daemon 写入的运行时记录，`effective_runtime_role_for_project()` 作为兜底
- 重构方向：source 改为 meta_env_value 读 LAST_ROLE_HINT，空则 fallback 到函数推导

### 消费者 4：状态展示函数 (lines 1716-1950)

多个函数 `source` workcell-state.env 来展示 baseline/live status：
- `DESIRED_RUNTIME_STATE` ← baseline status (line 1716)
- `LAST_EXIT_REASON` ← live status (line 1735)
- `LAST_STATE_UPDATED_AT` ← live status (line 1830)
- `LAST_ROLE_HINT` ← live status (line 1913)
- `LAST_SUPERVISOR_STATE` ← active_runtime check (line 3495)

这些都是**运行时状态读取**，workcell-state.env 就是它们的正确源（daemon 实时写入的文件快照）。

- 重构方向：`source` → `meta_env_value` 逐字段安全读取

### 消费者 5：`startup_self_heal_*` (lines 5464-5616)

```bash
source "$state_file"  # 判断 daemon 是否 alive
```

- 读什么：`DESIRED_RUNTIME_STATE`, `LAST_EXIT_REASON`
- 权威源：workcell-state.env（daemon 运行时写入）
- 重构方向：`source` → `meta_env_value`

### 消费者 6：`refresh_workcell_state_projection()` (line 12051)

```bash
desired_state="$(meta_env_value "$state_file" "DESIRED_RUNTIME_STATE")"
```

- 状态：**已经是 meta_env_value**，无需改动

### 消费者 7：loop guard (lines 9338-9489)

```bash
source "$state_file"  # 读 DESIRED_RUNTIME_STATE, LAST_EXIT_REASON, LAST_STATE_UPDATED_AT
```

- 读什么：运行时字段
- 权威源：workcell-state.env（daemon 运行时）
- 重构方向：`source` → `meta_env_value`

### 消费者 8：worktree fleet status (Python, line 16475)

```python
state_file = os.path.join(wt_path, ".freely", "run", "workcell-state.env")
# 读取 DESIRED_RUNTIME_STATE, LAST_EXIT_REASON
```

- 读什么：运行时状态
- 权威源：workcell-state.env
- 重构方向：**Python 代码已经用 `line.split("=", 1)` 安全解析**，无 source 风险

### 重构优先级

| 优先级 | 改动 | 影响 |
|--------|------|------|
| P0 | **创建 test-gate.env**：wt-create 写入 + daemon 更新 + 门禁检查 | 测试证据从 workcell-state.env 独立出来 |
| P0 | **精简 workcell-state.env**：删掉 16 个 LAST_WORKER_* | 职责清晰，只剩运行时状态 |
| P0 | `monitor-ai-cli.sh` source 改 meta_env_value + 停止写 closeout | 消除与 write_workcell_state 同源的命令注入向量 |
| P0 | `start-lead-agent.sh` role_hint 改为调函数、closeout 从 prompt 读 | 消除 source + 冗余读取 |
| P1 | 其他 shell `source` → `meta_env_value`（6处） | 消除所有 unsafe source |
| P2 | Python fleet status 不用改（已安全） | — |

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
