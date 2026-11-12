# PRD — 指引文案单源化 + raw-issue-pull 工位路径正确性

- milestone: M-20261112T031638Z-A
- raw: raw-20261112T031638Z / GitHub #4310 / Gitee IKUSRE
- issues: I-20261112T031638Z-A（文案面）、I-20261112T031638Z-B（调用路径面）

## 问题陈述

Freely 的封装命令在拦截用户时会打印「下一步怎么做」的指引。这些指引是 agent
在被门禁拒绝时唯一的自救入口。当前存在两类缺陷：

1. **指引内容错误**：引用了三个从不存在的 skill 名
   （`freely-fix-execution` / `freely-feature-execution` / `freely-feat-execution`），
   并把可选参数 `--skill` 当主参数展示、漏掉真正必填的 `--kind`。
   agent 照抄会走向不存在的 skill、执行会失败的命令。
2. **指引触发时机错误**：`wt-create` 已经 cd 进合法 dev 工位，但
   `raw-issue-pull → issue-sync` 链路用脚本物理位置判定分支，必然撞主仓
   develop guard，每建一个工位稳定产生 ERROR + WARN，且 platform title
   归一化这一步被静默跳过。

## 用户与场景

- **主要用户**：在 Freely 上工作的 AI agent（以及人类开发者）。
- **触发场景**：① 在 protected root 误调 `issue-sync`；② pre-tests 未 green 就提 PR；
  ③ `wt-close` 遇到未合并分支；④ `freely launch` 因工位/分支不合法被拒；
  ⑤ 手动创建分支被 hook 拦截；⑥ 每次 `wt-create` 新建工位。
- **频次**：⑥ 是每轮必经路径，①–⑤ 是异常路径但恰恰是最需要正确指引的时刻。

## 目标

- G1：所有面向用户的指引只引用真实存在的 skill，且 wt-create 指引含必填 `--kind`。
- G2：「零幽灵名」成为**全域**不变量，由 CI 断言守护，新增载体自动被拦。
- G3：`wt-create` 新建工位不再产生 protected-root ERROR/WARN，platform title
  归一化正常执行。
- G4：不削弱任何门禁——protected guard 在真正该拦截时仍必须拦截。

## 非目标

- 不清理死代码（`.bak.py`）。
- 不改测试 fixture 里的任意字符串字段值。
- 不改 `--skill` 的解析逻辑与 `commands.md` 对它的正确记录。
- 不重构 `issue-sync` 的 ROOT_DIR 推导机制。

## 验收（对应 pre-tests）

| 目标 | 验收项 |
|---|---|
| G1 | AT-001 静态：全部活代码/模板/文档指引含真实 skill 名与 `--kind` |
| G2 | AT-001 全域扫描白名单外零命中；进 `CORE`/`CI_CORE`；epics story 注册 |
| G3 | AT-002 行为：真实新建一次 fix 工位，输出无 ERROR/WARN |
| G4 | AT-002 反向：主仓 develop 上直接调 `issue-sync create` 仍 exit 1 |

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 全域扫描误伤合法出现（AT 黑名单常量、fixture、死备份） | 显式白名单 + 逐条理由，RED 阶段先验证白名单不误放真缺陷 |
| 触及 `runtime/freely` 触发 Step 2.5 拒绝 | 同轮新增 `tests/unit/t-guidance-01.sh` 函数级单测 |
| 改文案破坏既有测试的正向断言 | 已识别 `test-wt-close-protected-branch-guard` Test 6 固化了幽灵名，同轮改为反向断言 |
| `--project` 传参破坏 raw-issue-pull 的 JSON 契约 | 只加参数不改输出；AT-002 断言 STDOUT 仍单 JSON |