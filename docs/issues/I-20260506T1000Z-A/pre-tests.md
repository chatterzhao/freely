# Pre-tests: I-20260506T1000Z-A

## TC1: wait 模式不发射 AI

1. 设置 `FREELY_TASK_MODE=wait`
2. 启动 Freely
3. 确认日志包含 wait-mode polling，无 build prompt / launch AI 日志
4. 确认无 AI API 调用

## TC2: auto 模式行为不变

1. 设置 `FREELY_TASK_MODE=auto`
2. 启动 Freely
3. 确认正常 build prompt + launch AI

## TC3: id:<scan-id> 模式行为不变

1. 设置 `FREELY_TASK_MODE=id:scan-001`
2. 启动 Freely
3. 确认正常 build prompt + launch AI

## TC4: wait→auto 切换后恢复

1. 设置 `FREELY_TASK_MODE=wait`
2. 启动 Freely，确认进入 wait polling
3. 执行 `task-mode set auto`
4. 确认恢复 build prompt + launch AI

## TC5: stop_ai handler 不受影响

1. 设置 `FREELY_TASK_MODE=auto`
2. 启动 Freely，AI 运行中
3. 触发 stop_ai
4. 确认 stop_ai handler 正常执行
