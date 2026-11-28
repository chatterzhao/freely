# PRD: 批次① sync+skills 投影化
## Goal
按 R32.5 判定把 raw-issue-pull / issue-sync-bootstrap / deploy-skills 迁到 scripts 真源。
## 实现
逐字复制实现到 scripts/{sync,skills}/；bin 入口 5 行 exec；删除 registry 三条；刷新 projection.lock。
## Handoff
先 RED 锁定投影与 registry 状态，再迁移。
