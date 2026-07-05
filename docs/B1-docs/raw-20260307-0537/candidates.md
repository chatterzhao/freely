# 候选项列表

日期：2026-03-07
来源：头脑风暴 - AI 工具 Worktree 目录访问

---

## C-20260307-0537-A: legacy issue

### 基本信息
- promoted_issue_path: `pending://issue-materialization`
- milestone: `pending://milestone-binding`
- session_refs: [{tool: iflow, session_id: "iflow-cli-20260307", jsonl_path: "unavailable://historic-session-log-not-captured", role: "analysis"}]

### 描述

在 `monitor-ai-cli.sh` 的 `launch_iflow()` 函数中，自动检测并添加 `--include-directories` 参数，让 iflow 能够访问同级 worktrees 目录。

### 动机

1. Freely 宪法规定 worktree 目录与项目同级
2. iflow 有目录保护机制，需要显式添加外部目录
3. 保持与其他 AI 工具的行为一致性

### 实现要点

1. 在 `launch_iflow()` 中计算 worktrees 目录路径：
   ```bash
   project_name=$(basename "$project")
   project_parent=$(dirname "$project")
   worktrees_dir="$project_parent/${project_name}-worktrees"
   ```

2. 检测目录是否存在，存在则添加参数：
   ```bash
   if [[ -d "$worktrees_dir" ]]; then
     dir_args=(--include-directories "$worktrees_dir")
   fi
   ```

3. 应用到 iflow 命令：
   ```bash
   exec iflow "${dir_args[@]}" "${args[@]}" -p "..." -y --max-turns 100
   ```

### 影响范围

- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- `docs/system/workspace/tools.md`（补充文档）

### 验收标准

1. 在 worktree 目录中启动 iflow 时，自动添加 worktrees 目录参数
2. 主项目中启动 iflow 时，也能添加 worktrees 目录参数
3. 不影响现有功能

### 依赖

无

### 路由

`doc-ibm-execution` -> `dev-loop-execution`

---

## C-20260307-0537-A: legacy issue

### 基本信息
- promoted_issue_path: `pending://issue-materialization`
- milestone: `pending://milestone-binding`
- session_refs: [{tool: iflow, session_id: "iflow-cli-20260307", jsonl_path: "unavailable://historic-session-log-not-captured", role: "analysis"}]

### 描述

在 `docs/system/workspace/tools.md` 中补充各 AI 工具的目录访问能力说明，帮助 AI 在路由时做出正确决策。

### 动机

1. AI 需要知道每个工具的目录访问限制
2. kiro-cli 没有额外的目录访问参数，需要文档化
3. 为未来的工具扩展提供参考

### 实现要点

在 tools.md 中添加：

```markdown
## Directory Access Capabilities

### iflow
- Supports `--include-directories` for external directories
- Freely automatically adds worktrees directory

### codex
- Uses `-C` to specify project root
- Worktree isolation is handled correctly

### kiro-cli
- No explicit external directory parameter
- Recommend starting in the worktree directory directly
- May have limited access to sibling directories
```

### 影响范围

- `docs/system/workspace/tools.md`

### 验收标准

1. 文档准确描述各工具的目录访问能力
2. AI 能够据此做出正确的工具选择

### 依赖

C-20260307-1101

### 路由

`doc-ibm-execution`

---

## 优先级排序

1. **P0**：C-20260307-1101（iflow 改进）
2. **P1**：C-20260307-1102（文档补充）

---

## 需要进一步研究

1. kiro-cli 是否有配置文件可以扩展目录访问？
2. 是否需要让 AI 工具访问主项目目录（从 worktree 中）？
3. 多项目场景下的目录隔离策略？
