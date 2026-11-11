# Implementation Decision Note
- issue_id: I-20261104T075959Z-A
- issue_path: docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/issues/I-20261104T075959Z-A.md
- decision: 新增 `skill-map.yaml` 单一真源 + 37 份 `loop`/`owner`/`supersedes` frontmatter + `bin/check-skill-frontmatter`（0/1/2）+ AT-001；消除 1 处重复 gate 枚举措辞；AT 进 `CORE`/`CI_CORE`；epics-map 注册 story。删并型重构另立 raw。
- why_this: 三组「重叠」经真源普查是阶段/owner 分工，直接删并会破坏 dispatcher 与 TDD 顺序；真正缺的是机器可读的路由真源与漂移检测，而零语义变化的契约可以先落地并给后续删并提供 `supersedes` 落点。矩阵用 JSON 兼容 YAML 1.2 子集，安装态无 PyYAML 也能 `json.loads`。
- alternatives_considered: ①按 issue 原方案删并到 ≤25——合并的是分工而非重复，且牵动 AGENTS/workflow/hooks/索引/打包，风险不可控；②只写一份 markdown 矩阵——零风险但无法机检，frontmatter 继续漂移；③把 lint 放进 SKILL.md 的说明里——没有退出码，等于没有门禁。
- boundary_non_goals: 不删任何 skill；不改 SKILL.md 正文语义；不改 workflow 全链路顺序；不改 `runtime/freely`；不改 `pr_body.py` / Step 2.5 / issue 同步契约；不把 `inputs`/`outputs`/`triggers` 填成臆测的精确值。
- residual_risk: ①矩阵的输入/输出/触发词是结构化占位，删并轮需补真实值；②lint 不扫描正文里的重复命令表，只消除已实证的 1 处并禁止该短语回归；③三组判定为 `keep_separate`，删并轮必须同步 `routing`/`supersedes`/索引；④`supersedes: []` 全空是预留落点，不代表已合并。

## 验收标准 4 为什么改了范围

B1 `issue.md` 正文把 `grep -r "从 gate 源码提取" docs/ 为 0` 写进验收标准，
于是这句短语本身出现在 `docs/B1-docs/` 里，字面断言自指、恒不成立。
按 `AGENTS.md` 的仓库分层，B1/B2/milestones 是「指导开发 Freely」的过程文档，
`docs/system/workspace/` 才是会被 agent/runtime 消费的能力目录；重复枚举的
真实危害只发生在能力目录，检查范围据此收窄，并在 AT、pre-tests、review 三处留痕。
