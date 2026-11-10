---
schema_version: '1'
local_id: raw-20261109T085539Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4246'
    url: https://github.com/chatterzhao/freely/issues/4246
    synced_at: ''
  gitee:
    issue_id: IKU1PH
    url: https://gitee.com/zhaoquan/freely/issues/IKU1PH
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-09T08:55:39Z'
updated_at: '2026-11-09T08:55:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# fix: 状态文件可执行化 + TSV 派发通道 + 剩余 python3 -c 拼接（输入边界二）

workflow_kind: fix

## 背景

从 #4156 / IKSQ2C（外部字符串代码化与 TSV 拼接）拆分。原 issue 有 4 条修复面，本轮已完成：

- (1) `pr-review-guarded` 把外部分支名插值进 `python3 -c` 脚本体（RCE）→ 改 heredoc + argv
- (4) `sed -i ''` 6 处（BSD-only，GNU sed 下会被当文件名且 `set -e` 中止）→ 统一 `sed -i.bak` + 同命令清理备份；顺带修了 `wt-close:1251` 基线就存在的 `.bak` 残留

本 issue 承接剩余三条。

## 问题 1：状态文件是「可执行脚本」

- `freely` 用 heredoc 写 session state 时把 45 个 `"$var"` 直接插值（无 `printf %q`），读侧直接 `source` 该文件 → 值含双引号即执行任意命令；含换行在 `set -e` 下让 supervisor 循环崩溃。
- 同族：`workcell-state.env`、`manager-worker-launch-state.env`。
- 对比：外部文件 `meta.env` 反而是安全的（白名单 awk 解析 `load_meta_env_snapshot`），说明正确做法在仓库里已有先例。

修复方向：状态文件改不可执行格式（`KEY<TAB>value` 或 JSON），读侧复用 `load_meta_env_snapshot` 白名单解析；禁止 `source` 状态文件。

## 问题 2：TSV 传 AI 生成的 prompt

- `consume_worker_tasks.py` 只替换 `\n\r` 不处理 `\t`，输出 TSV；`freely` 按 `\t` 切分 → prompt 含 tab（代码块缩进极常见）→ 字段错位 → `[[ ! -d ]]` 恒真 → 任务被标 `input-required / worktree_missing`，worker 永久派不出去且原因完全误导。
- 同处 `except: pass` 让畸形输入表现为「没有待派发任务」。

修复方向：改 `json.dumps` 单行 JSON + 消费侧 `json.loads`，删除 TSV 通道；`except: pass` 改显式报错并按行跳过 + 计数。

## 问题 3：剩余 `python3 -c` 拼接

- 全仓仍有约 195 处 `python3 -c "..."`，其中少量把外部变量插值进单引号字符串。
- 修复方向：逐步改 heredoc + `sys.argv`；先加 boundary lint（禁止在 `python3 -c` 字符串体内出现单引号包裹的 `$var`），再按 lint 清单收敛。

## 验收标准

- RED：状态值含双引号与换行 → source 后执行命令 / 崩溃；修复后不执行且不崩。
- RED：prompt 含 tab 的 submitted 任务被标 `worktree_missing`；修复后正常派发。
- GREEN：`grep -rn 'source "\$state_file"' freely` 无命中。
- GREEN：TSV 通道删除，派发走 JSON。
- GREEN：boundary lint 覆盖 `python3 -c` 插值，违规数随迁移下降。
