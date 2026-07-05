# 头脑风暴：AI 工具 Worktree 目录访问

日期：2026-03-07
状态：进行中
会话：iFlow CLI

---

## 1. 问题背景

### 1.1 现象

当用户在项目目录中启动 AI 工具（如 cc、codex、iflow、kiro-cli）时，AI 工具有目录级别的保护机制。如果项目使用 git worktree 且 worktree 放在项目同级目录（如 `{project}-worktrees/`），AI 工具会认为 worktree 目录在"项目外部"，拒绝访问。

### 1.2 行业惯例与冲突

**Git 官方和行业推荐**：
- worktree 放在 `<project_parent>/<project_name>-worktrees/`
- 与项目目录同级并列

**AI 工具的保护机制**：
- 进入项目目录后，工具认为工作范围是该目录
- 访问 `../xxx-worktrees/` 被视为"外部目录"
- 触发目录保护，提示"没有权限"

### 1.3 Freely 的场景

Freely 是一个自主循环运行器，会调用外部 AI 工具（codex、iflow、kiro-cli）来执行任务。当 Freely 在 worktree 中启动 AI 工具时，需要确保 AI 工具能够：
1. 访问当前 worktree
2. 必要时访问主项目或其他 worktree

---

## 2. 调研结果

### 2.1 各 AI 工具的目录访问配置

| 工具 | 额外目录参数 | 自动批准参数 | 备注 |
|------|-------------|-------------|------|
| **iflow** | `--include-directories` 或 `--add-dir` | `-y` | 支持多目录 |
| **codex** | `-C <project-root>` 已指定项目根 | `--dangerously-bypass-approvals-and-sandbox` | 绕过所有审批和沙箱 |
| **kiro-cli** | 无直接参数 | `--no-interactive --trust-all-tools` | 无额外目录配置 |
| **Claude Code** | `--add-dir` 或 `/add-dir` 或 `additionalDirectories` | `bypassPermissions` 模式 | 配置文件支持 |

### 2.2 当前 Freely 的实现

文件：`docs/system/workspace/scripts/monitor-ai-cli.sh`

```bash
# codex: 已使用 -C 指定项目根目录
launch_codex() {
  local -a args=(exec --skip-git-repo-check -C "$project")
  # ...
  exec codex "${args[@]}" - <"$prompt_file"
}

# iflow: 未添加 worktrees 目录参数
launch_iflow() {
  # ...
  exec iflow "${args[@]}" -p "$(cat "$prompt_file")" -y --max-turns 100
}

# kiro-cli: 无额外目录参数
launch_kiro_cli() {
  # ...
  exec kiro-cli chat --no-interactive --trust-all-tools --model "$model" <"$prompt_file"
}
```

### 2.3 问题分析

1. **codex**：使用 `-C` 指定项目根目录，但如果在 worktree 中启动，`-C` 指向的是 worktree 目录，而非主项目。这是正确的。

2. **iflow**：未添加 `--include-directories` 参数，可能导致无法访问主项目或其他 worktree。

3. **kiro-cli**：无额外目录参数，需要在项目目录中启动，或使用其他方案。

---

## 3. 候选方案

### 方案 A：为 iflow 添加 worktrees 目录参数

**实现**：
```bash
launch_iflow() {
  local project_name=$(basename "$project")
  local project_parent=$(dirname "$project")

  # 检查是否存在同级 worktrees 目录
  local worktrees_dir="$project_parent/${project_name}-worktrees"
  local -a dir_args=()

  if [[ -d "$worktrees_dir" ]]; then
    dir_args=(--include-directories "$worktrees_dir")
  fi

  if [[ "$mode" == "auto" ]]; then
    exec iflow "${dir_args[@]}" "${args[@]}" -p "$(cat "$prompt_file")" -y --max-turns 100
  else
    exec iflow "${dir_args[@]}" "${args[@]}" -p "$(cat "$prompt_file")" --default --max-turns 100
  fi
}
```

**优点**：
- 符合 Freely 宪法的 worktree 目录策略
- 不改变用户习惯
- iflow 原生支持

**缺点**：
- 仅解决 iflow 的问题
- kiro-cli 无此参数

### 方案 B：在 worktrees 父目录启动 AI 工具

**实现**：
让 Freely 在 `<project_parent>/` 目录启动 AI 工具，而非在项目目录内启动。

**优点**：
- 一个目录包含主项目和所有 worktrees
- AI 工具自动拥有所有子目录的访问权限
- 不依赖工具特定参数

**缺点**：
- 改变 Freely 的目录约定
- 可能与其他项目冲突（如 openclaw、evomap 在同一父目录）

### 方案 C：混合方案（推荐）

**实现**：
1. **iflow**：添加 `--include-directories` 参数
2. **codex**：保持现有实现（`-C` 已足够）
3. **kiro-cli**：
   - 在 worktree 中启动时，提示用户可能的限制
   - 或提供配置选项让用户选择启动目录

**优点**：
- 针对每个工具的最优解
- 保持现有架构稳定
- 增量改进

**缺点**：
- 不同工具有不同行为

### 方案 D：kiro-cli 的替代方案

**问题**：kiro-cli 没有 `--include-directories` 类似参数。

**子方案**：

D1. **在主项目目录启动，通过 prompt 指定 worktree**
```bash
kiro-cli chat --model "$model" "请在 worktree 目录 $worktree_path 中工作..."
```

D2. **创建 AGENTS.md/CLAUDE.md 在父目录**
在 `<project_parent>/` 创建一个 AGENTS.md，让 kiro-cli 以此作为项目根。

D3. **文档化限制**
在 tools.md 中明确 kiro-cli 的限制，让 AI 在路由时知道这一点。

---

## 4. 候选项收敛

### 4.1 推荐：方案 C + D3

1. **iflow 改进**：添加 `--include-directories` 参数
2. **codex**：保持不变
3. **kiro-cli**：文档化限制，AI 路由时考虑

### 4.2 代码改动点

**文件**：`docs/system/workspace/scripts/monitor-ai-cli.sh`

**改动**：
1. 在 `launch_iflow()` 中添加 worktrees 目录检测和 `--include-directories` 参数
2. 在 `docs/system/workspace/tools.md` 中补充各工具的目录访问能力说明

---

## 5. 待确认问题

1. 是否需要让 AI 工具访问**其他** worktree？（当前场景主要是访问当前 worktree）
2. 主项目目录是否需要被 worktree 中的 AI 工具访问？
3. kiro-cli 是否有隐藏参数或配置文件可以扩展目录访问？

---

## 6. 参考资料

- Claude Code 权限文档：https://code.claude.com/docs/en/permissions
- Codex 配置文档：https://developers.openai.com/codex/config-reference/
- iflow --help 输出
- kiro-cli chat --help 输出
- Freely CONSTITUTION.md 第 2 章第 3 条（工作树纪律）
