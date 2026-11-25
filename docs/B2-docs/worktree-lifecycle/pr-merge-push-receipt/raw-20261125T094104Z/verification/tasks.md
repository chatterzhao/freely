# Tasks: I-20261125T094104Z-A

- issue_id: I-20261125T094104Z-A
- phase_state: in_b2_ibm

## T1 — push 块改造
- [ ] 去掉 `git push all "$_src_branch" 2>/dev/null || true`
- [ ] 遍历 configured remotes（跳过 all），逐 remote push 并捕获结果
- [ ] 汇总成功/失败到变量

## T2 — 回执 fail-closed
- [ ] 失败 remote 汇总 failed_remotes + 非零退出
- [ ] 失败回执含可执行重试命令（封装入口提示）
- [ ] 成功回执逐 remote 列状态，删除无条件 "pushed" 打印

## T3 — 验收
- [ ] AT-001 RED（develop 基线）→ GREEN（工位）
- [ ] 回归：pr-merge 相关既有 AT 全绿
- [ ] test-all --ci 全绿
