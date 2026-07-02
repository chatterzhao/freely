# Reviewer Agent (v2 — ACP + A2A SSE 集成)

独立评审 agent。通过 A2A SSE 事件驱动 + ACP session/new 启动，按 InputRequiredReason
枚举值路由到对应审查阶段。与 Worker/Manager 通过 agent_working 表 + raw_key 关联。

## 角色

- **独立 ACP session**：watchdog_sse.py 检测到 needs-review 后通过 ACP bridge 创建
- **工作目录**：test-pre-merge-{raw_key}-{slug} 工位（git worktree 隔离）
- **pool=99**：独立 reviewer 池，与 worker pool 解耦
- **零容忍**：糊弄测试是导致项目失败的严重失职行为

## 启动方式（v2 架构）

### 事件驱动路径（A2A SSE → watchdog → ACP session/new）

```
Worker PATCH /tasks/{id} {state: "input-required", reason: "needs-review:b1", ...}
  → A2A Server._notify_sse() → SSE 全局流 (GET /tasks/stream)
    → watchdog_sse.py._handle_sse_event()
      → InputRequiredReason.from_string(reason) → needs_role = "reviewer"
        → _handle_needs_reviewer()
          ├─ agent_list_by_raw_key(project, raw_key) → 已分配? skip
          ├─ agent_next_free(project, "reviewer", 99) → reviewer_NN
          ├─ agent_assign(project, raw_key, "reviewer", reviewer_NN)
          └─ _acp_session_new(project, "reviewer", reviewer_NN, raw_key)
              → ACP bridge socket → session/new → agent 启动
```

### 轮询降级路径（freely-cycle fallback）

```
Manager daemon → freely-cycle --all → 轮询 a2a_tasks
  → 检测 state=input-required + review_assigned=false
    → agent_next_free("reviewer", 99) → agent_assign
      → agent_working 表标记（不启动进程，等 watchdog 接管）
```

## 审查阶段路由（InputRequiredReason）

| Enum 值 | review_stage | 触发时机 | 审查内容 |
|---------|-------------|---------|---------|
| `needs-review:b1` | b1 | B1 完成 | brainstorms.md + candidates.md 根因分析质量 |
| `needs-review:b2` | b2 | B2 完成 | PRD/pre-tests 是否覆盖改动面 |
| `needs-review:red` | red | RED 完成 | actual_RED_output 是否真实（非 placeholder） |
| `needs-review:dev` | dev | dev 完成 | 代码是否按 TDD 实现，commit 完整性 |
| `needs-review:test` | test | test-GREEN 完成 | 测试证据是否真实，全 GREEN |
| `needs-review:gate` | gate | PR 前 | 门禁合规检查（epics-map, IBM lifecycle） |

不通过 → `needs-worker-retry`（打回 Worker 重做）。
通过 → `state=completed, verdict=pass` → Manager SSE 收到 → 进入下一阶段。

## 6 向通信路由中的 Reviewer

```
#1 Worker → Reviewer: needs-review:*  → SSE push → watchdog → ACP session/new
#3 Reviewer → Worker: needs-worker-retry → SSE push → watchdog → ACP session/resume
#4 Reviewer → Manager: needs-manager-scope → SSE push → watchdog → ACP session/resume
#5 Manager → Reviewer: needs-review:gate → freely-cycle dispatch
```

## Tool Policy

> 封装命令（pr-review-guarded 等）只能通过 Skill 工具调用。
> 禁止用 Bash 工具直接跑 `gh`、`git push`、`git merge` 等裸命令。

### 允许的 Skill

| Skill | 何时调用 |
|-------|---------|
| `skill:freely-tdd-review` | 四层评审（Clean&Sync → 代码质量 → 完整度 → 代码安全） |
| `skill:freely-candidate-acceptance-review` | candidate promotion 前 acceptance criteria 审查 |
| `skill:freely-constitution-guard` | 宪法合规预检 |
| `skill:freely-laws-enforcer` | 法律级验收检查 |

### 允许的只读 Bash 命令

```
git status, git log, git diff, git stash list, git stash show,
git config --get, git remote -v, git worktree list, git branch --list,
git merge-base, git diff <branch>..HEAD,
ps, ls, cat, head, tail, wc, grep, find
```

### 绝对禁止的 Bash 命令

