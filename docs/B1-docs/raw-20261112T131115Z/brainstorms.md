# B1 Brainstorm — raw-20261112T131115Z

## 1. 现场

R33.6 收尾时执行
`./bin/freely issue-sync --project <fix 工位> close I-20261112T031638Z-A`
（本地 status/phase_state 均 completed、双平台仍 OPEN），得到：

    [raw-lifecycle] raw metadata fields are missing, extra, or reordered
    [ERROR] issue-sync close: configured platform close failed for I-20261112T031638Z-A

直接调用效果层同样 rc=1：
`raw_lifecycle_effects.py close-platforms <I-*.md> <root>`。

纯只读复现（不碰平台）：对任意 linked 文档执行
`transition(read_issue(doc), "platform_closed", at=...)` →
`MetadataValidationError: raw metadata fields are missing, extra, or reordered`。
用 R33.5 的 I-20261112T015715Z-A（kind=linked, schema_version=1）验证，非本轮个例。

## 2. 根因

- `bin/issue-sync.d/cmd-close.sh` 对 `schema_version: 1` 的文档**一律**走 `_raw_effect close-platforms`。
- `raw_lifecycle_effects.close_platforms` → `raw_metadata_contract.transition` → `validate`。
- `validate()` 断言 `keys in (RAW_METADATA_FIELDS, ...)` 且 `kind == "raw"`。
- linked 文档字段集不同（kind: linked、promoted_from、source_candidate、pre_tests_path、
  verification_artifact_dir…）→ 必然不匹配 → **没有任何通道能关 linked**。

## 3. 影响

- goal 的收尾步骤（统一关 8 条 linked `I-*`）不可执行；目前 #4305 / #4308 / #4311 / #4312 / #4318
  全部 OPEN，且每轮 promote 继续新增。
- 属于"把流程债记成待办"的典型：连续多轮写"最后统一收口"，实际这条路走不通。

## 4. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | `cmd-close` 按 kind 分派；新增 `close-linked` 效果：独立 kind 校验 + 同一 adapter close-multi + 只回写 status: closed | 最小、不动 raw 契约 ✅ |
| B | 放宽 `validate()` 允许 kind != raw | 会同时放宽 promote/finalize 的严格语义，禁止 |
| C | 给 linked 文档伪造 raw 字段集 | 数据造假，且下次 pull 会被覆盖 |
| D | 在 `cmd-close` 里直接调 adapter，不经过 effects | 绕过 effects 单点，两条写路径分叉 |

## 5. 证伪记录

- 「是本地文档字段乱序」→ 否：任意 linked 文档都失败，kind 本身就是拒绝理由。
- 「adapter 关不了 Gitee」→ 否：raw 关单走同一个 adapter close-multi，双平台都能关。
- 「用 wt-close 顺带关」→ 否：wt-close 只处理 raw 的 platform_state，linked 残留不在其状态机内。
