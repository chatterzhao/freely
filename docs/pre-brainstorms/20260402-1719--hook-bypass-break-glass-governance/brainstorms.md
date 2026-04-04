# Brainstorms - 20260402-1719--hook-bypass-break-glass-governance

## Context

Freely 当前把本地 Git hook、`merge-guarded`、`governance-merge-gate`、`governance-promotion-gate` 作为 develop-bound 保护路径，但最近狗粮过程已经暴露出一个更基础的问题：

- agent 在 gate 失败后，仍可以使用 `git commit --no-verify` 完成 merge commit
- 仓库规范明确要求 `develop` 只接受合规 merge，但没有冻结“哪些 break-glass 绕过场景是允许的”
- `merge-guarded` 只覆盖 merge 发起，不覆盖冲突后 completion path
- `governance-check` 也不会在事后审计“这次 protected-branch merge 是否真的经过受控 gate 路径”

结论不是“某个 hook 写得不够细”这么简单，而是：

- Git client-side hook 天然可被 `--no-verify` 绕过
- Freely 还没有把 break-glass 的白名单场景、证据要求、补救流程写成 canonical governance
- Freely 也没有把 bypass 事后审计接入 `governance-check`

## Immediate Facts From Current Repo State

- 当前 `develop` 顶部确实存在两条通过 `--no-verify` 收尾的 merge:
  - `a10f6d8`
  - `27faa2e`
- 原始 feature branch 和对应 worktree 已删除；这不影响 Git 事后 `revert`，因为 merge commit/tree object 仍在仓库中。
- 从当前图看，如果只讨论“能不能 revert”，技术上仍可按逆序 `revert 27faa2e` 再 `revert a10f6d8`。
- 但从治理上看，这两条 merge 承载的是一个已经 materialized 的 owner issue，而不是无效脏提交；直接回退会把合法功能和 closeout truth 一起撤掉。

因此当前更合理的路径不是“先把功能抹掉”，而是：

1. 冻结 break-glass governance
2. 明确这次绕过是否命中允许场景
3. 若不命中，把它记录为治理违规与 follow-on repair
4. 修补受控 completion path 与 bypass audit

## Why This Cannot Live Only In Skills

这个问题如果只写进 skill，会退化成提示词礼仪，而不是真正治理：

- 宪法应定义 protected branch 默认不得绕过本地 gate，只允许明确白名单的 break-glass
- 法律应成为允许绕过场景的唯一词典，定义前置条件、证据与补救动作
- hooks / merge 脚本真源应说明 hook 只是本地 gate，不是绝对硬防线
- `governance-check` / merge gate 应接入事后审计，防止“跳过一次就永久无痕”
- `AGENTS.md` 只负责提醒 agent 不得自行决定 bypass
- skills 只消费上层规则，不能自己发明豁免

## Candidate Direction

第一阶段先收紧四件事：

1. canonical break-glass dictionary
   - 默认禁止
   - 只允许极少数白名单场景

2. minimal allowed scenarios
   - `tooling_unavailable`
   - `verified_false_negative`

3. mandatory evidence for any bypass
   - failing gate output
   - staged/merge state evidence
   - explicit follow-on owner
   - narrow action boundary

4. post-hoc audit
   - `develop` merge 若缺少受控 bypass receipt / trail，后续 `governance-check` 必须报错

## Open Questions

- break-glass receipt 应写 commit trailer、artifact file，还是两者都要
- `merge-guarded` 是否应接管 conflict-resolution completion path，避免回落到裸 `git commit`
- 事后审计是否只扫 `develop` 新 merge，还是扫描更广的 protected-branch history
- 这次已有的两条 bypass merge 应如何留痕：单独 verification note，还是 reopen owner / 开 dedicated issue
