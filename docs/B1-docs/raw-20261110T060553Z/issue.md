---
schema_version: '1'
local_id: raw-20261110T060553Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T060553Z-A
platform_ids:
  github:
    issue_id: '4252'
    url: https://github.com/chatterzhao/freely/issues/4252
    synced_at: ''
  gitee:
    issue_id: IKU9MB
    url: https://gitee.com/zhaoquan/freely/issues/IKU9MB
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T060553Z/issues/I-20261110T060553Z-A.md
last_synced_comment_at:
  github: '2026-11-10T07:45:54Z'
  gitee: '2026-11-10T07:45:54Z'
hash: ''
created_at: '2026-11-10T06:05:53Z'
updated_at: '2026-11-10T07:50:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T060553Z-A
source_candidate: ''
completed_at: '2026-11-10T07:45:53Z'
closeout_note: ''
severity: P1
---

# fix: 状态文件 source 可执行化，改不可执行格式与白名单读取

workflow_kind: fix

workflow_kind: fix

## 来源
从 #4246 / IKU1PH（输入边界二）拆分。原 issue 三条面，本轮已完成「TSV 派发改 JSON Lines + boundary lint」；本条承接**状态文件可执行化**。R22（#4156）同样采取 scope 收敛：4 面做 2 面、拆出 #4246，避免把协议迁移与行为不变的改动混在一个 PR。

## 问题
`docs/system/workspace/scripts/runtime/freely` 用 heredoc/`printf` 写 session / workcell / manager-worker-launch 状态时，把变量值直接插值成 `KEY="value"` 行；读侧直接 `source` 该文件。值含双引号即可注入任意命令，含换行会在 `set -e` 下让 supervisor 循环崩溃。AI 生成的摘要、reason、分支名都可能进入这些状态文件。

同族文件：`session-state.env`、`workcell-state.env`、`manager-worker-launch-state.env`、`preemption-state.env`、`cooldown state`。

**正面先例**：外部文件 `meta.env` 已用 `load_meta_env_snapshot` 白名单 awk 解析（freely:6584 等），不会 `source`。正确做法在仓库里已有。

## 实测（develop bb5770500）
- `grep -n 'source ".*state' docs/system/workspace/scripts/runtime/freely` 命中 **20 处**（如 :466 / :1873 / :2011 / :2623 / :8234 / :8451 / :9493）。
- 写入点 `cat >"$state_file" <<EOF` / `printf ... >"$state_file"` 至少 **15 处**（:475 / :687 / :2631 / :2698 / :8161 / :8667 / :9296 / :9378 / :11827 / :13525 / :15199 / :18004 等）。
- 状态格式目前是 shell 赋值语句，读写两侧耦合，必须成组迁移且给兼容读取期。

## 影响
- 值含 `"` / `$()` / 反引号 / 换行 → 在 daemon 上下文执行攻击者代码或让 supervisor 退出。
- 与 R22 已修的 `pr-review-guarded` 分支名注入同族，只是入口换成「AI 写进状态文件、下次巡逻读回」。

## 修复方案
1. 状态文件改为不可执行格式：`KEY<TAB>value` 单行制表符分隔（值内 tab/换行用 JSON 转义），或每行一个 JSON 对象。
2. 新增统一读写真源 `runtime/state_file.py`（write/read，白名单键、拒绝未知键），读侧复用 `load_meta_env_snapshot` 的白名单思路，全部去掉 `source`。
3. 兼容期：reader 同时接受旧 `KEY="value"` 行但**不执行**（按 `=` 切分、去首尾引号、不展开 `$`），保证滚动升级时旧状态文件可读。
4. 逐组迁移 20 处读 + 15 处写，每组单独提交并跑对应 `test-freely-*` 回归（全仓已有大量 manager-worker-launch 状态测试可作护栏）。

## 验收标准
- RED：构造含 `"` 与换行的状态值写入后 `source`，断言注入命令被执行 / supervisor 崩溃（PoC 限临时仓库，不访问平台）。
- GREEN：同样值经新 reader 读出后**逐字节相等**，且不执行、不崩溃；未知键被拒绝。
- GREEN：`grep -n 'source ".*state' docs/system/workspace/scripts/runtime/freely` 无命中。
- GREEN：兼容 reader 能读旧格式且不展开 `$()`；现有 `test-freely-manager-worker-launch-*` 等状态回归全绿。

## 不退化边界
- 不改状态文件的**键名与语义**（下游 20+ 处读取依赖）。
- 不改 `load_meta_env_snapshot` 对 `meta.env` 的既有解析。
- 迁移期间旧状态文件必须可读，不得要求人工清空 `.freely/run/`。
- 不引入第三方依赖（沿用 stdlib）。

## 明确不纳入
- 一次性删除全部状态文件（会丢 daemon 恢复信息）。
- 把 `python3 -c` 的 108 个 lint 候选中剩余项一次改完（需逐处判定外部值，先守「禁止新增」边界）。
- 修 `pr-merge-guarded` 收尾的 `unknown: origin` 噪音（#4136 覆盖）。

## 证伪
#4156 / R22（已合并）只做 argv 与 sed；#4246（本轮）只做 TSV + lint；#4239 / R23.6 是派发 CAS / SSE / pkill；#4157 / R25 是 watchdog 与日志，均不覆盖状态文件协议迁移。

### comment-20261110T074553Z
- source: system
- event: promote_finalized
- children: ["I-20261110T060553Z-A"]

拆解为以下任务:
1. [I-20261110T060553Z-A](will-be-updated)
