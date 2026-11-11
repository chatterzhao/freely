# Pre-Tests: skill 重叠矩阵与 frontmatter 单一契约
- issue_id: I-20261104T075959Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `skill-map.yaml` 成为 37 个 skill 的路由/重叠单一真源；每个 SKILL.md frontmatter 声明 `loop`/`owner`/`supersedes` 且与矩阵一致；`bin/check-skill-frontmatter` fail-closed；能力目录不再重复定义 gate 枚举；AT 进 CI；epics-map 注册 story
- acceptance_target: agent 首跳路由有机器可读且被 lint 守护的真源
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；lint 行为用临时 fixture 项目，不访问真实平台
- required_evidence: 19 项静态 + 2 组行为 = 21 项全 GREEN；真实语料 lint rc=0；`test-all --ci` 15/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-skill-frontmatter-contract.py
- test_command: python3 docs/system/workspace/scripts/tests/test-skill-frontmatter-contract.py
- expected_output: SUMMARY: 21 ok, 0 failed
- expected_RED_output: SUMMARY: 0 ok, 21 failed
- actual_RED_output: develop `49958c1d9` 基线 + 最终版 AT-001 → `0 ok, 21 failed`（AT-001-RED.log）：无 `skill-map.yaml`、无 lint、37 个 frontmatter 全缺 `loop`/`owner`/`supersedes`、B2 skill 仍写「从 gate 源码提取」、AT 未进 `CORE`/`CI_CORE`、epics-map 无 story。
- actual_output: 工位同一断言 → `21 ok, 0 failed`（AT-001-GREEN.log）；`python3 bin/check-skill-frontmatter` → `ok (37 skills, 12 loops)`；`bin/test-all --ci` → `15 ok, 0 failed`。
- evidence_file: docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态断言矩阵存在/可解析/覆盖 37 个 skill/条目字段齐全/三组重叠判定合法/12 个 loop 唯一入口/frontmatter 三字段/枚举合法/逐条一致/无孤儿/能力目录无重复措辞/AT 进两个 CI 列表/epics-map story；行为上用临时 fixture 跑 lint 的「缺字段拒绝」与「合规接受」两种退出码。
- red_how: `git archive develop | tar -x -C /tmp/r28-base`，只注入最终版 AT-001，`--source-dir /tmp/r28-base` 运行；快照不含本轮任何实现文件。
- implementation_findings: ①验收标准 4 的字面 `grep -r docs/` 与 B1 `issue.md` 正文自指矛盾，按 AGENTS.md 仓库分层把范围收窄到 `docs/system/workspace/`；②`skill-map.yaml` 必须是 JSON 兼容子集，否则安装态无 PyYAML 时 lint 静默跳过（R23 同族坑）；③`pr_body.py` 的 RED 证据段与 lint 共用 `pre-tests.md` 的 `actual_RED_output` 字段；④`epic-skills` 已存在，新增 story 后其后所有 epic 的 y 坐标整体 +26。

## Unit

- acceptance_target: frontmatter 解析、枚举判定、矩阵一致性
- testing_layer: unit
- target_environment: 工位真源 + 临时 fixture 项目
- required_evidence: AT-001 静态 19 项 + `bin/check-skill-frontmatter` 两个 fixture 退出码
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-skill-frontmatter-contract.py`（21/0）
2. `python3 bin/check-skill-frontmatter`（37 skills / 12 loops，rc=0）
3. 缺 `loop`/`owner` 的 fixture → rc≠0；合规 fixture → rc=0；缺 `skill-map.yaml` → rc=2

## Integration

- acceptance_target: 新增 lint 与 AT 接入既有聚合测试且不拖红回归
- testing_layer: integration
- target_environment: test-pre-merge-20261104T075959Z-skill-overlap-matrix test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0 与 `.freely/run/test-evidence.log`；`bin/test-all --ci` 15/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（15/0，新 AT 进 `CORE`/`CI_CORE`）
2. `python3 bin/check-epics-map`（16 epics / 210 stories aligned）
3. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`
4. 全仓 `grep -rn "从 gate 源码提取" docs/system/workspace/` → 0

## End-to-End

- acceptance_target: 真实 PR 链路上 lint 与证据链不阻断非 runtime 变更
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded` / `freely pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；review Step 2.5 skip；merge 门禁通过
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR 创建/复用，body 含 RED 证据段
2. `freely pr-review-guarded <branch>` → Step 2.5 对非 runtime diff 输出 skip 并继续
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮不改 `runtime/freely`、不删任何 skill、不改 workflow 顺序，运行时与 dispatcher 行为零变化；新增 lint 与矩阵在真实语料（37 个 SKILL.md）上跑过，AT 在真实 develop 基线快照上复现 RED。删并型重构另立 raw，不在本轮引入真实环境风险。
