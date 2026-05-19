# Tasks: I-20260506T1000Z-A

## T1: 定位 supervisor 主循环入口

- 找到 supervisor 主循环文件中 `select_launch_kind` 的调用位置
- 确认其前一个可插入门禁的位置

## T2: 插入 task_mode=wait 前置门禁

- 在 `select_launch_kind` 前添加：读 task_mode_gate → 若 wait → sleep CHECK_INTERVAL → continue
- 复用已有的 task_mode_gate 读取逻辑

## T3: 验证

- task_mode=wait 启动：确认无 AI 调用，日志显示 wait polling
- task_mode=auto 启动：确认行为不变
- task_mode=id:<scan-id> 启动：确认行为不变
- stop_ai handler 触发：确认不受影响
