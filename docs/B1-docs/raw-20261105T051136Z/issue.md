---
schema_version: '1'
local_id: raw-20261105T051136Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T051136Z-A
platform_ids:
  github:
    issue_id: '4188'
    url: https://github.com/chatterzhao/freely/issues/4188
    synced_at: ''
  gitee:
    issue_id: IKT3HL
    url: https://gitee.com/zhaoquan/freely/issues/IKT3HL
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T05:11:37Z'
updated_at: '2026-11-05T14:00:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-05T14:00:18Z'
closeout_note: ''
---

# fix: raw-issue-pull 按 created_at 反推 key，物化目录与 local_id 静默漂移

workflow_kind: fix

## 优先级

P0 — 位于所有 issue 的入口链路。raw key 被静默改写会让本地治理目录、frontmatter、分支名与平台 raw key 脱节，B1/B2、milestone、门禁全部按错误 key 查找文件；同时使既有的平台标题自动达标链路失效。

## 既有能力与不退化边界（本 issue 的前提）

以下四处是已有的达标/兼容能力，修复必须保留，不得删除或绕过：

- `docs/system/workspace/scripts/runtime/freely` 的 `cmd_feedback` create 路径：`--title` 类型前缀与长度校验、`--body` 长度与 `##` 章节校验，并以 `[RAW-<stamp>] ` 前缀写入平台标题。
- `bin/issue-sync` 的 `_platform_title()`：create/update 时统一生成 `[RAW-<key>] <title>`，是对人工创建或标题被改写 issue 的**自动修正达标**真源。
- `docs/system/workspace/scripts/sync/platform-adapter.py` 的 `_resolve_raw_identity()`：按 `^\[RAW-<key>\]` 前缀优先解析，保留「单条匹配兜底」以兼容无前缀的历史/人工 issue。
- `pull_raw_issue()` 中按 `created_at` 反推 key 的兼容分支：用于处理标题未声明 canonical 身份的 issue。**该分支的意图是兼容，不是缺陷本身，不应删除。**

因此本 issue 的目标不是「禁止反推」，而是：保留兼容判定，修正其动作——平台侧把标题写到达标格式，本地侧身份保持调用方传入的 raw key 不变。

## 根因

`pull_raw_issue()` 在标题不含 `raw-<key>` 时，把 `created_at` 推导出的 `sk` 同时用于三件事：改平台标题、改本地 `raw_key`、改 `target_dir`。其中后两件造成身份漂移；第一件又是 no-op：

- `platform-adapter.py:1205` 的 `title.replace(f"raw-{raw_key}", f"raw-{sk}")` 在标题里没有 `raw-<key>` 子串时不产生任何变化，所以平台标题根本没被修正达标。
- `platform-adapter.py:1206` 的 `raw_key = sk; target_dir = target_dir.parent / f"raw-{raw_key}"` 把本地身份与落盘路径改成了平台创建时间。
- `docs/system/workspace/scripts/worktree/wt-create:400-415` 的 `_pull_raw_issue()` 只执行 `grep -q '"local_id"'`，不比对返回值，因此打印「materialized raw-083043Z」的假成功。
- `bin/raw-issue-pull` 末尾的 `issue-sync create "$local_id"` 使用**原始** key 查 `docs/B1-docs/raw-<原始key>/issue.md`；因物化落在漂移后的目录而找不到文件，`|| true` 静默吞掉失败，导致 `_platform_title()` 的自动达标修正没有被触发。

## 证据

- 实测：raw key `20261104T083043Z`（GitHub #4186 / Gitee IKSWU2）的标题被 `freely feedback edit --title` 改成不含 `[RAW-...]` 前缀的形式；`feedback edit` 的 title 参数直接透传给 adapter，不做达标补全（`runtime/freely:24970` 附近）。
- 执行 `freely wt-create --raw-key 20261104T083043Z --source platform --kind fix --slug wt-create-resume-test-worktree` 后，dev 工位实际出现 `docs/B1-docs/raw-20261104T083059Z/issue.md`，其 frontmatter `local_id` 也是 `raw-20261104T083059Z`；`083059Z` 是该 GitHub issue 的 `created_at` `2026-11-04T08:30:59Z` 换算值，与传入 key 相差 16 秒。
- 同一轮 `wt-create` 仍报告物化 `raw-20261104T083043Z`，无告警。
- 双平台 open issue 实测：GitHub 55 条、Gitee 50 条，各有且仅有 1 条标题不符合 `^\[RAW-<key>\]` 规范，即 #4186 / IKSWU2。这是上述链路失效的下游结果，而非独立人工遗留。

## 影响

- 任何标题未声明 canonical 身份的 issue（平台手工创建、标题规范化、`feedback edit` 改标题）物化后发生 key 漂移。
- 工位分支名含 `083043Z`，但 B1 目录、B2 路径、milestone、门禁按 `083043Z` 查找，全部找不到文件。
- 漂移目录作为未跟踪文件残留，判重与 scan 失效。
- 平台标题长期停留在不达标状态，`_platform_title()` 的自动修正链路被静默中断。

## 修复方案

1. **保留** `created_at` 反推分支作为兼容判定；把它推导出的 `sk` 仅用于识别「平台侧身份与调用方 key 不一致」，**不得**再改写本地 `raw_key` 与 `target_dir`。本地身份以调用方传入 key 为唯一真源。
2. 把 `_update_issue_title()` 的动作改为真正达标：写入 `[RAW-<调用方 key>] <原用户标题>`（保留原有类型前缀、去掉重复前缀、遵守 100 字符上限），同步到所有已配置平台；替换掉当前的 no-op `title.replace(...)`。
3. 保证 `bin/raw-issue-pull` 末尾的 `issue-sync create "$local_id"` 能命中正确落盘的 `issue.md`，从而触发既有 `_platform_title()` 修正；失败不得再被 `|| true` 静默吞掉，至少输出可诊断告警。
4. `wt-create._pull_raw_issue()` 校验返回的 `local_id` 严格等于 `raw-<raw_key>`，并校验目标文件确实存在于预期路径，否则拒绝创建工位并清理已建 dev 工位。
5. 考虑在 `freely feedback edit --title` 路径复用同一达标规则（与 `_platform_title()` 收敛为单一真源），避免 edit 再次制造不达标标题；此项需评估对历史 issue 的影响，不得直接回写历史标题。
6. 补回归测试：标题不含 canonical 前缀时，物化目录名与 `local_id` 仍等于传入 key；平台标题被修正为 `[RAW-<key>] ...`；双平台一致。

## 验收标准

- RED：对标题不含 canonical 前缀的平台 issue 执行 `wt-create`，当前会物化出与 raw key 不一致的目录、报告成功，且平台标题保持不达标。
- GREEN：物化目录名、frontmatter `local_id`、平台标题三者与传入 raw key 一致。
- GREEN：平台标题符合 `^\[RAW-<key>\] <type>: ...`，双平台一致，`_resolve_raw_identity()` 仍可对无前缀历史 issue 走单条兜底（兼容能力未退化）。
- GREEN：`_pull_raw_issue()` 在 `local_id` 不匹配时返回失败，`wt-create` 拒绝创建工位且不残留 dev 工位。
