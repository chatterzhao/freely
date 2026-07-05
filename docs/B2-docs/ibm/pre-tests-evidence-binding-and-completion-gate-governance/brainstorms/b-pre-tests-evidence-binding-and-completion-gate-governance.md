# Brainstorm: pre-tests-evidence-binding-and-completion-gate-governance

## Goal

把 `pre-tests.md` 从“已写文档”升级成“宣称 completed 时必须通过的 gate 输入”，让 Freely 不再能在缺少 real-env / integration evidence 的情况下误判完成。

## Key Decisions

1. gate 以当前 issue 为入口，不扫描全仓
2. 第一阶段只卡 `phase_state=completed`
3. `pre-tests.md` 继续使用 Markdown，但要加入 machine-readable acceptance items
4. hook 与 standalone CLI 必须共用同一实现
5. artifact plane 仍是 canonical evidence；gate 只验证摘要与引用存在性

## Non-Goals

- 不在本批次统一所有历史 issue 的 `pre-tests.md`
- 不一次性解决 merged worktree auto-retire 的全部问题
- 不引入新的独立 JSON schema 或测试数据库

## Outcome

其他 worktree 只要合并这条能力、继续开发，在把 issue 改成 `completed` 时就会被同一套 gate 约束，不再依赖人脑记忆“这次到底测没测够”。
