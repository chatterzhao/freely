# Brainstorms: raw-20261105T062506Z

## 问题

`docs/system/workspace/package-allowlist.txt` 把 `.freely/tool-boundary-bootstrap.md` 声明为打包必需输入，但 `docs/system/workspace/worktree-seed.toml` 只声明了 `.freely/agent-table.toml`（link）与 `.env`（copy）。`.gitignore:2` 忽略整个 `.freely/`，因此 `git worktree add` 不会把该文件带进新工位，工位里的打包或打包相关测试必然报：

```
[ERROR] missing file: .freely/tool-boundary-bootstrap.md
[ERROR] 1 allowlist path(s) not found — packaging aborted
```

本轮 R5 dev 工位本身即复现：`ls .freely/` 只有 `agent-table.toml` 与 `config.toml`，bootstrap 缺失。

## 证据与规模

- 主仓库 bootstrap 存在（2525 字节），但未被 git 跟踪（`git ls-files` 无命中；`git check-ignore -v --no-index` 命中 `.gitignore:2:.freely/`）。
- 逐行扫描 allowlist 的全部条目，**仅** `.freely/tool-boundary-bootstrap.md` 是 gitignored 路径，其余（`docs/...`、`bin/`、`.githooks/`、`templates/`）都是 tracked，无需 seed。
- 允许清单与 seed 清单各自维护、没有一致性校验；以后新增位于 gitignored 路径的白名单条目仍会静默漏配。

## 不退化边界（评审要点）

1. **seed 条目 required=false**：全新 clone 没有本地 `.freely/` 目录；若设 `required=true`，`worktree_seed.apply()` 会抛 `required seed missing`，使 `wt-create` 在干净环境里整体失败——这是新增硬失败，属退化。改为 false 后，缺源只记 `missing` 并继续；打包阶段由既有 allowlist 校验 fail-closed。
   **review 补充观察（诚实边界）**：隔离验证显示，一个完全没有 `.freely/` 的最小源项目运行 `worktree_seed.apply()` 仍会因**既有**的 `.freely/agent-table.toml required=true` 抛 `required seed missing`。因此本条 required=false 保证的是「不新增同类硬失败点」，并不等于宣称「干净 clone 一定能创建工位」；真实链路里 `_seed_worktree` 的 seed 源是主项目树 / `FREELY_HOME`，该既有约束不在本 issue 范围。评审判定：证据不足以认定它是「现有 open issue 未覆盖的新 bug」，未新建 raw issue。
2. **mode=copy 而非 link**：静态文档，且工位需要拥有自己的副本才能独立打包（link 会指向主仓库，打包产物含符号链接，语义不同）。
3. **一致性检查只读**：只比对「声明」，不改写 allowlist 或 seed manifest；复用项目自己的 `worktree_seed.load()` 作为 manifest 解析真源，不另写解析器。
4. **检查位置**：在 `freely-package` 的 `rm -rf "$OUTPUT"` **之前**，且保留 #4158 的输出路径守卫与其顺序；守卫仍在前。
5. **不改** `worktree_seed.py` / `wt-create` / `_init_test_worktree_state()`；不改 allowlist 内容；不批量改写历史工位。
6. 顶层 `return 1` 三处（#4201）、R3 四态判定、R4 反查、Q2 标题契约均不动。

## 关键设计

- 新增 `docs/system/workspace/scripts/quality/package-seed-parity.py`：读 allowlist → 用 `git check-ignore -q --no-index` 找出 gitignored 条目 → 用 seeder 的 `load()` 读 manifest 路径集合 → 任一 gitignored 条目未声明则打印具体路径并 exit 1。
- `bin/freely-package` 在输出路径守卫之后、清理输出之前调用该检查；检查脚本缺失时跳过（兼容旧安装态），但主仓库打包仍会由 allowlist 校验拦下缺文件。
- 回归测试 `test-worktree-seed-package-parity`：static 8 项 + behavior 5 项，含「最小 seed 项目直接跑真实打包命令」与「新增未 seed 的 gitignored 白名单条目被拦下」。

## Related findings（自举评审）

- 本轮未发现「现有 open issue 未覆盖」的新缺陷：#4201（顶层 return）、#4151（预存红测试）、#4146（fail-open 家族）、#4157（失败语义）均已覆盖本轮观察到的相邻现象，未重复立项。
- 当前 R5 工位是修复前创建的，缺 bootstrap；用**封装 seeder**（`worktree_seed.py apply`，以修复后的 manifest 为源）补齐，不是手工 cp；补齐后 `test-freely-package-output-guard` PASS。
