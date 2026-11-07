# Brainstorms: raw-20261106T100938Z

## 问题

`docs/system/workspace/package-allowlist.txt` 只列目录（`agents/`、`skills/`、`hooks/`、`scripts/`、`bin/`、`.githooks/`、`templates/`）与 9 个 `.md`，**没有列出 `docs/system/workspace/` 顶层的非 `.md` tracked 文件**。`freely-package` 逐行按 allowlist 复制，这些文件因此全部不进安装态。

全量核查：顶层 17 个 tracked 文件中 8 个不在 allowlist。R5 收口打包后实测安装态（`~/.freely/versions/latest`）：

- `freely-package --output <tmp>` → exit 1 `[ERROR] allowlist not found`（它连自己的 allowlist 都没有）；
- `worktree_seed.load(installed)` → `source=builtin entries=1`，R5 刚修的 3 条 seed 声明全部失效；
- `package-seed-parity.py --project installed` → exit 2 `allowlist not found`。

## 覆盖域与 scope

一个独立问题（产物内容完整性），一个 candidate。改动面：`package-allowlist.txt` + `bin/freely-package` 前置检查 + 新增只读 checker + 新增回归测试。

## 分类评审（逐条实证，不凭 issue 正文照抄）

| 文件 | 引用点 | 判定 |
|---|---|---|
| `worktree-seed.toml` | `worktree_seed.py:21`、`bin/freely-package`、`package-seed-parity.py` | **运行时必需**（SELF_ROOT 真源） |
| `package-allowlist.txt` | `bin/freely-package:18`、`package-seed-parity.py:27` | **运行时必需**（自举打包的入口清单） |
| `AGENTS.md.example` | `runtime/freely:8608` 的 `$SELF_ROOT/...` 模板、`:8629` 提示 | **运行时必需**（SELF_ROOT 真源） |
| `install-lifecycle-allowlist.txt` | `runtime/freely:8682`、`check-supply-chain-baseline:147` | **运行时能力清单**，但**repo-scoped**（见下） |
| `release-build-allowlist.txt` | `check-build-artifact-exposure:77` | **运行时能力清单**，但**repo-scoped**（见下） |
| `commands.md` | 0 处运行时引用，35 处 B1/B2 治理文档引用 | **文档，不随包** |
| `three-loop-lifecycle.svg` | 0 处运行时引用，6 处治理文档引用 | **文档，不随包** |
| `command-wrapper-metadata-lifecycle.md` | 仅 1 处 `scripts/tests/test-command-wrapper-metadata-contract.py` 引用 | **测试契约资料，不随包** |

### 诚实修正（相对 issue 正文）

`install-lifecycle-allowlist.txt` / `release-build-allowlist.txt` 实际是 **repo-scoped**：`runtime/freely:8682` 用 `$project/docs/system/workspace/install-lifecycle-allowlist.txt`，且 `ensure_install_lifecycle_allowlist_file()` 在缺失时会自动生成；两个 quality 脚本的默认值也经 `abs_path_allow_missing "$project" ...` 基于目标项目解析。因此「安装态 doctor 门禁缺清单」这一表述**不准确**——门禁读的是被检查项目自己的清单，不是安装态自带的。

它们仍随包发布，理由是：① tracked 的运行时能力清单，被质量门禁以字面路径引用；② 保持安装态与开发态 workspace 产物等价，避免「同一份 workspace 在开发态/安装态内容不同」的隐性漂移；③ issue 验收标准明确要求 5 个文件 sha256 对齐。真正的自举阻断者是 `package-allowlist.txt`（无它则无法打包）、`worktree-seed.toml`（无它则 seeder 回退）与 `AGENTS.md.example`（无它则 AGENTS 生成降级）。

## 不退化边界（逐条评审）

1. **保留显式白名单机制**：不得改成「自动包含整个 `docs/system/workspace/`」——#4157 已记录按目录 `cp -R` 会把 `__pycache__/`、死代码、构建期文档一起装出去。新增 5 行显式文件路径，不动机制。
2. **3 个纯文档不随包**：避免扩大安装态体积；防复发 checker 的扫描范围也明确排除 `scripts/tests/` 与 B1/B2 文档，否则会把测试契约文档误判为运行时必需（这正是「不误改功能逻辑」的关键）。
3. **与 R5 的 checker 职责分开**：`package-seed-parity.py` 管「gitignored allowlist 条目 ↔ seed 声明」；本轮 `package-runtime-file-parity.py` 管「运行时引用的 tracked 顶层文件 ↔ allowlist」。不重复实现、不改前者一行。
4. **不改** `worktree_seed.py` 的 `load()` / `apply()`（builtin 回退是极简 checkout 的兼容能力）；不改 R5 的 `worktree-seed.toml` 三条声明；不改输出路径守卫（#4158）与 R5 parity 的调用顺序；不改 allowlist 复制循环与既有后置 `integrity: verified` 校验（该校验已覆盖「产物存在性」，本轮只补「声明完整性」）。
5. **不夹带** #4194（打包触发机制）、#4179（投影副本漂移）、#4168（遗留脚本清理）、#4201（顶层 return）。
6. **不批量改写历史安装版本目录**：只保证此后打出的产物完整。`~/.freely/versions/20261106T1004Z-nightly` 的既有缺口在本轮收口重新打包后自然消失。

## 关键设计

- 新增只读 checker：枚举 `docs/system/workspace/` 顶层 tracked 文件（`git ls-files`，安装态无 `.git` 时降级为物理文件枚举）→ 在 `bin/`、`scripts/runtime|quality|worktree/` 的字面文本中找引用 → 未在 allowlist 则点名并 exit 1。排除自身文件（按文件名，兼容 `--project` 指向别的项目）、排除 `__pycache__`、排除 `scripts/tests/` 与治理文档。
- `bin/freely-package` 在 R5 seed parity 之后、`rm -rf "$OUTPUT"` 之前调用；脚本缺失时跳过以兼容旧安装态（主仓库打包仍由 allowlist 复制循环 fail-closed）。
- 回归测试 `test-package-runtime-allowlist-parity`：static 14 项 + behavior 8 项；真实打包到安全临时目录、对产物执行**安装态自举打包**、对产物 seeder/parity checker 做真实调用、构造含新增未声明文件的隔离 git 项目验证防复发。

## Related findings（自举评审）

本轮未发现「现有 open issue 未覆盖」的新缺陷。相邻现象（#4201 顶层 return、#4151 预存红测试、#4194 打包触发、#4179 投影漂移）均已被覆盖，未重复立项。
