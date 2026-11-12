---
schema_version: '1'
local_id: raw-20261104T080259Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T080259Z-A
platform_ids:
  github:
    issue_id: '4179'
    url: https://github.com/chatterzhao/freely/issues/4179
    synced_at: ''
  gitee:
    issue_id: IKSWCJ
    url: https://gitee.com/zhaoquan/freely/issues/IKSWCJ
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/issues/I-20261104T080259Z-A.md
last_synced_comment_at:
  github: '2026-11-11T14:02:34Z'
  gitee: '2026-11-11T14:02:34Z'
hash: ''
created_at: '2026-11-04T08:02:59Z'
updated_at: '2026-11-12T01:48:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T080259Z-A
source_candidate: ''
completed_at: '2026-11-11T14:02:33Z'
closeout_note: ''
---

# fix: 建立投影一致性检查，消除 hooks/skills/bin 复制漂移

workflow_kind: fix

## 根因
多处以复制方式维护投影：`.githooks/*` 是 wrapper 但也有 4 个 stale `.sh` 副本；skills 通过复制部署；`bin/` 部分入口是完整实现。复制品与源不一致时无任何检测。

## 证据
- `.githooks/` 有 7 个 wrapper，另有 4 个 `.sh` 死副本（`pre-commit.sh`/`pre-merge-commit.sh`/`pre-push.sh`/`reference-transaction.sh`），与 `docs/system/workspace/hooks/*.sh` 语义不同。
- `bin/deploy-skills` 以复制方式部署 skill，无 hash 校验。
- `bin/pr-review-guarded` 是完整实现，`scripts/` 下无对应真源。
- `ensure_project_agents_md` 生成的 AGENTS 与当前 skill 名不一致。

## 影响
- 同一门禁两份实现，维护者改错文件。
- 部署后的 skill 与源不一致，问题无法复现。
- 无法用机器证明投影与真源一致。

## 修复方案
1. 删除 4 个 stale `.sh` 副本，`.githooks/` 只保留 wrapper。
2. 所有投影加 hash 清单：`projection.lock` 记录源路径 + hash + 目标路径。
3. 加 `freely projections verify`：逐项比对 hash，不一致即失败。
4. `deploy-skills` 部署后写回 hash，CI 定期校验。

## 验收标准
- GREEN：`.githooks/` 无 `.sh` 副本，只有 7 个 wrapper。
- GREEN：`projection.lock` 覆盖 hooks/skills/bin/AGENTS 四类投影。
- GREEN：`freely projections verify` 在一致时退出 0，篡改任一投影时退出非零。
- GREEN：CI 每次 PR 运行投影校验。

### comment-20261111T140234Z
- source: system
- event: promote_finalized
- children: ["I-20261104T080259Z-A"]

拆解为以下任务:
1. [I-20261104T080259Z-A](will-be-updated)
