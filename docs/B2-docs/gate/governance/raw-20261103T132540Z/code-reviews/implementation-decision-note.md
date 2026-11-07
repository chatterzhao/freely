# Implementation Decision Note
- issue_id: I-20261103T132540Z-A
- decision: 用单一 verdict 真源（Python 解析 + bash wrapper）同时约束写侧、读侧与审计侧；合并只认字面 pass，写侧「无法判定」落 needs_changes 且覆盖必须带 reason，审计侧 completed 豁免只保留记账部分
- why_this: 读侧只看文件存在、写侧默认 pass、审计侧把 completed 当全豁免，三者叠加使「评审通过」不携带任何信息；只要解析逻辑还存在第二份副本，写读两侧就一定会再次漂移。
- alternatives_considered: 读侧内联正则（第二份副本）；只认单一 verdict 写法（1 份 frontmatter 裸键历史文档解析失败）；保留无 reason 覆盖（issue 点名的滥用路径）；completed 全量套用未完成分支要求（历史 verification_artifact_dir 大量缺失，会立刻自锁每轮合并）；测试只断言源码字符串（无法证明行为）。
- boundary_non_goals: 不改 `.githooks/`、`commit-msg.sh`、`post-checkout`；不改 R8/R9/R9.5 的 fail-closed 语义与 receipt 审计；不批量改写 401 份历史 review 文档（本轮只新增 1 份）；不夹带 #4149（写通道）与 #4151（测试证据链）。
- residual_risk: ①审计侧 completed 分支仍不强制 `verification_artifact_dir` 字段，只要求绑定 review + pass verdict —— 这是为避免历史语料自锁的有意取舍，已在 brainstorms 决策 5 说明。②ACP 的 `freely-review` 路径在本机 owner lane 不可用，该分支（默认值反转 + 覆盖落痕）只有静态断言与代码评审覆盖，未做运行时冒烟；manual 路径的拒绝逻辑已实测。③`verdict` 字段与 #4154 的契约索引尚未接线，字段名目前以本模块文档注释为准。④新的 completed 规则要求「评审产物先于 PR 存在」，改变了此前 pr-create 时无 review 也能过门的顺序（此前正是靠 completed 全豁免通过）；本轮的 review 文档因此在 pr-create 之前落库。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；`verdict` 字段登记属既有 #4154 范围，按其正文登记，不重复立项。

## Implementation Decision Note
- decision: 单一 verdict 真源 + 三侧共用；合并只认 pass；写侧默认 needs_changes 且覆盖带 reason；completed 只保留记账豁免
- why_this: 「文件存在=通过」「判不出来=通过」「评审过就免证据」三者叠加，使合并门禁对 develop 的强制力恒为真；解析逻辑一旦有第二份副本，写读两侧必然再次漂移
- alternatives_considered: 读侧内联正则；只认单一写法；保留无 reason 覆盖；completed 全量套用未完成分支要求（立即自锁）；测试只断言源码字符串
- boundary_non_goals: 不动 `.githooks/` / `commit-msg.sh` / `post-checkout`；不动 R8/R9/R9.5 语义；不批量改写 401 份历史 review；不夹带 #4149 / #4151
- residual_risk: completed 分支仍不强制 verification_artifact_dir（有意取舍）；ACP freely-review 分支仅有静态断言覆盖；verdict 字段待 #4154 登记；评审产物必须先于 PR 存在
