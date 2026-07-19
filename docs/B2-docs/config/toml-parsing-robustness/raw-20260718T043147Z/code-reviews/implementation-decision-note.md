---
issue_id: I-20260718T043147Z-A
issue_path: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/issues/I-20260718T043147Z-A.md
phase_state: in_dev
---

- issue_id: I-20260718T043147Z-A
- issue_path: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/issues/I-20260718T043147Z-A.md

## Implementation Decision Note

### Decision 1: `monitor-ai-acp.sh` awk pattern 修复
- decision: 将 awk 条件改为容忍等号两侧空格
- why_this: 即时解除 P0 阻塞。原 awk pattern `$1 == k " ="` 要求等号左侧恰好一个空格，与 TOML 规范不一致
- commit: cf6e94c42

### Decision 2: `freely_config.py get` — awk → 标准 TOML 解析器
- decision: 将 `monitor-ai-acp.sh` 的 config.toml 取值从 awk 替换为 `freely_config.py get`（基于 Python `tomllib` 标准库）
- why_this: awk/sed/grep 手写 TOML 解析本质上是维护一个残缺的解析器，格式稍有变化（等号空格、多行字符串、inline table）就会出错。`tomllib.load()` 是 Python 3.11+ 标准库，正确处理所有合法 TOML 语法，零维护成本
- alternatives_considered:
  - (A) 继续修 awk pattern — 打地鼠式修复，每次遇到新格式都得再修，不解决系统性问题
  - (B) 引入第三方 TOML CLI（如 `tomlq`、`yj`）— 增加外部依赖，而项目已有 `freely_config.py` 封装了 `tomllib`
  - (C) 所有取值走 Python — 选择在已有 `freely_config.py` 上加 `get` 子命令，最小增量
- boundary_non_goals: 不修改其他 `freely_config.py` 子命令；不影响 `start-lead-agent.sh` 中解析 state 文件（非 TOML）的 awk
- residual_risk: 无。`tomllib` 是标准库，`freely_config.py` 已有成熟的结构
