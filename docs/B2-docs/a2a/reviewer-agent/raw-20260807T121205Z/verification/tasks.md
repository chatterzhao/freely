# Tasks: I-20260807T121205Z-A

- [x] T1 B1 预研：B0 广搜 / 锚点 / 判定 bug；candidate promoted 入 M-20260807T121205Z-A
- [x] T2 B2 设计：prd / pre-tests / tasks / IDN / verdict 文档，story 复用 a2a/reviewer-agent
- [x] T3 设计 AT：test-reviewer-assign-raw-key.py，覆盖发出 / 拒绝 / 优先级 / 不变 / watchdog 断言 / 双列表注册
- [x] T4 RED：对 develop 基线跑 AT，确认 failed（2 ok / 4 failed），回填 actual_RED_output
- [x] T5 dev：a2a_task.py a2a-exit 更新分支补 raw_key + fail-closed
- [x] T6 GREEN：fix 工位 6 ok / 0 failed；test 工位 merge + test-gate 验证

后续生命周期（issue-sync promote / raw 表对齐 / PR 门禁链 / wt-close）由 workflow skill 驱动，不属于本 owner issue 的实现切片。
