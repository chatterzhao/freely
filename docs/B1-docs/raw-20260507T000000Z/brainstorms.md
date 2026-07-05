# Brainstorms: Unified platform layer for issue-sync

## Discovery

### 来源
- Raw issue: `raw-20260507T070000Z`
- GitHub issue #243 — platform
- created_at: 2026-05-07T10:30:15Z
- platform_state: open

### 问题陈述
当前平台交互散落在 5+ 个文件中，功能重叠但不统一：

| 文件 | 职责 | 问题 |
|------|------|------|
| `bin/issue-sync` | 主写路径 | 缺多平台自动补齐 |
| `platform-adapter.py` | Python 封装 | 缺 labels/hash/comment-tracking |
| `issue-sync-batch.py` | 历史遗留 | GitHub-only，绕过 issue-sync |
| `raw-issue-pull` | 平台拉取 | 只找第一个平台 |
| `wt-create` | 工位创建 | chat-inbox 物化后没调 issue-sync create |

**目标**: merge develop 后，所有用户已配置的仓库平台上的 issue 数量、状态、评论完全一致。

### 当前状态
Raw issue 已确认，详细设计方案已在 issue 中描述，但未进入正式 B1 预研。

### 方案概要
统一的仓库平台层，提供 `create/update/close/comment/pull` 操作，所有 CLI/脚本统一调用：
- chat-inbox → raw issue：wt-create materialize 后调用 `platform.create(local_id)`
- 平台拉取 → raw issue：补建缺失的平台记录
- merge 后同步：调用 `platform.update/close` 同步所有平台

### 价值与时效性判断
- 多平台支持是项目长期可用的基础设施需求
- 当前散落的实现增加了维护成本和引入新平台的门槛
- 统一的平台层是后续自动化流程的基础

**结论**: 价值确认，进入 B1 预研流程。

## Status

discovery (needs B1 research)

## Next Action

complete B1 pre-brainstorm — 评估现有 5+ 文件的职责和重叠范围，设计统一平台层的架构和迁移路径。
