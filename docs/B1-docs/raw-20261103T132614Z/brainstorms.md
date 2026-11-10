---
raw_id: raw-20261103T132614Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审：重做真源普查（#4154 正文行号来自 2026-11-03，已漂移）

工位基于 develop `56d4cd2c9`。逐文件核对后，五个面里只有两个面仍与正文一致且有可执行验收；
其余面已被后续改动部分修复或被队列里的其他 open issue 覆盖。

### 面 1：tool-registry.toml 路径多副本 —— 成立，但只剩 2 处

- 正确常量：`runtime/freely:67` 与 `runtime/tool-launchers.sh:56` 都指向
  `docs/system/workspace/tools/tool-registry.toml`（文件真实存在）。
- 错误副本仍有两处：`bin/deploy-skills:72` 与 `runtime/freely::_init_acp_tool_setup` 内的
  `scripts/runtime/tool-registry.toml`。
- **正文说 `bin/ensure-acp-binary:8` 也是错误副本，该文件已不存在**（实现迁到
  `runtime/ensure-acp-binary`），这条已过时。
- 静默降级确凿：`deploy-skills` 在注册表缺失时走到 `[[ -z "$tools" ]] && tools="claude"`；
  `_init_acp_tool_setup` 是 `[[ -f "$registry" ]] || { log_warn ...; return 0; }`。
  两者都不报错，用户只看到「没有工具」或「跳过」。

### 面 2：raw key 多套正则 —— 成立

- `runtime/raw_key_canon.py` 已是 agent_working 的单一所有者，但只认 `YYYYMMDDTHHMMSSZ`
  与 `raw-` 前缀形式。
- `worktree/wt-create:279-284` 仍接受 legacy `YYYYMMDD-HHMM[SS]`，且**只告警不规范化**，
  随后 `raw_key` 原样拼进分支名 `raw-20261103-1326`；下游 `freely` 五处、`hooks/pre-commit.sh`、
  `owner_lane.py` 的 `T...Z` 正则全部提取不到 → `raw_key=""`。
- `bin/worktree-common.sh` 是第三套正则（历史遗留），本轮不合并，只在 issue 的证伪范围内
  由 wt-create 入口统一规范化后调用方自然收敛。

### 面 3/4/5/6：不在本轮

| 面 | 承接的 open issue |
|---|---|
| 桥接契约 TS↔Rust、事件枚举不对称 | #4179 投影一致性检查 / #4165 TDD 证据链 |
| 平台写直连 `gh` / labels 缺失 | #4166 收敛双平台同步入口与副作用 |
| 错误模型 4 套（`Result` / `CommandAck.ok` / 字符串 / `SystemExit`） | #4161 Bash↔Python 跨进程数据契约 |
| `$SELF_ROOT/docs` vs `$project/docs` 两代脚本 | #4179 投影一致性 |

这些面在队列里已有明确的 open raw，**不拆新 raw**（用户已明确不要无限拆分），本轮只把
「单一来源」这一主题做透。

## 方案方向

### 方向 A：抽 `runtime/paths.sh` 作为路径单一所有者 + 缺失 fail-closed（选中）
- `paths.sh` 提供 `freely_tool_registry_path` / `freely_tool_registry_query_path`；
- `runtime/freely` 按既有 `_freely_lib_missing` 范式 source 它，`TOOL_REGISTRY` 由函数产出；
- `bin/deploy-skills` source 同一个库，注册表缺失 → `exit 1`，删除 claude fallback；
- `_init_acp_tool_setup` 改用 `$TOOL_REGISTRY`，缺失 → `log_error` + `return 1`。
- 好处：只有一个字符串决定路径；任何调用方都不会再「自己拼一份」。

### 方向 B：只在两个错误点写回正确字面量（否决）
能过 RED，但仍是两份字面量，下一处新增调用点会再漂移一次 —— 正是本条要消除的成本。

### 方向 C：raw key 在 wt-create 内联第二套正则（否决）
issue 明确要求复用 `runtime/raw_key_canon.py`；内联等于把「多套正则」从 3 套变成 4 套。

### 方向 D：直接拒绝 legacy 格式（否决）
会破坏历史工位/分支与已有脚本；legacy 输入是可规范化的，拒绝只会把成本转给用户。

### 方向 E：拆新 raw 承接面 3–6（否决）
队列里已有 #4179 / #4166 / #4161；再拆会重复排期，也与用户「不要无限拆」冲突。

## 被否决
改 `bin/worktree-common.sh` 的第三套正则（超出入口规范化的必要范围）、改 `platform-adapter.py`
（#4166）、改 Rust/TS 契约（#4179）、放宽 `test-all`、动 `raw_key_canon` 的 opaque key 语义。

## fidelity 基线

- RED 必须证明：注册表缺失时 `deploy-skills --dry-run` 仍 rc=0（fallback 生效）；
  注册表存在时旧代码也能「跑」（所以 present 断言必须是「真的读到注册表里的 cline」，
  而不是 rc=0）；`wt-create` 不含 canon 调用；canon 不可作为 CLI 调用且不认 legacy。
- GREEN 必须证明：静态 6 项接线（含「生产代码无错误路径」的负向扫描）；注册表 present
  时读到 cline、missing 时 fail-closed、显式 `--tools` 仍工作；legacy 4 种输入全部规范化。
- RED 的 1 项 PASS 是守卫：显式 `--tools claude` 在改前改后都应成功。

## 价值判定

- 不过时：面 1 的两处错误路径、面 2 的 legacy 只告警，均在 develop `56d4cd2c9` 上实测。
- 不重叠：#4179/#4166/#4161 覆盖其余面，但都不覆盖「路径常量所有权」与「raw key 入口规范化」。
- 价值：这两类漂移不会编译失败、不会测试失败，只会表现成「工具莫名不部署」「工位建了但
  daemon 拒启动」——属于最贵的静默债。