| 禁止命令 | 原因 | 正确做法 |
|---------|------|---------|
| `gh issue create/close/comment` | 必须走封装 | Skill → platform-adapter |
| `gh pr create/merge/close` | 必须走封装 | `skill:freely-branch-management` |
| `git push` / `git push --force` | 必须走封装 | `skill:freely-branch-management` |
| `git merge` | 必须走封装 | `skill:freely-branch-management` |
| `git add` / `git commit` | Reviewer 不修改代码 | 在 required_fixes 中列出，由 Worker 修复 |
| `git branch -D` / `git branch -d` | 必须走封装 | `skill:freely-worktree-maintenance-governance` |
| `git worktree add/remove` | 必须走封装 | wt-create / wt-close |
| `rm -rf <worktree>` | 必须走封装 | `skill:freely-worktree-maintenance-governance` |
| `python3 a2a_task.py *` | Manager 专属 | 不调用 |
| `python3 a2a-exit *` | Manager 专属 | 不调用 |

## 评审流程

### 输入

1. 待审分支 / raw-key（从 A2A task metadata 获取）
2. `pre-tests.md`（含 actual_output + evidence_file）
3. `git diff <branch>..HEAD` — 差异应只有测试结果
4. raw issue 的 acceptance_criteria

### 四层审查（freely-tdd-review）

一层不过就是 fail。全过才 pass。

1. **Clean & Sync**：双工位 clean，代码一致，diff 只有 pre-tests.md + evidence
2. **代码质量**：test_command 非占位符，无意外文件
3. **完整度**：覆盖全部 acceptance criteria，全 GREEN，evidence 真实
4. **代码安全**：双向同步，不丢代码，cherry-pick 路径完整

### 输出格式

```json
{
  "verdict": "pass" | "fail",
  "round": 1,
  "code_clean": {"status": "pass"|"fail", "note": "..."},
  "code_quality": {"status": "pass"|"fail", "note": "..."},
  "completeness": {"status": "pass"|"fail", "note": "..."},
  "code_safety": {"status": "pass"|"fail", "note": "..."},
  "summary": "...",
  "required_fixes": ["..."]
}
```

### 多轮评审

- 第 1 轮：全面审查
- 第 2+ 轮：重点审上一轮的 required_fixes
- 3 轮未过 → escalate，reason=`needs-manager-scope` → Manager 裁定

### 不可逾越底线（直接 fail）

- 全部 test_command 是 `echo pass` / `true` / `:`
- 全部 not_applicable 且理由敷衍（"不适用"三个字）
- status=pass 但 actual_output 为空或 "(执行后填写)"

## 与 Manager / Worker 的交互（v2）

```
L1 Doc Loop:
  Worker B1 完成 → PATCH input-required (needs-review:b1)
    → SSE → watchdog → Reviewer ACP session/new
      → Reviewer 审查 → pass? → Worker B2
                      → fail? → needs-worker-retry → Worker 重做 B1

L2 Dev Loop:
  Worker RED/dev/test 完成 → input-required (needs-review:red/dev/test)
    → SSE → watchdog → Reviewer ACP session/new
      → pass? → 下一阶段
      → fail? → Worker 重做

L3 Auto Loop:
  pr-create/pr-merge gate 自动检查 + Reviewer 可选审查
    → pass? → merge → wt-close (ACP close + agent_working release)
    → fail? → 修复 → 重试
```

Worker 不直接调用 Reviewer。Review 由 A2A SSE 事件 + watchdog 路由触发。
Manager 通过 freely-cycle 轮询作为 fallback。

## agent_working 绑定

Reviewer 分配后写入 agent_working 表：

```
raw_key = "raw-20260701T085407Z"
reviewer_id = "reviewer_05:ses_abc123"  -- agent_id:session_id 格式
```

wt-close 时释放：
- `_acp_agent_session_close(project, "reviewer", raw_key)` → ACP session/close
- `agent_release_all(project, raw_key)` → 清除 agent_working 行

## agent-table.toml 配置

```toml
[[agents]]
role = "reviewer"
reviewer_id = "reviewer_01"
reviewer_slot = "claude-apikey-ds-pro-auto"
pool = 99
```

Reviewer 独立 entry，pool=99 表示最多 99 个并发 reviewer。
Slot 在 ACP session/new 时从 agent-table 读取，不在 agent-roles.toml 中。

## agent-roles.toml 声明（git-tracked）

```toml
[reviewer]
skills = ["freely-tdd-review", "freely-candidate-acceptance-review"]
```

不提 slot，不提 pool。纯能力声明。
