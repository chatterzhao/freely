---
raw_id: raw-20261104T075810Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（issue 4 条修复面）

| # | 面 | develop 实测 | 本轮 |
|---|---|---|---|
| 1 | 建 `contracts/config/schema.yaml` | 不存在；无任何契约文件 | ✅ 修 |
| 2 | `freely doctor` 校验类型/未知键/必填 + 行号 | `cmd_doctor` 只做 doc/hook/supply-chain/install-state，**零配置类型校验** | ✅ 修 |
| 3 | 修正 `.freely/config.toml` 与模板的 `allowed_paths` | `.freely/config.toml:60` 是 `str`；**模板早已是 list**（issue 描述不准） | ✅ 修本地运行时状态；模板无需改 |
| 4 | 角色配置二选一（合并或写边界） | `agents/agent-roles.toml` 与 `.freely/agent-table.toml` 双真相 | ➡ 不改（见「被否决」） |

## 数据偏差（必须如实记录）

- issue 说「`.freely/config.toml` 仅 58 个键」——实测 **58 个 flat key**（57 顶层 + `[skip_ibm_gate].allowed_paths`），数字一致但构成不同：其中 6 个（`AGENT_AI_TOOL_*`/`AI_MODEL`/`AI_REASONING_EFFORT`）是 runtime 追加、模板里没有。
- issue 说 `governance-merge-gate:392-397` 有 `isinstance(raw, list)` 分支——实测在 **:408-433**，且 `except Exception: pass` 确实吞掉解析失败。行号已漂移。
- issue 说「一次性修正模板的 `allowed_paths` 写法」——模板 `templates/config.toml.example` **本来就是 8 项 list**，验收标准 3 的前半在基线已成立，不能假装改过。
- `.freely/config.toml` 是 **gitignored 本地运行时状态**，不在版本控制内。因此「一次性修正」只能作为本地现场修正交付，代码侧真正的可移植修复是 schema + 校验器 + 打包白名单。

## scope 收敛

本轮只做 1 + 2 + 3（本地状态），理由：

- 1/2 是同一个「配置错误不可观测」根因的两面，合起来才能让外部项目验证配置是否被正确理解。
- 3 是根因的直接证据与现场清理，不改任何 tracked 代码。
- 4 要合并两份角色真相，属于「agent 路由 schema」独立议题（#4172 / R39），且会改动 runtime 加载路径；混进本 PR 无法独立验证「行为不变」。

## 方案方向

### 面 1+2：契约 + 单一校验器

- schema 用 **YAML 1.2 的 JSON 兼容子集**（`json.loads` 与 `yaml.safe_load` 双可读），理由：安装态机器未必有 PyYAML，而安装态 `freely doctor` 必须能校验；纯 stdlib 是 fail-closed 的前提。
- 新增 `quality/config_schema.py` 作唯一真源，暴露 CLI（rc 0/1/2）。doctor **只调用它一次**，不复制第二份判定。
- schema 必须随包：`package-allowlist.txt` 加 `contracts/`。否则安装态 doctor 找不到契约 → 又变成静默失效（R5.5 同族坑）。

### 关于 gate 消费端（关键边界）

`_load_skip_ibm_allowed_paths()` 对非 list 静默返回空列表，`is_governance_only_path()` 因而回退到内置默认白名单。**本轮不改它**：

- 改成 fail-closed 会让当前所有工位（本地 config 仍是字符串）的每次 PR 门禁硬失败，R8 已实证这类自锁；
- 本轮提供的是「可观测」而非「改变豁免判定语义」：doctor 明确报出 `:60` 与期望类型，schema 声明 `list[str]`，本地配置现场修正为 list。gate 的行为逐字节不变（`shasum` 守卫）。
- 「gate 静默回退默认值」作为残余风险登记，归入 #4157（失败语义与可观测性）族，不在本轮夹带。

### doctor 的退出码语义

`cmd_doctor` 现有 `check_*_or_fail` 系列会 `exit 1`。若把配置校验也做成硬失败，**当前所有历史项目的字符串配置会让每轮 commit/PR/selfhost 自锁**。因此 doctor 只打印 `config_schema: INVALID/ok` 诊断（含 `文件:行号`），不改变 doctor 自身退出契约；机器可判定的 fail-closed 出口是 `config_schema.py` 的 rc 1/2，供门禁/CI 直接调用。这是「诊断命令」与「门禁命令」的职责分离，不是 fail-open。

## fidelity 基线

- schema 必须覆盖实测 58 键（不是凭空 58），每键有 type/default/scope/required/consumers，consumers 来自真实 grep 而非编造。
- RED 必须用 develop 基线快照注入最终版 AT-001，且对照组（模板已是 list、gate 静默分支存在）必须 PASS——证明断言没测错东西。
- 行为断言要真的构造「字符串 allowed_paths / 未知键 / 缺必填 / bool↔int 混淆」四类坏配置，并逐条核对 `file:line`。

## 价值判定

- 不过时：`:60` 的字符串配置、doctor 零校验、gate 的 `isinstance(raw, list)` 静默分支实测都在。
- 不重叠：#4157 是 watchdog/失败语义族，#4172 是 agent 路由 schema，均不覆盖「config.toml 无契约 + doctor 不校验类型」；#4194 是安装态版本一致性，属 doctor 的另一个检查项。
- 高价值：配置写错不报错、行为悄悄降级，外部项目无法自查；这是所有后续配置项的地基。

## 被否决

- **引入 PyYAML 依赖写「漂亮」的 YAML**：安装态机器不保证有，缺依赖时校验会静默跳过，正是要修的病。
- **把 schema 放进 `docs/system/workspace/`**：那是产品能力目录，但 `contracts/` 是 issue 指定的路径且更贴合「被检查项目也要能引用」；放错位置会让 `package-runtime-file-parity.py` 的顶层文件扫描语义混淆。
- **改成 gate fail-closed**：会自锁每轮 PR（R8 实证），且改变了豁免判定语义，超出验收标准。
- **顺带合并两份角色配置**：需要 runtime 加载路径迁移，属 #4172，不夹带。
- **让 doctor 因配置错误 exit 1**：历史本地配置会让每轮门禁自锁；改为独立 CLI 承担 fail-closed 判定。

## Related findings

- `templates/config.toml.example` 有 52 键、`.freely/config.toml` 有 58 flat key，模板是 config 的真子集（差 6 个 runtime 追加键）。schema 以 58 为准，并允许模板缺这 6 个（required=false）。
- `bin/test-pre-merge-selfhost` 的 Step 3 用 `grep -qi "fail|error"` 检查 doctor 输出；本轮 doctor 新增诊断文案不含这两个词，且本地配置已修正为 ok，selfhost 不受影响。
