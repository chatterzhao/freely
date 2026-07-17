# Implementation Decision Note

- issue_id: I-20260717T203109Z-A

## Implementation Decision Note

- decision: 修 db_manager handler 列名（d[0]→d[1]，回归命名键契约）+ wt-close gate 韧性四件套（try/except 降级、_main_root 主仓根解析、rev-list 免管道 merge 检测、usage 同步）。
- why_this: 四根因（B1 P1-P4）均为判定输入通道缺陷，gate 判定矩阵本身（PR #3980）无需动。handler 修复对齐同文件 a2a_tasks 六个 handler 的既有 `desc[1]` 写法，一处修复恢复全部 8 处命名键消费者（含 watchdog_sse worker/reviewer 复用路径）。
- alternatives_considered: ① gate 内改数字键取值适配——把 bug 固化成接口，其余消费者仍坏，拒绝；② db 查询外置 wrapper 预查——破坏 gate 单函数自治，拒绝；③ _has_merge 保留管道加 || true——竞态仍在只是不再致命，判定恒 false 的正确性问题未解，拒绝。
- boundary_non_goals: 不改 gate 判定矩阵语义；不改 agent_working.py 客户端与 watchdog_sse（自动恢复）；不在本 lane 重启主 daemon（随 runtime 整体重启）；不处理 reviewer 多对逗号分隔解析的潜在增强。
- residual_risk: 主 daemon 重启前 handler 仍返回数字键——gate 因 try/except 降级为"无活跃 agent"，行为等同 PR #3980 现状，无回退；`--path-format=absolute` 需 git ≥2.31，低于则 _main_root 回退 $PROJECT_ROOT（等同修复前行为）；socket hash 用 `os.path.abspath`（不解 symlink），而 git 返回物理路径——若主仓经 symlink 路径启动 daemon 则 hash 不一致连不上（gate 降级放行，非阻断）。生产主仓路径为物理路径不受影响；该 path-form 敏感性是 socket-hash 设计既有特征，harness 已用 pwd -P 归一，如需根治（双侧 realpath）应独立立案。
