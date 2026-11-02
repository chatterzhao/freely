- issue_id: I-20261102T130721Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/issues/I-20261102T130721Z-A.md

## Implementation Decision Note

- decision: 清单随仓库（`docs/system/workspace/worktree-seed.toml`）+ 独立执行器（`worktree_seed.py`）+ `wt-create` 单一调用点；删除上一轮的硬编码 `cp`。
- why_this: `git worktree add` 只检出被跟踪文件，而 `.freely/` 整体被忽略。上一轮为 `agent-table.toml` 加的那行 `cp` 是补丁式做法：每缺一个文件就要改脚本、走一遍 PR，且换项目不可用。清单化之后，项目自己维护“哪些未跟踪文件必须带进工位”，脚本只负责执行。
- alternatives_considered:
  - 写进 `.freely/config.toml`：不随仓库走，换机器要重配；且 config.toml 是生成物，手改容易与 init 冲突。
  - 保持硬编码：需求会线性增长，且清单散落在 shell 里无法维护。
- boundary_non_goals: 不做双向同步；不做模板渲染；不把 `freely.db` 放进清单（它是运行态，不是配置）；不支持 glob（显式路径更可审计）。
- residual_risk:
  - `link` 模式下工位内的写入会写回主树（本仓库对 `agent-table.toml` 正是想要这个效果，但这是显式选择，默认仍是 `copy`）。
  - 清单会漂移：源被删或工位被手工清理后，只能等到下次建工位或运行时报错。已立 C-B（`wt-seed check` 巡检）但未实现。
  - 大目录若被写进清单会拖慢建工位；当前没有大小上限与告警。
  - `_seed_worktree` 在 `worktree_seed.py` 不存在时静默跳过（为了兼容旧工位），这意味着“脚本被误删”不会被发现。

### 实现要点

1. `load()` 返回 `(entries, source)`，`source ∈ {manifest, builtin}`；清单为空视同不存在，回落内置默认。
2. `apply()` 先校验路径（绝对路径、`..` 越界直接抛），再判断目标是否存在（跳过不覆盖），最后按 `copy` / `link` 执行；目录走 `copytree`。
3. Python 无 `tomllib`（<3.11）时用受限解析器兜底，只支持 `[[seed]]` 表面；`tomllib` 报错则抛 `SeedError` 而不是静默用兜底。
4. `wt-create` 的 `_seed_worktree` **以 FREELY_HOME 为源**：工位里本来就没有这些文件，用自身为源必然 `required seed missing`（这是实现过程中真实踩到的第一步）。
5. 失败时与既有 pull 失败同路径回滚：删除两个 worktree 与两个分支。

### 与既有 `.freely` clone 的关系

保留 clone（`freely.db` / `a2a_task.db` 是运行态，语义不同），seed 只负责清单内路径。两者顺序：先 seed（建立 `.freely/` 与链接），再 clone（写数据库）——互不覆盖。
