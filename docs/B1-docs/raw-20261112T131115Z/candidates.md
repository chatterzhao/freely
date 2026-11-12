# B1 Candidates — raw-20261112T131115Z

## C-20261112T131115Z-A：issue-sync close 支持 kind=linked

- kind: fix
- 范围：
  1. `bin/issue-sync.d/cmd-close.sh`：按 `kind` 分派（linked → `close-linked`，raw → `close-platforms`）。
  2. `raw_lifecycle_effects.py`：新增 `close_linked`，只校验 kind=linked + platform_ids + adapter 全绿，
     成功后把 `status: closed` 与 `updated_at` 写回，其余字段与顺序原样保留，**不经过 raw 的 `validate()`**。
  3. 新增 AT `test-issue-sync-close-linked.py` 与 unit `t-linked-close-01.sh`，接入 CORE / CI_CORE。
- 验收：
  - 全绿关单 → rc=0 且 `status: closed`、body 与 linked 专属字段逐字保留；
  - 部分关单 → rc!=0 且文档字节不变（可幂等重试）；
  - kind=raw 传给 `close-linked` → 拒绝；
  - `close-platforms` 对 linked 仍然拒绝（raw 严格契约未被放宽）。
- 不退化边界：
  - raw 的 `validate()` / `close-platforms` 语义一行不改；
  - 平台写仍全部经 adapter `close-multi`（不直连 gh/gitee）；
  - 不改 promote / promote-finalize；不改 linked 的 phase_state 语义（completed 是开发完成的历史）。
- 修复后动作：一次性关掉现存 linked 残留（#4305 / #4308 / #4311 / #4312 / #4318 及其 Gitee 副本），
  在 goal 「收尾」段记录清理结果。
