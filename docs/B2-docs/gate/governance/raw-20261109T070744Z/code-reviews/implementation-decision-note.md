# Implementation Decision Note
- issue_id: I-20261109T070744Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20261109T070744Z/issues/I-20261109T070744Z-A.md
- decision: 门禁对「基线副本不可解析」的 issue 文档做结构修复豁免——把这类路径整体从本次 merge 的 owner 集合剔除并记 warning；判定用纯 YAML，兼容 `--staged` 与 `--range` 两条执行路径
- why_this: GATE 1 把「diff 触及的每个 issue 文档」都当 owner，而 23 份历史坏文档的 key 各不相同，任何修复分支必然被判「一工位多 issue」，于是坏文档在门禁下永远无法被修复。一份 frontmatter 不可解析的文档，其 phase/candidate/issue 链从未读到过它的状态，修它的结构不可能改变任何人的治理状态。
- alternatives_considered: ①按 diff 内容判断（只改 frontmatter 行）——需要精确语义 diff，易被构造绕过；②路径白名单文件——清单本身要过门禁，又一个死锁；③逐条把 GATE 1 mismatch 降级为 warning——实测后续 phase-vs-code / review-artifact / milestone 三类校验仍报 28 条，必须整体剔除；④改用安装版门禁——hook 用 `git rev-parse --show-toplevel` 取主仓脚本，安装态不参与，且移除主仓 hook 属违规绕过。
- boundary_non_goals: 不改 GATE 1 对「基线可解析」文档的拦截；不改 `pr-merge-guarded` / hook 包装层 / `install_state`；不引入 `parse_issue_text` 依赖（#4148 尚未合并，门禁必须先landing）；不做 issue 文档的批量格式统一。
- residual_risk: ①判定只看「YAML 是否能 load」+「闭合是否粘连」+「是否成对冲突标记」，若将来出现新的损坏形态（例如 frontmatter 合法但字段类型错）不会被识别，需另行扩展；②豁免是「整份文档退出 owner 校验」，若有人故意把基线文档弄坏再借豁免改内容，门禁看不出来——但把文档弄坏本身就需要一次 develop 提交，成本高于收益；③`--staged` 模式依赖 `HEAD` 为合并前状态，若将来改成 octopus merge 或直接 push 路径需重新确认。
- verification: AT-001 develop 基线快照 RED `5 ok / 8 failed` → 工位 GREEN `13 ok / 0 failed`；真实场景 `raw-20261103T132517Z` 的 PR 在 develop 侧从 28 条错误降为结构性修复 warning 并通过门禁。
- self_bootstrap_findings: ①初版只降级 GATE 1，实测后面还有 28 条连锁错误——证明「逐条放行」是错的，必须整体剔除；②初版只在 `--range` 生效，而 `pr-merge-guarded` 走 `--staged`，等于没修；③初版依赖 #4148 的 `parse_issue_text`，但门禁必须先于它进入 develop，改用纯 YAML 判定。

## Implementation Decision Note
- decision: 基线不可解析 → 结构修复豁免（整体剔除 owner 集合），纯 YAML 判定，staged/range 双路径
- why_this: 坏文档在任何工位都会被判「多 issue 混入」，形成修复死锁
- alternatives_considered: diff 内容判断 / 路径白名单 / 逐条降级 / 安装态绕过
- boundary_non_goals: 不放宽可解析文档的拦截，不动 pr-merge-guarded 与 hook，不依赖未合并解析器
- residual_risk: 新损坏形态识别不到、豁免可被蓄意利用（成本高）、staged 依赖 HEAD 语义
