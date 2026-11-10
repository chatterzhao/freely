---
raw_id: raw-20261110T084522Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（develop `6b927cae1` 实测）

R23.12 的前置普查发现 `state_file.py::ALLOWED_KEYS` 注释声称「全量扫描」但漏登记 heredoc 写入键，遂立项本条。本轮**重新做一次更严格的真源普查**，结论比立项时更严重：

| 维度 | 立项时 | 本轮实测 |
|---|---|---|
| 写入形态 | heredoc + printf（2 种） | **5 种**：heredoc、here-string `<<<`、`printf` 模板、`echo "KEY=..." >`、`--kv` argv |
| 未登记键 | 21 | **65**（77 → 142） |
| 大写键 | 21 | 59 + 6 个小写锁状态键 |
| 扫描器自身 | 无 | 首版漏 15 个 manager/preemption 键、误抓 7 个局部变量 |

逐类写入点：

- heredoc 15 处，其中 `cat >"$(manager_worker_launch_state_file "$project")" <<EOF` 这类**目标含空格与命令替换**的写法，早期正则 `[^"\s]*` 完全匹配不到 → 漏 15 键（正是立项时 21 个里的主体）。
- here-string 2 处（`LOOP_GUARD_L1/L2`），**首行键与 `<<<` 同一物理行**，只扫后续行会漏 `prev_exit_kind` / `LOOP_GUARD_L2_START_BYTES`。
- `printf 'TEST_STATUS="%s"\n'` 等 4 处模板（test-gate 状态）。
- `echo "LOOP_GUARD_L3_ACCUMULATED=..." >`、`echo 'FORCE_FRESH=true' >`、`echo "WORKER_PROMPTS_CSV=..." >>` 3 处。
- `--kv` 6 处（R23.11/R23.12 已迁族），若不纳入会产生 6 个假 stale。
- 文档式 heredoc：`$meta_file`（intake resolution）、`$contract_file`（worker verification contract）、`$identity_file`（supervisor identity）、`$pending_file` 等，虽不是 `.env` 但同样是 `KEY=value` 且被 `source` 读 —— 协议若要成为单一所有者，这些键也必须能读。

## 根因不是「少写了几个键」

`read_state` 对**每一行**（含 legacy `KEY=value`）都调 `_check_key`，因此一个未登记键会让整份存量状态文件抛 `StateFileError`；shell 侧的 `|| true` 把错误吞掉，值静默回落默认值 —— **比报错更危险**：状态在迁移那一刻悄悄丢失。

所以修复必须是「让扫描器本身成为契约」，而不是人工再补一次清单。

## 方案方向

### 方向 A：只补 21 键（issue 原文）
- 缺点：漏掉其余 44 个写入形态；下一次迁移仍会撞上；注释继续宣称「全量」但仍是假的。

### 方向 B：放宽 `read_state`，legacy 行不校验键（否决）
- 优点：立刻不抛错。
- 缺点：未知键拒绝是「防止拼错静默产生新状态」的护栏，放宽等于削弱；且写侧仍严格，读写语义不一致。**issue 明确要求不放宽**。

### 方向 C：自动扫描 lint + 按实测补齐（选中）
1. 新增 `bin/check-state-file-keys`：从 `runtime/freely` 抽取 5 种写入形态的 KEY= 键集合，与 `ALLOWED_KEYS` 求差集；missing 非空即失败，stale 只告警。
2. 把 65 个键补进白名单（77 → 142），注释改为「由 lint 校验」，删掉「full scan」的错误声明。
3. AT-001 用**独立夹具**验证扫描器自身覆盖 5 种形态 + 命令替换目标 + 不误抓局部变量 —— 否则「lint 通过」只是自证。
4. 保留未知键拒绝语义（反向断言）。

## 返工记录（本轮踩了两次「扫描器漏判」）

1. **首版 lint 漏 15 键**：heredoc 目标用了 `[^"\s]*`，匹配不到 `cat >"$(fn "$project")" <<EOF`。改为 `.*<<(?!<)` 后差集从 50 变 65，两个先前被误报 stale 的 here-string 首行键也归位。
2. **正则过宽引入噪声**：`.*<<` 会把 `<<<` 当 heredoc，把 here-string 载荷里的 `accumulated=`、`now_epoch=` 等**局部变量**误当状态键（多出 7 个）。修法：here-string 分支必须**先于** heredoc 判定，且 heredoc 用 `(?!<)` 排除第三个 `<`；AT 加了「无局部变量泄漏」断言。
3. 这两条恰好证明：**扫描器自己也需要被测试**。若只写「补键」不写「扫描器夹具」，下次新增写入形态仍会静默漏登记。

## 被否决

- 只补 21 键、放宽 legacy 校验、删掉白名单改为任意键、把 lint 做成只告警不失败、用 `git grep` 手工清单代替可执行的键抽取器。

## fidelity 基线

- RED 必须包含 issue 的原始复现：含 `LAST_MANAGER_CONTINUITY_GENERATED` + `QUEUED_WORKER_PROMPTS` 的 legacy 文件 `read_state` 抛错。
- GREEN 必须证明：lint 差集与 stale 皆为 0；65 个键的 legacy 与 TAB+JSON 都逐字节往返；**伪造键仍被拒绝**（唯一 RED PASS，防止把护栏一起放宽）。
- 扫描器夹具必须覆盖 6 类：heredoc、含命令替换目标的 heredoc、here-string 首行、printf、echo、`--kv`，以及「无局部变量泄漏」反向断言。

## 价值判定

- 不过时：65 个键实测全部仍被写入，77 键白名单实测仍不完整。
- 不重叠：R23.9 建协议、R23.11/R23.12 迁调用点；本条修协议真源 + 建契约 lint，是后续大族迁移的**前置阻塞项**。
- 高价值：不修则 `manager_worker_launch`（14 读 / 11 键）、`loop_guard`、`test-gate` 等族一旦迁移就会静默丢状态。
