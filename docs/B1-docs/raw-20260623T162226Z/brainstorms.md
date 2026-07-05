# Brainstorm: L0-L3 兜底死循环检测

## Discovery
- raw issue: raw-20260623T162243Z26Z (#3392)
- 上游: #3381 空循环分析 — semantic_loop Guard 10 盲区，SSE/状态管理已修但缺安全网

## Research
SSE Watchdog + _restore_tasks 已大幅降低空循环概率。但仍有场景需要兜底：
- SSE Watchdog 挂了 → 无实时推送
- Manager session 卡住 → 无决策输出
- AI 模型陷入短回复循环 → "无变化，退出。"

现有基础设施可用：restart_storm 滑动窗口模式、cache_metrics、task_mode、stop_ai→listen 降级。

## Decision: 四层递进，全部在 supervisor 侧，不依赖 AI

L0: 独立 TSV 窗口，5min 内 fresh>3 + 全零产出 → wait
L1: (exit_kind, worker_launched_count) 3 轮相同 + 0 worker → 递进→listen
L2: 10min >20K tokens + 0 worker → listen（依赖 #3386，降级 prompt_bytes*0.25）
L3: 总 token >500K → wait + stop marker

L1/L2→listen（自动恢复），L0/L3→wait（人工介入）。
不替代现有 semantic_loop——保留为观测信号。
