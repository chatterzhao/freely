# 20260506T1000Z -- task-mode wait pre-launch gate

## 上下文

`task_mode=wait` 原始实现 (32243539) 仅在 AI 结束后的 `stop_ai` 处理器中放置门禁。wait 模式 sleep CHECK_INTERVAL 后返回 continue，supervisor 回到主循环再次 build prompt + launch AI。这不是等待——这只是延迟重新发射。

## 设计决策

两段式门禁：
1. **前置门禁**（新增）：supervisor 主循环 `select_launch_kind` 之前，manager 专属检查 `read_task_mode=wait` → sleep + continue
2. **后置门禁**（已有）：AI 写 `stop_ai` 后，wait 模式覆盖 stop 决策，keep supervisor 存活

仅对 `role_hint=manager` 生效；worker 不受 task_mode 约束。

## 替代方案

- 在 supervisor 循环入口处放置门禁（选中）：最小侵入，与现有后置门禁正交
- 在 `build_prompt` 内部检查（否决）：prompt 已经构建，浪费计算
- 完全移除后置门禁改为前置（否决）：运行中切 wait 时无法等待 AI 自然结束
