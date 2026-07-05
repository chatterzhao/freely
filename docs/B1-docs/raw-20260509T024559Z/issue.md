---
local_id: raw-20260509T024559Z59Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
phase_state: completed
platform_ids:
  github:
    issue_id: '265'
    url: https://github.com/chatterzhao/freely/issues/265
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-09T03:28:23Z'
updated_at: 2026-05-17T04:47:25Z
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 目标

`freely daemon start` 支持多项目、多 issue 并发开发。项目路径通过 `--project` 指定。

## 使用方式

开发过程（狗粮）:
```
cd /path/to/freely
freely daemon start --task-mode auto --project /path/to/freely
```

安装后:
```
freely daemon start --task-mode auto --project ~/my-project
```

## --project 参数规则

| task-mode | --project | 说明 |
|-----------|-----------|------|
| wait / 未传 | 可选 | 不传时启动但 task_mode 强制切为 wait，打印: "未指定要开发的项目。使用 --project <your-dev-project-root-path> 指定。" |
| auto | **必传** | 支持逗号分隔多个项目: `--project ~/a,~/b` |
| id:<scan-id> | **必传** | 且只能有一个项目: `--project ~/a` |

## 实现逻辑

```
freely daemon start --task-mode auto --project <root>

1. 验证 project root（looks_like_project_root）
2. 读 milestones.md → 找 active raw issue
3. task-mode=id:<scan-id> → 读 scan 文件 → 根据数据语义理解任务
4. git -C $project worktree list → 找到对应 raw-key 的工位
5. 判断: cd 到已有工位 / wt-create 新建工位 / 报错
6. Manager patrol 产出 continuity + worker prompt
7. Worker launch 到 fix/feature 工位（#264 验证）
```

## 多项目隔离

- 每个项目独立 git repo → `git -C $project worktree list` 天然隔离
- 门禁验证: worktree 路径必须在 `{project}-worktrees/` 下
- raw-key 在同一 repo 内唯一，跨 repo 不冲突

## 狗粮

Freely 开发 Freely 就是:
```
cd /path/to/freely
freely daemon start --task-mode auto --project /path/to/freely
```
和其他项目无区别。
