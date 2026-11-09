---
schema_version: '1'
local_id: raw-20261103T132517Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132517Z-A
platform_ids:
  github:
    issue_id: '4148'
    url: https://github.com/chatterzhao/freely/issues/4148
    synced_at: ''
  gitee:
    issue_id: IKSPQ2
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ2
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/platform/raw-20261103T132517Z/issues/I-20261103T132517Z-A.md
last_synced_comment_at:
  github: '2026-11-09T06:49:51Z'
  gitee: '2026-11-09T06:49:51Z'
hash: ''
created_at: '2026-11-03T13:25:17Z'
updated_at: '2026-11-09T07:35:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132517Z-A
source_candidate: ''
completed_at: '2026-11-09T06:49:50Z'
closeout_note: ''
---

# refactor: 统一 SDD frontmatter 解析所有权

workflow_kind: feature

## 根因
同一份 issue frontmatter 存在 3 套解析器、2 套写入路径，没有任何一方被指定为唯一所有者；仓库里已有规范实现（严格校验 + 原子写），但运行时路径不用它。

## 证据
- 规范实现：`docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py:244-252`（YAML 错误抛 `MetadataValidationError`）、`:255-270`（tmp+rename 原子写）。
- 第二套（scan 侧）：`docs/system/workspace/scripts/runtime/task-lifecycle-scan.py:357-377` 手写切片 + `yaml.safe_load`，`except Exception: pass` → 返回 `{}`。
- 第三套（同步侧）：`bin/issue-sync:34-80` 内联 `python3 -c` 的 `_fm_get/_fm_set`，错误一律 `2>/dev/null || true`；同文件 `:77-89` 又并存规范路径 `_raw_effect`。
- 已提交的坏数据（仓库内实测，非推断）：`docs/B1-docs/raw-20260519T145435Z/issue.md:3-6` 含 git 冲突标记 `<<<<<<< HEAD / ======= / >>>>>>>`；12 个 `issue.md` 的闭合 `---` 粘在末字段上（`platform_state: closed---`）；`local_id` 出现双后缀 `raw-20260616T140126Z26Z`。
- 无告警通道：损坏项经 `scan` 得 `phase_state=""`，落入 `task-lifecycle-scan.py:139-175` 的「状态不对齐/缺 phase_state」类目。

## 影响
规格面是 SDD 的前置输入。解析失败不报错，表现为「状态不对齐 → Manager 每轮去修一个不存在的状态」，或该 issue 从生命周期中消失但仍被计为已完成；两种情况都无错误输出，人只能从「AI 反复做无用功」间接察觉，同时消耗 AI 周期与 token。

## 补充证据（2026-11-04 复核）

- `freely feedback` 当前**只调** `platform-adapter create-issue`，不写本地 `docs/B1-docs/raw-<key>/issue.md`（`runtime/freely:25130-25230` 无本地落盘分支）；`raw-issue-pull` 反向物化时又不写 `# <title>` 行（只有 frontmatter + 正文），且 `develop`/`main` 直接拒绝 pull。
- 结果：本地 799 条 raw 中 700 条无标题（87.6%），平台与本地真源系统性分叉；新建 issue 在本地不可见，只能靠平台反查。
- 建议把「feedback 必须本地先写、再同步平台；pull 必须还原标题」纳入本 issue 的写入所有权与验收范围。

## 修复方案
1. `task-lifecycle-scan.py:357-377` 改为调用 `raw_metadata_contract.read_issue()`，删除手写切片与 `except: pass`；解析失败产出一条 `metadata_validation_error` 并计入「待修」类目，而不是当成空 metadata。
2. `bin/issue-sync:34-80` 的内联 `_fm_get/_fm_set` 改为复用同一模块（或改走同文件 `:77-89` 的规范路径 `_raw_effect`），删掉第三套实现。
3. 提供一次性存量修复脚本（放 `scripts/` 下、幂等、默认 dry-run）：修 12 个悬浮 `---` 与 1 个含冲突标记的 issue。
4. `raw_metadata_contract` 暴露 `validate_issue_path()`，供 scan / issue-sync / gates 共用同一判定。

## 验收标准
- RED：夹具里放一个 `platform_state: closed---` 的 `issue.md`，`task-lifecycle-scan.py` 输出必须含 `metadata_validation_error` 且列入「待修」；当前实现静默得到空 phase。
- RED：给 `raw_metadata_contract.read_issue()` 喂非法 YAML，断言抛 `MetadataValidationError` 而非返回 `{}`。
- GREEN：`grep -c "yaml.safe_load" task-lifecycle-scan.py` = 0，`grep -c "_fm_get" bin/issue-sync` = 0（或仅剩薄封装且内部走规范路径）。
- GREEN：对 12+1 个存量坏文件跑 repair 后，`scan` 不再产出任何 `phase_state=""`。
- GREEN：新增对等测试，断言 `scan` 与 `issue-sync` 对同一份损坏 frontmatter 给出**一致**结论；当前两者对同一坏输入的判定不同。

### comment-20261109T064951Z
- source: system
- event: promote_finalized
- children: ["I-20261103T132517Z-A"]

拆解为以下任务:
1. [I-20261103T132517Z-A](will-be-updated)
