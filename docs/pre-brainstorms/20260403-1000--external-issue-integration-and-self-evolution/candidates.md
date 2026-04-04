# Candidates - 20260403-1000--external-issue-integration-and-self-evolution

## C-20260403-1000-A

- candidate_format_version: `v2`
- title: 外部 Issue 消化与候选 Issue 闭环流程
- problem: Freely 需求来源多元（GitHub issue、Gitee issue、内部需求），但缺乏统一的消化流程和状态同步机制。外部 issue 未消化就可能被重复消费，内部需求缺乏透明化追踪，状态更新无法同步回 GitHub。
- why_now:
  - Freely 已具备"打工"能力，打工中会持续发现 Freely 自身缺口
  - 需要开放仓库让用户提交反馈，同时避免未消化 issue 被重复处理
  - 需要内部需求与外部需求统一的追踪机制
- acceptance_criteria:
  - 定义外部 issue（GitHub/Gitee）消化流程：扫描 → 过滤已消化 → 预研 → 候选 issue (C-xxx，内部)
  - 定义里程碑接纳流程：候选 issue 被接纳后创建里程碑 issue (I-xxx) 到 GitHub
  - 定义来源 issue 绑定流程：创建里程碑 issue 后在来源 issue 添加评论链接 + `status: triaged` 标签，但不关闭来源 issue
  - 定义映射关系：`里程碑 issue I-xxx (内部) ↔ GitHub 里程碑 issue #xxx ↔ GitHub 来源 issue #xxx`（如有）
  - 定义双边状态同步：项目内部 phase_state 变更时同时更新来源 issue（评论）和里程碑 issue（标签+评论）
  - 定义完成时关闭流程：来源 issue 和里程碑 issue 同时关闭
  - 定义内部需求流程：预研 → 候选 issue → 里程碑 issue 到 GitHub（无来源 issue，单边追踪）
  - 定义标签体系：`status: new/triaged/in-progress/completed` + `source: github/gitee/internal`
  - 定义来源 issue 与里程碑 issue 的区分：来源 issue 无 source 标签，里程碑 issue 有 source 标签
- promotion_gate:
  - 证明流程能避免外部 issue 重复消费
  - 证明状态同步不会产生竞态条件
  - 证明标签体系足够区分不同状态
  - 保持聚焦在 issue 生命周期管理，不扩展到完整的项目管理系统
- open_questions:
  - 多平台（GitHub/Gitee/GitLab）API 如何抽象
  - 同步频率：启动时全量 vs 增量 vs webhook
  - 内部需求是否强制同步到 GitHub（透明化 vs 效率）
  - 来源 issue 在预研期间被外部关闭如何处理
- acceptance_reviews:
  - reviewer: `human`
    verdict: `supports`
    note: 流程设计完整，核心规则清晰，可以推进实现
- decision_reason:
  - 这是 Freely 自身迭代的基础设施，决定需求如何流动
  - 统一入口可以避免需求散落在多个渠道
  - GitHub 作为公开窗口，用户可以看到 Freely 正在做什么
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `iflow`
    session_id: `current-thread`
    jsonl_path: `unavailable://iflow-thread-only`
    role: `author`
- next_action:
  - 确认流程设计是否完整
  - 评估是否需要拆分为多个 issue（扫描、消化、同步）
- revisit_trigger:
  - 发现新的需求来源渠道
  - 状态同步出现不一致
  - 标签体系无法满足分类需求

---

## C-20260403-1000-B

- candidate_format_version: `v2`
- title: GitHub Issue 扫描与状态同步 Skill
- problem: Freely 需要一个 skill 来扫描 GitHub/Gitee issue，并根据项目内部状态同步更新 issue 状态。当前没有这样的 skill 存在。
- why_now:
  - 上一候选 issue (C-20260403-1000-A) 定义了流程，需要具体实现
  - GitHub CLI (`gh`) 已可用，可以作为 API 调用基础
- acceptance_criteria:
  - 实现扫描 GitHub open issues 的能力
  - 实现过滤已消化 issue（带 `status: triaged` 标签）的能力
  - 实现区分来源 issue 和里程碑 issue：来源 issue 无 source 标签，里程碑 issue 有 source 标签
  - 实现创建里程碑 issue (I-xxx) 到 GitHub 并添加标签的能力
  - 实现在来源 issue 添加评论链接 + `status: triaged` 标签的能力（不关闭来源 issue）
  - 实现映射关系存储：`里程碑 issue I-xxx (内部) ↔ GitHub 里程碑 issue #xxx ↔ GitHub 来源 issue #yyy`
  - 实现映射关系读取：根据内部里程碑 ID 查找对应的 GitHub issue 编号
  - 实现状态同步：`triaged` → `in-progress` → `completed`
  - 实现完成时同时关闭来源 issue 和里程碑 issue
  - 定义里程碑 issue 内容格式：包含标题、来源链接、预研链接、验收标准
  - 支持 Gitee API（或预留扩展点）
