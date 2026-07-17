# Tasks: wt-close autonomous gate 收尾

- issue_id: I-20260717T203109Z-A
- owner_issue: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/issues/I-20260717T203109Z-A.md

## 任务分解

1. [x] 根因定位：bash -x 全量 trace + python heredoc 直跑（P1 FileNotFoundError 静默死）
2. [x] 根因定位：socket per-root hash 核算（主仓 80d307e1… vs 工位 02fe6bdaf9…）
3. [x] 根因定位：_has_merge 竞态（隔离复现 true、脚本内恒 false → SIGPIPE×pipefail）
4. [x] 根因定位：RPC 数字键（活跃行存在但 gate 判 zero activity；PRAGMA d[0]=cid）
5. [ ] RED：AT-001~005 对 HEAD 版本/未修复 handler 全部复现
6. [ ] dev：wt-close gate 韧性四件套（已在工位应用，待 RED 后正式提交）
7. [ ] dev：freely_db_manager.py 两处 d[0]→d[1]
8. [ ] GREEN：AT-001~005 全绿 + test-pre-merge 工位全量
9. [ ] PR → review → merge → wt-close
10. [ ] 合并后：runtime（含 db daemon）重启载入
