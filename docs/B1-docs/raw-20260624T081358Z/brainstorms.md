# Brainstorms: skills/AGENTS 测试文档 daemon 假设修复

## Discovery
`docs/B1-docs/raw-20260624T081358Z58Z/issue.md`：freely-fix-execution、freely-test-execution、freely-feat-execution 和 AGENTS.md 中测试步骤写成 "stop/start daemon → 验证"，假设所有项目都是 daemon 型。Freely 面向任意类型项目，测试方式应由 pre-tests.md 定义。

## Research
**根因**：Freely 自举开发中 naturally 以自身（daemon 型）为参考写成。
**方案**：skill 文档只描述流程（"按 pre-tests.md 执行验证"），不硬编码验证手段。委托链：B2_IBM 写 pre-tests.md → dev-loop RED-GREEN → test-execution 执行。

## Decision
Promote。改 4 个文件，纯文档修整，不涉及代码逻辑。
