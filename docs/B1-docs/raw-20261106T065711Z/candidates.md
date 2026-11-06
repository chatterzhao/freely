# Candidates: raw-20261106T065711Z

## C-20261106T065711Z-A — 批量化治理门禁读取（promoted）

- source: brainstorms.md §Candidates a
- scope: 仅两项零语义变化优化
  1. `pr-create-guarded` Step 2e → 单进程 Python 扫描 `comment-resolution-scan.py`
  2. `governance-merge-gate` → 单一真源 `governance_repo_view.py`（持久 `git cat-file --batch` + 进程内缓存）
- non-goals: 不改 `search_raw_issue` 的搜索字段/状态范围/分页/limit；不改 `_retry_read` 重试与 fail-closed；不跨写操作缓存 remote head；不改 staged > range > disk 视图优先级与 `FileNotFoundError` 语义；不碰 `issue-sync` / `pull_raw_issue` 标题达标逻辑（Q2 刚收敛）。
- acceptance: gate verdict 对同一输入 byte-identical；4,363 份真实治理文档双视图逐函数 0 差异；子进程 3423 → 个位数；Step 2e 无进程扇出；相关回归零新增失败。
- decision: **promoted** → `I-20261106T065711Z-A`

## C-20261106T065711Z-B — 改按 title 精确搜索（rejected）

- reason: 证伪见 brainstorms §关键评审。会丢 body 搜索、漏 closed 老副本、破坏 ambiguous 判定与平台 parity。
- decision: **rejected（明确不纳入，禁止夹带）**

## C-20261106T065711Z-C — 削减重试 / 跨写缓存 remote head（rejected）

- reason: 削弱「读失败 ≠ 无 issue」与「读到陈旧值」两类正确性语义。
- decision: **rejected**

## C-20261106T065711Z-D — 把性能优化与标题达标逻辑合并（rejected）

- reason: 越界；Q2 刚收敛的兼容能力有退化风险；用户明确要求「不要修改了退化」。
- decision: **rejected**
