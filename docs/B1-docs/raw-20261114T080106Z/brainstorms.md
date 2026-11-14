# B1 Brainstorm — raw-20261114T080106Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `.freely/goal-arch-debt.md:22`「安装态自洽：`install-state-check --json` → `ok:true`……**吃狗粮前提已满足**」；`docs/system/workspace/commands.md`「`freely doctor`」；`quality/install-state-check.py` 模块文档「`freely doctor` entry point: prove the installed state equals this source tree. **Thin wrapper — every rule lives in install_state.py**」。
  - 既有验收测试: `tests/test-install-state.py:94-95`「`cli = q / "install-state-check.py"` / `install-state-check CLI exists`」、`:112`「`cmd_doctor reports install state`」；`test-runtime-split.py` 的 budget 断言「budget is below baseline and not above actual」。
  - 门禁源码注释/理由: `runtime/freely:27151`「`*) log_error "unknown command: $cmd"; usage; exit 1`」；`cmd_doctor()` 在 `:24817` 调用 `_isc`；`check-bin-projection:59`「`threshold = int(doc.get("threshold_lines") or 40)`」；`check-runtime-size` 输出「`ok (27158 lines, budget 27158)`」。
  - 既有同类实现: `bin/freely`（投影：`exec bash "$ROOT_DIR/docs/system/workspace/scripts/runtime/freely" "$@"`）；`bin/freely-package`（打包真源）；`quality/install_state.py::main()` 支持 `--json`。
  - 配置约束: 无；但 `runtime/freely` 有 **27158 行硬预算**（当前 27158/27158）。
- 判定（五分类）: **实现未完成** + **文档偏差**。自检能力（脚本 + doctor 消费）已存在，但缺一个 goal 可照抄的一等入口（实现未完成）；goal 写的 `install-state-check --json` 与实际可执行入口不一致（文档偏差）。**不是**设计错误、**不是**实现偏差、**不是** bug——`install-state-check.py` 与 `cmd_doctor()` 都按设计工作。
- 与既有断言的冲突: 无。`check-bin-projection` 只约束 >40 行的 bin 文件；`check-runtime-size` 只约束 `runtime/freely` 行数；新增 ≤8 行薄投影不触碰两者的拒绝条件。
- 影响面: 新增 `bin/install-state-check`；`goal-arch-debt.md` 与 `commands.md` 的命令写法；新增一条 AT。**不改** `runtime/freely`、不改 `cmd_doctor()`、不改 `freely-package`、不改 `install_state.py`。

### 0.1 全局适配反思（四问）

1. **类别**：流程能力（安装态自检入口）+ 文档一致性修复，不是副本传播、不是治理元数据、不是实现 bug。
2. **职责边界**：判定真源唯一 = `quality/install_state.py`；`install-state-check.py` 是薄 wrapper；`cmd_doctor()` 是消费方；`freely-package` 是生产方。新入口**只转发**，绝不拥有第二套判定逻辑。
3. **结构性冲突**：若为了让 `./bin/freely install-state-check` 能跑而往 `runtime/freely` dispatch 表加一行 → 27159 > budget 27158，`check-runtime-size` 判红；若为绕开预算而复制一套自检 → 第二真相源。两条都明确排除。
4. **门禁失配**：`check-runtime-size` 测行数、`check-bin-projection` 测 >40 行登记；本轮是新增独立小文件，不在两者测量面内，无失配。**不改任何门禁**，也不为凑预算去压缩无关代码。

## 1. 现象（吃狗粮实测）

```
$ ./bin/freely install-state-check --json
[ERROR] unknown command: install-state-check
```

但 goal:22 把这句写成「吃狗粮前提」。真实入口是 `python3 docs/system/workspace/scripts/quality/install-state-check.py --json`（`cmd_doctor()` 内部调用），`runtime/freely` dispatch 没有该分派。执行者按 goal 抄会拿到 `unknown command`，无法确认「是否吃到过期安装态」——正是用户担心的风险面。

实测当前安装态：`ok:true`，`project_head = packaged_from = 7cf9dabf6`，`active_version = 20261114T0824Z-nightly`；`./bin/freely-package --version auto --activate` → `already matches HEAD`。**当前没有过期**，缺的是「按 goal 抄就能跑」的自检入口。

## 2. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 新增 `bin/install-state-check` 薄投影（exec 真源脚本，≤8 行）+ 修 goal/commands.md 命令写法 + AT | 不碰预算、不复制真源、文档与实现一致 ✅ |
| B | 在 `runtime/freely` dispatch 加 `install-state-check)` 一行 | 27159 > 27158，`check-runtime-size` 判红 ❌ |
| C | 只修文档，不加入口 | 能力面仍缺一等命令，goal 只能照抄 python 长路径 ❌ |
| D | 新写一份自检逻辑 | 第二真相源，与 `install_state.py` 漂移 ❌ |
| E | 给 `bin/freely` 加通用 fallback（未知命令转发 `bin/$1`） | 改变未知命令语义，属过度设计 ❌ |

采用 A。

## 3. 证伪

- 「`freely doctor` 已经自检了，不用新入口」→ 否：doctor 输出的是人读摘要，goal 要的是 `--json` 机器可读结论；且 doctor 是内部调用，文档没写清。
- 「加一行 dispatch 再删一行注释就能过预算」→ 否：为凑预算去动无关代码，属绕过约束的变体；且引入不必要 diff。
- 「这是 `IKTSRS / raw-20261108T134701Z` 的范围」→ 否：那条讲 `freely install` 与 `@freely-dev-path` 的安装/卸载承诺，本条讲**自检入口与文档一致性**，不重复（已在 raw 正文证伪）。

## 4. 边界

- 不改 `runtime/freely`（行数）、不改 `cmd_doctor()` 行为、不改 `freely-package` 幂等/激活语义；
- 不复制自检判定逻辑；不新增第二份安装态真相源；
- 不放宽 `check-runtime-size` / `check-bin-projection`；不加硬门禁；
- 不自动修复不一致：自检只报告并给出 `freely-package --version auto --activate`。
