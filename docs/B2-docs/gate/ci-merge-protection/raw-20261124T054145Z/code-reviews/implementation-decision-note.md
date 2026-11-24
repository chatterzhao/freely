# Implementation Decision Note: I-20261124T054145Z-A

- decision: 三处一起修——workflow 补 checks: write、develop 配分支保护、pr-merge-guarded 移除自签 fallback 改为 fail-closed。
- why_this: 三处断点互相掩盖，任一处单独修复都无法让「禁止绕过门禁」成为可验证事实；自签 fallback 是最危险的绕过通道，必须与权限/保护同步移除。
- alternatives: ① 只补权限——check 存在但无人强制，否决；② 补权限+保护但保留自签——仍有绕过通道，否决；③ 换 GitHub Ruleset / 第三方 CI——超出本 raw 边界，记录为后续演进。
- boundary: 不改 check 名、不改 verify job、不改 SUMMARY 格式、不放宽任何既有 governance gate、不触碰平台 issue 生命周期。分支保护是平台一次性设置，本轮只验证结果。
- residual_risk: 分支保护依赖平台一次性设置，若未来仓库重建/迁移需重配；已写入 workflow 注释与 AT-003 证据要求，但设置动作本身不在自动化回归内。实现期另有一项事实修正：全仓 grep 确认 `_set_governance_check_pass()` 在 pr-merge-guarded 内**只有定义、没有调用点**，因此自签 fallback 是死代码、并非当前活跃的绕过通道；仍按契约将其移除并改为 fail-closed，以消除未来被接线时重新引入绕过风险。此项不改变"缺 checks: write 与缺分支保护"两个已坐实的活跃缺陷。
- evidence_correction: Grep `_set_governance_check_pass` 于工作树全量搜索，唯一命中为函数定义本身；该事实记录于此，供 review 核对。
