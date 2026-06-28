---
issue_id: I-20260628T005815Z-A
issue_path: docs/issues/I-20260628T005815Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260628T005815Z-A
- issue_path: docs/issues/I-20260628T005815Z-A/issue.md

## Implementation Decision Note

- decision: 将 `freely chat` 拆分为 `freely comment`（平台直写评论）、`freely discuss`（AI 群聊讨论）和讨论归档 skill（手工触发，分析讨论 → 评论/raw issue）
- why_this: 三种场景（评论、讨论、讨论整理）共享同一套本地 DB 存储路径，导致评论延迟、讨论无法结构化、入口混淆。拆分为独立命令各自走最合适路径：评论直达平台、讨论本地+平台双向同步、导出纯手工。
- alternatives_considered:
  - Option A（修补现有 chat）：加更多 flag → 拒绝，复杂度叠加不解决根本矛盾
  - Option C（全部走平台废弃本地 DB）→ 拒绝，讨论需要本地私有、Gitee 无 Discussions
  - 选择 Option B：评论平台直写 + 讨论本地+平台同步 + 导出手工触发
- boundary_non_goals:
  - 不改造 B1 skill（讨论头脑风暴是独立重建，B1 不动）
  - 不自动调用导出（纯手工）
  - 不处理 chat --new-issue 自动 feedback（已有独立 issue）
  - 不处理 wt-create assignee（已有独立 issue）
  - Gitee Discussions 不参与（平台不支持）
  - I-* issue 不碰（内部维护）
  - close issue 不自动 reopen（独立路径）
- residual_risk:
  - GitHub Discussions API 可能限制频率或格式，需实测验证
  - GitCode Discussions API 文档可能与实际有差异
  - 讨论 webhook/轮询机制依赖平台能力，Gitee 无 Discussions 导致该平台讨论不可见
  - 旧 chat 入口废弃需要过渡期，直接删除可能影响现有 TUI/CLI 用户习惯
  - 大改动（~10 文件），合并冲突风险较高
