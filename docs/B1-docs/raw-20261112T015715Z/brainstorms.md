---
b1_id: B1-20261112T015715Z
phase_state: completed
source_raw: raw-20261112T015715Z
source_url: https://github.com/chatterzhao/freely/issues/4307
produced_candidate: C-20261112T015715Z-A
created_at: 2026-11-12
---

# B1_IBM: 让 registry 契约测试不再绑定机器安装状态

## Discovery

### Input

- raw #4307 / Gitee IKUR3Z，P2，`workflow_kind: fix`。
- 来源：R33（#4179）收口重刷 `test-gate run` 时暴露 `20 ok / 1 failed`，唯一红项是
  `[FAIL] registry present: registry tools are read (cline detected)`。

### 覆盖域

`docs/system/workspace/scripts/tests/test-contract-single-source.py` 的 `registry_checks()`、
`bin/deploy-skills` 的工具探测段、`bin/test-all` 的 `CI_CORE`、
`freely test-gate run` 证据链（`TEST_STATUS` / `TEST_EXIT_CODE`）、
`pretests-retirement-gate` 与 `wt-close` 的收口判据。

### Scope 与价值

一个独立问题（测试的环境前提），拆多 candidate 无收益 → 一个 `C-...-A`。
仍高度相关且属**跨 issue 阻塞级**：不修则后续每一轮收口都要人工 shim，
`test-gate` 证据也失去机器无关性。无过时/被覆盖情况（#4307 是本轮新建）。

## Research

### 真源普查（不照 raw 描述照抄）

| 检查项 | 实测（develop `e003532b5`） | 结论 |
|---|---|---|
| 是否本轮引入 | develop 基线 `27e91e50c` 直接跑同一测试也是 `12 ok / 1 failed` | 否，预存缺陷 |
| R33 是否触达 | `git diff develop..HEAD -- bin/deploy-skills` 的新增只在 `dry_run == 0` 分支；测试走 `--dry-run` | 不触达 |
| CI_CORE 是否 R33 新加 | `bin/test-all` 的 R33 diff 只加 `test-projection-consistency.py`；`test-contract-single-source.py` 本就在 `CI_CORE` | 一直在 |
| 机器状态 | `command -v cline` 在交互/登录 shell 均无；`~/.freely/tool-registry.toml` 不存在；`query --list` 正常返回 claude/cline/codex/opencode | 纯机器状态 |
| 补齐前提后 | 临时可执行 `cline` stub 前置 PATH：**基线与 R33 分支都** `13 ok / 0 failed`，其余 12 条断言不变 | 失败仅来自未声明的环境前提 |

根因链：`bin/deploy-skills:77-98` 按 registry 逐项取 `test_command` 首词并用
`command -v` 判定 installed → 本机无 cline → `--dry-run` 只输出 claude →
测试 `143-149` 把「输出含 cline」当作 registry 被读取的证据 → 断言绑定了机器状态。
产品侧「只部署已安装工具」是正确语义，**错的是测试的隐含前提**，不是产品代码。

### Option A: 测试自建 tempfile stub 并注入 subprocess PATH（推荐）

在 `registry_checks()` 内用 `tempfile.TemporaryDirectory()` 创建只含可执行 `cline`
stub 的目录，构造 `env = dict(os.environ, PATH=stub + os.pathsep + os.environ["PATH"])`
传给三个 `subprocess.run`。`deploy-skills` 于是真的从 registry 读到 cline，
断言验证的是「registry 被读取」这一契约，而非「这台机器装了 cline」。
stub 生命周期限于测试进程，不写仓库、不污染全局 PATH。

优点：改动面最小（单测试文件），保留 registry missing fail-closed 与
explicit --tools 两条行为断言，CI 立刻机器无关。
代价：stub 文件名须与 registry 的 `test_command` 首词一致，将来改 registry 要同步 ——
用 AT 静态断言守住。

### Option B: 改断言为直接验证 registry 解析结果

把「输出含 cline」换成「`--dry-run` 解析出的工具集合 == 由 query 算出的 installed 集合」。
语义最准，但要重做 `deploy-skills` 的可观测性（当前只输出部署行），
改动面从测试扩散到产品脚本，超出本 fix 的 scope。列为后续可选，不在本轮做。

### Option C: CI 环境预装 cline / 全局 shim

否决：把机器状态前提固化进部署流程，换台机器仍红；且要求所有贡献者装 cline，
违反「CI 子集机器无关」的初衷。R33 收口用的临时 shim 只是应急，不能制度化。

### Option D: 把该项移出 CI_CORE 或标 known-broken

否决：削弱验收面、把真实契约漂移藏进 591 条 known-broken；而 known-broken 记录的是
「尚未 onboard」不是「已知红」，语义不符。CONSTITUTION §5 不允许用放宽门禁代替修问题。

## Decision: Option A

1. 只改 `test-contract-single-source.py`：自建 stub + 注入 `env`，**不碰产品代码**。
2. 新增 AT-001 覆盖：静态（stub 自建 / 注入 env / 无硬编码机器路径）、
   行为（干净 PATH 下该测试 `13 ok / 0 failed`、`test-all --ci` `21 ok / 0 failed`、
   `test-gate run` 不带外部 shim 也 rc=0）、不退化（registry missing 仍判红、
   既有 20 项 CI 全绿、其它 AT 不受影响）。
3. 验收必须写明「**不带任何外部 shim**」——否则等于把 R33 的人工绕法制度化。

## 边界与依赖

- 不改 `bin/deploy-skills`、`bin/test-all`、`test-gate`、任何门禁。
- 不改 `CI_CORE` 成员、不上调行数预算、不动 `projection.lock`。
- 依赖：无（R33 已合并，本轮基于 develop `e003532b5`）。
