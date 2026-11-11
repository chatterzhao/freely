# Brainstorms: 收口 Bash 与 Python 的跨进程数据契约

- source_raw: raw-20261104T075857Z
- 覆盖域：state 文件协议、错误信封、退出码、超时语义、边界声明、lint、单页文档。

## 真源普查（不照 issue 旧描述改）

| issue 旧描述 | 实测 | 结论 |
|---|---|---|
| 52 处 `source *.env` 状态文件 | **22 处**，且样本全部落在 `scripts/tests/test-freely-*` 夹具 | 生产侧已由 R23.9–R23.13 的 `state_file.py` 协议迁移；验收标准 3 按「生产代码」范围基本已成立 |
| `gitee-issue.py` 位置参数调用 | 实测 8 个 `add_parser` 子命令 + 33 个 `add_argument` | 位置参数问题已在 R26 的 adapter 收敛中修过，issue 的边界样本过时 |
| `|| echo` 吞错 | 33 处，多数是 JSON 解析回退 | 不能一刀切，需逐点复核 |
| 无 state 协议实现 | `scripts/runtime/state_file.py` 已存在（10471 字节，含 ALLOWED_KEYS 白名单） | 协议有实现，缺的是**声明** |

**真实剩余缺口**：跨边界没有机器可读声明 → 每个调用点自己发明错误处理：
`values()` 对缺失 key 返回空字符串（分不清「没有」和「空」）、类型被 `str()` 强转、
超时与普通失败共用退出码。

## 方案对比

1. **按 issue 原方案把 22 处 source 全量归零**：大多是测试夹具，改它们不减少生产风险，
   且会拖累夹具可读性 → 否决。
2. **逐个改 `|| echo`**：33 处需逐点判断「吞错 vs JSON 回退」，无法在一轮内给出可复现
   RED → 留后续。
3. **契约声明 + 边界 runner + 三条边界测试 + lint**（本轮）：把三类失败变成可执行的
   断言，零业务语义变化，给后续逐点迁移留落点 → 采用。

## Decision

1. `contracts/cross-process/contract.yaml`：state 协议 / 错误信封 / 退出码 / 超时语义 /
   4 条已登记边界 + 每段真源标注 + 已知缺口。
2. `quality/cross_process_boundary.py`：把声明变成可执行——缺字段 → 3/`missing_field`，
   类型错 → 3/`type_error`，超时 → **4**/`timeout`（必须可与 3 区分）。
3. `bin/check-cross-process-contract`：0/1/2，校验契约完整性、边界生产方文件存在、
   runner 的退出码常量与契约一致。
4. AT-001：14 静态 + 3 行为；进 `CORE`/`CI_CORE`；epics-map 注册 story。

## 与既有 gate 的一致性

契约声明 `3` = 契约违规，与 `pr_body.REFUSE_EXIT = 3`（R27 的 RED 证据门禁）同义；
`2` = 不适用/真源缺失，与 `bin/check-skill-frontmatter`、`runtime_red_gate` 的 SKIP=2
同义。AT 的 c14 把这个交叉一致性做成了断言，避免契约自成一套编号。

## 范围诚实标注

`source` 归零、33 处 `|| echo` 逐点复核、消费方逐点机检，均写进 `known_gaps`，
不在本 PR 里假装完成。
