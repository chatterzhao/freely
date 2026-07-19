---
local_id: raw-20260719T192542Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T192542Z-A
platform_ids:
  github:
    issue_id: '4025'
    url: https://github.com/chatterzhao/freely/issues/4025
    synced_at: ''
  gitee:
    issue_id: IK25JE
    url: https://gitee.com/zhaoquan/freely/issues/IK25JE
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T19:26:05Z'
updated_at: '2026-07-19T19:26:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

当前三个agent的prompt模板有以下缺陷:
1. Manager看不到agent_working数据 → 不知道谁在处理什么 → 重复委派
2. Manager角色边界约束太弱 → 自己写代码 → 跳过治理
3. Worker收到的指令不是完整workflow → 只做PR+merge → 跳过B1/B2/review
4. Reviewer从未被触发 → Worker不调用input-required needs-review
5. 没有pool利用率数据 → Manager不知道并发上限

## 需要深入研究的问题

### agent_working数据怎么结构化注入
- 格式设计: 表格式? JSON? 自然语言?
- 包含什么字段: raw_key, worker_id, session_id, slot, worktree, branch
- pool利用率: total/free/occupied per role
- 如何让AI正确解读这些数据

### Manager prompt
- 明确角色边界: 不写代码, 不执行B1/B2/dev
- 工作流: scan→diagnose→create_issue→wt_create→delegate_worker(完整workflow skill)
- 如何使用agent_working数据: 查空闲slot, 防重复委派, 监控Worker进度
- 出口: delegate_workers / stop_ai

### Worker prompt  
- 收到委派后: 严格按workflow skill B1→B2→RED→dev→GREEN→PR→merge→close
- 每个阶段后: a2a-exit input-required needs-review
- 审查不通过: 根据feedback修正, 重新提交
- 出口: completed / input-required(needs-review)

### Reviewer prompt
- 审查触发: A2A SSE input-required needs-review
- 审查方法: 从raw issue开始逐级检查fidelity
- 输出: pass/fail + 具体修正指导

## 修复范围
freely中的prompt构建函数(Manager/Worker/Reviewer三段)
