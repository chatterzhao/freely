---
issue_id: I-20260720T023136Z-A
issue_path: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/issues/I-20260720T023136Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260720T023136Z-A
- issue_path: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/issues/I-20260720T023136Z-A.md

## Implementation Decision Note

- decision: 将 `docs/system/workspace/scripts/runtime/freely` L6700 的 log_error 参数从双层双引号改为整体单引号包裹
- why_this: 双引号内嵌套双引号使外层引号提前闭合，`<描述>`/`<详细描述>` 落入非引号区被 bash 解释为输入重定向；单引号内 `<`、`>`、`"` 全部按字面量输出，是最小且语义正确的修复
- alternatives_considered: Option B 转义尖括号（`\<描述\>`）可行但可读性差且嵌套引号易复发；Option C 用 printf '%s' 改 log_error 调用方式，超出最小修复面
- boundary_non_goals: 不扫描/不改写其他 log_error 消息；不改 log_error 函数签名；不新增帮助文档；不改变 chat 命令执行语义
- residual_risk: 若未来该消息需要插入变量或引入新嵌套引号，需重新审视引号策略；低风险，因当前为纯静态字符串
