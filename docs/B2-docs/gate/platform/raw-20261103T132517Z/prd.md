# PRD: SDD frontmatter 解析所有权收口
- issue_id: I-20261103T132517Z-A
- source_candidate: docs/B1-docs/raw-20261103T132517Z/candidates.md#C-20261103T132517Z-A
- milestone: M-20261103T132517Z-A

## 背景

同一份 issue frontmatter 有 3 套解析器、2 套写入路径，没有任何一方被指定为唯一所有者：

| 位置 | 实现 | 失败行为 |
|---|---|---|
| `lifecycle/raw_metadata_contract.py` | 严格校验 + 原子写（规范实现） | 抛 `MetadataValidationError` |
| `runtime/task-lifecycle-scan.py` | 手写切片 + `yaml.safe_load` + 行解析 fallback | `except Exception: pass` → 返回 `{}` |
| `bin/issue-sync` | 内联 `python3 -c` 的 `_fm_get`/`_fm_set` | `2>/dev/null \|\| true` |

仓库里已有 23 份被写坏的历史文档（12 份 B1 + 11 份 B2），而损坏没有任何错误输出：该 issue 从生命周期中消失，但仍被计为已完成；或表现为「状态不对齐 → Manager 每轮去修一个不存在的状态」。人只能从「AI 反复做无用功」间接察觉。

## 目标

1. 契约模块成为唯一解析与写入所有者；scan 与 issue-sync 只做薄封装。
2. 解析失败显式产出一条 `metadata_validation_error`，不再退化成空 metadata。
3. 提供幂等、默认 dry-run 的存量修复入口，并把 23 份坏文档修好。
4. **不把历史格式误判为损坏**：无 YAML 块的 linked 文档仍按 bullet 解析，186 处 bullet `phase_state` 一个不丢。

## 非目标

- 不改 raw metadata 的字段契约（21/22 字段、severity 语义不动）。
- 不改 `bin/issue-sync` 的对外命令语义与退出码约定。
- 不做 `docs/B2-docs/**` 全量格式统一（历史 bullet 格式保留为受支持格式）。
- 不改平台侧 issue 内容。

## 实现

- `raw_metadata_contract.py`：新增 `extract_bullet_fields` / `validate_issue_text` / `parse_issue_text` / `validate_issue_path`；`read_issue` 把 `yaml.YAMLError` 包装成 `MetadataValidationError`。冲突标记判定要求 `<<<<<<<` 与 `>>>>>>>` **成对**出现（单个 `=======` 是合法 Markdown setext 分隔线）。
- `task-lifecycle-scan.py`：`parse_frontmatter` 改为调 `parse_issue_text`；失败返回 `{"__metadata_validation_error__": ...}`，由 `read_issues_dir` 落到两条读取路径（B1 raw / B2 linked）已有的 `metadata_validation_error` 字段。legacy 无 YAML 文档回退 bullet 视图；YAML 有效时**不**补 bullet（精确复刻收口前语义，避免正文 bullet 泄漏进 metadata）。
- `frontmatter_contract_cli.py`（新增）：`get` / `has-key` / `set` / `check` / `repair`；`repair` 覆盖 B1 `*/issue.md` 与 B2 `**/issues/I-*.md`，修四类形态——glued 闭合 `---`、git 冲突标记、YAML 内混入 bullet 行、相邻字段粘连。
- `bin/issue-sync`：`_fm_get` / `_fm_set` / `_fm_has_key` 改为调用 CLI 的薄封装，33 处调用点不变。

## 验收

- AT-001：develop 基线快照 RED `7 ok / 14 failed` → 工位 GREEN `21 ok / 0 failed`。
- 18 项相关回归 worktree/baseline 退出码对比。
- 全量 1082 份 B1+B2 文档：25 份差异全部可解释（23 修复 + 2 新增），其余 1057 份字段级一致；`metadata_validation_error` 计数 0。
- `bin/test-all --ci` 退出 0。

## 风险

- `bin/issue-sync` 新增了对 `docs/system/workspace/scripts/lifecycle/frontmatter_contract_cli.py` 的硬依赖。真实打包（`package-allowlist.txt` 的 `docs/system/workspace/scripts/` 整目录）已覆盖；受影响的是把 `bin/issue-sync` 单独复制出来的测试夹具——本轮已为 4 个夹具补齐依赖，并在 AT-001 里用静态断言守住「薄封装 + CLI 存在」。
