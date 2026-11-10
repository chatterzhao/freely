# Implementation Decision Note
- issue_id: I-20261110T060553Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T060553Z/issues/I-20261110T060553Z-A.md
- decision: 先交付状态文件安全协议单一所有者与冻结边界，不改现有 55 处 source / 15 处写入点；逐组迁移拆独立 issue
- why_this: 状态值是 shell 赋值且被 `source`，AI 生成的摘要/reason/分支名含 `"`/`$()`/换行即注入或让 supervisor 崩溃。但 55 读 + 15 写、77 个键、部分位置格式，一轮全迁无法验证「行为不变」；issue 原文即要求「逐组迁移，每组单独提交」。
- alternatives_considered: ①一轮把 55 处 source 全替成 helper——白名单可能漏键、位置格式需单独判定、安全中间文件仍需评审；②`printf %q` 后继续写 shell 赋值——写入侧仍是代码，无法排除未来新值；③拒绝读旧格式——要求人工清空 `.freely/run/`，违反不退化边界；④无白名单接受任意 KEY——状态键没有契约，拼错会静默产生新状态。
- boundary_non_goals: 不改 `runtime/freely` 任何一行；不改 39 处非状态 source；不改 `load_meta_env_snapshot`；不回填/删除既有状态文件；不引入第三方依赖。
- residual_risk: ①现有 55 处 `source` 仍在，注入面**尚未关闭**——本轮只是提供安全协议与冻结边界，真正消除依赖第二阶段；②`ALLOWED_KEYS` 77 键来自 develop 全量扫描，若第二阶段发现新键须扩充；③兼容 reader 对旧格式只去一层引号，畸形行（多个 `=`/未闭合引号）按原样保留，不报错；④`to-shell` 生成的是 shell 赋值，调用方必须只 source 这段生成文本而非原文件。
- verification: AT-001 基线 RED `1 ok / 7 failed`（PoC 创建 marker）→ 工位 GREEN `9 ok / 0 failed`；6 个相关测试 + `bin/test-all --ci` + `check-state-file-sources` 全绿。
- self_bootstrap_findings: ①issue 报 20 处 source，实测 55 处，且另有 39 处非状态 source 绝不能误改；②RED 快照初版误把实现文件也拷进基线导致全绿——基线**只能注入最终版 AT**；③`parse`/`eval` 一字之差决定安全性，因此 lint 把 `eval(`/`exec(`/`subprocess` 列为禁止原语。

## Implementation Decision Note
- decision: 协议真源 + 兼容 reader + 冻结边界；逐组迁移拆出
- why_this: 状态文件可执行化是延迟触发的注入面，但全迁不可一轮验证
- alternatives_considered: 一轮全替 / printf %q / 拒读旧格式 / 无白名单
- boundary_non_goals: freely 现有代码、非状态 source、meta.env、既有状态文件均不动
- residual_risk: 注入面仍在、白名单需扩充、畸形旧行、to-shell 调用约定
