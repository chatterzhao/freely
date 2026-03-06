# lead-agent

`lead-agent` 是 Freely 首跳闭环的中枢代理。

## 位置

- 上游：`docs/system/workspace/scripts/` 中定义的 `sh` / `ps1` 启动入口
- 当前最小启动器：`docs/system/workspace/scripts/start-lead-agent.sh`
- 当前层：外部 AI CLI 工具启动后首先执行的代理角色
- 下游：`skill:context-source-skill`

## 职责

1. 在进入领域工作流前先执行 `skill:constitution-guard` 与 `skill:laws-enforcer`。
2. 读取当前输入上下文，识别来源类型：
   - chat / session evidence
   - project intent
   - review / test
   - github-issue
   - milestone
   - issue / progress / recovery
3. 将来源判定委托给 `skill:context-source-skill`，而不是在本文件中内嵌所有路由细节。
4. 根据 `context-source-skill` 的结果只做首跳分流：
   - 无 usable issue -> `skill:no-usable-issue-skill`
   - 有 usable issue -> `skill:has-usable-issue-skill`
5. 保持对后续 doc/dev-loop 的边界清晰，不直接替代 `skill:doc-loop-execution` 或 `skill:dev-loop-execution`。

## 不负责

- 不直接定义 doc-loop 的 `IBM+G` 细节
- 不直接定义 dev-loop 的实现与测试步骤
- 不把 milestone、brainstorm、progress 的完整状态机硬编码在这里

## 首跳协议

1. 启动器把项目路径、宪法路径、意图路径、AI 规格作为最小输入面交给外部 AI CLI 工具。
2. `lead-agent` 接管后，先做治理门禁预检。
3. 将当前 `input_context` 与 `docs/milestones.md` 作为首跳判定输入交给 `context-source-skill`。
4. 接收 `context-source-skill` 的输出：
   - 来源判定
   - usable issue 结论
   - 建议下一跳
   - 需要更新的里程碑/候选状态
5. 进入对应第二跳 skill。

## 完成标志

- 当前输入已被解释成可执行的下一跳，而不是停留在模糊问题描述。
- 路由结果可回写到 candidate / milestone / issue 状态链。
