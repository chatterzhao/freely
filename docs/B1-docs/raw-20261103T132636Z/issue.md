---
schema_version: '1'
local_id: raw-20261103T132636Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132636Z-A
platform_ids:
  github:
    issue_id: '4156'
    url: https://github.com/chatterzhao/freely/issues/4156
    synced_at: ''
  gitee:
    issue_id: IKSPQD
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQD
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132636Z/issues/I-20261103T132636Z-A.md
last_synced_comment_at:
  github: '2026-11-09T08:57:24Z'
  gitee: '2026-11-09T08:57:24Z'
hash: ''
created_at: '2026-11-03T13:26:36Z'
updated_at: '2026-11-09T08:57:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132636Z-A
source_candidate: ''
completed_at: '2026-11-09T08:57:23Z'
closeout_note: ''
---

# fix: 消除外部字符串代码化与 TSV 拼接

workflow_kind: fix

## 根因
没有统一的「外部输入 → shell / python 传参」规范：到处是 `"$var"` 拼进 `python3 -c`、拼进可执行 env、拼进 TSV。输入边界与代码边界重叠。

## 证据
- `python3 -c "..."` 拼接 121 处（`bin/` + `scripts/`；只有 3 处用 heredoc）。高危入口：`bin/pr-review-guarded:48-69` 把第一个位置参数拼进 `python3 -c` 的**单引号字符串**；`git check-ref-format` 实测 `'`、`;`、`$HOME`、`` `id` `` 全部 VALID（双引号 INVALID）→ 审查外部 PR 时分支名可控。
- 状态文件「可执行脚本化」：`freely:14992-15039` 用 heredoc 写 45 个 `"$var"` 直接插值（无 `printf %q`），读侧 `:8508-8511` `source` 它 → 值含 `"` 即执行任意命令；含换行则 `set -e` 下 supervisor 循环崩溃。同族：`workcell-state.env`（`:8533-8536,18772-18775,20667-20669`）、`manager-worker-launch-state.env`（`:13571-13573`）。对比：外部文件 `meta.env` 反而是安全的（`:6585` 白名单 awk 解析）。
- TSV 传 AI 生成的 prompt：`docs/system/workspace/scripts/runtime/consume_worker_tasks.py:23` 只替换 `\n\r` **不处理 `\t`**，`:24` 输出 TSV，`freely:13927` 按 `\t` 切分 → prompt 含 tab（代码块缩进极常见）→ 字段错位 → `:13935` `[[ ! -d ]]` 恒真 → 任务被标 `input-required / worktree_missing`，worker 永久派不出去且原因完全误导；`:25-26 except: pass` 让畸形输入表现为「没有待派发任务」。
- `sed -i ''` 平台不兼容：`bin/pr-review-guarded:710` 在 GNU sed 下 `''` 被当文件名 → 非零 → `set -e` 中止，且发生在评审**通过后**（review 已提交但 phase 未更新）；同型 `freely:1973,5391,17637,21386`（后三处带 `|| true` 静默失败）。

## 影响
三条路径后果不同但同源：① maintainer 机器上任意命令执行（审查外部 PR 的常规动作）；② 状态机里跑任意命令或 supervisor 崩溃；③ worker 无故派不出去且原因显示为「worktree 缺失」，排障方向被误导。另有一条跨平台故障：Linux 上评审通过后流程中止、状态未推进。

## 修复方案
1. 121 处 `python3 -c "..."` 逐步改为 `python3 - <<'PY' ... PY` heredoc + `sys.argv` 传参；先改 3 处高危入口（`pr-review-guarded:48-69`、`freely:13179`、`pr-merge-guarded:504-505`）。
2. 状态文件改为不可执行格式（`KEY<TAB>value` 或 JSON），读侧复用已存在的 `load_meta_env_snapshot:6585` 白名单解析；禁止 `source` 状态文件。
3. worker 派发改 `json.dumps` 单行 JSON，消费侧 `json.loads`，删除 TSV 通道；`consume_worker_tasks.py:25-26` 的 `except: pass` 改为显式报错并跳过该行（带计数）。
4. `sed -i ''` 统一改 `sed -i.bak` 或 python 实现，并清理 4 处 `|| true`。

## 验收标准
- RED：`git check-ref-format "refs/heads/fix/x');print(1);#"` 通过后跑 `pr-review-guarded` 的等价 python 片段，断言不执行内联代码；当前会执行（PoC 限临时仓库，不调平台）。
- RED：构造含 `"` 与换行的状态值写入 session state 后 source，断言不执行命令且不崩溃；当前会执行 / 崩溃。
- RED：构造含 `\t` 的 message 的 submitted 任务，断言 worker 被正常派发；当前被标 `worktree_missing`。
- GREEN：`grep -c 'python3 -c "'` 在上述 3 个高危文件中为 0。
- GREEN：GNU sed 环境下 `pr-review-guarded` 的 pass 分支不再中止（Linux 容器验证，报告 U5）。
- GREEN：状态文件读侧不再 `source`（`grep -rn 'source "\$state_file"' freely` 无命中），改用白名单解析。

### comment-20261109T085723Z
- source: system
- event: promote_finalized
- children: ["I-20261103T132636Z-A"]

拆解为以下任务:
1. [I-20261103T132636Z-A](will-be-updated)
