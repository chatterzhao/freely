# Pre-Tests: skill 删并的索引兼容期
- issue_id: I-20261111T083905Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: alias 兼容层 + 3 组语义删并 + 知识并入 + supersedes 回填 + 路由 CLI + lint 守护 + 可执行真源无悬空引用 + CI 接线 + epics-map
- acceptance_target: 删并 skill 后历史名字仍可解析、知识不丢、引用不悬空
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；lint 与 route 行为用临时 fixture 项目，不访问真实平台
- required_evidence: 15 静态 + 2 行为 = 17 项全 GREEN；R28 AT 回归 21/0；`test-all --ci` 16/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-skill-merge-compat.py
- test_command: python3 docs/system/workspace/scripts/tests/test-skill-merge-compat.py
- expected_output: SUMMARY: 17 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 15 failed
- actual_RED_output: develop `faab26c14` 基线 + 最终版 AT-001 → `2 ok, 15 failed`（AT-001-RED.log）：无 aliases 段、无 `bin/skill-route`、4 个目录仍在、supersedes 全空、README 仍列全、lint 不校验 alias、AT 未进 CI、epics-map 无 story。2 项 ok 是空集合/负向守卫（lint 接受合法 alias、可执行真源本就无 dangling 名），不是缺陷证据。
- actual_output: 工位同一断言 → `17 ok, 0 failed`（AT-001-GREEN.log）；`bin/check-skill-frontmatter` → `ok (33 skills, 12 loops)`；R28 AT `21 ok / 0 failed`；`bin/test-all --ci` `16 ok / 0 failed`；`check-epics-map` 16 epics / 211 stories aligned。
- evidence_file: docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态断言 aliases 段/内容/retired 不在 matrix/目录消失/总数下降/CLI 存在/supersedes 回填/合并章节/README 索引/AT 接线/epics-map；行为上跑 `bin/skill-route` 的 4 个 alias 与 `--loop intake`，并用临时 fixture 验证 lint 对悬空 alias rc≠0、合法 alias rc=0；另扫描 AGENTS/.githooks/bin/agents/hooks 确认无 dangling 引用。
- red_how: `git archive develop | tar -x -C /tmp/r28-5-base`，只注入最终版 AT-001，`--source-dir /tmp/r28-5-base` 运行。
- implementation_findings: ①四个候选都含真实知识，只删目录 + 别名会永久丢失，必须以章节并入；②引用普查要排除 `.git`/`.freely`/安装态，否则历史文档会虚高计数；③`skill-route` 的 ROOT 由脚本位置推导，RED 快照与 GREEN 工位各读各的矩阵；④lint 的 alias 校验必须同时检查 target 存在、alias 不存活、supersedes 回填三项，缺一就会出现「假兼容」；⑤R28 的 AT 与 lint 是回归基线，删并后仍须 21/0。

## Unit

- acceptance_target: frontmatter supersedes 解析、alias 解析、枚举一致性
- testing_layer: unit
- target_environment: 工位真源 + 临时 fixture 项目
- required_evidence: AT-001 静态 15 项 + `bin/skill-route` 5 次解析 + lint 两个 fixture 退出码
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-skill-merge-compat.py`（17/0）
2. `python3 bin/check-skill-frontmatter`（33 skills / 12 loops，rc=0）
3. 悬空 alias fixture → rc≠0；合法 alias fixture → rc=0

## Integration

- acceptance_target: R28 契约不因删并退化，聚合测试不拖红
- testing_layer: integration
- target_environment: test-pre-merge-20261111T083905Z-skill-merge-compat test 工位（`test-gate run`）
- required_evidence: R28 AT 21/0、`test-all --ci` 16/0、epics-map 对齐
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-skill-frontmatter-contract.py`（21/0）
2. `bin/test-all --ci`（16/0）
3. `python3 bin/check-epics-map`（16 epics / 211 stories）
4. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`

## End-to-End

- acceptance_target: 真实 PR 链路上删并不阻断流程
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded` / `freely pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；review Step 2.5 skip；merge 门禁通过
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR 创建/复用
2. `freely pr-review-guarded <branch>` → Step 2.5 对非 runtime diff 输出 skip
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 删并只影响 skill 语料与索引，不改 `runtime/freely`、不改 workflow 全链路、不动 dispatcher 三条 claim 路径；被删 4 个 skill 经全仓扫描确认无运行时/hooks/tests 引用；合并后 followthrough 会重新打包安装态，届时 skills 目录文件数下降即为真实环境验证。历史 B1/B2 文档里的名字属研发留痕，不是可执行引用。
