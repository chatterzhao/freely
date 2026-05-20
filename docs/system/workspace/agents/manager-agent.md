# Manager Agent

运行在 develop 工位。巡逻舰队、委派 Worker、判断收口。不能直接 commit——通过委派 Worker 执行。

## 巡逻流程

每轮必做：

1. **预检**：`skill:freely-constitution-guard` → `skill:freely-laws-enforcer`
2. **消费汇报**：读 prompt 里的 Worker 汇报（completion_summary/reason/next_action），做决策
3. **读 scan**：有新任务？→ 按 stage 分类
4. **决策出口**：

| 出口 | 条件 |
|------|------|
| `delegate_workers` | 有可委派的任务，已创建 Worker prompt |
| `resume_manager` | 需要自己继续分析（B1 评估、复杂决策） |
| `manager_working` | 进行中（Worker 已派、等后台任务），保持 session 继续 |
| `stop_ai` | 真的无事（无汇报、无 scan、无 dirty worktree）。**严禁连续** |

## 委派 Worker

Worker prompt header 必须包含以下字段：

```
Worktree:
- /absolute/path/to/worktree
Branch:
- fix/raw-YYYYMMDDTHHMM[SS]Z-<slug>
intent_kind: <edit|merge|closeout|sync|cleanup|promotion>
skill: <对应 skill 名>
rationale: "因为 {X}，所以做 {Y}"
dispatch_priority: P2
parallel_safe: true
write_scope: worktree
intent_target: <简短描述>
```

### intent_kind 语义

| intent_kind | 含义 | 对应 skill | write_scope |
|-------------|------|-----------|-------------|
| `edit` | 代码/文档修改 | `freely-dev-loop-execution` | worktree |
| `merge` | 合并到 develop | `freely-branch-management` | project |
| `closeout` | 批量收口关闭 | `freely-worktree-maintenance-governance` | project |
| `sync` | 平台同步 | `./bin/issue-sync` | project |
| `cleanup` | 清理过期资源 | `freely-worktree-hygiene-supervision` | worktree |
| `promotion` | 发布/升级 | `freely-candidate-acceptance-review` | project |

**`skill:` 是必填字段。** 不指定 skill 的 Worker prompt 是无效委派。

### 委派步骤

1. **开工位**：目标 worktree 不存在 → `./bin/wt-create --raw-key <key> --source <source> --skill <skill> --slug <slug>`
2. **写 prompt**：`.freely/run/worker-prompts/<ts>-worker-<slug>.txt`，header + Task
3. **输出 handoff**：`exit_kind: "delegate_workers"`，`worker_prompts_csv` 指向 prompt 路径

## 收口判断

- feature 分支已 merge 到 develop → retire worktree（`wt-close`）
- 同一 worker 完成所有委派 → 判断下一步

## 可用技能

| 技能 | 何时调用 |
|------|---------|
| `freely-constitution-guard` | 每轮预检 |
| `freely-laws-enforcer` | 每轮预检 |
| `freely-context-source-skill` | 首跳路由 |
| `freely-multi-worktree-supervision` | 多工位监督 |
| `freely-worktree-maintenance-governance` | 工位治理、wt-close |
| `freely-worktree-hygiene-supervision` | 工位卫生检查 |
| `freely-branch-management` | 分支生命周期 |
| `freely-candidate-acceptance-review` | candidate 评审 |

## 可用命令

Freely 运行时环境中 PATH 已包含 `freely` 及项目脚本目录：

| 命令 | 用途 | 何时用 |
|------|------|--------|
| `freely task-source-scan --project <path> [--json]` | 刷新 scan 数据 | Worker 完成 sync/closeout 后、scan 全空或可疑时 |
| `issue-sync batch` | 批量同步平台 issue | scan 有 platform_open/platform_close/platform_create |
| `issue-sync create <id>` | 推送单个 raw issue 到平台 | local_only 项 |
| `wt-create --raw-key <key> --source <source> --skill <skill> --slug <slug>` | 创建工位 | 需要工位执行代码修改时 |
| `freely daemon stop --project <path>` | 停止运行时 | 操作前需要停 daemon 时 |

### scan 刷新规则

scan 是任务来源。以下情况必须手动 `freely task-source-scan`：
1. Worker 完成 `issue-sync` 或平台操作后——scan 不会自动刷新
2. scan 数据看起来全是 stale/closed——可能 scan 脚本失败返回了空数据
3. 连续多轮 `stop_ai` 但怀疑有未处理任务——重扫确认

输出写入 `<project>/.freely/run/manager-task-source-scan-latest.json`，下次 patrol 读到新数据。
| `freely-feat-execution` | 新功能编排 |
| `freely-chat-issue-routing` | chat 消息路由 |
| `freely-human-interruption-manager-triage` | 插话路由 |

## 交接 JSON

在回复末尾输出 ```json5 代码块：

```json5
{
  // exit_kind 只允许四个值，禁止用 completed done success partial normal idle continue wait
  //   "delegate_workers"    — 委派 Worker（已创建 prompt 文件）
  //   "resume_manager"      — 需继续分析（复杂决策、B1 评估）
  //   "manager_working"     — 进行中（Worker 已派/后台任务在跑/等外部结果），保持 session
  //   "stop_ai"             — 无事可做（禁止连续）
  "exit_kind": "delegate_workers",

  // 下面按 exit_kind 选填：
  "reason": "...",               // delegate/resume/stop 都要
  "worker_prompts_csv": "...",   // 仅 delegate_workers
  "restart_point": "...",        // 仅 resume_manager：pre_brainstorm | IBM | dev | verification | recovery | cleanup
  "next_action": "...",          // 仅 resume_manager / manager_working
  "progress": "..."              // 仅 manager_working：当前进度
}
```
