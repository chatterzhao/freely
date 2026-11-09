---
candidate_id: C-20261103T132517Z-A
status: promoted
source_raw: raw-20261103T132517Z
created_at: 2026-11-09
milestone: M-20261103T132517Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261103T132517Z-A: SDD frontmatter 解析收口到单一所有者

- candidate_format_version: v2
- title: 契约模块暴露严格解析入口；scan 与 issue-sync 删除第二/第三套解析器；幂等修复 12 个存量坏文档；损坏项统一报 metadata_validation_error
- status: promoted
- decision_reason: 三套解析器 + 静默失败让 12 个历史文档从生命周期中消失却无错误输出，Manager 反复做无用功；不收口所有权则修数据后仍会复发。
- next_action: 建 AT-001（9 静态 + 9 行为，真实驱动 scan / contract / CLI / repair），改 3 个真源 + 新增 CLI + 修复 12 个文档。
- revisit_trigger: 若新增第四种文档布局或改用数据库存储，需同步扩展 `validate_issue_path()` 的判定与 CLI 入口。
- acceptance_criteria:
  - RED：夹具 `platform_state: closed---` → scan 输出 `metadata_validation_error`；当前静默空 phase。
  - RED：`read_issue()` 喂非法 YAML → 抛 `MetadataValidationError`；当前抛 `yaml.ParserError`。
  - GREEN：`grep -c yaml.safe_load task-lifecycle-scan.py` = 0；`_fm_get` 仅剩调用共享 CLI 的薄封装。
  - GREEN：12 个存量坏文件 repair 后 scan 不再产出 `phase_state=""`，全量 B1 严格解析 0 失败且 repair 幂等。
  - GREEN：scan 与 CLI 对同一损坏 frontmatter 给出一致结论。
- promotion_gate: AT-001 RED → GREEN + 18 个相关回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对三套解析器；实测 12 个坏文档形态；驱动真实 scan `read_issues_dir` 复现静默；证伪 #4183/#4184/#4216/#4151 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261103T132517Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261103T132517Z/issues/I-20261103T132517Z-A.md
- milestone: M-20261103T132517Z-A
- session_refs: []
