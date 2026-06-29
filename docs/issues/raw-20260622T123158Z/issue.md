---
local_id: raw-20260622T123158Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T123158Z-A
platform_ids:
  github:
    issue_id: '3363'
    url: https://github.com/chatterzhao/freely/issues/3363
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T12:32:15Z'
updated_at: '2026-06-29T13:43:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

Manager/Worker Agent 当前用 Bash 工具直接跑 `freely wt-create`、`freely wt-close` 等封装命令，没有 Tool Policy 约束。Agent 可以绕过 Skill 直接用 Bash 跑 `gh issue create`、`git push` 等裸命令。

## 设计

在 `manager-agent.md` 和 `worker-agent.md` 中加 Tool Policy 章节：

```markdown
## Tool Policy

### 允许的 Skill（通过 Skill 工具调用）
| Skill | 封装的操作 |
|-------|-----------|
| freely-fix-execution | wt-create → fix → B1 → B2 → pr-* → wt-close |
| freely-feat-execution | wt-create → B1 → B2 → dev → pr-* → wt-close |
| freely-doc-B1_IBM-execution | raw → brainstorm → candidate → milestones |
| freely-doc-B2_IBM-execution | I-* → PRD → tasks → pre-tests → milestones |
| freely-dev-loop-execution | implement → test → progress → code-review |
| freely-branch-management | pr-create-guarded / pr-merge-guarded |
| freely-worktree-maintenance-governance | wt-close / issue-sync |

### 允许的只读 Bash 命令
git status, git log, git diff, git stash, git config --get, git remote -v, git worktree list

### 绝对禁止的 Bash 命令
- gh issue create/close/comment — 必须走 Skill → 封装命令 → platform-adapter
- gh pr create/merge — 必须走 pr-create-guarded / pr-merge-guarded
- git push / git merge / git branch -D — 必须走封装命令
- git worktree add/remove — 必须走 wt-create / wt-close
- rm -rf <worktree> — 必须走 wt-close

### 为什么用 Skill 而不是 Bash 直接调封装命令
- Skill 是 AI CLI 工具无关的描述层——Claude Code / Codex / 未来 agent 都读 .md + frontmatter
- 封装命令的内部实现（CLI 参数、platform-adapter、gh）对 Agent 透明
- Agent 不需要知道 CLI 参数细节，Skill 描述已经包含了工作流
```

## 涉及文件
- `docs/system/workspace/agents/manager-agent.md` — 加 Tool Policy
- `docs/system/workspace/agents/worker-agent.md` — 加 Tool Policy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Subagent 评审结论 (2026-06-22)

### 核心发现

1. **Prompt-level Tool Policy 是建议性的，不是强制性的** — AI 仍然可以通过 Bash 工具绕过。但仍有价值：将隐式规则显式化、统一化。

2. **Manager 和 Worker 必须分开定义 Tool Policy**：
   - Manager: 禁止 git add/commit/push，允许 a2a_task.py/a2a-exit/task-source-scan
   - Worker: 允许 git add/commit/test-lane/cp，禁止 a2a_task.py/a2a-exit

3. **缺失 Skill 封装的命令**: freely feedback, a2a_task.py, a2a-exit, test-lane

4. **需要运行时强制**: 建议加 governance-tool-policy-gate，在 a2a-exit 时扫描 A2A task 的 completion summary 检测违规命令

5. **建议用 YAML 替代 prose 表格**: 机器可读，可被 constitutional-guard 和 governance-tool-policy-gate 共同解析

### 推荐实现路径

| 优先级 | 任务 |
|--------|------|
| P0 | Manager/Worker 分开定义 Tool Policy |
| P0 | governance-tool-policy-gate（a2a-exit 时扫描违规） |
| P1 | TOOL_POLICY.yaml 机器可读策略文件 |
| P2 | 补 freely-feedback skill、a2a 管理 skill |
