---
issue_id: I-20260705T231534Z-A
issue_path: docs/B2-docs/ibm/b2-governance/raw-20260705T231534Z/issues/I-20260705T231534Z-A.md
phase_state: done_b2_ibm
---
- issue_id: I-20260705T231534Z-A
- issue_path: docs/B2-docs/ibm/b2-governance/raw-20260705T231534Z/issues/I-20260705T231534Z-A.md

## Implementation Decision Note
- decision: ./bin/xxx → freely xxx，分三 pass 执行，保留 source/chmod/-x 检查
- why_this: 项目已支持 freely 全局命令，统一用户体验。保留文件操作相关模式避免破坏 hook 功能
- alternatives_considered: (1) sed 一键全替换 — 会错误替换 source/chmod 导致 hook 失效；(2) 逐文件手动改 — 230 处不可行
- boundary_non_goals: 不修改测试文件(88处，低优先级)；不修改 ./bin/ 安装指令(chmod +x)；不修改文件存在性检查(-x/-f)
- residual_risk: 无。所有替换均经 grep 验证保留模式未被改动
