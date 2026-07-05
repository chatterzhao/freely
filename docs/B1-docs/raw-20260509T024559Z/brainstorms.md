# Brainstorm: 多项目、多 Issue 并发隔离

- 来源: raw-20260509T024559Z (#265)
- 日期: 2026-05-09
- 核心问题: 如何保证 AI 不工作在错误工位？

## 隔离模型

```
project-a/                          # 项目 A（如 Freely 自己）
  ├── milestones.md                 # active issue 列表
  └── project-a-worktrees/          # 所有工位
      ├── test-pre-merge-{key1}-{slug1}   # issue 1 的 test
      ├── fix/raw-{key1}-{slug1}          # issue 1 的可写工位
      ├── test-pre-merge-{key2}-{slug2}   # issue 2 的 test
      └── feature/raw-{key2}-{slug2}      # issue 2 的可写工位

project-b/                          # 项目 B（用户的项目）
  ├── milestones.md
  └── project-b-worktrees/
      └── ...
```

## 隔离保证（三层）

### 第1层: Git 天然隔离

`git -C $project_root worktree list` 只返回该 repo 的工位。不同项目在不同 git repo，不可能跨。

### 第2层: raw-key 精确匹配

工位名和分支名都包含 raw-key：
- `test-pre-merge-{key}-{slug}` → 包含 key
- `fix/raw-{key}-{slug}` → 包含 key
- `feature/raw-{key}-{slug}` → 包含 key

AI 永远通过 raw-key 搜索工位：
```bash
git -C $project_root worktree list --porcelain | grep "raw-${raw_key}"
```

### 第3层: 工位归属验证

任何操作前验证工位在项目边界内：
```bash
project_path_is_under_worktrees_root "$project_root" "$target_worktree"
```

如果 target_worktree 不在 `{project}-worktrees/` 下 → 拒绝。

## Worker 定位流程

```
Manager 写 continuity: "delegate worker for raw-{key}"

Runtime 解析:
  1. raw_key = extract from continuity
  2. project_root = from daemon config
  3. candidates = git -C $project_root worktree list | grep "raw-${raw_key}"
  4. writable = filter: branch starts with fix/ or feature/
  5. validate: project_path_is_under_worktrees_root "$project_root" "$writable"
  6. cd $writable && launch worker
```

### 找不到可写工位时

```
→ 报错: "raw-{key} 没有可写工位（fix/* 或 feature/*）"
→ 提示主管: 用 wt-create 创建工位
→ 不 fallback 到 develop 或 test-pre-merge
```

### 多个可写工位时

```
→ 选择最近的（mtime）或优先 fix/ > feature/
→ 记录选择理由到 launch log
```

## 多项目并发

```
freely daemon start --task-mode auto --project ~/freely,~/my-app

Manager patrol:
  for each project_root:
    1. 读 milestones.md → active issues
    2. 读 scan → 任务优先级
    3. 跨项目排序（P0 > P1 > ...）
    4. 产出 per-project continuity + worker prompts
    5. Worker dispatch 到各自项目的工位
```

多项目之间通过 `project_root` 隔离。Worker A 在 `~/freely-worktrees/fix/raw-xxx`，Worker B 在 `~/my-app-worktrees/feature/raw-yyy`。不同 git repo，不同 worktree root，天然不干扰。

## 门禁防跨项目

pr-merge-guarded 增加检查:
```bash
# 验证 source branch 的 worktree 在 project_root 的 worktrees 下
if ! project_path_is_under_worktrees_root "$project_root" "$source_worktree"; then
  error "工位 $source_worktree 不属于项目 $project_root"
fi
```

## Manager 不绑定工位

Manager daemon 本身不"住"在任何 worktree。它从 project root 运行:
```
cd $project_root
freely daemon start --project $project_root
```

Manager 使用的工具:
- `git -C $project_root worktree list` — 查看所有工位
- `git -C $project_root log` — 查看 develop 历史
- `freely task-scan --project $project_root` — 扫描任务

Manager **永远不在 test-pre-merge 或 fix/feature 工位中 cd**——它只读 project root 的数据做决策。Worker 才 cd 到工位。

## 与现有机制的兼容

| 现有机制 | 保留/改 | 说明 |
|---------|---------|------|
| wt-create 创建 test+fix/feature 配对 | 保留 | 工位命名不变 |
| raw-key 在工位名中 | 保留 | 定位基础 |
| project_worktrees_root_for_path | 保留 | 边界验证 |
| looks_like_project_root | 保留 | 项目识别 |
| daemon 绑定 test 工位 | **移除** | daemon 从 project root 运行 |
| worker_prompt_resolved_worktree | **重写** | 增加 raw-key 搜索 + 归属验证 |
| pr-merge-guarded 不检查项目边界 | **增加** | 跨项目防护 |

## ACP Bridge 隔离分析

### 当前 ACP 架构

```
每个 test-pre-merge 工位:
  ├── ACP bridge (acp-bridge.py, 常驻进程)
  │   ├── socket: /tmp/freely-acp-{hash(project_path)}.sock
  │   └── 启动 claude-agent-acp 子进程（stdin/stdout JSON-RPC）
  └── daemon 通过 socket 与 bridge 通信
```

- socket 路径由 project_path 的 SHA256 hash 决定
- 每个项目只有一个 socket
- `claude-agent-acp` 每次 end_turn 退出，bridge 重启

### 多项目/多 issue 下 ACP 的变化

**当前限制**：
- 一个 daemon 实例绑定一个 test 工位
- 一个 ACP bridge 绑定一个项目路径
- `claude-agent-acp` 单进程，单 session

**目标模型**：
```
daemon@project_root
  ├── ACP bridge per project（不同 socket 路径，按 project hash 隔离）
  │   └── claude-agent-acp per worker session
  │       ├── worker-A → session-A (on fix/raw-{keyA})
  │       ├── worker-B → session-B (on feature/raw-{keyB})
  │       └── ...
  └── manager patrol → session-M (read-only, project-level)
```

**隔离保证**：
1. **Socket 隔离**：不同项目有不同 socket path（hash 不同），天然隔离
2. **Session 隔离**：`session/new` 创建独立 session，cwd 指向对应工位
3. **CWD 隔离**：worker 的 `cwd` 参数设为其 fix/feature 工位路径
4. **进程隔离**：每个 worker 是独立的 `claude-agent-acp` 子进程

**ACP 不限制并发**：
- `claude-agent-acp` 支持多个 `session/new` → 多个独立 session
- Bridge 的 `_send_request` 是线程安全的（有 `server_lock`）
- 每个 session 的 `session/prompt` 操作互不干扰
- 限制在于：多个 worker session 共享一个 `claude-agent-acp` 进程，内存/CPU 争用

**潜在瓶颈**：
- `claude-agent-acp` 单进程处理多 session → 如果 worker A 在处理大量 tool calls，worker B 的 prompt 需排队
- 解决：每个 worker 可以 fork 独立的 `claude-agent-acp` 进程（bridge 已支持 `_restart_server`）

### 多项目 ACP 部署

```
freely daemon start --task-mode auto --project ~/freely,~/my-app

~/$FREELY_HOME/
  ├── freely daemon（主进程，跨项目调度）
  │
  ├── ACP bridge for ~/freely
  │   ├── socket: /tmp/freely-acp-{hash(freely)}.sock
  │   └── claude-agent-acp
  │       ├── session: manager patrol
  │       ├── session: worker-raw-keyA
  │       └── session: worker-raw-keyB
  │
  └── ACP bridge for ~/my-app
      ├── socket: /tmp/freely-acp-{hash(my-app)}.sock
      └── claude-agent-acp
          ├── session: manager patrol
          └── session: worker-raw-keyC
```

**多项目隔离**：
- 不同项目 = 不同 git repo = 不同 ACP bridge = 不同 socket
- worker-A 的 session cwd = `~/freely-worktrees/fix/raw-keyA`
- worker-C 的 session cwd = `~/my-app-worktrees/fix/raw-keyC`
- 跨项目不可能串工位（cwd 指向不同 worktree root）

## 架构本质

多项目、多 issue、多工位——本质是同一模式在不同层级：

| 层级 | 隔离单位 | 定位方式 |
|------|---------|---------|
| 项目 | git repo | project_root |
| Issue | raw-key | git worktree list \| grep raw-{key} |
| 工位 | fix/feature 分支 | 分支名含 raw-key |
| Session | session ID | ACP session/resume，cwd 绑定工位 |

每层都有独立的 key 空间和隔离边界。不需要发明新的隔离机制——git、ACP socket、session cwd 已经提供了所需的一切。

## 项目结构

每个项目（包括 Freely 自己）结构一致：

```
项目根目录（main + develop 所在）
  ├── main
  ├── develop
  ├── docs/
  ├── milestones.md
  └── {project}-worktrees/          ← 所有 issue 工位
      ├── test-pre-merge-{key1}-{slug}   ← issue 1 的 test
      ├── fix/raw-{key1}-{slug}          ← issue 1 的可写工位
      ├── test-pre-merge-{key2}-{slug}   ← issue 2 的 test
      └── feature/raw-{key2}-{slug}      ← issue 2 的可写工位
```

## --project 参数

`--project <your-dev-project-root-path>` 指向 **main/develop 所在的根目录**。不是 test 工位。

```
Freely 开发 Freely:
  freely daemon start --project /path/to/freely

用户开发自己的应用:
  freely daemon start --project ~/my-app
```

两者模型完全一致。

## 端到端调试

test-pre-merge 是 e2e 验证环境——fix/feature 代码合并进去后，在 test 上启动 Freely 验证：

```
fix/raw-{key} → merge → test-pre-merge-{key}
  → cd test-pre-merge-{key}
    → freely daemon start --project <项目根>
      → 端到端测试
```

fix 模式：test 上可 dirty 临时测试，但 commit 必须回 fix 工位。

## App1 vs App2 分离模型

### 打包安装

Freely 打包后安装到本机，成为全局命令：

```
# 安装后
freely daemon start --project <path>
```

### 两个角色的分离

| | App1: Freely CLI | App2: 被开发的项目 |
|---|-----------------|-------------------|
| 位置 | 全局安装（如 /usr/local/bin/freely） | --project 指向的目录 |
| 代码 | 安装版本，不可变 | 被开发的源码，在工位中修改 |
| 职责 | 调度、patrol、worker launch | 被开发、被测试 |
| 狗粮时 | 不变 | /path/to/freely（Freely 自己） |

### 为什么这解决了混淆

当前 `./bin/freely` 和 `--project /path/to/freely` 指向同一个 repo——容易混淆"工具代码"和"被开发的代码"。

打包后：
```
freely daemon start --project /path/to/freely
  ↑ App1                 ↑ App2

App1 的代码: /usr/local/bin/freely（安装版本，不动）
App2 的代码: /path/to/freely（被 Freely 开发的 Freely 源码）
```

开发其他项目时：
```
freely daemon start --project ~/my-app
  ↑ App1                 ↑ App2（用户的另一个项目）
```

### 用户启动位置

不管用户在 main、develop、还是 test-* 执行 `freely daemon start`：
- `freely` 命令本身在哪里不重要（已全局安装）
- `--project` 指定被开发的项目的根目录
- 项目根目录下有 main/develop + worktrees/
- daemon 从项目根开始工作

### 启动时不判断当前分支

`freely daemon start` 不判断"我在哪个分支启动"。它只关心：
1. `--project` 指向一个合法的项目根（looks_like_project_root）
2. 项目根下面有 worktrees/ 目录
3. milestones.md 中有 active issue 可开发

daemon 自己需要的工作目录是项目根（读 milestones.md、scan、worktree list），不依赖当前分支。

## 自举开发循环

Freely 开发 Freely 的唯一闭环：

```
fix/raw-{key} 或 feature/raw-{key}
  │
  ├─ 写代码 + commit
  ├─ merge → test-pre-merge-{key}
  │
  ├─ cd test-pre-merge-{key}
  ├─ 打包: freely-package
  ├─ 安装: 替换全局 freely 命令
  │
  ├─ freely daemon start --project /path/to/freely
  │   （安装版 freely 开发 Freely 自己）
  │
  ├─ e2e 测试通过 → merge test-pre-merge → develop
  └─ 需要继续改 → 回到 fix/feature 工位
```

**限制**：同一时间只能测试一个 issue（安装替换是全局操作）。

**并发**：多个 issue 可以同时在各自的 fix/feature 工位开发。打包测试排队即可。

## 主管-Worker 交接管道重构

### 现状

```
Manager AI cycle
  → 写 continuity.md（markdown，AI 自由格式）
  → 写 exit-contract.env（env 格式，仅 CSV 列表）
  → 写 worker-prompts/*.txt（markdown，Worktree/Branch header）

Runtime launch
  → 解析 continuity.md → 提取 worker prompt 路径（awk regex）
  → 解析 worker prompt → 提取 Worktree/Branch header（awk regex）
  → 不校验 worktree/branch 合法性
  → 启动 worker（可能在 develop 上）
```

### 已有的基础设施

`worker_delegation` 表（SQLite，已存在）：

| 字段 | 类型 | 说明 |
|------|------|------|
| delegation_id | TEXT | 唯一委派 ID |
| prompt_file | TEXT | worker prompt 路径 |
| worktree | TEXT | **工位路径** |
| branch | TEXT | **分支名** |
| intent_kind | TEXT | 任务类型 |
| owner_issue | TEXT | raw-key |
| status | TEXT | pending/launched/completed/blocked |
| launched_at | TEXT | 启动时间 |
| completed_at | TEXT | 完成时间 |
| exit_kind | TEXT | 退出方式 |
| session_id | TEXT | ACP session ID |

`worker-store.py`（已存在）：
- `init` — 建表
- `migrate --project` — 从旧 exit_contract 迁移
- `mark-stale --timeout-minutes` — 标记超时 stale

### 目标管道

```
Manager AI cycle
  → 写 exit-contract.json（machine-readable，带 worktree/branch）
      {
        "exit_kind": "delegate_workers",
        "workers": [
          {
            "delegation_id": "20260509T024559Z-001",
            "raw_key": "20260509T024559Z",
            "worktree": "/path/to/fix/raw-20260509T024559Z-multi-project-isolation",
            "branch": "fix/raw-20260509T024559Z-multi-project-isolation",
            "prompt_file": "/path/to/worker-prompts/p1.txt"
          }
        ]
      }

Runtime:
  1. 读 exit-contract.json
  2. 对每个 worker:
     a. 校验 branch 是 fix/* 或 feature/* → 否则拒绝
     b. 校验 worktree 在 project-worktrees/ 下 → 否则拒绝
     c. INSERT INTO worker_delegation (delegation_id, worktree, branch, prompt_file, status='pending')
     d. cd worktree → launch worker AI (ACP fork session)
     e. worker 完成 → UPDATE status='completed', exit_kind='worker_done'
  3. 下一轮 Manager 读 worker_delegation 表获取完成状态
```

### ACP Fork 模型

不再启动新 daemon。Worker AI 作为 ACP fork session：

```
Manager ACP bridge (常驻)
  ├── session/manage (Manager patrol)
  └── session/fork-{delegation_id} (Worker)
      → session/new → cwd=worktree → session/prompt
      → AI 处理（tool calls）
      → end_turn → exit contract
      → UPDATE worker_delegation SET status='completed'
```

每个 worker 是独立的 ACP session，不是独立进程。共享一个 ACP bridge，通过 session ID 隔离。

### 并发控制

`worker_delegation` 表天然支持多 worker 并发：
- `SELECT * FROM worker_delegation WHERE status='pending'` — 待 launch
- `SELECT * FROM worker_delegation WHERE status='launched'` — 运行中
- `SELECT * FROM worker_delegation WHERE raw_key='xxx'` — 同一 issue 的 worker 历史
- `SELECT * FROM worker_delegation WHERE branch='fix/*'` — 按工位类型过滤

同一 raw-key 可以有多条记录（多次委派），按 delegation_id 区分。追加记录，不覆盖。

### 多项目扩展

每个项目有独立的 `freely.db` → 独立的 `worker_delegation` 表：
- `~/freely/.freely/freely.db` → Freely 项目的 worker 表
- `~/my-app/.freely/freely.db` → 用户项目的 worker 表

Manager patrol 跨项目时，读各项目的 `worker_delegation` 表汇总 worker 状态。

### 与 #264 的关系

#264（worker launch 验证 fix/feature）是这个管道的**最后一道防线**：
- Manager 指定了错误工位 → exit-contract.json 已有错误
- Runtime 校验 branch 不是 fix/feature → 拒绝 launch
- 报错回写：UPDATE worker_delegation SET status='rejected', exit_kind='invalid_worktree'

### 不做

- 不改 `worker_delegation` 表结构（已够用）
- 不改 `worker-store.py` 核心逻辑（已存在）
- 不删除 continuity.md（保留跨周期上下文职能）
- 不删除 exit-contract.env（渐进迁移，先支持 JSON 再废弃 env）

## 交接表设计（替换文件）

### 表名：`handoffs`

不再分主管/worker 两个文件。一个表，role 字段区分。

```sql
CREATE TABLE handoffs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  handoff_id TEXT NOT NULL UNIQUE,       -- "20260509T024559Z-001"
  role TEXT NOT NULL,                    -- 'manager' | 'worker'
  raw_key TEXT NOT NULL,                 -- issue key，所有记录都有
  worktree TEXT,                         -- worker 有值，manager 为 NULL
  branch TEXT,                           -- worker 有值，manager 为 NULL
  prompt_file TEXT,                      -- 交接文档路径
  parent_handoff_id TEXT,               -- worker 指向触发它的 manager handoff
  intent_kind TEXT,                      -- patrol|cleanup|implementation
  status TEXT NOT NULL DEFAULT 'pending',-- pending|launched|completed|rejected|blocked
  exit_kind TEXT,                        -- delegate_workers|worker_done|stop_ai|invalid_worktree
  session_id TEXT,                       -- ACP session
  launched_at TEXT,
  completed_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### INSERT vs UPDATE 规则

**INSERT（新记录）**：
- Manager 完成 patrol → INSERT role=manager, status=completed
- Manager 委派 worker → INSERT role=worker, status=pending, parent_handoff_id=manager 的 id
- 同一 issue 多次委派 → 多条 role=worker 记录，通过 parent_handoff_id 关联到不同 round

**UPDATE（状态变更）**：
- Worker launch 成功 → UPDATE status=launched, launched_at=now, session_id=xxx
- Worker 完成 → UPDATE status=completed, exit_kind=worker_done, completed_at=now
- Worker 拒绝（工位不对）→ UPDATE status=rejected, exit_kind=invalid_worktree
- Worker 阻塞 → UPDATE status=blocked, exit_kind=worker_blocked

### 多轮交接示例

```
Round 1:
  Manager patrol #1
    INSERT handoff_id=M1, role=manager, raw_key=keyA, status=completed
    INSERT handoff_id=W1, role=worker, raw_key=keyA, worktree=fix/raw-keyA, parent=M1, status=pending
    → launch → UPDATE W1 status=launched
    → done  → UPDATE W1 status=completed, exit_kind=worker_done

Round 2:
  Manager patrol #2（读了 W1 的结果）
    INSERT handoff_id=M2, role=manager, raw_key=keyA, status=completed
    发现 W1 没做完，重新委派:
    INSERT handoff_id=W2, role=worker, raw_key=keyA, worktree=fix/raw-keyA, parent=M2, status=pending
    同时委派另一个 issue:
    INSERT handoff_id=W3, role=worker, raw_key=keyB, worktree=feature/raw-keyB, parent=M2, status=pending
```

### 查询灵活性

```sql
-- 某 issue 的所有活跃 worker
SELECT * FROM handoffs WHERE raw_key='xxx' AND role='worker' AND status IN ('pending','launched');

-- 最新 manager continuity
SELECT * FROM handoffs WHERE role='manager' ORDER BY created_at DESC LIMIT 1;

-- 某工位是否已有运行中的 worker（防重复 launch）
SELECT COUNT(*) FROM handoffs WHERE worktree='xxx' AND status='launched';

-- 跨 issue worker 完成率
SELECT raw_key, COUNT(*) as total,
  SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as done
FROM handoffs WHERE role='worker' GROUP BY raw_key;

-- 某 round 的所有 worker（通过 parent_handoff_id）
SELECT * FROM handoffs WHERE parent_handoff_id='M2';
```

### 历史保留策略

- **issue 在开发中**：所有记录保留，追加不覆盖
- **issue 收口（工位删除）**：记录保留不删除，作为审计 trail
- **不软删除**：不设 archived_at。SQLite 千万行无压力，Freely 的 issue 数量不会到那个量级
- **清理时机**：未来如果需要，按 raw_key 批量删除已收口的。但默认保留

### 迁移路径

1. 停止写 env/md 文件
2. worker-store.py 建 `handoffs` 表
3. Manager AI 输出 JSON → runtime 解析 → INSERT 到表
4. 旧的 worker-prompts/ 目录保留为文本备份，不再作为 launch 数据源
5. 表成为 worker launch 的唯一数据源

## 三层职责拆分

```
#267 交接表（数据层）
  → 建表、读写、迁移
  → INSERT: manager 产出 + worker 委派
  → UPDATE: status 流转（pending→launched→completed/rejected/blocked）
  → SELECT: 按 raw_key/worktree/status/role 多维查询

#264 验证（执行层）
  → 从 #267 表读 worktree + branch
  → 校验: branch 必须是 fix/* 或 feature/*
  → 校验: worktree 绝对路径在 project-worktrees/ 下
  → 校验: 同一 worktree 没有 status=launched 的其他 worker
  → cd <worktree> → launch AI → 等完成 → UPDATE status

#265 多项目（编排层）
  → 每项目独立 freely.db → 独立 handoffs 表
  → Manager patrol 跨项目汇总 worker 状态
  → 通过 #267 读写，通过 #264 launch
```

## 关键设计决策

### 1. 工位路径存绝对路径

```sql
worktree TEXT NOT NULL  -- /Users/zhaoyu/.../freely-worktrees/fix/raw-xxx
```

### 2. Runtime cd，不靠 AI

Runtime 从 handoffs 表读到 worktree 绝对路径 → cd $worktree → launch worker。
AI prompt 中告知路径作为上下文，但不依赖 AI cd。

### 3. 写时校验 + 读时兜底

**写时（Manager 写 exit contract）**:
- worktree 路径存在？磁盘 `test -d $worktree`
- branch 合法？`git -C $project worktree list | grep $branch`
- 不通过 → INSERT status='rejected', exit_kind='invalid_worktree_write'
- 不 block Manager——让它知道错误，下次修正

**读时（Runtime launch worker）**:
- branch 是 fix/* 或 feature/*？（#264 核心校验）
- worktree 在 project-worktrees/ 下？
- 同 worktree 是否已有运行中 worker？
- 不通过 → UPDATE status='rejected'，拒绝 launch

### 4. 错误码

| 阶段 | exit_kind | 含义 |
|------|-----------|------|
| 写 | invalid_worktree_write | Manager 写了不存在的工位 |
| 读 | invalid_branch | 分支不是 fix/* 或 feature/* |
| 读 | invalid_worktree_missing | 工位不存在 |
| 读 | invalid_worktree_boundary | 不在 project-worktrees/ 下 |
| 读 | duplicate_worker | 同工位已有运行中 worker |
| 执行 | worker_done | 正常完成 |
| 执行 | worker_blocked | 阻塞 |
| 执行 | worker_timeout | 超时 |

### 5. 写不达标时

Manager 写了错误工位 → INSERT status='rejected'（不 block patrol）。
下一轮 Manager 读到 rejected → 修正 → INSERT 新记录（不 UPDATE 旧记录，保留审计 trail）。
