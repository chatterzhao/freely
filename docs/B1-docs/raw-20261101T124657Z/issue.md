---
local_id: raw-20261101T124657Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '4115'
    url: https://github.com/chatterzhao/freely/issues/4115
    synced_at: ''
  gitee:
    issue_id: IKS3AV
    url: https://gitee.com/zhaoquan/freely/issues/IKS3AV
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-01T12:46:57Z'
updated_at: '2026-11-01T13:07:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

# feat: dsh-freely issue→PR E2E slice

raw_key: raw-20261101T124657Z

## 背景

`@freely/dsh-freely` P1 打包 raw 只交付 bundle/preset/白名单/bridge。

完整 issue→PR E2E 依赖上游 C-B/C-D 的 ownership/handoff/HarnessPort，不能在 P1 里假装完成。

## 任务

1. 等 C-B/C-D merge 后，接 Manager→Worker→Reviewer→PR 全链路。
2. 使用 P1 插件作为 DSH host；不复制 loop。
3. 通过 pretests-gate 和真实 PR 验证。

## 非目标

- 不在本 raw 重做 P1 打包。

