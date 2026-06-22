---
local_id: raw-20260622T021827Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T021827Z-A
platform_ids:
  github:
    issue_id: '3317'
    url: https://github.com/chatterzhao/freely/issues/3317
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T02:18:46Z'
updated_at: '2026-06-22T02:51:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## pre-tests.md 完整模板（B2_IBM skill 内置）

B2_IBM skill 直接包含以下模板。AI 按模板填写，无需查看任何其他文件。模板已满足 LAWS.md §4c 全部要求。

```markdown
## Acceptance Items

### acceptance-1
- acceptance target: <raw issue 验收标准>
- testing layer: unit | integration | end-to-end
- target environment: test-pre-merge-{key}-{slug}
- required evidence: <测试通过的证据要求>
- test_command: <实际执行的 shell 命令>
- expected_output: <命令的预期输出>
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/)
- blocker: (失败时填写) definition_missing | commands_only | evidence_plan_missing | execution_pending_or_failed
- status: pending | passed | failed

### acceptance-2
...
```

## 三条铁律

1. **B2 就写好 test_command + expected_output** — 不是"应该测什么"，是"运行这条命令，期望这个结果"
2. **dev 先跑 RED 再 GREEN** — 先确认测试失败（证明测试有效），再实现到通过
3. **test skill 全绿才过** — 有一条 failed 就不能进 PR

## 迁移策略

旧 pre-tests.md：2 周兼容期，不阻塞门禁。新写的 pre-tests.md 必须用此格式。

## 涉及文件

| 文件 | 改动 |
|------|------|
| freely-doc-B2_IBM-execution/SKILL.md | 内置完整 pre-tests.md 模板 |
| freely-dev-loop-execution/SKILL.md | 情景 D 指向 B2 模板 |
| pretests-gate | 按新格式验证 |
