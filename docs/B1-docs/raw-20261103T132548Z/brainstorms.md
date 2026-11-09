# Brainstorms: raw-20261103T132548Z

## 问题

架构承诺「证据 + 门禁 > agent 自述」，但唯一能证明「测试跑过」的机器证据是明文本地文件，且唯一 CI 是打印 `CI OK` 的桩。

## 证据（本机实测 + 既有语料）

- `.gitee-ci.yml` 注释直言 `Minimal CI — satisfies Gitee's "must pass tests" merge requirement`，`script: - echo "CI OK"`；`only` 只有 `develop / feature/* / hotfix/*`，而本仓主力是 `fix/*` → 连桩都不触发。
- `.github/workflows/pr-merge-guard.yml` 只有 `actions/github-script` 建 `in_progress` check，**无任何 `run:` 步骤**。
- `quality/pretests-retirement-gate` 只校验 `TEST_STATUS != not_tested`、时间非 1970、`LAST_TESTED_COMMIT == HEAD`；三行 `printf` 手写 `test-gate.env` 就能返回 0（无签名、无 hash、无退出码）。
- R12.5（#4216）已把写入收口到 `freely test-gate record`（原子写、仅 test 工位、daemon 不再冒充结果），但它仍只写 3 个字段、**不执行测试**，agent 说 completed 就是 completed。本条是 R12.5 之后剩下的那一半。
- `docs/system/workspace/scripts/tests/` 有 500+ 测试资产，无聚合 runner；回归靠人记得跑哪几个。
- 本轮实测：构造隔离 git 项目树 + 手写三行 `test-gate.env` → 真实 `pretests-retirement-gate` 返回 **0**（缺陷复现）。

## 证伪（现有 open issue 未覆盖）

- #4216（R12.5，已关闭）解决「没有 agent 可用的记录命令」，验收只到「唯一写入/原子/工位校验」，不含退出码与证据 hash。
- #4146 / #4147（R8/R9，已关闭）是门禁 fail-open 与孤儿接线，不涉及测试证据内容。
- #4198（R1）是门禁性能批量化；#4075 是 gate failure followthrough；均与「证据可否验证」无关。
- 其余 open issue 无 `CI 桩 / test-all / evidence hash` 相关项。

## 关键设计

1. **单一真源** `quality/test-evidence.py`：`write` 原子写 8 字段（含 `TEST_COMMAND`、`TEST_EXIT_CODE`、`EVIDENCE_FILE`、`EVIDENCE_SHA256`、`EVIDENCE_HEAD`）；`validate` 校验字段齐全、退出码 0、证据文件 sha256 匹配、HEAD 一致、时间非 1970。
2. **只有真实 runner 能产出合法证据**：新增 `freely test-gate run --worktree <test wt> -- <command>` —— 在 test 工位真实执行命令、把输出落到 `.freely/run/test-evidence.log`、记录真实 rc；`rc=0` 才写 `completed`。旧 `record` 保留但写出的是无机器证明的 legacy 格式，门禁拒绝。
3. **门禁 fail-closed**：`pretests-retirement-gate` 在 freshness 检查后调用 `test-evidence.py validate`；缺 helper 也拒绝，不静默放行。
4. **替换 CI 桩**：`.gitee-ci.yml` 删 `echo "CI OK"`、加 `fix/*`、跑 `bin/test-all --ci`；GitHub workflow 加真实 `run:` job。
5. **聚合入口** `bin/test-all`：白名单（已验证子集）+ 明确 known-broken 清单，避免一上来全红；`--ci` 只跑纯本地子集。
6. **证据入版本控制**：新增 `freely evidence add <file>`（内部 `git add -f` + 记录 hash 到 manifest），替代人工记 `-f`。

## 被否决

- 继续信任 `record` 的 `--status completed`：仍是自述，验收 RED 明确要求拒绝。
- 一次性跑全部 500+ 测试：大量预存红会让 CI 永久红，失去信号；先白名单 + known-broken。
- 把证据写进 git 提交信息：跨工位/跨机器不可解析，且门禁读不到。
- 用签名密钥：本机没有 PKI，hash + HEAD 绑定已足以防止「手写三行」。
