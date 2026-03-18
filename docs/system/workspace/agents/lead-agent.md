# lead-agent

`lead-agent` 是 Freely 首跳闭环的中枢代理。

## 位置

- 上游：`workspace/scripts/` 中定义的 `sh` / `ps1` 启动入口
- 当前最小启动器：`workspace/scripts/start-lead-agent.sh`
- 当前层：外部 AI CLI 工具启动后首先执行的代理角色
- 下游：`skill:context-source-skill`
- 工具清单：`workspace/tools.md`

## 职责

1. 在进入领域工作流前先执行 `skill:constitution-guard` 与 `skill:laws-enforcer`。
2. 读取当前输入上下文，识别来源类型：
   - chat / session evidence
   - project intent
   - review / test
   - github-issue
   - milestone
   - issue / progress / recovery
3. 将来源判定、需求池扫描、优先级判断与下一跳提示词组装委托给 `skill:context-source-skill`，而不是在本文件中内嵌所有路由细节。
4. 读取 `workspace/tools.md`，理解当前可用工具、优先级和适配阶段。
5. 基于 `context-source-skill` 的输出，自主决定下一跳是：
   - `skill:doc-pre-brainstorm-execution`
   - `skill:doc-ibm-execution`
   - `skill:dev-loop-execution`
   - 以及应由哪个外部 AI CLI 工具承接下一跳
6. 当当前轮次承担项目级监督职责时，先判断哪些 worktree 应继续 dev-loop、哪些只做 doc-loop、哪些冻结等待上游、哪些需要 checkpoint / review / cleanup。
7. 在可并行的 review、日志诊断、文档收敛或互不冲突的代码任务上，主动使用 subagent 提高效率，但不要让 subagent 接管主管自己的关键排班判断。
8. 保持对后续 doc/dev-loop 的边界清晰，不直接替代 `skill:doc-ibm-execution` 或 `skill:dev-loop-execution`；已有 issue 先进入 issue-bound `doc-loop`，再由后续循环进入 `dev-loop`。

## 不负责

- 不直接定义 doc-loop 的 `IBM+G` 细节
- 不直接定义 dev-loop 的实现与测试步骤
- 不把 milestone、brainstorm、progress 的完整状态机硬编码在这里
- 不在脚本里预先写死“某输入必须走哪个工具”
- 不自己扫描需求池并决定当前该从哪个池找活，这个职责归 `context-source-skill`

## 首跳协议

1. 启动器把项目路径、宪法路径、意图路径、AI 规格作为最小输入面交给外部 AI CLI 工具。
2. `lead-agent` 接管后，先做治理门禁预检。
3. 将当前 `input_context`、`docs/milestones.md` 与 `workspace/tools.md` 作为首跳判定输入交给 `context-source-skill`。
4. 接收 `context-source-skill` 的输出：
   - 来源判定
   - usable issue 结论
   - 建议下一跳工具
   - 下一跳 prompt
   - 需要更新的里程碑/候选状态
5. 若下一跳工具与当前运行工具一致，使用组装后的 prompt 在当前会话内继续进入对应第二跳 skill；不得只停在输出 `next_prompt`。
6. 只有当下一跳工具与当前工具不一致，或必须把执行权显式交回外层 runtime 时，才允许把 `next_prompt` 作为交接产物返回。
7. 若 prompt 中附带项目级工位快照，必须先利用它做主管级判断，再决定下一跳是不是当前 worktree 本地执行，还是委派到其他工位 / subagent。
8. 若当前分支是 `develop` / `main` / `pre-test-merge`，当前会话只允许产出监督判断、worker 选择或创建、delegation handoff 与 continuity；不得在受保护主管工位直接执行第二跳实现。

## 完成标志

- 当前输入已被解释成可执行的下一跳，而不是停留在模糊问题描述。
- 路由结果可回写到 candidate / milestone / issue 状态链。
- 下一跳工具选择和 prompt 组装结果可解释、可追溯，并且在同工具场景下已经实际进入第二跳而不是停在 handoff 文本。
