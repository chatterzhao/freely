# Implementation Decision Note
- issue_id: I-20260718T004314Z-A

## Implementation Decision Note
- decision: ①删除 runtime L2120 孤儿赋值行；②manager_reconcile_agent_id_env 内 PROJECT_ROOT 改 `local _proj="${PROJECT_ROOT:-$SELF_ROOT}"` 回退（status 派发路径到达时 PROJECT_ROOT 未赋值，同链第二 set -u 致命点，GREEN 阶段暴露）。
- why_this: 赋值无消费者、变量本作用域未定义、set -u 下必死且绕过全部 || true/重定向防护；正确逻辑在 manager_reconcile_agent_id_env 默认参内已存在。
- alternatives_considered: ①加 ${source_project:-} 默认——保留死代码且语义错误，拒绝；②手工清 launch-state 残留绕过触发路径——掩盖根因，拒绝。
- boundary_non_goals: 不动 manager_reconcile_agent_id_env；不清理 launch-state 数据；不在本 lane 做 set -u 全面审计（如需独立立案）。
- residual_risk: 脚本内可能存在其他 set -u 潜伏点（$source_project 全仓已核查；裸 ${PROJECT_ROOT} 使用面未逐一审计，如需全面 set -u 审计应独立立案）。SELF_ROOT 回退在从工位脚本调用时指向工位根——与修复前 PROJECT_ROOT 未定义即死相比严格改善，且 agent_cleanup_stale 幂等无害。
