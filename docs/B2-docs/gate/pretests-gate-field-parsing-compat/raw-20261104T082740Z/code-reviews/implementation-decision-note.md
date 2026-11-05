---
issue_id: I-20261104T082740Z-A
issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20261104T082740Z/issues/I-20261104T082740Z-A.md
phase_state: completed
---

- issue_id: I-20261104T082740Z-A
- issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20261104T082740Z/issues/I-20261104T082740Z-A.md

## Implementation Decision Note

- decision: 在 `docs/system/workspace/scripts/quality/pretests-gate` 中新增唯一字段解析真源 `_field_line_value(text, key) -> (present, value)`，把 8 处各自复制的有缺陷正则全部收敛到它；值取 `- key:` 之后的整行剩余内容，用 `[ \t]*` 严格限制在单行内，仅剥离首尾成对的同型引号，并逐调用方保留原有空值语义。
- why_this: raw issue 只描述「反引号被当作边界」，但实测发现两个更根本的问题：① `\s*` 在 `re.MULTILINE` 下会跨行，空值字段会静默把下一行内容读成自己的值，这是错读而非误报；② #3957 只放宽了 `parse_issue_binding` 一处，其余 7 处仍是旧规则，同一份文档在不同读取路径下结论不同，且 `parse_scalar` 至今不支持单/双引号。只修两处正则会留下 6 处不一致，也保不住 #3957 的兼容契约。抽成返回 `(present, value)` 的真源后，「不存在 / 存在但空 / 有值」三态可区分，才能分别兑现 `has_blocker_taxonomy()` 的「空值行也算存在」与 `issue_is_follow_on()` 的「空值不算 follow-on」。
- alternatives_considered: ①只改两处字符类——改动最小但留下 6 处旧正则与跨行错读，属修表面症状；②改用 YAML/frontmatter 解析——治理文档不是合法 YAML（各章节重复同名键），且会牵动 200+ 份既有 pre-tests.md 与全部 skill 模板，远超边界；③在门禁里预剥离反引号——无法区分「值内行内代码」与「整体反引号包裹」，还会破坏需要保留原文的证据字段。
- boundary_non_goals: 不改 pre-tests.md 字段集合与取值枚举；不改门禁失败分类；不改 `bin/pretests-gate` shim；不改证据文件路径约定；不修平台读通道静默返回空清单、raw key 漂移、`raw-issue-pull` 缺一级标题等独立缺陷；不修 9 个 legacy 门禁测试的断言漂移（已由 #4151 覆盖）。
- residual_risk: ①本次治理文档自身的 `- key: value` 字段值刻意不写行内反引号——因为 `pr-merge-guarded` 在 develop 分支执行时，develop 尚未包含本修复，其旧版 gate 仍会误判。可执行的反引号证明由新增回归测试承担，而不是靠治理文档自证；本 PR 合并后该约束自动消失。②`_field_line_value()` 的引号剥离要求「首尾同型且内部无同型引号」，因此形如 `'it's fine'` 这种内部含同种引号的值不会被剥离；旧正则同样无法处理，属既有边界，未扩大也未缩小。③9 个 legacy 门禁测试在 develop 基线上仍为红，本 PR 未修（#4151 范围），因此「全量测试绿」目前仍不能作为质量声明依据；本 PR 用逐项基线对比替代全绿声明。
