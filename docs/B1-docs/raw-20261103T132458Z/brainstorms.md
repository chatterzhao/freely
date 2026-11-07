# Brainstorms: raw-20261103T132458Z

## 问题

门禁把「拿不到判断依据」翻译成「通过」：`.githooks/` shim 找到真身就 exec、找不到就 `exit 0`；`pre-commit.sh` 多处 `-x` 守卫与 `|| exit 0`；`pr-create-guarded` 四处 `[WARN] ... not found, skipping`；`checkpoint-guard` 默认 `FAIL_ON_REQUIRED=0` 恒返回 0；`check-file-size` 全仓无调用点且只扫 `*.sh/*.py`，漏掉 26,837 行无扩展名真源。于是环境异常与真实通过共用退出码 0。

## 覆盖域与 scope

一个独立问题（门禁 fail-open 收敛），一个 candidate。改动 10 个真源文件 + 新增回归测试。统一退出码约定 **0=通过 / 1=不通过 / 2=环境不可用（按不通过处理）**。

## 评审中的关键发现（决定方案，避免自锁/误伤）

1. **`post-checkout` 绝不能按 shim 模板改**：它是自包含实现（自带 `freely_wt_assert_strict_root` 等逻辑），本来就没有 `docs/system/workspace/hooks/post-checkout.sh`。`git worktree add` 会触发 post-checkout；若无差别改整族，后续每轮 `wt-create` 都会被自己的 hook 阻断。因此 shim 族精确限定为 6 个：`pre-commit` / `pre-merge-commit` / `pre-push` / `reference-transaction` / `pre-rebase` / `post-rewrite`。
2. **外部项目误伤风险**：`pre-commit.sh:153` 的 `[[ -f ./bin/worktree-common.sh ]] || exit 0` 在「外部项目使用 installed freely 的 hook」时是**合法早退**（外部项目本就没有该 helper）。直接改成 exit 2 会让所有外部项目无法提交。方案：仅当 `./docs/system/workspace/hooks/pre-commit.sh` 存在（即这是 freely 自举源码树）时，缺失 helper 才是环境故障 exit 2；否则保持 exit 0。
3. **`check-file-size` 自锁风险**：全量运行已有 7 个历史 `[ERROR]`（含 26,837 行 `runtime/freely`）。若直接接进 pre-commit 并阻断，**每轮 commit 都会失败**。方案：新增 `--staged-only` 增量模式（只判断本次暂存文件、随后 early-exit），pre-commit 用它；历史遗留仍在全量运行中可见但不阻断未来提交。同时全量扫描扩展到无扩展名真源脚本，使 `runtime/freely` 被点名报 `[ERROR]`（验收标准）。
4. **`pr-create-guarded` 的正常跳过不能改**：`:266` 「no raw key found in branch, skipping review check」是无 raw key 的合法路径，保持继续；只把 4 处「门禁文件 not found, skipping」改为 `[ERROR]` + exit 2。
5. **AGENTS.md 约束方向**：禁止的是「修改 `.githooks/` **以削弱检查**」；本轮是 fail-open → fail-closed 的**加强**，方向相反，不违反。
6. **`.githooks/bin/git` 不做 PATH 注入**：全仓无安装器/PATH 引用；接线属独立基础设施改动，不在本 PR。文档中不再宣称其已生效，作为残余风险如实记录。
7. **真实 commit 冒烟测试是必须项**：本轮改的是每轮 commit 必经链路，必须在真实工位执行一次 `git commit` 确认不自锁（已验证 exit 0 / 1s）。

## 关键设计

- 6 个 shim：`[[ -x ]]` → `[[ -f ]]`（`bash file` 不需要执行位），末尾 `exit 0` → 明确诊断 + `exit 2`。
- `pre-commit.sh`：hooksPath 不符 `exit 2`；helper 缺失按「自举/外部」区分；`governance-merge-gate` 守卫 `-x`→`-f`，并显式检查 `checkpoint-guard` / `pretests-gate` / `check-file-size` / `pre-merge-commit.sh` 真身存在，缺失即 `exit 2`。
- `pr-create-guarded`：4 处 skipping → `[ERROR]` + `exit 2`。
- `checkpoint-guard`：`FAIL_ON_REQUIRED=1` 默认值。
- `check-file-size`：`--staged-only` 增量门禁 + 全量扫描覆盖无扩展名脚本。
- 新增 `test-gate-fail-closed`（static + 3 个隔离 git 仓库行为用例，28 项检查）。

## 自举评审

本轮未发现「现有 open issue 未覆盖」的新缺陷。4 个预存红测试（`test-pre-commit-hook` / `test-pre-merge-commit-hook` / `test-governance-merge-gate` / `test-merge-guarded` ENOENT）在 develop 基线同码失败、输出逐字节一致，已被 #4151 与 R1 记录覆盖，未重复立项。
