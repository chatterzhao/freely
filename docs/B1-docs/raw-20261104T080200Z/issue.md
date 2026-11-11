---
schema_version: '1'
local_id: raw-20261104T080200Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T080200Z-A
platform_ids:
  github:
    issue_id: '4175'
    url: https://github.com/chatterzhao/freely/issues/4175
    synced_at: ''
  gitee:
    issue_id: IKSWC7
    url: https://gitee.com/zhaoquan/freely/issues/IKSWC7
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/issues/I-20261104T080200Z-A.md
last_synced_comment_at:
  github: '2026-11-11T13:00:46Z'
  gitee: '2026-11-11T13:00:46Z'
hash: ''
created_at: '2026-11-04T08:02:00Z'
updated_at: '2026-11-11T13:00:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T080200Z-A
source_candidate: ''
completed_at: '2026-11-11T13:00:45Z'
closeout_note: ''
---

# refactor: 把 pr-review-guarded 的业务实现移回 scripts/

workflow_kind: feature

## 根因
`bin/` 被定义为运行时投影层，不应包含业务逻辑；但 `bin/pr-review-guarded` 是 1,200+ 行完整实现，`docs/system/workspace/scripts/` 下没有对应文件，破坏真源在 scripts/ 的架构约定。

## 证据
- `docs/system/workspace/scripts/README.md:117-122`：投影层不应包含真实业务逻辑；真实实现必须回到 `workspace/scripts/**`。
- `bin/pr-review-guarded` 约 1,200+ 行，含评审调用、verdict 解析、结果落盘等完整逻辑。
- `docs/system/workspace/scripts/` 下无 `pr-review-guarded` 对应实现。
- 同类问题可能存在于其他 `bin/` 入口，需一并盘点。

## 影响
- 真源与投影边界失效，修改者不知道改哪份。
- 无法用投影一致性检查发现漂移。
- 打包/部署可能漏带真源。

## 修复方案
1. 把 `bin/pr-review-guarded` 的实现迁到 `docs/system/workspace/scripts/worktree/pr-review-guarded`，`bin/` 改为薄投影。
2. 盘点其余 `bin/` 入口，按「行数 + 是否含业务判断」识别同类，列入同一批迁移。
3. 加投影一致性检查：`bin/<cmd>` 只能是 `exec` 或参数透传，超过阈值即失败。
4. 迁移期保持行为不变，用现有测试验证。

## 验收标准
- GREEN：`bin/pr-review-guarded` 行数降到投影层阈值内，实现位于 `scripts/worktree/`。
- GREEN：`find bin -type f | xargs wc -l` 中无超过阈值的业务实现。
- GREEN：投影一致性检查接入 CI，覆盖全部 86 个入口。
- GREEN：迁移后相关测试全绿，行为无变化。

### comment-20261111T130046Z
- source: system
- event: promote_finalized
- children: ["I-20261104T080200Z-A"]

拆解为以下任务:
1. [I-20261104T080200Z-A](will-be-updated)