- promotion_gate:
  - 证明 `gh` CLI 可以满足所有 GitHub 操作需求
  - 证明 skill 可以被 Freely runtime 调用
  - 证明错误处理（API 限流、网络异常）足够健壮
- open_questions:
  - 是否需要 GitHub App 认证还是 Personal Token
  - 是否需要支持私有仓库
  - 多平台 API 如何统一抽象
- acceptance_reviews:
  - reviewer: `pending`
    verdict: `pending`
    note: 待上一候选 issue 确认后推进
- decision_reason:
  - 这是流程实现的基础设施
  - 需要在确定流程后实现
- priority: `P2`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260403-1000-A`
- session_refs:
  - tool: `iflow`
    session_id: `current-thread`
    jsonl_path: `unavailable://iflow-thread-only`
    role: `author`
- next_action:
  - 等待 C-20260403-1000-A 确认
- revisit_trigger:
  - GitHub API 变更
  - 需要支持新的 issue 平台

---

## C-20260403-1000-C

- candidate_format_version: `v2`
- title: 内部需求回流机制
- problem: 打工中发现的 Freely 缺口、运行时异常、治理漂移等内部需求，缺乏统一的回流机制。需要决定是否同步到 GitHub，以及如何避免循环消费。
- why_now:
  - Freely 已具备打工能力，会持续发现自身缺口
  - 内部需求需要与外部需求统一管理
  - 用户可能希望看到 Freely 的开发透明度
- acceptance_criteria:
  - 定义内部需求分类：Freely 自身问题 vs 用户项目问题
  - 定义回流路径：写入 Freely 的 pre-brainstorms/
  - 定义是否同步到 GitHub 的判断规则
  - 定义同步后的标签：`status: triaged` + `source: internal`
  - 确保已同步的内部 issue 不会被预研重复消费
- promotion_gate:
  - 证明分类逻辑可以区分"用户项目问题"和"Freely 自身问题"
  - 证明同步与否的决策规则清晰
  - 证明不会产生循环消费（内部 issue → 预研 → 候选 issue → 内部 issue）
- open_questions:
  - 内部需求是否强制同步到 GitHub
  - 不同步的内部需求如何追踪
  - 打工中发现的缺口如何自动识别为 Freely 问题
- acceptance_reviews:
  - reviewer: `pending`
    verdict: `pending`
    note: 待上一候选 issue 确认后推进
- decision_reason:
  - 这是 Freely 自身迭代的关键机制
  - 需要在确定流程后实现
- priority: `P2`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260403-1000-A`
- session_refs:
  - tool: `iflow`
    session_id: `current-thread`
    jsonl_path: `unavailable://iflow-thread-only`
    role: `author`
- next_action:
  - 等待 C-20260403-1000-A 确认
- revisit_trigger:
  - 发现新的内部需求来源
  - 分类逻辑出现误判

---

## C-20260403-1000-D

- candidate_format_version: `v2`
- title: Freely 自身迭代与用户项目开发调度策略
- problem: Freely 在打工过程中发现自身缺口后，需要迭代自身。但如何调度才能不打断用户项目开发？资源如何竞争？什么时候切换到 Freely 自身开发？
- why_now:
  - 外部 issue 集成流程已定义 (C-20260403-1000-A)
  - 内部需求回流机制已定义 (C-20260403-1000-C)
  - 缺少调度策略来协调 Freely 自身开发和用户项目开发
- acceptance_criteria:
  - 定义调度策略：串行切换 vs 并行 worker vs 需求收集+批量迭代
  - 定义优先级规则：阻塞性问题立即处理 vs 非阻塞问题排队
  - 定义上下文切换时机：用户项目空闲时 vs 累积到阈值时
  - 定义 Freely 升级对用户项目的影响：版本锁定 vs 跟随更新
  - 定义回切规则：Freely 开发完成后如何回到用户项目
- promotion_gate:
  - 证明调度策略不会频繁打断用户项目
  - 证明阻塞性问题能得到及时处理
  - 证明上下文切换不会丢失用户项目状态
- open_questions:
  - 一个 Freely runtime 能否同时管理多个项目
  - 是否需要独立的 Freely 自身开发 worktree
  - Freely 升级时是否需要重启 runtime
- acceptance_reviews:
  - reviewer: `pending`
    verdict: `pending`
    note: 待流程设计确认后推进
- decision_reason:
  - 这是 Freely 自身迭代落地的关键机制
  - 需要在流程和回流机制就位后实现
- priority: `P2`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260403-1000-A`
  - `C-20260403-1000-C`
- session_refs:
  - tool: `iflow`
    session_id: `current-thread`
    jsonl_path: `unavailable://iflow-thread-only`
    role: `author`
- next_action:
  - 等待流程设计确认
- revisit_trigger:
  - 调度策略导致用户项目频繁中断
  - Freely 升级导致用户项目状态丢失
