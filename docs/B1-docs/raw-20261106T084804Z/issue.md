---
schema_version: '1'
local_id: raw-20261106T084804Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261106T084804Z-A
platform_ids:
  github:
    issue_id: '4201'
    url: https://github.com/chatterzhao/freely/issues/4201
    synced_at: ''
  gitee:
    issue_id: IKTHI3
    url: https://gitee.com/zhaoquan/freely/issues/IKTHI3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-06T08:48:04Z'
updated_at: '2026-11-07T07:40:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T07:40:00Z'
closeout_note: ''
---

# fix: wt-create 主流程顶层误用 return 1，失败时输出 bash 语法错误

workflow_kind: fix

## 优先级

P1 — 工具链失败语义错误。不是每次都造成可见损害（直接执行时 `set -e` 兜住了退出码 1），但错误信息误导、且一旦脚本被 source 或被包一层 wrapper 就可能「失败后继续往下跑」，属于可靠性缺口。

## 不退化边界（本 issue 的前提）

本 issue 只修「可执行脚本顶层误用 `return`」，不得顺手改动：

- `wt-create` 的四态幂等判定、恢复模式、legacy 补建逻辑、seed 与 `_init_test_worktree_state()` 单一真源（#4186 / #4190 相关，禁止夹带）。
- `bin/wt-create` 的 `exec bash` shim 结构不变（它是唯一入口，本脚本不是被 source 的库）。
- 所有清理动作（`git worktree remove --force` / `git branch -D` 带 `|| true` 兜底）与错误文案保持不变。
- 函数内部的 `return`（如 `_pull_raw_issue`、`_seed_worktree`、`_create_worktree`、`_init_test_worktree_state` 里的 15 处）全部合法，**不在本 issue 范围**，不得改成 `exit`。

注意与既有 open issue 的区别，避免误合并：
- `#4153` 是 `runtime/freely` 被 source 时「顶层 `exit 1` 应改为 `return 1`」，方向**相反**（那个文件是库）。
- `#4157` 是「失败被表达成正常结束 / 降级告警」与 `freely-watchdog` 的 `PRE_CHECK_MAP` 里 `return 1` 结束 `while` 子壳，是不同文件、不同语义。
- 两者都未覆盖「`wt-create` 作为被 `exec bash` 直接执行的入口脚本，在主流程顶层使用 `return 1`」。

## 根因

`docs/system/workspace/scripts/worktree/wt-create` 的主创建流程是**顶层内联代码**（不在任何函数内，最近的 `}` 在 `_init_test_worktree_state()` 之后），却在三处失败分支用了 `return 1`：

- `:889` — raw-issue-pull 失败后的清理分支
- `:909` — dev worktree seed 失败后的清理分支
- `:917` — test worktree 初始化失败后的清理分支

`return` 只允许出现在函数或被 `source` 的脚本中。该文件由 `bin/wt-create` 以 `exec bash <path>` 直接执行，因此这三处是非法控制流。

## 证据（本轮 RED 测试期间实测）

- 隔离 git 仓库中让 `raw-issue-pull` 返回不匹配的 `local_id`，执行 `wt-create --raw-key ... --source platform --kind fix --slug ...`：退出码 1，输出末尾为
  `docs/system/workspace/scripts/worktree/wt-create: line 889: return: can only \`return' from a function or sourced script`。
  清理动作确实执行了（`Deleted branch fix/...`），但**没有**给出「命令因失败而终止」的明确语义，而是 bash 的语法错误提示。
- 用括号深度分析逐行核对：全文件共 18 处 `return 1`，其中 **仅 3 处在顶层**（889 / 909 / 917），其余 15 处都在函数内部，合法。
- `grep -rn 'source.*wt-create'` 在 `bin/` 与 `docs/system/workspace/` 中零命中；`bin/wt-create` 内容为 `exec bash "$ROOT_DIR/docs/system/workspace/scripts/worktree/wt-create" "$@"`，确认本脚本是入口而非库。
- 直接执行时 `set -euo pipefail` 使非法 `return` 的非零状态终止脚本，故未继续创建 test 工位（实测 `git worktree list` 只剩主仓库，无 `test-pre-merge` 分支）。但这是**依赖 shell 隐式行为**的偶然正确性：若将来有 wrapper `source` 该脚本、或把主流程包进函数/子壳，`return 1` 会变成「从 source 返回」而不会终止整个命令，调用方可能继续往下执行并误判成功。

## 影响

- 失败时打印 bash 语法错误而非业务错误，排障者难以判断是「平台拉取失败」还是「脚本写错了」。
- 失败语义依赖 `set -e` 的隐式兜底，不是显式契约；脚本结构一旦调整（例如把主流程收进 `main()` 或被 source）就退化为静默继续。
- 与「优秀的 freely」要求的 fail-closed、可观测失败语义不符。

## 修复方案

1. 把 `:889` / `:909` / `:917` 三处顶层 `return 1` 改为 `exit 1`（保留各自上方的错误文案与清理动作，逐字不动）。
2. 若未来确实需要支持被 source，应显式抽出 `main()` 并用 `BASH_SOURCE` 守卫，而不是在顶层混用 `return`；此项不在本次范围，需另立 issue。
3. 补行为回归测试：在隔离仓库分别触发三处失败分支，断言
   - 退出码为 1；
   - 输出包含对应的业务错误文案且**不包含** `can only \`return'`；
   - 清理已执行（dev/test 分支与工位不残留）；
   - 未继续创建 test 工位。
4. 静态断言：顶层 `return` 计数为 0，函数内合法 `return` 数量不变（防止修复时误改函数内部）。

## 明确不纳入（已评审否决）

- 改 `runtime/freely` 的 source 安全（#4153）、watchdog 的 `PRE_CHECK_MAP`（#4157）、`wt-create` 四态判定（#4190）—— 都是独立 issue，禁止夹带。
- 把函数内部的 `return` 改成 `exit` —— 会破坏子命令与失败清理的组合语义。
- 修改 `bin/wt-create` shim 或引入 `main()` 重构 —— 越界且风险高。

## 验收标准

- GREEN：三处失败分支均 `exit 1`，输出只有业务错误文案，无 bash `return` 语法错误。
- GREEN：隔离仓库中失败后不留 dev/test 分支与工位，不产生半成品。
- GREEN：顶层 `return` 计数 = 0；函数内 `return` 数量与修复前一致；`bash -n` 通过。
- GREEN：`wt-create` 正常创建、恢复模式、legacy 补建、双工位幂等 no-op 的既有行为测试全部仍通过（零退化）。
