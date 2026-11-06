---
schema_version: '1'
local_id: raw-20261105T062506Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T062506Z-A
platform_ids:
  github:
    issue_id: '4192'
    url: https://github.com/chatterzhao/freely/issues/4192
    synced_at: ''
  gitee:
    issue_id: IKT4G2
    url: https://gitee.com/zhaoquan/freely/issues/IKT4G2
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T06:25:06Z'
updated_at: '2026-11-06T10:02:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T09:45:00Z'
closeout_note: ''
---

# fix: worktree-seed 未声明打包白名单必需的 tool-boundary-bootstrap.md

workflow_kind: fix

优先级：P1（所有新工位里的打包测试都会失败，且与被测代码无关）

## 现象

`docs/system/workspace/package-allowlist.txt` 第 42 行把 `.freely/tool-boundary-bootstrap.md` 声明为打包必需文件，但 `docs/system/workspace/worktree-seed.toml` 只 seed 了 `.freely/agent-table.toml`（link）与 `.env`（copy）。`wt-create` 的 `_init_test_worktree_state()` 也只复制 `freely.db` 与 `a2a_task.db`。

## 实测

在由 `wt-create` 新建的 test-pre-merge 工位执行 `bash docs/system/workspace/scripts/tests/test-freely-package-output-guard`，安全目标分支真实打包时报：

```
[ERROR] missing file: .freely/tool-boundary-bootstrap.md
[ERROR] 1 allowlist path(s) not found — packaging aborted
```

测试判定 RED。主仓库存在该文件（2525 字节），工位里没有。把主仓库文件复制到工位 `.freely/` 后，同一测试 GREEN（`PASS: output guard holds`）。该工位已现场补全，代码与清单缺陷仍在。

## 影响

- 任何在新 worktree（dev 或 test-pre-merge）里执行的打包或打包相关测试都会失败，失败原因与被测代码无关，容易误判成功能回归。
- 允许清单与 seed 清单各自维护，没有一致性校验；以后新增位于 gitignored 路径的白名单条目仍会漏配。

## 修复方向

1. 在 `worktree-seed.toml` 增加 `.freely/tool-boundary-bootstrap.md` 的 copy 声明（静态文档，copy 比 link 更合适）。
2. 增加一致性检查：打包白名单里位于 gitignored 路径的条目必须在 seed manifest 中有声明，作为打包前置检查或脚本级测试。
3. 回归测试覆盖「由 `wt-create` 新建的最小工位直接执行打包」的场景。

## 验收标准

- RED：新建工位不人工补齐该文件时，打包测试报 allowlist 缺文件。
- GREEN：由 `wt-create` 创建的工位无需人工复制即可跑通打包测试；新增白名单条目若未同步 seed 会被一致性检查拦下。
