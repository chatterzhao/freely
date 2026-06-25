---
local_id: raw-20260625T084506Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3494'
    url: https://github.com/chatterzhao/freely/issues/3494
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T08:45:25Z'
updated_at: '2026-06-25T08:45:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

B2_IBM skill 当前只提供 pre-tests.md 模板，没有告诫用户：不要凑字段糊弄门禁。用户倾向全部写 not_applicable + mock 绕过。

## 应加强

在 pre-tests.md 模板说明前加：

```
pre-tests.md 不是给门禁看的，是给测试执行者看的。
每条 acceptance item 必须是真实的测试用例。
如果不知道该测什么，重新读 raw issue 理解改动范围。
如果改动不影响某层，写 not_applicable 且写明理由——不是偷懒跳过。
禁止无理由全部 not_applicable + mock，禁止 status 写 pass 但 actual_output 为空。
```

## 改动

freely-doc-B2_IBM-execution SKILL.md
