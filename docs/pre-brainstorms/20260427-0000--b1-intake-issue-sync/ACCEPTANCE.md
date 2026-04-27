# Acceptance - 20260427-0000--b1-intake-issue-sync

## 成功标准

### S1. 平台隔离
- [ ] ibm-framework.md 明确：AI 永远不直接读写平台内容
- [ ] scan 是平台→本地的唯一桥梁
- [ ] sync 是本地→平台的唯一桥梁
- [ ] sync 触发是确定性的生命周期事件，不是 AI 判断

### S2. 本地 issue 存储
- [ ] `.freely/issues/` 目录结构定义完整
- [ ] `ISSUES.md` 索引格式明确（local_id、kind、platform_ids、sync_state）
- [ ] `raw-*` 和 `I-*` 两种 issue 类型的区分清晰
- [ ] comment 独立存储，frontmatter 记录 `belongs_to`

### S3. chat 路由
- [ ] 每条 `freely chat` 必须落地为 issue 或已有 issue 的 comment
- [ ] 不存在 inbox——每一条插话都有归属
- [ ] chat-routing skill 只做路由，不做价值判断
- [ ] OPEN issue→comment，CLOSED issue→reopen 或新建并 link，新内容→新建 raw issue

### S4. dropped 语义
- [ ] 丢弃是 B1_IBM 的决定，不是 chat skill 的决定
- [ ] 即使内容看似无价值，也创建 raw issue，由 B1 标记 dropped
- [ ] `drop_reason` 是枚举值（out_of_scope / already_addressed / not_worthwhile / superseded / user_withdrawn）

### S5. sync 触发
- [ ] sync 触发事件表完整（chat、promoted、in_dev、merge、cleanup）
- [ ] sync 是异步的，不阻塞 AI 工作
- [ ] 网络不可用时 sync 失败不阻断 hook/gate

### S6. 文档一致性
- [ ] ibm-framework.md 包含 issue 存储和平台隔离章节
- [ ] AGENTS.md 引用新的 chat→issue 路由模型
- [ ] 不再引用已废弃的 `.freely/intake/`

### S7. 术语统一
- [ ] 全项目使用 B1_IBM / B2_IBM
- [ ] I = Input source（不是 Issue）
- [ ] raw issue / linked issue 区分明确
