---
issue_id: I-20260629T160852Z-A
issue_path: docs/epics/wt-close-raw-key/raw-key-param/raw-20260629T160852Z/issues/I-20260629T160852Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260629T160852Z-A
- issue_path: docs/epics/wt-close-raw-key/raw-key-param/raw-20260629T160852Z/issues/I-20260629T160852Z-A.md

## Implementation Decision Note

- decision: 在 wt-close 脚本的 arg 解析后增加 raw key → branch 转换逻辑。输入匹配 `raw-YYYYMMDDTHHMMSSZ` 时，通过 `git branch --list` 搜索对应的 fix/feature 分支。同时更新 usage() 帮助文案
- why_this: 最小改动，与 wt-create --raw-key 对齐。Phase 6b 已有 test-pre-merge 自动清理，无需新增复杂逻辑
- alternatives_considered:
  - 新增 --raw-key 标志: 增加参数复杂度，raw key 格式本身足够区分
  - 不做 raw key 入口只改 help: 用户仍需记分支名，API 不对称
- boundary_non_goals:
  - 不改变 wt-close 核心流程（Phase 1-7）
  - 不改变 Phase 6b 的 test-pre-merge 自动清理逻辑
  - 不修改其他脚本
- residual_risk: 极低。raw key 正则严格匹配，不会误匹配现有的分支名。新增逻辑在 arg 解析后、所有核心逻辑前
