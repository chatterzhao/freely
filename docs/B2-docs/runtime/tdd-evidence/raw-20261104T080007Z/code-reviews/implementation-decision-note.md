# Implementation Decision Note
- issue_id: I-20261104T080007Z-A
- issue_path: docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/issues/I-20261104T080007Z-A.md
- decision: 新增 `tests/unit/` 函数级语料（14 文件 / 68 断言）+ `worktree/pr_body.py` 强制 `## RED 证据` + `quality/runtime_red_gate.py` 接到 `pr-review-guarded` Step 2.5；用三个历史修复前快照补录 RED
- why_this: 运行时是 sourceable 库（#4153），65ms 即可加载，所以「函数级测试」的成本是写 harness，而不是重构 27k 行；PR body 是唯一不会被 `gh pr create` 冲掉的位置（仓库连模板都没有）；review 侧必须在 ACP reviewer 之前失败，否则缺失只会变成一条提示。
- alternatives_considered: ①只加 `.github/PULL_REQUEST_TEMPLATE.md`——`pr-create-guarded` 用 `--body` 显式传值，模板永远不生效；②从 27k 行里大规模抽纯函数——超出本 issue 范围，会把「建证据链」变成「重写运行时」；③review 侧只做人工提示——issue 明确要求 `needs_changes`；④把 RED 证据塞进 commit message——不可机检、跨平台不一致。
- boundary_non_goals: 未改 `runtime/freely` 任何一行；未改 `issue-write-one` 契约与 0/3/1 退出码；未改 promote/close 语义；未把 ACP reviewer 换掉（gate 只是前置）。
- residual_risk: ①`pr_body.py` 的「是否碰 runtime」默认用 `git diff --name-only <base>...HEAD`，深 rebase 或非标准 base 时可能判错（可用 `--touches-runtime` 显式覆盖）；②RED gate 依赖 pre-tests 的 `actual_RED_output` 字段名，字段改名即失效（AT 会用 fixture 抓到）；③14 个单测只覆盖状态机/锁/退出码/事件/DB 五类，27k 行里其余函数仍在端到端测试下；④`tests/unit/` 的测试依赖 `source runtime/freely` 成功，若运行时头部加载逻辑变更（#4153 的契约）需要同步调整 harness。

## 三个补录为什么可复现

RED 不是回忆，而是**快照重放**：`git archive <fix-merge-parent> | tar -x` 后把
`tests/unit/` 注入该树，`run.sh <group>` 直接跑。日志里能看到具体失败形态
（FATAL 缺函数 / 5 failed 缺 severity / SCHEMA=missing）。

## 一个刻意的设计取舍

`runtime_red_gate.py` 用 **三个退出码**（0 pass / 1 refuse / 2 skip）而不是
「pass/skip 都是 0」。`pr-review-guarded` 必须在 `set -e` 下区分「不适用」与
「通过」，否则 skip 会被当成 pass 静默放行。
