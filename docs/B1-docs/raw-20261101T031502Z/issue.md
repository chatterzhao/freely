---
schema_version: '1'
local_id: raw-20261101T031502Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4110'
    url: https://github.com/chatterzhao/freely/issues/4110
    synced_at: ''
  gitee:
    issue_id: IKS0MD
    url: https://gitee.com/zhaoquan/freely/issues/IKS0MD
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-01T03:15:02Z'
updated_at: '2026-11-01T03:15:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# docs: Super-agent 架构与 Freely agent 协作模型对比研究

workflow_kind: feature

## 背景
DeepSeek Harness 团队 2026-10-31 发布设计文章《Exploring Super-agent Design: Towards a More Autonomous Agent System》，并开源研究原型 https://github.com/deepseek-ai/dsh-superagent-prototype（MIT，TypeScript，9 篇按序编号设计文档）。核心主张是用计算机系统经典思想（双层 Router/Worker、事件驱动、订阅直通、存算分离、外部 Watchdog）接管会话调度，把人的注意力留给决策与验收。

## 要做的事
1. 完整阅读其文章与原型 9 篇设计文档、prompts/、skills/、核心 src/ 实现，提炼设计理念与约束。
2. 与 Freely 现有架构做客观比较，重点在 agent 协作：角色分工（Router/Worker vs Manager/Worker/Reviewer）、Task 协调协议（Subscription/Fan-out/Handoff/Attention vs A2A）、授权模型（Mandate/Policy vs worktree/branch/gate/IBM 生命周期）、事件与状态（Trigger/Thread/Ticket vs scan/a2a_tasks/milestones）、失败与恢复（Watchdog/Assignment restart vs supervisor/watchdog/loop guard）、可观测与人机交互面。
3. 明确双方前提、成本与未解问题，不做优劣站队式结论；给出对 Freely 可借鉴/不可照搬的判断。
4. 产物落 freely 规范文档，并给出 candidate 建议。

## 验收
- 研究文档覆盖上述比较维度，事实可回溯到文章/仓库文档/源码。
- 明确指出至少 3 处结构性差异及其影响。
- 给出可执行的 candidate 建议（或明确判定无需吸收）。
