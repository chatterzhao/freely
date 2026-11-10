---
raw_id: raw-20261110T093145Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 立项假设与实测修正

立项（R23.13 期间）时的假设是「`wt-create` 物化时**没有**写 `# 标题` 行」。本轮前置评审**否掉了这个假设**：

- `git log -L 1508,1518:platform-adapter.py` 显示 H1 注入逻辑早已存在（commit `e219b49b4`，#4181 / `raw-20261104T082542Z`），注释还明确写着「Without it every first PR of a new raw issue is blocked with content_diverged」。
- 项目还已有单一所有者 `sync/raw_title_contract.py`（`local_heading_title` / `canonical_raw_title`）、回归护栏 `tests/test-materialize-h1` 与回填命令 `bin/raw-issue-backfill-h1`。
- 对比两个 raw：#4264 物化出的 B1 **缺 H1**，#4269 物化出的 B1 **有 H1**。差异不在物化开关，而在 body 内容：#4264 的 python 代码块里有行首 `# -> StateFileError: unknown state key: ...` 注释（body 第 59/61 行），#4269 没有。

**精确根因**：三处代码都用裸 `^#\s+` / `^#[ \t]+\S` 判定或提取 H1，**都不排除 fenced code block**。

| 位置 | 裸正则 | 后果 |
|---|---|---|
| `platform-adapter.py:1514`（物化） | `re.search(r"^#[ \t]+\S", body, re.MULTILINE)` | 把代码块注释当「已有 H1」→ **跳过注入**，物化文档真的没有 H1 |
| `raw-reconciliation-gate.py:_local_record` | `re.search(r"^#\s+(.+)$", body, re.MULTILINE)` | 把同一注释当 **LOCAL title**，并 `body = body[match.end():]` 丢掉它之前的全部正文 |
| `bin/raw-issue-backfill-h1`（两处） | `H1 = re.compile(r"^#[ \t]+\S", re.MULTILINE)` | 历史回填把这类文档误判为「已有标题」而跳过修复 |

两侧叠加：`pr-create-guarded` Step 0b 报 `raw replicas are inconsistent`，日志里 local.title 变成 `-> statefileerror: unknown state key: 'last_manager_continuity_generated'`，而双平台 title 是正常标题。R23.13 靠**手工补回 H1** 才通过，属人工绕过。

## 方案方向

### 方向 A：在 `wt-create` 后再补一次 H1（否决）
- 治标；gate 与 backfill 仍会误判，且「哪一层负责 H1」更模糊。

### 方向 B：只改 gate（否决）
- 物化仍不写 H1，下次照样被挡；且 backfill 仍跳过修复。

### 方向 C：单一所有者扩展为「代码块感知」+ 三处复用（选中）
1. `raw_title_contract.py` 新增 `find_local_heading(body)`：逐行扫描，` ``` ` / `~~~` 围栏（允许 0–3 空格缩进、长度 ≥3、闭合需同字符且长度 ≥ 开启）内的行一律跳过，只返回代码块外第一个 `^#[ \t]+\S` 的标题与其结束偏移；无真实 H1 返回 `None`。
2. 物化侧、gate 侧、backfill 侧（含 `--apply` 的幂等复检）**全部**改用它，删掉各自的裸正则。
3. gate 在 `--require-local` 且本地无真实 H1 时追加显式诊断 `missing_local_title`（指向 `raw-issue-pull` 重新物化），不再静默借注释、不再报误导性的 `content_diverged`。
4. AT 用**真实 `pull_raw_issue`**（只 stub 平台读取）与**真实 `_local_record`** 验证，不是只测 helper。

## 被否决
- 放宽副本一致性检查（跳过 fail-closed）——削弱治理。
- 改 `canonical_projection` 的其它维度（labels / comments / state）。
- 手工批量回填历史 B1 文档 —— 回填工具修好后按需执行，本轮不制造大规模 diff。
- 另造一套 H1 工具函数 —— 项目已有 `raw_title_contract` 单一所有者，重复会再次漂移。

## fidelity 基线

- RED 必须复现原始症状：`_local_record` 读到 `'-> StateFileError: not a title'`、物化文档没注入真实 H1、backfill 跳过修复。
- GREEN 必须证明：①无 H1 + 代码块注释 → helper 返回 None ②真实 H1 优先 ③`~~~` 围栏同样忽略 ④物化注入 H1 且保留完整正文 ⑤`_local_record` 的 title 为空且 body 完整 ⑥backfill 能修复这类文档 ⑦既有 `test-materialize-h1` 18 项全绿。
- 2 项 RED PASS 是守卫（既有 H1 回归套件仍通过、物化保留正文），不是新功能。

## 价值判定

- 不过时：三处裸正则在 develop `34d80fe18` 上实测仍在。
- 不重叠：#4181 只解决「物化不写 H1」，未考虑代码块注释；#4231 是 severity 物化；均不覆盖本条。
- 高价值：任何由 `feedback` 建单、body 含 python/shell 代码注释的 raw（bug 报告里极常见）都会在首个 PR 被误挡，且诊断完全误导。修的是「副本一致性检查本身可信度」。

## 明确不纳入

不放宽检查、不改其它投影维度、不回填历史文档、不改 `canonical_projection` 的 severity/labels 比较。
