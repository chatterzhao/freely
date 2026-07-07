---
candidate_id: C-20260707T065926Z-A
status: absorbed
source_raw: raw-20260707T065926Z
milestone: M-20260707T065926Z-A
---
## C-20260707T065926Z-A: 增加执行位置
- status: absorbed
- decision_reason: 每个命令标注必须在哪个工位运行
- promoted_issue_id: I-20260707T065926Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T065926Z/issues/I-20260707T065926Z-A.md
- acceptance_criteria:
  - 10 个命令各有 "执行位置" 字段
  - pr-create-guarded: 标注必须 fix/raw-* 或 feature/raw-*
  - pr-merge-guarded: 标注必须 develop
  - issue-sync: 标注禁止保护分支
