---
schema_version: '1'
local_id: raw-20261106T100938Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261106T100938Z-A
platform_ids:
  github:
    issue_id: '4205'
    url: https://github.com/chatterzhao/freely/issues/4205
    synced_at: ''
  gitee:
    issue_id: IKTIOQ
    url: https://gitee.com/zhaoquan/freely/issues/IKTIOQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-06T10:09:38Z'
updated_at: '2026-11-07T06:41:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T11:20:00Z'
closeout_note: ''
---

# fix: 打包 allowlist 遗漏运行时必需的 workspace 顶层文件，安装态不自洽

workflow_kind: fix

## 优先级

P1 — 安装态产物不自洽。开发态因 PATH 固定指向项目真源而不受影响，但安装态的 `freely-package` 无法自举打包、worktree seeder 回退到 builtin 默认、多个 doctor 门禁缺运行时清单。这直接违背「保证 freely 总是最新、不会从安装位置用到旧命令」的目标，且每轮收口的重新打包都会带着这个缺口。

## 不退化边界（本 issue 的前提，逐条实证）

本 issue 只补「打包清单遗漏的运行时必需文件」并加一致性约束，**不得**顺手改动以下既有设计：

1. **不得删除或绕过 `package-allowlist.txt` 的显式白名单机制**。#4157 已记录「按 allowlist `cp -R` 会把 `__pycache__/` 与死代码一起装出去」，allowlist 的存在正是为了收口；改成「自动包含 `docs/system/workspace/` 全部 tracked 文件」会把构建期文档、测试契约文档、遗留资料一并打进安装态，属方向错误。
2. 不得改 R5（`raw-20261105T062506Z`）刚建立的 `package-seed-parity.py` 只读语义、`worktree-seed.toml` 的三条 seed 声明、以及 `bin/freely-package` 的输出路径守卫与 parity 调用顺序。
3. 不得改 `worktree_seed.py` 的 `load()` / `apply()` 行为（builtin 回退是为极简 checkout 保留的兼容能力）。
4. 不得改 #4194 关注的「打包/部署触发机制」——那是独立 issue，本 issue 只管**产物内容完整性**。
5. 不得改 #4179 关注的 hooks/skills/bin 投影副本漂移，也不得改 #4168 的遗留脚本清理范围。

## 根因

`docs/system/workspace/package-allowlist.txt` 只列出若干目录（`agents/`、`skills/`、`hooks/`、`scripts/`）与 9 个 `.md`，**没有列出 `docs/system/workspace/` 下的顶层非 `.md` 文件**。`freely-package` 逐行按 allowlist 复制，因此这些 tracked 文件全部没有进入安装态。

## 证据（2026-11-06 R5 收口打包后实测）

- 全量比对：`git ls-files docs/system/workspace` 中直接位于 `docs/system/workspace/` 顶层的 tracked 文件共 **17** 个，其中 **8 个不在 allowlist**：
  - `worktree-seed.toml`
  - `package-allowlist.txt`
  - `install-lifecycle-allowlist.txt`
  - `release-build-allowlist.txt`
  - `AGENTS.md.example`
  - `commands.md`
  - `three-loop-lifecycle.svg`
  - `command-wrapper-metadata-lifecycle.md`
- 其中 **5 个被运行时代码直接引用**（不是纯文档）：
  | 文件 | 引用点 | 安装态缺失后果 |
  |---|---|---|
  | `worktree-seed.toml` | `worktree_seed.py:load()`、`bin/freely-package`、`package-seed-parity.py` | seeder `load()` 返回 `source=builtin`，只剩 `.freely/agent-table.toml` 一条 copy；R5 刚修的 bootstrap seed 声明在安装态完全失效 |
  | `package-allowlist.txt` | `bin/freely-package:18` 的 `ALLOWLIST` | **安装态执行 freely-package 直接报 `[ERROR] allowlist not found` 并 exit 1**，产物无法自举打包；R5 的 parity checker 同样报 `allowlist not found` |
  | `AGENTS.md.example` | `runtime/freely:8608` 的 `ensure_project_agents_md` 模板、`:8629` 提示文案 | 安装态生成 AGENTS 时模板路径不存在 |
  | `install-lifecycle-allowlist.txt` | `runtime/freely:8682`、`quality/check-supply-chain-baseline:147` | 安装态 doctor / supply-chain 门禁缺清单 |
  | `release-build-allowlist.txt` | `quality/check-build-artifact-exposure:77` | 安装态 build-artifact 暴露门禁缺清单 |
