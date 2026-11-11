---
schema_version: '1'
local_id: raw-20261104T080007Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T080007Z-A
platform_ids:
  github:
    issue_id: '4165'
    url: https://github.com/chatterzhao/freely/issues/4165
    synced_at: ''
  gitee:
    issue_id: IKSW9M
    url: https://gitee.com/zhaoquan/freely/issues/IKSW9M
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/issues/I-20261104T080007Z-A.md
last_synced_comment_at:
  github: '2026-11-11T01:55:44Z'
  gitee: '2026-11-11T01:55:44Z'
hash: ''
created_at: '2026-11-04T08:00:07Z'
updated_at: '2026-11-11T01:55:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T080007Z-A
source_candidate: ''
completed_at: '2026-11-11T01:55:43Z'
closeout_note: ''
---

# feat: 核心 runtime 变更建立 TDD 证据链

workflow_kind: feature

## 根因
宪法 §16 要求自举开发不得自我豁免，但核心 runtime 的变更长期缺少 TDD 证据：没有「先写失败测试、再实现、再转绿」的可追溯记录，只有结果性脚本测试。

## 证据
- `docs/system/workspace/scripts/runtime/freely` 26,823 行，无对应单元测试目录。
- `scripts/tests/` 552 个文件以端到端/脚本级为主，缺少针对单个函数的 RED→GREEN 记录。
- `freely-test-RED-execution` skill 已定义 RED 的要求，但核心 runtime 的 PR 未见引用该证据。
- 宪法 §16.1：Freely 自身开发不得绕开治理链。

## 影响
- 自举公信力下降：无法证明关键修复先有失败测试。
- 回归只能靠大范围脚本测试，定位成本高。
- 与托管项目的验收标准不一致。

## 修复方案
1. 为核心 runtime 建立最小单测框架：按函数抽 shell 函数测试，先覆盖状态机、锁、退出码三类。
2. PR 模板增加「RED 证据」必填项：失败测试输出/命令/commit。
3. `pr-review-guarded` 检查 RED 证据存在性，缺失则 needs_changes。
4. 先把最近 3 个 runtime 修复补成 RED→GREEN 样例，作为模板。

## 验收标准
- GREEN：核心 runtime 有 ≥10 个函数级测试，可在 CI 运行。
- GREEN：PR 模板含 RED 证据字段，review 侧能校验。
- GREEN：至少 3 个已合并修复补齐 RED→GREEN 记录。
- GREEN：`freely-test-RED-execution` 的验收项在核心 runtime PR 中被实际引用。

### comment-20261111T015543Z
- source: system
- event: promote_finalized
- children: ["I-20261104T080007Z-A"]

拆解为以下任务:
1. [I-20261104T080007Z-A](will-be-updated)
