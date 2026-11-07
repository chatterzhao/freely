# Implementation Decision Note
- issue_id: I-20261103T132540Z-A
- decision: 用单一 verdict 真源（Python 解析 + bash wrapper）同时约束写侧、读侧与审计侧；合并只认字面 pass，写侧「无法判定」落 needs_changes 且覆盖必须带 reason，审计侧 completed 豁免只保留记账部分
- why_this: 读侧只看文件存在、写侧默认 pass、审计侧把 completed 当全豁免，三者叠加使「评审通过」不携带任何信息；只要解析逻辑还存在第二份副本，写读两侧就一定会再次漂移。
- alternatives_considered: 读侧内联正则（第二份副本）；只认单一 verdict 写法（1 份 frontmatter 裸键历史文档解析失败）；保留无 reason 覆盖（issue 点名的滥用路径）；completed 全量套用未完成分支要求（历史 verification_artifact_dir 大量缺失，会立刻自锁每轮合并）；测试只断言源码字符串（无法证明行为）。
- boundary_non_goals: 不改 `.githooks/`、`commit-msg.sh`、`post-checkout`；不改 R8/R9/R9.5 的 fail-closed 语义与 receipt 审计；不批量改写 401 份历史 review 文档；不夹带 #4149（写通道）与 #4151（测试证据链）。
- residual_risk: ①审计侧 completed 分支仍不强制 `verification_artifact_dir` 字段，只要求绑定 review + pass verdict —— 这是为避免历史语料自锁的有意取舍，已在 brainstorms 决策 5 说明。②ACP 的 `freely-review` 路径在本机 owner lane 不可用，该分支（默认值反转 + 覆盖落痕）只有静态断言与代码评审覆盖，未做运行时冒烟；manual 路径的拒绝逻辑已实测。③`verdict` 字段与 #4154 的契约索引尚未接线，字段名目前以本模块文档注释为准。
- verification: AT-001 基线快照（`git archive develop -- docs bin`）RED 静态 13 项 FAIL / behavior 中止 → GREEN `SUMMARY: 13 ok, 0 failed`；CASE F 真实语料 `401 review docs, 399 with verdict, 0 unparseable`；11 个相关回归以未修改 develop HEAD 基线对比零新增失败（退出码与行数全部一致，5 处逐字节差异均为耗时/mktemp 随机名）；真实工位反向探针（review 改 `verdict: fail`）令 `pr-merge-guarded` 与 `governance-merge-gate --staged` 均阻断，还原 pass 后真实受控合并通过。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；`verdict` 字段登记属既有 #4154 范围，按其正文登记，不重复立项。
