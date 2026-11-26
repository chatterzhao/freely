---
schema_version: '1'
local_id: raw-20261125T065112Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4698'
    url: https://github.com/chatterzhao/freely/issues/4698
    synced_at: ''
  gitee:
    issue_id: IKXVXF
    url: https://gitee.com/zhaoquan/freely/issues/IKXVXF
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T06:51:12Z'
updated_at: '2026-11-25T06:51:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P1
---

# fix: wt-close 职责边界与提示语漂移

workflow_kind: fix

## fix: wt-close 职责边界与提示语漂移

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T065112Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-25T06:51:12Z |
| updated | 2026-11-25T06:51:12Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T065112Z`。实现前请用 `wt-create --raw-key 20261125T065112Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（本轮吃狗粮实证 + git 历史交叉验证）
1. 文档与代码职责漂移：commands.md:14/33/217/224、AGENTS.md:14-15、workflow SKILL:337/270-275 仍写「正常收口 = 双平台 close issue」「先关 test 工位再关 dev 工位」，但当前代码实现是 --raw-key 唯一入口、拒绝 test-pre-merge 目标、正常路径只校验 platform_state 不写平台。
2. 提示语触发跨 raw 写：wt-close:1138 提示 `freely issue-sync --project <本工位> batch` 未带过滤键；cmd-batch.sh 明确「unscoped batch is a cross-raw write (GATE 1)」，pr-merge-guarded:568-573 用的是 `batch "$_raw_key"`。本轮照提示执行后创建了 #4689-#4696 等无关平台 issue，并改写 10 份其他 lane 的 I-* 文档（本地已 git restore，平台噪声仍在）。
3. frontmatter 契约冲突：B2 SKILL:455-470 示例推荐 bullet 格式 I-* frontmatter，但 wt-close:1100-1107 用 ctext.split("---") + yaml.safe_load 解析；仅 bullet 的文档被读成 phase_state=- / platform_state=-，直接阻塞收口，且 issue-sync batch 也静默跳过。
4. 历史遗留复杂度：Phase 7 test-pre-merge 分支自 5e5277e37 后不可达但仍占约 47 行；dev↔test 一致性在 wt-close:672-782 与 worktree-common.sh:212-268 双实现；merge 证据谓词在 wt-close:208 与 postmerge_commit_guard.py:53-55 重复；保护分支检查重复。
5. 演进主线（git 历史）：1b115062c(05-23,370 行) 单工位清理器且自带 develop 写权 → 8e0fa3a14/0c3e1885c/2a72b7947 主动交出写权 → 5e5277e37 唯一 --raw-key 入口 → f1be6b5c3 让 wt-close 直接关 I-* → 8bc4773cf 立即撤回改回委托 issue-sync → e3420687a/764e29df1 事故驱动护栏堆叠至 1576 行。方向正确（只读门禁 + 不可逆清理器），但文档未同步、旧阶段未清理、提示语漏 scope。

## 根因
职责从「清理器」演进为「终态门禁 + 不可逆清理器」，写权逐步交还 pr-review / pr-merge / issue-sync；但文档、提示语、示例模板未按同一节奏更新，导致执行者按过时文档操作，产生跨 raw 平台写与解析空字段。

## 期望
1. wt-close 正常路径保持 write-free（issue 文件与平台写均由 pr-review/pr-merge/issue-sync 负责）；--platform-only 与 --force dropped 作为显式例外需审计与文档标注。
2. 修复 wt-close 子问题提示为带 raw key 的 batch（--auto 或显式 key），并加 AT 防回归。
3. 同步 commands.md / AGENTS.md / workflow SKILL 的步骤与职责描述。
4. 为 B2 I-* 文档加 frontmatter schema 硬门禁（schema_version + YAML --- block），与 wt-close/issue-sync 解析器对齐。
5. 清理 Phase 7 死代码，统一 dev↔test 一致性与 merge 证据判定为单一真源。
