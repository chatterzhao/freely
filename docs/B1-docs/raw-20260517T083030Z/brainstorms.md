# Brainstorms

## Discovery

- **来源**: GitHub issue #504 (`raw-20260517T083030Z`), chat-inbox, P2
- **原始描述**: supervisor 检测到 bash 在 freely:18777 以 rc=0 退出，判定为 crash
- **last_exit_reason_before_crash**: `set_e_exit_cmd=bash@freely:18777_rc_0`
- **工具/模式**: `cc-ds-flash-auto` (Claude Code deepseek flash, auto mode)
- **适配器**: acp (ACP bridge)
- **启动方式**: resume

## Research

### 问题本质

bash 以 rc=0（成功）退出，但 supervisor 将其判定为 crash。有两种可能：

1. **假阳性**：supervisor 的 crash 检测逻辑未过滤 rc=0，将任何受管进程退出都视为 crash，无论退出码。
2. **预期外退出**：bash 本应作为长驻进程保持运行（维持 AI CLI 会话），其退出（即使成功）触发了 supervisor 的 crash 处理逻辑。

### 关键观察

- `last_exit_reason_before_crash` 字段表明 supervisor 有 exit reason 追踪机制，说明 crash 检测有结构化记录
- rc=0 是 shell 成功退出的标准码，正常情况下不应触发 crash 处理
- 工具是 `cc-ds-flash-auto`，说明 AI CLI 进程是通过 bash + ACP adapter 管理的
- `launch_kind: resume` 表明这是续接会话，bash 退出导致续接失败

### 当前问题边界

| 维度 | 状态 |
|------|------|
| 已知 | supervisor 将 bash rc=0 判定为 crash |
| 已知 | bash 退出码为 0（成功） |
| 未知 | supervisor crash 检测的具体代码路径 |
| 未知 | 这是系统性 bug 还是一次性边缘情况 |
| 未知 | 是否已有其他同类误报但未被上报 |

### 需要继续研究的问题

1. supervisor 的 crash 检测逻辑在哪里？是否直接用了进程退出事件而不检查退出码？
2. bash 是 supervisor 的直接子进程还是有中间进程层？
3. `set_e_exit_cmd` 的含义是什么？是否是 bash 成功执行完某条指令后的正常退出？
4. 当前是否有其他类似 rc=0 被误报为 crash 的案例？
5. 修复范围：仅在 crash 检测中过滤 rc=0，还是需要改更上层的进程生命周期管理？

## Decision

- **判定**: 需进一步研究才能决定是否值得进入 B2_IBM 实现
- **下一跳**: 研究 supervisor 源码中的 crash 检测逻辑
- **风险**: 如果 rc=0 确实是正常退出却被误报，当前 supervisor crash 统计可能包含大量假阳性，影响 crash 分析和自愈决策的准确性
