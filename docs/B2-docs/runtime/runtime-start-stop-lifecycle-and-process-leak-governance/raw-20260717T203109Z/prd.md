# PRD: wt-close autonomous gate 收尾

- issue_id: I-20260717T203109Z-A

## Goal

PR #3980 合入的 `_autonomous_close_gate()` 判定矩阵在位，但三条判定输入全部失效且带致命副作用（db socket 缺失时整个 wt-close 静默死亡）。本 lane 让 gate 的判定输入真实可用：agent_working 活跃查询、merge 证据、a2a/B1 状态全部指向正确数据源且对基础设施缺席韧性降级。

## 实现方案

| # | 修点 | 文件 | 内容 |
|---|------|------|------|
| 1 | RPC 命名键 | freely_db_manager.py | `h_aw_get`/`h_aw_get_all` 的 `PRAGMA table_info` 取 `d[1]`（列名）替代 `d[0]`（cid） |
| 2 | gate 降级韧性 | wt-close | python heredoc try/except 全包裹 + 赋值 `|| true`；db 缺席 = 无活跃 agent，不阻断 |
| 3 | 主仓根解析 | wt-close | `_main_root` 经 git-common-dir；agent_working socket / a2a db / B1 phase_state（develop 权威版优先）均指向主仓 |
| 4 | merge 检测免管道 | wt-close | `git rev-list develop --merges --grep "raw-${key}" --count`，消除 grep -q SIGPIPE×pipefail 竞态 |
| 5 | usage 同步 | wt-close | `--force` 描述对齐 autonomous gate 语义 |

## Dev-Loop Handoff

- RED：对 HEAD 已提交版本复现（AT-001/002 用 `git show HEAD:` 提取旧脚本执行；AT-003/004 对未修复 handler 起临时 daemon）
- GREEN：工位版本全绿后进 test-pre-merge 工位跑全量
- 合并后：主仓 db daemon 需重启载入 handler 修复（随 runtime 整体重启）
