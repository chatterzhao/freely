# Tasks: A2A-Native Delegation

## Phase 1: a2a_task.py 消除 CSV
- [ ] a2a-exit 移除 --workers 参数
- [ ] create() 不再需要 worker_prompts_csv
- [ ] update() 同上

## Phase 2: freely runtime A2A 查询
- [ ] manager_exit_contract_kind(): tasks/list --state=submitted 替代 CSV
- [ ] manager_runtime_launch_workers(): task.message → prompt file
- [ ] 移除 _db_exit_contract_field worker_prompts_csv 引用
- [ ] 移除 validate 中 WORKER_PROMPTS_CSV 检查

## Phase 3: Manager prompt 更新
- [ ] manager-agent.md: a2a-exit --message 替代 --workers + 文件写入
- [ ] 移除 "写 prompt 文件" 相关指令
