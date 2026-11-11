---
schema_version: '1'
local_id: raw-20261104T075849Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T075849Z-A
platform_ids:
  github:
    issue_id: '4160'
    url: https://github.com/chatterzhao/freely/issues/4160
    synced_at: ''
  gitee:
    issue_id: IKSW8W
    url: https://gitee.com/zhaoquan/freely/issues/IKSW8W
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/issues/I-20261104T075849Z-A.md
last_synced_comment_at:
  github: '2026-11-11T12:31:43Z'
  gitee: '2026-11-11T12:31:43Z'
hash: ''
created_at: '2026-11-04T07:58:49Z'
updated_at: '2026-11-11T12:31:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T075849Z-A
source_candidate: ''
completed_at: '2026-11-11T12:31:42Z'
closeout_note: ''
---

# refactor: runtime 26,823 行单体拆分并规划 Rust 迁移

workflow_kind: feature

## 根因
核心运行时 `docs/system/workspace/scripts/runtime/freely` 是 26,823 行、935 个 shell 函数、54 个 `cmd_*` 入口的单文件，同时承担 daemon、调度、session、平台客户端、TUI 与 prompt 模板。宪法 §4 要求核心运行时/编排器/监控/恢复使用 Rust，当前实现与该硬性约束不一致。

## 证据
- `wc -l` = 26,823；函数 935 个；`cmd_*` 54 个。
- 文件头自述：`# file-size: skip (legacy 20K line monolith, split pending)`。
- 265 个文件引用该路径（含全部 `scripts/tests/*`），被 4 个脚本 `source`。
- `bin/` 86 个入口中，worktree 类已采用 `exec bin/<cmd>` 分派，是可复用的拆分模式；supervisor/A2A/task-mode/ACP/PR scan/reviewer/SSE/init/scan/status 仍内联。
- 宪法 §4 点名核心运行时/编排器/监控/恢复应为 Rust；§16 要求自举不得自我豁免。

## 影响
- 无类型系统、无结构化错误处理，不可单测、不可审计。
- 任何改动的影响面无法静态判定，回归只能靠 552 个脚本测试兜底。
- 与宪法 §4 长期不一致，外部无法据此评估架构承诺。

## 修复方案
1. 先按 `cmd_*` 清单做依赖矩阵，标出每个子命令的输入/输出/状态读写/平台调用，产出一张可评审的拆分顺序表。
2. 复用 `exec bin/<cmd>` 模式，按子命令逐个外移到 `scripts/runtime/<domain>/`，每个外移独立可合并、行为不变。
3. 优先迁移状态机、session、dispatch 三类（宪法 §4 点名的核心面）。
4. 外移完成后再评估 Rust 迁移：先做 FFI/子进程边界 PoC，明确哪些面进 Rust、哪些留在 shell。
5. 拆分期间用 `check-file-size` 锁住行数不再增长。

## 验收标准
- GREEN：给出 `cmd_*` 依赖矩阵与拆分顺序表，每个子命令标注输入/输出/状态读写。
- GREEN：至少 3 个子命令完成外移，`bin/<cmd>` 为薄投影，行为由现有测试验证不变。
- GREEN：`runtime/freely` 行数较 26,823 下降且有 CI 检查阻止回升。
- GREEN：Rust 迁移 PoC 文档给出边界、成本、回滚路径；未完成前不宣称已迁移。

### comment-20261111T123142Z
- source: system
- event: promote_finalized
- children: ["I-20261104T075849Z-A"]

拆解为以下任务:
1. [I-20261104T075849Z-A](will-be-updated)
