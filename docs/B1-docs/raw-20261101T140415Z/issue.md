---
schema_version: '1'
local_id: raw-20261101T140415Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261101T140415Z-A
platform_ids:
  github:
    issue_id: '4117'
    url: https://github.com/chatterzhao/freely/issues/4117
    synced_at: ''
  gitee:
    issue_id: IKS3MM
    url: https://gitee.com/zhaoquan/freely/issues/IKS3MM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-01T14:04:15Z'
updated_at: '2026-11-02T10:26:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-02T09:45:41Z'
closeout_note: ''
---

# docs: super-agent 架构研究补全（react/事件/ownership/示例项目）

workflow_kind: feature

## 背景

上一轮 Super-agent 对比研究把 ReAct 只当成一句“Async ReAct，不吸收”，没有按意图分析经典 ReAct Loop、异步 ReAct、事件准入、Thread/ownership、上下文组织、Watchdog、部署形态与示例项目。

用户要求系统化重做：

- 抓取并归档微信原文（含图）到 B1 research。
- 每个重要模块按“解决什么问题 / Freely 是否也解决 / 现状好坏 / 吸收/改造/不吸收”评审。
- 不按叫法对齐，按功能/意图。
- 覆盖示例项目 dsh-superagent-prototype 的实现与缺口。
- 给出明确 ADR 与后续 candidate。

## 产物

- `research/super-agent/`：source.html、article.md、15 图、metadata、逐节笔记、意图矩阵、示例项目分析、Freely 评审、ADR。
- 不实现 runtime 变更；研究完成后按 ADR 另开实现 issue。

## 验收

- 文章正文/图片可本地打开，来源与 hash 可追溯。
- 五个模块 + ReAct/示例项目都有意图级分析。
- 每个模块有明确态度与证据。
- 不把“文章主张/原型实现/Freely 现状”混为一谈。
