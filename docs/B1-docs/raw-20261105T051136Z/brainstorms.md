---
b1_id: B1-20261105T051136Z
phase_state: completed
source_raw: raw-20261105T051136Z
source_url: https://github.com/chatterzhao/freely/issues/4188
produced_candidate: C-20261105T051136Z-A
created_at: 2026-11-05
---

# B1_IBM: raw 身份漂移与失效的标题自动达标

## Input

- GitHub #4188 / Gitee IKT3HL，执行队列 Q2，P0。用户在上轮明确约束：**「以前的实现是有这些的。我的意思是，你不要修改了退化。或者优化方向错误。」**
- raw issue 自身已列出「既有能力与不退化边界」四项：`cmd_feedback` create 校验与 `[RAW-stamp]` 前缀、`bin/issue-sync._platform_title()` 自动达标、`platform-adapter._resolve_raw_identity()` 单条兜底、`pull_raw_issue()` 的 `created_at` 反推兼容分支。
- 覆盖域：`platform-adapter.py` 的 `pull_raw_issue()` / `_created_at_to_key()` / `_update_issue_title()` / `_resolve_raw_identity()`；`wt-create._pull_raw_issue()`；`bin/raw-issue-pull`；`bin/issue-sync._platform_title()`；`runtime/freely.cmd_feedback` 的 edit 路径。
- 事实边界：本 issue **不是**「禁止按 created_at 反推」。反推是兼容能力；缺陷是它的**动作**——既改错本地身份，又做了一次 no-op 的平台标题修正。

## Problem

`pull_raw_issue()` 在标题不含 canonical 身份时，把 `created_at` 推导的 `sk` 同时用于三件事：改平台标题、改本地 `raw_key`、改 `target_dir`。

- 改平台标题用的是 `title.replace(f"raw-{raw_key}", f"raw-{sk}")`：标题里通常没有 `raw-<key>` 子串，替换不改变任何字符；即便有，产出的也不是 `[RAW-<key>]` 达标格式。这是一次 **no-op 修正**。
- 改 `raw_key` / `target_dir` 把本地目录名、frontmatter `local_id`、返回值统一改成平台创建时间对应的 key，与分支名中的调用方 key 脱节。实测 #4186 从 `20261104T083043Z` 漂到 `20261104T083059Z`（相差 16 秒）。
- `wt-create._pull_raw_issue()` 只 `grep -q '"local_id"'`，任何含该字段的 JSON 都算成功，于是打印「materialized raw-<原始 key>」的假成功；`bin/raw-issue-pull` 末尾又用 `|| true` 吞掉 `issue-sync create` 的失败，使 `_platform_title()` 的自动修正链路彻底静默。
- `feedback edit --title` 把 `edit_title` 原样透传给 adapter，不做达标补全，是制造不达标标题的入口（#4186 的成因）。

## Root Cause

1. **身份真源不唯一**：调用方 key、平台 `created_at`、平台标题三处都可能被当成身份，实现选择了最不可靠的一个覆盖本地身份。
2. **兼容判定与兼容动作耦合**：`created_at` 反推本身合理，但被直接当成「改写本地身份」的授权；判定应只触发「平台标题补齐」，不应触发身份迁移。
3. **达标规则分散**：`cmd_feedback` create 自己拼 `[RAW-stamp]`、`issue-sync` 自己拼 `[RAW-key]`、edit 路径完全不拼、adapter 的 replace 又不是拼前缀。四处没有共享规则，也没有去重复前缀/长度上限的统一实现。
4. **失败被静默**：`wt-create` 的 grep 假成功 + `raw-issue-pull` 的 `|| true` 双层吞错，使上层无法感知身份漂移。

## Brainstorm

### Option A: 禁止按 created_at 反推，标题不达标即报错

- 论据：改动最小，身份永远不漂移。
- 反证：**直接删除既有兼容能力**，违反用户明确约束；平台手工创建/历史无前缀 issue 会全部无法开工位。放弃。

