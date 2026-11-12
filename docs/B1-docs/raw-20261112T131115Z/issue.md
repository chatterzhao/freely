---
schema_version: '1'
local_id: raw-20261112T131115Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T131115Z-A
platform_ids:
  github:
    issue_id: '4315'
    url: https://github.com/chatterzhao/freely/issues/4315
    synced_at: ''
  gitee:
    issue_id: IKUZ17
    url: https://gitee.com/zhaoquan/freely/issues/IKUZ17
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261112T131115Z/issues/I-20261112T131115Z-A.md
last_synced_comment_at:
  github: '2026-11-12T13:56:29Z'
  gitee: '2026-11-12T13:56:29Z'
hash: ''
created_at: '2026-11-12T13:11:15Z'
updated_at: '2026-11-12T13:56:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T131115Z-A
source_candidate: ''
completed_at: '2026-11-12T13:56:29Z'
closeout_note: ''
severity: P1
---

# fix: issue-sync close 对 kind linked 的 I-* 文档必然失败，linked 残留无法收口

workflow_kind: fix

## fix: issue-sync close 对 kind linked 的 I-* 文档必然失败，linked 残留无法收口

| Field | Value |
|-------|-------|
| local_id | `raw-20261112T131115Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-12T13:11:15Z |
| updated | 2026-11-12T13:11:15Z |

---

> **Freely 治理**：这是 raw issue `raw-20261112T131115Z`。实现前请用 `wt-create --raw-key 20261112T131115Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

`./bin/freely issue-sync --project <工位> close I-<key>-A` 恒定失败：

    [raw-lifecycle] raw metadata fields are missing, extra, or reordered
    [ERROR] issue-sync close: configured platform close failed for I-<key>-A

即使本地文档已是 `status: completed` / `phase_state: completed`、双平台 issue 仍 OPEN。

## 复现（2026-11-12，develop 8ad2c2a83）

1. `./bin/freely issue-sync --project <fix 工位> close I-20261112T031638Z-A` → rc=1，只打印上面两行。
2. 直接调用效果层同样失败：
   `PYTHONPATH=docs/system/workspace/scripts/lifecycle python3 docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py close-platforms <I-*.md> <root>` → rc=1。
3. 纯只读复现（不触碰平台）：对任意 linked 文档执行
   `transition(read_issue(doc), "platform_closed", at=...)` → `MetadataValidationError: raw metadata fields are missing, extra, or reordered`。
   已用 R33.5 的 `docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/issues/I-20261112T015715Z-A.md`（kind=linked, schema_version=1）验证，非本轮文档个例。

## 根因（已定位到函数）

- `bin/issue-sync.d/cmd-close.sh` 对 `schema_version: 1` 的文档一律走 `_raw_effect close-platforms`。
- `raw_lifecycle_effects.close_platforms` → `raw_metadata_contract.transition` → `validate`。
- `validate()` 断言字段序列等于 `RAW_METADATA_FIELDS`（或带 severity 变体）且 `kind == "raw"`；linked 文档字段集不同（kind: linked、promoted_from、source_candidate、pre_tests_path、verification_artifact_dir 等），必然不匹配。
- 因此 close 路径从设计上只能关 raw，linked 文档没有任何可用收口通道。

## 影响

- goal「架构债清零」的收尾步骤（8 条 linked `I-*` 统一 `issue-sync close`）不可执行；GitHub 仍有多条 linked 残留（#4305 / #4308 / #4311 / #4312 …），每轮 promote 还会新增。
- 多轮把「linked 残留」记作「不占开发轮次、最后统一收口」，实际这条路走不通，属被掩盖的流程债。

## 期望

1. `issue-sync close` 按 `kind` 分派：linked 文档用 linked 字段集校验后走平台 close；raw 保持严格语义。
2. 增加 AT：linked 文档 `close-platforms` 的本地校验阶段必须通过（mock adapter，断言不触碰真平台），同时断言 raw 的严格校验未被放宽。
3. 修复后一次性关掉现存 linked 残留（双平台同 key），并在 goal 收尾段记录清理结果。

## 边界

- 不放宽 raw 的 `validate()`（kind 必须仍是 raw）；
- 不动 promote / promote-finalize 语义；
- 平台关单仍必须经 adapter，禁止手工 gh/gitee 直接关。

### comment-20261112T135629Z
- source: system
- event: promote_finalized
- children: ["I-20261112T131115Z-A"]

拆解为以下任务:
1. [I-20261112T131115Z-A](will-be-updated)
