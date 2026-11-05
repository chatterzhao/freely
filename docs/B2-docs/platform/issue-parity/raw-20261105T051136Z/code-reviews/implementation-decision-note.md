---
issue_id: I-20261105T051136Z-A
issue_path: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/issues/I-20261105T051136Z-A.md
phase_state: completed
---

- issue_id: I-20261105T051136Z-A
- issue_path: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/issues/I-20261105T051136Z-A.md

## Implementation Decision Note

- decision: 保留 `pull_raw_issue()` 的 `created_at` 反推兼容分支，但把推导值降为诊断信号；调用方 raw key 成为本地身份与落盘路径的唯一真源；平台标题改由新增纯模块 `sync/raw_title_contract.py` 构造为 `[RAW-<key>] <type>: ...` 并同步到所有 replica。`adapter` / `issue-sync` / `feedback edit` 三处共用该模块作为达标单一真源，`wt-create` 与 `raw-issue-pull` 补齐可观测性。
- why_this: 根因不是「反推」，而是反推被当成改写本地身份的授权、标题修正是 no-op、失败被两层静默吞掉。只删反推会删除用户明确要求保留的兼容能力并让无前缀历史 issue 无法开工位；只加校验不修动作则平台标题长期不达标、双平台 fingerprint 持续 diverged。抽出纯模块可让 bash 侧三处规则一致，且 `linked` 及其他 kind 的历史投影保持不变。
- alternatives_considered: ①禁止 created_at 反推——直接退化，放弃；②只在 wt-create 层把漂移目录改名回来——frontmatter 与返回值已污染，平台标题仍不达标，放弃；③把达标规则做成 adapter CLI 子命令供 bash subprocess 调用——issue-sync sync 遍历数百 issue 时加载整个 adapter 开销大且 bash 侧不可单测，改用轻量纯模块；④让 raw-issue-pull 在 issue-sync create 失败时直接失败——会把「标题未归一化」升级成「无法开工位」，超出边界，改为可诊断告警。
- boundary_non_goals: 不删 `_resolve_raw_identity()` 单条兜底、不改 `cmd_feedback` create 校验与前缀、不改 `_created_at_to_key()`、不改 `linked` 投影；不回写历史 issue 标题；不修 Q3 物化缺一级标题；不修平台读通道、raw replica reconciliation、scan 状态机；不改 bin shim 分层与打包白名单结构。
- residual_risk: ①`_platform_title()` 现在会去重复 `[RAW-...]` 前缀并截到 100 字符，803 份真实 B1 issue.md 中有 9 份输出发生变化（6 份去重复前缀、3 份截断）。这是与 `cmd_feedback` create 既有规范对齐的**修正**，但只有在后续 `issue-sync update` 真正写回平台时才会改变那 9 条平台标题；本 PR 未触发批量写回。②物化 body 仍缺一级标题（Q3），本 PR 只在 B1 issue.md 现场补回；若未来 Q3 修复前有人直接跑 `issue-sync update`，`_issue_title()` 会 fallback 到 local_id 生成不理想的标题。③`feedback edit` 的补全只在用户显式传 `--title` 时生效，历史不达标标题仍需按既有流程单独修正。④`raw-issue-pull` 的告警不阻断 pull，若 `issue-sync create` 持续失败，平台标题归一化可能仍不完整，需靠 `[WARN]` 与上层严格校验发现。⑤`docs/B1-docs/raw-20260519T145435Z/issue.md` 残留 git 冲突标记导致 YAML 不可解析，已被 #4148 / IKSPQ2 覆盖，本 PR 不动。⑥2 个相关回归测试在未修改 develop HEAD 上同样为红，属预存的断言漂移（#4151 覆盖范围），本 PR 未修。
