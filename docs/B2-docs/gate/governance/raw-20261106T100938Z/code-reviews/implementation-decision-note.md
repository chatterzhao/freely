# Implementation Decision Note
- issue_id: I-20261106T100938Z-A
- decision: 显式补齐 5 个运行时必需的 workspace 顶层文件到打包 allowlist；新增只读 checker 作为打包前置防复发约束；安装态由此可自举打包、seeder 读到随包 manifest
- why_this: allowlist 与「运行时实际引用」两份事实各自维护且无机器约束，导致安装态缺自己的 allowlist / seed manifest / AGENTS 模板，形成「开发态全绿、安装态静默降级」。用户要求「优秀的 freely」，安装位置必须完整可用。
- alternatives_considered: 自动包含整个 `docs/system/workspace/`（破坏 #4157 收敛，会把文档/测试资料/__pycache__ 带进安装态）；把 3 个纯文档一并打包（扩大体积且无运行时消费者）；把防复发检查合并进 R5 seed parity（职责混淆）；批量改写历史安装版本（高风险无收益）；改 `worktree_seed.load()` 删掉 builtin 回退（破坏极简 checkout 兼容）。
- boundary_non_goals: 不改 R5 的 `package-seed-parity.py` / `worktree-seed.toml` / 输出路径守卫 / 调用顺序 / allowlist 复制循环与后置完整性校验；不改 `worktree_seed.py`；不夹带 #4194 / #4179 / #4168 / #4201；不批量改写历史安装版本。
- residual_risk: ①顶层 `return 1` 仍待 #4201（队列 R6.5）。②checker 在脚本缺失的旧安装态会跳过（兼容性折中），主仓库打包仍由 allowlist 复制循环 fail-closed。③checker 以「字面引用」判定运行时依赖，若未来改用动态拼接路径构造引用可能漏检，需随打包机制演进调整。④安装态无 git 元数据时降级为物理文件枚举，仍能发现「已存在但未声明」的文件。
- verification: AT-001 RED 精确复现（产物缺 5 文件 / 安装态 `allowlist not found` / seeder `source=builtin entries=1`）→ GREEN 全通过（sha256 parity、安装态自举 `integrity: verified`、seeder `source=manifest entries=3`、R5 parity `undeclared=[]`、防复发拦截点名）；10 个回归全 PASS；9 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；相邻现象已被 #4201 / #4151 / #4194 / #4179 覆盖，未重复立项。评审中实证修正了 issue 正文「安装态 doctor 门禁缺清单」的不准确表述（两份 allowlist 实为 repo-scoped），已写入 B1 brainstorms 与本轮 GREEN 证据。
