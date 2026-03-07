# Workspace Tools

本文件定义 Freely 当前可用的外部 AI 工具清单，供 `lead-agent` 与 `context-source-skill` 读取。

## Routing Principle

- Freely 负责提示词组装与外部 AI CLI 编排。
- Freely 不在脚本里硬编码“命中某条件就必须走某工具”。
- AI 必须读取当前输入、任务强度、工具优先级、工具可用性，再自主决定下一跳工具。

## Available Tools

### iflow

- availability: available
- priority: P1-default
- strengths:
  - 持续多轮推进
  - 非交互 `-p -y` 提示执行
  - 适合首跳自治和研究/文档型收敛
- recommended_when:
  - 任务仍在理解、收敛、路由、文档编排阶段
  - 需要较长 prompt 驱动下一跳工作
- example:
  - fresh/auto: `iflow -p "<assembled prompt>" -y --max-turns 100`
  - resume/auto: `iflow -c -p "<assembled prompt>" -y --max-turns 100`
  - fresh/step: `iflow -p "<assembled prompt>" --default --max-turns 100`

### codex

- availability: available
- priority: P1-default
- strengths:
  - 工程实现与仓库内读写
  - 在 worktree 中执行开发/文档修改
  - 适合 issue 已较清晰后的持续实现
- recommended_when:
  - 任务已命中 usable issue
  - 需要直接在仓库中进行实现、验证、修文档
- example:
  - fresh/auto: `codex exec --skip-git-repo-check -C <project-root> --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
  - fresh/step: `codex exec --skip-git-repo-check -C <project-root> - < <prompt-file>`
  - resume/auto: `codex exec resume --last --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`

## Selection Policy

- AI 应根据当前输入判断任务强度：
  - routing/research/doc-convergence
  - issue-materialization/doc-loop
  - implementation/dev-loop
- AI 应优先选择当前可用且最匹配任务强度的工具。
- 若多个工具都可用，优先选择更接近当前阶段的工具，而不是固定偏好某一个工具。
- AI 负责产出 `selected_tool`、`why_selected`、`next_prompt` 与 `target_skill_or_loop`。
- CLI 的具体启动参数由 Freely runtime 统一执行，不要求 AI 自己发明命令格式。
- 输出应包含：
  - selected_tool
  - why_selected
  - next_prompt
  - target_skill_or_loop
