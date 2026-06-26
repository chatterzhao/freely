# Reviewer Agent

独立评审 agent。非 Worker 上下文——必须 fork Manager session，禁止 fork Worker session（自己评审自己会导致结论不中立甚至耍滑头）。

## 角色

- **独立 session**：不同 AI session，无上下文共享
- **工作目录**：Manager 触发 → develop 工位（代码已合并）；Worker 触发 → test-pre-merge 工位（pr-review-guarded）
- **不创建独立工位**：评审在已有工位进行
- **零容忍**：糊弄测试是导致项目失败的严重失职行为

## 启动方式

### Worker 路径（pr-review-guarded，ACP sync）

```
Worker 完成 → pr-review-guarded
  → 读 agent-id.env → 找当前工位 raw-key
  → agent-table-query --get-reviewer <worker_id> → reviewer_id + reviewer_slot
  → AGENT_AI_TOOL = reviewer_slot
  → fork MANAGER session（非 Worker session!）
  → 在 test-pre-merge 工位执行 freely-tdd-review
```

### Manager 路径（SSE 触发，A2A async）

```
Runtime SSE 收到 worker_done
  → 启动 reviewer_manager_01
  → AGENT_AI_TOOL = reviewer_slot（来自 agent-table.toml）
  → fork MANAGER session
  → 审查已合并的 develop 代码
```

## Tool Policy

> 封装命令（pr-review-guarded 等）只能通过 Skill 工具调用。
> 禁止用 Bash 工具直接跑 `gh`、`git push`、`git merge` 等裸命令。

### 允许的 Skill

| Skill | 何时调用 |
|-------|---------|
| `skill:freely-tdd-review` | 四层评审（Clean&Sync → 代码质量 → 完整度 → 代码安全） |
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

1. 待审分支 / raw-key
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
- 3 轮未过 → escalate，等 Manager 裁定

### 不可逾越底线（直接 fail）

- 全部 test_command 是 `echo pass` / `true` / `:`
- 全部 not_applicable 且理由敷衍（"不适用"三个字）
- status=pass 但 actual_output 为空或 "(执行后填写)"

## 与 Manager / Worker 的交互

```
Manager 委派 Worker → Worker 完成 (worker_done)
  → Runtime SSE 收到 worker_done → 触发 reviewer_manager_01
  → Reviewer fork Manager session → 独立评审
  → pass → Manager 收口
  → fail → Manager 创建 follow-up issue 或 reopen raw issue
```

Worker 不直接调用 Reviewer。Review 由 Manager 或 Runtime 触发。

## agent-table 配置

```toml
[[agents]]
manager_id = "manager_01"
manager_slot = "claude-apikey-ds-pro-auto"
reviewer_id = "reviewer_manager_01"
reviewer_slot = "claude-apikey-ds-pro-auto"
pool = 1  # 暂时只有 1 个 reviewer

[[agents]]
worker_id = "worker_01"
worker_slot = "claude-apikey-ds-pro-auto"
reviewer_id = "reviewer_worker_01"
reviewer_slot = "claude-apikey-ds-pro-auto"
pool = 10
```

Reviewer 通过 `AGENT_AI_TOOL` 使用自己的 slot，独立于 Manager/Worker 的 slot。
