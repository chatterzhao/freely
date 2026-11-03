# Tasks: I-20261102T130721Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | 清单加载与内置回落 | `worktree_seed.py::load` | — | AT-001 / AT-002 |
| T2 [x] | 复制/链接/跳过/缺失/越界 五类语义 | `worktree_seed.py::apply` | T1 | AT-003 ~ AT-006 |
| T3 [x] | CLI（apply / list） | 同上 | T2 | 手工 list/apply |
| T4 [x] | 本仓库清单（agent-table 用 link） | `worktree-seed.toml` | T1 | list 显示 manifest |
| T5 [x] | wt-create 单一调用点 + 回滚 | `wt-create::_seed_worktree` | T2 | AT-007 |
| T6 [x] | 删除上一轮硬编码 agent-table 复制 | `wt-create` | T5 | 代码审查 |
| T7 [x] | 证据与门禁 | `verification/test-evidence/*` | T1–T6 | 两份测试日志 |

## 备注

- 实现中发现：`wt-create` 运行在工位内，若以自身为源执行 seed 必然报 `required seed missing`，因此 `_seed_worktree` 从 `.freely/config.toml` 读 `FREELY_HOME` 作为源根。
- 未做：清单 glob、大小上限、`wt-seed check` 巡检（C-20261102T130721Z-B）。
