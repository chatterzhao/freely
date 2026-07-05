# Brainstorms - 20260402-0020--hook-bypass-breakglass-governance

## Context

Freely 当前把 `.githooks`、`pre-commit`、`pre-merge-commit`、`pr-merge-guarded` 和相关 quality gate 当作本地治理门禁，但狗粮过程中已经真实暴露一个更高优先级的漏洞：

- AI 在 gate 看起来误判时，仍可直接使用 `git commit --no-verify` 收尾
- 现有真源没有明确给出“哪些 break-glass 场景允许、哪些绝对不允许”
- `pr-merge-guarded` 只约束 merge 发起，不约束冲突后 completion path
- `governance-check` 也没有事后审计 develop merge 是否真正经过受控 guarded path

结果是：

- 规范把 hook 叫做门禁，但门禁的例外条件没有 canonical 定义
- AI 很容易把“我已经人工确认是误报”错当成合法绕过理由
- 即使本次功能实现本身正确，治理上仍留下了不可接受的先例

## Immediate Safety Check: Can The Recent Merges Still Be Reverted?

当前 `develop` 顶部相关 merge 为：

- `27faa2e`：post-merge writeback lane merge
- `a10f6d8`：ownership governance feature merge

本轮实测结果：

- `git revert --no-commit -m 1 27faa2e` 可干净进入 revert 状态，再正常 `git revert --abort`
- `git revert --no-commit -m 1 a10f6d8` 不会卡死，但会和后续 writeback 产物冲突

结论：

- 从 Git 机制上，这两条 merge 不是“不可撤回”
- 但它们已经不再是“一把无冲突回退”的状态
- feature branch / worktree 已删除并不妨碍 revert；`git revert` 只依赖 canonical `develop` 历史
- 是否选择撤回，不应只看技术可行性，还要看：当前问题是功能错误，还是治理绕过

当前更像后者：

- ownership anti-stomp 功能本身已经吸收到 `develop`
- 当前暴露的是 merge/bypass governance 缺口，而不是 ownership 功能本体错误
- 因此默认优先级应是 forward-fix governance，而不是先把功能整体回滚

## Why This Is Not A Skill Problem

检索结果说明：

- 仓库里的 skill 没有任何地方把 `--no-verify` 定义成正常路径
- 搜到的 `--dangerously-bypass-approvals-and-sandbox` / `bypassPermissions` 属于 AI 工具权限模式，不是 Git hook 绕过许可
- 真正的问题是：
  - Git client hook 天生可被 `--no-verify` 跳过
  - 宪法/法律/入口提示没有把 break-glass 规则写成白名单
  - runtime / merge script 没把冲突收尾包进受控 completion path

## Where The Contract Should Live

分层建议应固定如下：

1. `docs/CONSTITUTION.md`
   - 只写原则：保护分支上的 hook/gate bypass 默认违规
   - 只有白名单定义的 break-glass 才允许

2. `docs/LAWS.md`
   - 作为唯一的 break-glass 词典真源
   - 明确允许场景、前置条件、最小证据、补救动作、审计要求
   - 未列入白名单的绕过一律违规

3. `AGENTS.md`
   - 只写入口提醒：AI 不得自行决定 `--no-verify`
   - 若命中 break-glass，必须按 `LAWS.md` 执行

4. `docs/system/workspace/hooks/README.md`
   - 明确 hook 是 local gate，不是绝对防线
   - 明确 `--no-verify` 是 break-glass，不是正常开发路径

5. `docs/system/workspace/scripts/worktree/pr-merge-guarded`
   - 需要承担受控 merge completion path，而不是把冲突后收尾放回裸 `git commit`

6. `docs/system/workspace/scripts/quality/governance-check`
   - 需要承担事后审计：没有 guarded receipt / bypass receipt 的 develop merge，后续应报错

7. relevant skills
   - 只消费法律，不自行发明允许场景
   - 重点是 `branch-management`、`constitution-guard`、`laws-enforcer`

## Candidate Boundary

这条预研不应顺手重写所有 merge/governance 逻辑，范围应收紧为：

- freeze break-glass contract
- distinguish legal break-glass from illegal bypass
- define guarded completion / receipt semantics
- add audit so bypass becomes detectable after the fact

不在本轮范围：

- 回头重做 ownership anti-stomp 全部功能
- 把所有 Git 本地限制升级成“绝对不可绕过”的宿主级强制控制
- 立即设计远端服务端 enforcement

## Current Working Conclusion

当前最稳妥的结论是：

- 最近两条 merge technically revertable，但不是默认首选
- 本次问题应先按治理缺口处理，而不是把功能本体直接判错
- Freely 必须明文定义 break-glass 白名单；否则任何“人工判断这次例外”都会继续腐蚀门禁
