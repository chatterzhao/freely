# Implementation Decision Note
- issue_id: I-20261103T132526Z-A
- decision: 平台写通道的失败必须原样非零并可诊断；gitee 调用对齐 adapter 已在用的真实 CLI 契约、token 权威单点、探测区分四类原因、部分成功独立退出码且先落 id 再写 platform_state
- why_this: 写失败被 `|| echo` 兜底成「合法空结果」，token 门禁从未赋值又让整段 Gitee 通道静默跳过，探测四因合一再把它翻译成「不支持该平台」——三层叠加使「平台上根本没有对象」与「创建成功」不可区分，且可追溯性承诺在 Gitee 侧 100% 失效。
- alternatives_considered: 给旧 JSON 位置参数签名打补丁（第二层字符串拼装）；bash 侧读 token 再传（双权威）；继续文本 grep 判状态（status 行位置不稳）；夹带 #4184 关闭路径部分成功、#4154 常量收口、#4166 双平台入口收口。
- boundary_non_goals: 不改读通道（#4195 的 read_health/__degraded__）；不改 `cmd_close` 严格路径（#4184）；不改 .githooks/ 与 pr-merge-guarded；不批量重写历史 frontmatter。
- residual_risk: ①未真实创建平台 issue，写通道 happy path 由 stub CLI + 真实脚本覆盖，真机仅只读核验。②`cmd_close` 的非严格路径仍保留「先关平台后写本地状态」的顺序，属 #4184，本轮只在注释标注。③`_gitee_repo` 仍与 adapter 的 `detect_repo` 各有一份实现（语义已一致并有测试守护），统一归 #4154。④`create-issue` 的 `update-issue` 分支仍用全或退出码，未对齐 0/3/1（无调用方依赖部分语义，留待 #4166）。
- verification: AT-001 基线快照（`git archive HEAD -- bin docs`）RED `SUMMARY: 7 ok, 15 failed` → GREEN `SUMMARY: 22 ok, 0 failed`；9 个相关回归基线对比退出码全一致、5 处差异仅计时行；真机只读核验 `_gitee_repo=zhaoquan/freely`、adapter `Available: ['github','gitee']`。
- self_bootstrap_findings: 未发现「现有 open issue 未覆盖」的新缺陷；关闭路径部分成功归 #4184、契约收口归 #4154、双平台入口归 #4166，均在正文证伪后排除。

## Implementation Decision Note
- decision: 失败不兜底、token 单权威、探测报因、部分成功退出 3 且先落 id 后写状态
- why_this: 三层静默叠加使写通道「不做事也报成功」，可追溯性承诺失效
- alternatives_considered: 旧 JSON 签名打补丁；bash 侧读 token；文本 grep 判状态；夹带 #4184/#4154/#4166
- boundary_non_goals: 读通道、cmd_close 严格路径、.githooks/、pr-merge-guarded 均不动
- residual_risk: 未真实建单（stub 覆盖）；cmd_close 非严格路径归 #4184；repo 身份两份实现待 #4154；update-issue 退出码待 #4166
