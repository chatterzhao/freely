---
local_id: raw-20260622T021832Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T021832Z-A
platform_ids:
  github:
    issue_id: '3318'
    url: https://github.com/chatterzhao/freely/issues/3318
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T02:18:49Z'
updated_at: '2026-06-22T02:18:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 从 #3314 拆分 (C)

## 问题
pre-tests.md 只有 3 个章节标题要求 (## Unit / ## Integration / ## End-to-End)。AI 可以写空壳通过所有门禁。pr-review-guarded 只 grep 'adequacy:' 行数。

## 设计

### 测试条目格式
```markdown
## acceptance-{n}
- criterion_id: raw issue 第 n 条 acceptance criteria
- test_command: 实际执行的 shell 命令
- expected_pattern: 预期输出包含的文本
- actual_output: |
    命令的实际输出
- evidence_file: .freely/run/test-evidence/acceptance-{n}.log
- status: pending | passed | failed
```

### pretests-gate 加强
- status 必须全部 passed
- evidence_file 必须存在且非空
- actual_output 必须非空（证明执行过）

### 迁移策略
- 旧 pre-tests.md: 兼容期 2 周，不阻塞
- 新 pre-tests.md: 必须用新格式

## 涉及文件
- pretests-gate 脚本
- pr-review-guarded 维度4
- freely-dev-loop-execution/references/pre-tests-quality.md (新建)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
