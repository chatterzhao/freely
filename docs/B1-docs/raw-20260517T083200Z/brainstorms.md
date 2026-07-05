# Brainstorms

## Discovery

- **来源**: chat-inbox → `raw-20260517T083200Z` (GitHub #505)
- **摘要**: 运行时 supervisor (`freely:18777`) 上报 AI CLI 进程 crash。异常点：bash exit code 为 **0**（正常退出），但 supervisor 将其判定为 crash。
- **现场信息**:
  - `tool`: cc-ds-flash-auto (Claude Code deepseek flash auto mode)
  - `adapter`: acp (ACP bridge)
  - `launch_kind`: resume（续接会话）
  - `last_exit_reason_before_crash`: `set_e_exit_cmd=bash@freely:18777_rc_0`
- **核心异常**: `rc=0` 表示进程自愿正常退出。supervisor 的 crash 判定与 exit code 存在逻辑矛盾。

## Research

### 关键问题

1. **Supervisor crash 检测逻辑**：supervisor 判断 crash 的依据是什么？是否同时检查 exit code 和非预期断连信号？还是仅凭进程终止事件（不论 rc）就上报 crash？
2. **ACP bridge exit code 透传**：ACP bridge 是否在底层进程 crash 时仍返回 rc=0？bridge 本身异常退出和子进程 crash 的 exit code 是否区分？
3. **Resume 会话的特殊性**：`launch_kind: resume` 是否引入了特殊退出路径？续接会话的进程终止是否更容易被误报为 crash？
4. **已知关联 issue**：
   - `I-20260503T000000Z-A` ACP bridge crash resilience with self-healing——已处理 bridge crash 场景，但未覆盖 rc=0 被误判为 crash 的问题。
   - `I-20260413T042000Z-A` runtime supervisor attach reuse followthrough——涉及 supervisor 生命周期管理，与本问题有接触面。

### 当前可判断

- 这是一个 supervisor crash detection 的假阳性（false positive）或真阴性问题（rc=0 被错误归类）。
- 不影响运行时正常工作（进程已正常退出），但会导致：
  - 日志噪音（crash 日志对真正的事故分析造成干扰）
  - 不必要的 restart 或 recovery 开销
- 不能排除 ACP bridge 在进程异常终止但 shell 返回 0 的场景下未正确传播 exit code。

## Decision

当前信息不足以确认根因。需要在 supervisor 源码中检查 crash 判定逻辑，确认是 supervisor 层面的判定缺陷还是 ACP bridge 的 exit code 透传问题。

标记为 **needs_research**，直到根因收敛后再决定：
- 若为 supervisor 判定 bug → 修复 crash detection 逻辑
- 若为 ACP bridge 透传问题 → 修复 bridge exit code 传递
- 若为预期行为 → 记录文档，降低 crash 日志等级

下一跳：读取 supervisor 源码（`freely` runtime scripts / ACP bridge），聚焦 `crash` / `rc` / `exit_code` 相关判定逻辑。
