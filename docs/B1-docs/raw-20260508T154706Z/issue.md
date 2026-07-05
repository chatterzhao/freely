---
local_id: raw-20260508T154706Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '260'
    url: https://github.com/chatterzhao/freely/issues/260
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T15:47:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 改动

1. `--skill` 参数改为接受名称（`fix-execution` / `feat-execution`），内部映射到路径。不再需要传 `docs/system/workspace/skills/fix-execution/SKILL.md`
2. wt-create 成功后在输出末尾打印提醒：

```
工位创建成功。接下来：
  cd <fix-target>   # 进入 fix 工位
  仔细阅读 docs/system/workspace/skills/{name}/SKILL.md 及其引用的 skill
  按 skill 工作流进行实现
```

## 示例

```bash
# 旧
freely wt-create --skill docs/system/workspace/skills/fix-execution/SKILL.md ...

# 新
freely wt-create --skill fix-execution ...
```
- pre_tests_path: docs/B2-docs/skill-name-reminder/verification/pre-tests.md
- verification_artifact_dir: docs/epics/skill-name-reminder/code-reviews
