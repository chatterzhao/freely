# Brainstorms: runtime 26,823 行单体拆分并规划 Rust 迁移

- source_raw: raw-20261104T075849Z
- 覆盖域：cmd_* 依赖矩阵、子命令外移、行数守卫、Rust 迁移边界/成本/回滚。

## 真源普查（不照 issue 旧数字）

| issue 旧描述 | 实测（develop `d33855eb0`） | 结论 |
|---|---|---|
| 26,823 行 | **27,272 行** | 已涨 449 行，说明「无守卫」是真的 |
| 935 个函数 | **944 个** | 同上 |
| 54 个 `cmd_*` | **56 个** | |
| 4 个脚本 `source` 单体 | 仍是 4 个（`bin/freely` 等） | 拆分必须保持「可执行 + 可 source」双身份 |
| `bin/` 已用 `exec bin/<cmd>` 模式 | **12 个 `cmd_*` 已外移** | 模式成熟，可直接复制 |
| `check-file-size` 能锁行数 | 单体带 `# file-size: skip`，**完全跳过** | 必须新增专用守卫 |

## 依赖矩阵（自动生成，见 `runtime/split-plan.md`）

解析 944 个顶层函数后逐个 `cmd_*` 统计：内部依赖函数、state 键、平台调用、bin 下游：

- phase 0（已外移）15 个；phase 1（依赖 ≤3）6 个；phase 2（依赖 4–8）22 个；phase 3（>8）13 个。

第一阶段的三个目标由依赖数直接决定，不是凭感觉挑的：

| cmd | 行数 | 内部依赖 | 结论 |
|---|---|---|---|
| `cmd_test_gate_run` | 39 | `_test_gate_file`、`cmd_evidence_add`、`log_error` | 与 record/evidence 同簇，一起外移 |
| `cmd_test_gate_record` | 42 | `_test_gate_write`、`log_error` | 同上 |
| `cmd_evidence_add` | 22 | `log_error` | 最小，适合当第一个 |

## 关键发现：外移的真正前置条件是 helper 单源

这三个命令都要 `log_error`；后两个还要 `run_dir_for_project`、
`current_timestamp_utc_for_machine`。这些在单体里是内联定义，抽出后只有两条路：
复制（必然漂移）或 source 27k 行单体（循环依赖）。所以本轮先建
`runtime/lib/common.sh` 作为**唯一 owner**，单体改为 source 它 —— 这是后续
每个 phase 1/2 外移的通用前置条件。

## 方案对比

1. **一次性把 daemon/supervisor/dispatch 全搬走**：13 个 phase 3 命令互相通过全局变量
   耦合，一轮内无法给出可复现 RED → 否决。
2. **只写拆分计划，不动代码**：满足验收 1 但不满足验收 2/3（至少 3 个外移 + 行数下降）→ 不够。
3. **helper 单源 + 3 个子命令外移 + 行数守卫 + 依赖矩阵 + Rust PoC**（本轮）→ 采用。

## 附带发现（吃狗粮抓到）

给 `bin/test-all` 前置插入新 AT 后，R30 的 `test-cross-process-contract.py` 立刻红了：
它断言 `CORE=(\n  <自身>`，即「自己是数组第一行」。这是脆弱断言（顺序一变就红）。
已改为按数组成员判定，并在两个 AT 里共用 `array_has()` —— 属于本轮真实回归，
不掩盖。
