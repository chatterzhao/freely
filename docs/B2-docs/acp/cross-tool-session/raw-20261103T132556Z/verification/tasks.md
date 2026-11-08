# Tasks: ACP bridge 按 session 路由避免越权代答
- issue_id: I-20261103T132556Z-A
- pre_tests_path: docs/B2-docs/acp/cross-tool-session/raw-20261103T132556Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核运行时路径（SDK/execv）、bridge 广播实现、client sessionId 分布、permission-mode 生产注入链；证伪 3 个高风险字面方案并收窄为 fail-open + 显式 opt-in。
- [x] T2: 写 AT-001（4 静态 + 15 行为，隔离 mock），develop 基线快照确认 RED 9 ok/10 failed。
- [x] T3: `run-acp-prompt.py` 客户端入站过滤 + session 绑定 + 权限守卫；`acp-bridge.py` 定向投递 + 注册表 + 裸默认显式 opt-in。
- [x] T4: 跑 GREEN 19 ok/0 failed + 相关回归基线对比（0 新增失败）。
- [x] T5: 人工四层 TDD review → verdict → governance 门禁 → pr-create/pr-merge → wt-close → 打包 → 更新 goal。
