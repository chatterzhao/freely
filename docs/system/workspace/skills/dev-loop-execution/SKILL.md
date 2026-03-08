---
name: dev-loop-execution
description: 执行 milestone-owned ready issue 的实现、测试与进度回写。
---

# skill:dev-loop-execution

## 职责

- 只处理 docs 已足够的 ready issue。
- 在正确 worktree 中实现、测试并回写状态。
- 让 `progress` 只承载 dev-loop 的执行态。

## 不负责

- 不重新发明 issue 边界。
- 不把边界外新问题伪装成当前 issue 的实现细节。
- 不承担 pre-brainstorm / IBM 主工作。

## 情景步骤

### 情景 A：开始实现 ready issue

这样做：
1. 读取 issue、`prd.md`、`pre-tests.md`、`tasks.md`、milestone。
2. 确认当前 issue 已是 ready issue，而不是候选或仅 docs 收敛中的 issue。
3. 确认 issue / milestone 的 `phase_state=done_ibm` 或 `in_dev`。
4. 确认当前 worktree 正确：
   - 独立 issue -> 通常基于 `develop`
   - 依赖父分支 -> 基于 `execution_base`
5. 在当前 dedicated worktree 中实现变更。
6. 持续补齐测试与 code-review 证据。

### 情景 B：回写执行进度

这样做：
1. 仅把执行态写入 `docs/progress/{epic}/p-{issue}.md`：
   - 当前实现进度
   - 测试结果
   - blocker
   - 恢复上下文
   - 当前活跃 `session_refs`
2. 不把 candidate 收敛或纯 IBM 状态写进 `progress`。
3. 同步更新 milestone 与 issue 状态，并把 `phase_state` 置为 `in_dev`。

### 情景 C：实现中发现边界外新问题

这样做：
1. 不把它塞回当前 issue。
2. 在当前 issue / progress 中记录影响与 blocker。
3. 若会触发恢复或重跑，补充当前 `runtime_state` 与 `session_refs`。
4. 返回：
   - `status=reroute_required`
   - `next_recommended_route=doc-pre-brainstorm-execution`
   - 新问题证据摘要

### 情景 D：实现依赖未合并父分支

这样做：
1. 保留 issue 上携带的 `execution_base`、`integration_target`、`depends_on`。
2. 在提升前先确认父分支结果。
3. 父分支进入要求路径后，把当前分支 restack / rebase / merge 上游。
4. 重新执行必需测试，再继续提升。

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`

## 完成判定

- 代码、测试、issue、milestone、progress 已一致。
- 若有依赖父分支，已明确后续 restack / promote 要求。
