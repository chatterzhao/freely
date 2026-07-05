---
b1_id: B1-20260705T122651Z
phase_state: completed
source_raw: raw-20260705T122651Z
produced_candidate: C-20260705T122651Z-A
---
# B1: docs/epics 路径缺层
## Root cause: B2 SKILL.md 示例路径手写，漏 story/raw-{key} 层
## Impact: copy-paste 产生错误路径，review 落到错误位置
## Decision: 逐行补全 + pr-review-guarded 硬错误
## Candidate: C-20260705T122651Z-A promoted
