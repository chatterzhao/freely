# PRD: raw 身份不漂移 + 平台标题达标单一真源

- issue_id: I-20261105T051136Z-A
- source_raw: raw-20261105T051136Z

## Goal

让 `wt-create` 物化 raw issue 时，**调用方传入的 raw key 成为本地身份的唯一真源**：无论平台标题是否声明 canonical 身份，落盘目录、frontmatter `local_id`、返回值都不漂移；同时把平台标题真正修正为 `[RAW-<key>] <type>: ...` 并同步到双平台。`created_at` 反推兼容分支保留，只改变它的用途与动作。

## 非目标

- 不删除或绕过 `created_at` 反推分支、`_resolve_raw_identity()` 单条兜底、`cmd_feedback` create 校验、`_platform_title()` 自动达标能力。
- 不回写任何历史 issue 标题；`feedback edit` 的补全只在用户显式传 `--title` 时生效。
- 不修 Q3（物化缺一级标题）；本 PR 只在 B1 issue.md 现场补回 H1 以对齐平台 title。
- 不修平台读通道静默空、raw replica reconciliation、scan 状态机等独立缺陷。
- 不新增子命令、不改 `bin/*` 的 shim 分层、不改打包白名单结构（`scripts/` 整目录已在 allowlist）。

## 现状与约束

- 真源分层：`docs/system/workspace/scripts/` 是系统真源；`bin/` 是混合结构，`issue-sync` / `raw-issue-pull` 是就地真身，`platform-adapter.py` 在 `scripts/sync/`。
- `platform-adapter.py` 顶层已 `sys.path.insert(0, str(_ADAPTER_DIR))`，因此同目录新增纯模块可被脚本执行与 `importlib` 隔离加载两种方式同时 import。
- `raw_metadata_contract.validate()` 要求 21 个 frontmatter 字段齐全且 `platform_ids` 的 url 非空；测试夹具必须构造完整 schema v1 副本，否则测不到真实路径。
- `cmd_feedback` create 路径已实行「用户部分 ≤ 72 / 总长 ≤ 100 字符」与 `[RAW-<stamp>] ` 前缀；`issue-sync._platform_title()` 原先不实行，导致同一份文档在两条路径下产出不同标题（含重复前缀或超长）。

## 实现方案

### 1. 单一真源 `scripts/sync/raw_title_contract.py`

纯 stdlib、无平台 I/O，三个函数：

| 函数 | 契约 |
|---|---|
| `canonical_raw_title(raw_key, title, max_len=100)` | 去掉任意已有 `[RAW-...]` 前缀（大小写不敏感）→ 保留用户标题与类型前缀 → 补 `[RAW-<key>] ` → 只截用户部分，身份前缀永不丢失 |
| `is_canonical_raw_title(title, raw_key)` | 精确判定标题是否已声明该 key 的 canonical 身份 |
| `platform_title(local_id, kind, title)` | `raw` 走 canonical 契约；`linked` 及其他 kind 保持历史 `[<local_id>] <title>` 投影 |

### 2. `pull_raw_issue()`

保留原标题判定（精确 canonical 判定 + 原有大小写子串兜底）。进入兼容分支后：

- `_created_at_to_key(created_at)` 的结果记为 `suggested`，**只写诊断日志**，不赋值给 `raw_key`，不改写 `target_dir`。
- `canonical = canonical_raw_title(raw_key, title)`；遍历 `replicas` 的**每一个平台**，标题不等于 canonical 就调 `_update_issue_title()`，失败打 WARNING。
- 后续 `fm["local_id"] = f"raw-{raw_key}"`、返回值 `local_id`、`target_dir` 全部沿用调用方 key。

### 3. 三处调用方收敛

| 文件 | 改动 |
|---|---|
| `bin/issue-sync._platform_title()` | 改为调用 `platform_title()`；linked 分支语义不变 |
| `runtime/freely.cmd_feedback` edit | 仅当 `kind == raw` 且显式传 `--title` 时，用 `canonical_raw_title()` 规范化 `edit_title` 后再送 adapter |
| `bin/raw-issue-pull` | 去掉 `2>/dev/null` 与 `|| true`；`issue-sync create` 失败或目标文件缺失时输出可诊断 `[WARN]`，不阻断 pull |

### 4. `wt-create._pull_raw_issue()`

解析 `raw-issue-pull` stdout 的 JSON，严格比对 `expected_local_id = raw-<raw_key>`，并校验 `expected_issue_file = $PWD/docs/B1-docs/<expected_local_id>/issue.md` 存在；任一不满足返回 1。既有调用点 :860-865 已有「移除 dev 工位 + 删分支」的失败清理逻辑，无需新增绕过路径。

### 5. 回归测试

新增 `scripts/tests/test-raw-key-drift`，三组：`unit`（importlib 隔离加载 adapter，monkeypatch 平台 I/O，覆盖 17 条断言）、`static`（五处真源的收敛与告警契约）、`wtcreate`（提取 `_pull_raw_issue()` 函数体，在隔离临时仓库用 fake `raw-issue-pull` 做行为验证）。

## 验收

见 `verification/pre-tests.md` 的 AT-001，以及 `verification/test-evidence/AT-001-RED.log` / `AT-001-GREEN.log`。退化审计结论见 GREEN 证据与 review verdict。
