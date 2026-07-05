# Acceptance - 20260427-0000--b1-intake-issue-sync

## 成功标准

### S1. 平台隔离
- [x] ibm-framework.md 明确：AI 永远不直接读写平台内容
- [x] scan 是平台→本地的唯一桥梁
- [x] sync 是本地→平台的唯一桥梁
- [x] sync 触发是确定性的生命周期事件，不是 AI 判断

### S2. 本地 issue 存储
- [x] `docs/issues/` 目录结构定义完整
- [x] `ISSUES.md` 索引格式明确（local_id、kind、platform_ids、sync_state）
- [x] `raw-*` 和 `I-*` 两种 issue 类型的区分清晰
- [x] comment 追加在 issue.md 的 `## Comments` 章节，`###` 元数据行记录归属

### S3. chat 路由
- [x] 每条 `freely chat` 必须落地为 issue 或已有 issue 的 comment（chat-routing skill 设计完成）
- [x] 不存在 inbox——每一条插话都有归属
- [x] chat-routing skill 只做路由，不做价值判断（SKILL.md 已创建）
- [x] OPEN issue→comment，CLOSED issue→reopen 或新建并 link，新内容→新建 raw issue

### S4. dropped 语义
- [x] 丢弃是 B1_IBM 的决定，不是 chat skill 的决定
- [x] 即使内容看似无价值，也创建 raw issue，由 B1 标记 dropped
- [x] `drop_reason` 是枚举值（out_of_scope / already_addressed / not_worthwhile / superseded / user_withdrawn）

### S5. sync 触发
- [x] sync 触发事件表完整（chat、promoted、in_dev、merge、cleanup）
- [x] sync 是异步的，不阻塞 AI 工作
- [x] 网络不可用时 sync 失败不阻断 hook/gate

### S6. 文档一致性
- [x] ibm-framework.md 包含 issue 存储和平台隔离章节
- [x] AGENTS.md 引用新的 chat→issue 路由模型
- [x] 不再引用已废弃的 `.freely/intake/`（brainstorms 中已标记为 [当前]）

### S7. 术语统一
- [x] 全项目使用 B1_IBM / B2_IBM
- [x] I = Input source（不是 Issue）
- [x] raw issue / linked issue 区分明确