- 另 3 个（`commands.md`、`three-loop-lifecycle.svg`、`command-wrapper-metadata-lifecycle.md`）只被 B1/B2 治理文档或测试契约引用，属文档/测试资料，**是否随包发布需要单独判定**，不应无条件全塞进 allowlist。
- 实测安装态（`~/.freely/versions/20261106T1004Z-nightly`）：
  - `python3 <installed>/docs/system/workspace/scripts/quality/package-seed-parity.py --project <installed>` → exit 2，`[seed-parity] ERROR: allowlist not found`。
  - `python3 -c "worktree_seed.load(installed)"` → `source = builtin entries = [{'path': '.freely/agent-table.toml', 'mode': 'copy', 'required': False}]`。
  - `FREELY_PACKAGE_ALLOW_OUTSIDE=1 <installed>/bin/freely-package --version ... --output /tmp/x` → exit 1，`[ERROR] allowlist not found`。
  - 打包产物自身仍含 `.freely/tool-boundary-bootstrap.md`（由 R5 的 seed 条目在**开发态**提供），但 seed manifest 不在包里，安装态新建工位不会带上它。
- R5 收口的 hash parity 检查发现 `docs/system/workspace/worktree-seed.toml` 在 `latest` 中 `DIFFER`（缺失），其余 4 个关键文件 MATCH；这正是本缺陷的暴露点，不是 R5 的实现错误。

## 影响

- 安装态无法自举打包（`freely-package` 第一步就缺自己的 allowlist），只能依赖开发态工作树打包，「安装位置即完整可用」不成立。
- 安装态 seeder 回退 builtin，R5 修复的 bootstrap seed、`.env` seed、`agent-table` 的 link 语义全部丢失；从安装态执行 `wt-create` 的工位与开发态不等价。
- 安装态的多个 doctor 门禁因缺清单而失效或被绕过，形成「开发态全绿、安装态静默降级」。
- 与 #4194 叠加时风险更高：安装态既可能版本滞后，又天然不完整。

## 修复方案

1. **显式补齐运行时必需条目**：在 `package-allowlist.txt` 增加 `worktree-seed.toml`、`package-allowlist.txt`、`AGENTS.md.example`、`install-lifecycle-allowlist.txt`、`release-build-allowlist.txt` 五个文件条目（保持显式白名单机制不变）。
2. **单独判定 3 个文档/测试资料**：`commands.md`、`three-loop-lifecycle.svg`、`command-wrapper-metadata-lifecycle.md` 是否随包发布，在 issue 里写明结论（倾向不随包，避免扩大安装态体积；若判定需要则同样显式加入）。
3. **加一致性约束防复发**：新增机器检查——`docs/system/workspace/` 下所有被 `bin/`、`scripts/runtime/`、`scripts/quality/`、`scripts/worktree/` 中代码以字面路径引用的 tracked 顶层文件，必须出现在 allowlist 中；作为 `freely-package` 的打包前置检查或独立回归测试。注意与 R5 的 `package-seed-parity.py`（管 gitignored 条目与 seed 声明）职责分开，不要重复实现。
4. **加打包产物完整性验收**：打包后对 allowlist 的每条路径断言产物中存在；对安装态真实执行一次 `freely-package --output <安全临时目录>` 与 `worktree_seed.load(installed)`，断言 `source=manifest` 且声明条数与真源一致。
5. 补回归测试，覆盖「安装态自举打包成功」「安装态 seeder 读到 manifest 而非 builtin」「新增被运行时引用的 tracked 顶层文件未进 allowlist 时被一致性检查拦下」。

## 明确不纳入（已评审否决，禁止夹带）

- 把 allowlist 改成自动包含整个 `docs/system/workspace/` 或全部 tracked 顶层文件（会把文档/测试资料/`__pycache__` 带进安装态，破坏收口意图，见 #4157）。
- 删除 builtin seed 回退或改 `worktree_seed.load()` 语义。
- 修改 R5 的 parity checker、seed 声明、输出守卫顺序。
- 实现 #4194 的自动打包/部署触发、#4179 的投影一致性、#4168 的遗留脚本清理 —— 都是独立 issue。
- 批量改写历史安装版本目录；本 issue 只保证此后打出的产物完整。

## 验收标准

- GREEN：新打出的安装态中 5 个运行时必需文件全部存在，且 sha256 与项目真源一致。
- GREEN：在安装态执行 `freely-package --output <安全临时目录>` 成功，`integrity: verified`，产物含 allowlist 全部路径。
- GREEN：在安装态执行 `worktree_seed.load()` 返回 `source=manifest`，条目数与真源一致（含 R5 的 3 条声明）；安装态 parity checker 返回 `1 ignored / 0 undeclared`。
- GREEN：一致性检查能拦下「新增被运行时引用的 tracked 顶层文件但未加入 allowlist」的情形，并点名路径。
- GREEN：R5 的 `test-worktree-seed-package-parity`、#4158 的 `test-freely-package-output-guard`、以及相关回归测试零新增失败。
- 禁止：不得以减少重复为由删除显式白名单机制，不得改动既有门禁判定规则。