### Option B: 保留兼容判定、只修动作，并收敛达标规则为单一真源（推荐）

- 论据：`created_at` 反推保留为诊断信号；本地 `raw_key` / `target_dir` 以调用方为唯一真源；平台侧把标题写成 `[RAW-<调用方 key>] <原用户标题>` 并同步到所有 replica；新增纯 stdlib 模块 `sync/raw_title_contract.py`，让 adapter / issue-sync / feedback edit 三处共用同一规则。
- 代价：需改 5 个真源文件 + 新增 1 个模块；`issue-sync._platform_title()` 的行为会从「原样拼接」变成「去重复前缀 + 100 字符上限」，需要全量退化审计证明是修正而非退化。
- 收益：既有的四处兼容能力一个不删，且「自动修正达标」从失效变为真正生效。

### Option C: 只在 `wt-create` 层校验并事后把漂移目录改名回来

- 论据：不动 adapter，改动集中。
- 反证：漂移已写进 frontmatter 与返回值，改目录名治标不治本；平台标题仍不达标；`feedback edit` 仍会继续制造不达标标题。放弃。

### Option D: 把达标规则做成 adapter 的 CLI 子命令，bash 侧全部 subprocess 调用

- 论据：单一真源且无新增模块。
- 反证：每次调用都要加载整个 adapter（含 handler 注册），`issue-sync sync` 遍历数百个 issue 时开销显著；且 bash 侧无法直接单元测试契约。改为轻量纯模块更合适。

## Decision: Option B

六项落地动作，逐条对应 raw issue 的修复方案 1–6：

| # | 动作 | 不退化保证 |
|---|---|---|
| 1 | 新增 `sync/raw_title_contract.py`：`canonical_raw_title()` / `is_canonical_raw_title()` / `platform_title()` | 纯函数、无平台 I/O；`linked` 及其他 kind 的投影保持原样 |
| 2 | `pull_raw_issue()` 保留 `created_at` 兼容分支，但 `sk` 只用于诊断日志；删除 `raw_key = sk` 与 `target_dir` 改写 | 兼容判定与 `_created_at_to_key()` 完整保留 |
| 3 | 平台标题改用 `canonical_raw_title()` 构造，遍历所有 replica 同步，失败打 WARNING | 替换掉 no-op 的 `title.replace(...)` |
| 4 | `bin/issue-sync._platform_title()` 改为调用 `platform_title()` | 与 `cmd_feedback` create 的 100 字符/前缀规范对齐；保留 linked 分支 |
| 5 | `feedback edit --title` 对 `kind == raw` 复用 `canonical_raw_title()` | 只在用户显式 edit 时生效，**不扫描/回写任何历史 issue** |
| 6 | `raw-issue-pull` 不再 `|| true`；`wt-create._pull_raw_issue()` 严格比对 `expected_local_id` 并校验 `expected_issue_file` 存在 | 失败由既有 `wt-create` 分支清理 dev 工位，不新增绕过路径 |

边界：`_resolve_raw_identity()` 一行不改，`cmd_feedback` create 的校验与前缀一行不改；不修 Q3（物化缺一级标题，现场补 H1 规避）；不改平台读取通道、不改 scan 状态机。

## Related findings（未新建 raw issue）

退化审计发现 `docs/B1-docs/raw-20260519T145435Z/issue.md:3-6` 残留 git 冲突标记，YAML 无法解析。该缺陷已被现有 open issue **#4148 / IKSPQ2「统一 SDD frontmatter 解析所有权」** 正文直接点名（含文件路径与行号），按「只给未覆盖缺陷新建」的约束不重复创建。相关回归测试中 2 个基线失败（`test-command-lifecycle-wt-close.py`、`test-wt-create-source-local`）同属 #4151 覆盖的「测试断言与实现消息漂移」家族。

## Candidate

见 `candidates.md` 的 `C-20261105T051136Z-A`。
