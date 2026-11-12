# Brainstorms: 建立投影一致性检查，消除 hooks/skills/bin 复制漂移

- source_raw: raw-20261104T080259Z
- 覆盖域：`.githooks/` 死副本、projection.lock 四类投影、`freely projections verify`、
  deploy-skills 写回 hash、AGENTS 生成器 skill 名一致性。

## 真源普查（不照 issue 旧描述改）

| issue 描述 | 实测（develop `27e91e50c`） | 结论 |
|---|---|---|
| 4 个 `.sh` 死副本 | 确认，另有 **2 个未提及的残留**：`pre-push.bak.20260228-223112`、`reference-transaction.debug` | 共 6 个非 wrapper 文件要清 |
| `.githooks/` 只保留 7 个 wrapper | 实际有 **8 个** wrapper（含 `post-checkout`） | 数字以实测为准 |
| （未提及） | **`post-checkout` 是 105 行业务实现**，不是 wrapper；`workspace/hooks/post-checkout.sh` 不存在 | issue 漏掉的第 5 个「实现在投影层」实例 |
| `bin/pr-review-guarded` 无真源 | **R32 已修**（806→4 行投影） | 本轮不重复做 |
| AGENTS 与 skill 名不一致 | 确认：生成器与模板引用 `freely-fix-execution` / `freely-feature-execution` / `freely-feat-execution`，**三个都不存在** | 缺陷成立，且单体里共 6 处 |

全仓扫描确认：6 个待删文件**没有任何代码引用**（只有 `.githooks/.gitignore` 提到 debug 文件名）。

## 关键设计判断：投影有两种，不能一律按字节 hash

第一版 verifier 把 wrapper 与真源做字节比对 → **61/62 条全红**。这不是缺陷，是模型错了：

- **copy 型**（部署的 skill 目录）：目标必须与真源字节一致 → 比对 hash。
- **delegate 型**（`.githooks/<hook>`、`bin/<cmd>`）：wrapper **故意**与真源不同，
  它只是 `exec` 过去。按字节比对必然永远失败。

所以 lock 增加 `mode` 字段：`delegate` 记录**真源**的 hash，verify 检查
①真源未变 ②wrapper 仍 `exec` 该真源。两侧任一被破坏都算漂移。

## 第二个设计判断：skills 投影不能进仓库 lock

部署目标在 `~/.claude/skills` 等 **$HOME 绝对路径**下。写进仓库 lock 会把一台机器的
路径提交给所有人。因此：仓库 `projection.lock` 只存 hooks/bin/agents 三类（相对路径），
skills 投影写到部署目录旁的 machine-local lock，由 `deploy-skills` 部署后自动记录。

## 第三个判断：agents 投影校验的是「名字集合」而非字节

生成的 AGENTS.md 是项目专属的，字节 hash 无意义。真正要守的是**它引用的 skill 名都存在**。
所以 agents 条目的 hash 是「skills 目录名的有序集合」的 hash，verify 再从模板与生成器
里提取被引用的名字做存在性校验。

提取规则也踩了两次坑：裸 substring 会命中 `mktemp` 模板 `freely-a2a-worker-prompt.XXXXXX`；
反引号会命中 provenance 标记 `freely-runtime-fallback`。最终规则：`skill:<name>` 到处都算；
反引号只在 AGENTS 模板里算（那里整张表都是 skill 引用）。

## Decision

1. 删 6 个非 wrapper 文件；`post-checkout` 迁到 `workspace/hooks/post-checkout.sh` 并补 wrapper。
2. 修生成器 6 处 + 模板 3 处幽灵 skill 名，改为真实的 workflow / RED-dev-GREEN 三阶段。
3. 新增 `quality/projection_verify.py`（`record` / `verify`，0/1/2，copy 与 delegate 双语义）。
4. `bin/projections` 投影 + runtime 内联 `exec` 分派（**遵守 R31 行数预算**）。
5. `deploy-skills` 部署后写回 hash；AT 进 `CORE`/`CI_CORE`；epics 注册 story。
