---
schema_version: '1'
local_id: raw-20261103T132526Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132526Z-A
platform_ids:
  github:
    issue_id: '4149'
    url: https://github.com/chatterzhao/freely/issues/4149
    synced_at: ''
  gitee:
    issue_id: IKSPQ3
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:25:26Z'
updated_at: '2026-11-07T11:42:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T11:46:00Z'
closeout_note: ''
---

# fix: 平台写通道静默失败并自证已同步

workflow_kind: fix

## 根因
两条独立缺陷叠加：① 写通道失败被 `|| true` / `|| echo '{"ok":false}'` 归一化成正常返回，「是否需要重试」又由失败方自己写的 `platform_state` 判定；② 平台探测把「未安装 / 未认证 / 超时 / 无仓库权限」四类原因压成一个 `False`，于是「环境不通」与「平台不支持」对外不可区分，再叠加全或无退出码，「一个平台已建成、另一个失败」就变成整体失败。

## 证据（写通道）
- 调用契约失配：`bin/issue-sync:338-342` 用「方法名 + JSON 串」位置参数调 `gitee-issue.py`，被调侧 `docs/system/workspace/scripts/runtime/gitee-issue.py:309-317` 的 argparse 只接受子命令 + 具名 flag → 退出码 2 → 被 `|| echo '{"ok":false}'` 吞成合法 JSON。
- 返回结构失配：`gitee-issue.py:354-358` 直接 `json.dump` 平台原始对象，调用侧 `bin/issue-sync:495` 读 `d.get('output','')`（该字段不存在）→ 恒空 → 走 `:500` 失败分支。
- 门禁变量从未赋值：`grep GITEE_TOKEN bin/issue-sync` 仅命中 `:486,532,581,669` 四处条件判断，无任何赋值；凭证权威来源是 `gitee-issue.py:47-55`。按文档只把 token 放文件 → `-n "${GITEE_TOKEN:-}"` 恒假 → 整段 Gitee 写操作被跳过，脚本继续写 `platform_state open`、打印 `create complete`。
- 仓库身份三处独立计算，其中一处产出非法值：`bin/issue-sync:299-305` 的 awk 对 `git@gitee-zhaoquan:zhaoquan/freely.git` 得到 `git@gitee-zhaoquan:zhaoquan/freely`（带 host 段、未剥 `.git`）；而 `docs/system/workspace/scripts/sync/platform-adapter.py:504-513`（`GiteeHandler.detect_repo`）正确得到 `zhaoquan/freely`。
- 跳过逻辑自锁：`bin/issue-sync:793-794` 用 `platform_state` 判「两侧一致」从而跳过重试 → 分叉被永久固化。
- 通道是已配置的：`.freely/config.toml:35` `FREELY_REPO_PLATFORMS = "github,gitee"`，`origin` 指向 `git@gitee-zhaoquan:zhaoquan/freely.git`。不是死代码。

## 证据（探测与退出码，HEAD 9bcafa45f 实测）
- `platform-adapter.py:200-206` `GitHubHandler.detect()`：`subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner"], capture_output=True, timeout=10, check=True)`，`except Exception: return False`，**从不读 `capture_output` 抓到的 stderr**。PATH 缺 Homebrew 时真实异常是 `FileNotFoundError: 'gh'`；未登录、GraphQL 504、超时、无仓库权限同样返回 `False`。
- `platform-adapter.py:159-173` `_probe_handler` 把 `detect()` 的 `False` 当成「该平台不可用」；`_handler_for`（`:179`）随后返回 `None`。
- `platform-adapter.py:728-737` `create_issue()` 对 `handler is None` 直接产出 `{"status": "error", "error": "unsupported platform: github"}`（`:735`；同族 `:744`/`:824`/`:864`）→ `gh` 装着、登录着、仓库也通，却报「不支持该平台」。
- `platform-adapter.py:1318-1323` `create-issue` 分支要求 `all(item["status"] == "created")` 才 `exit 0`（`:1322`），否则 `exit 1`。
- `docs/system/workspace/scripts/runtime/freely:25205-25208` 调 adapter；`:25213` 用 `grep -q '"status": "created"'` 判「任一成功」；`:25224-25230` 逐平台 `grep -A2 "\"$_pf\""` 找 `"status": "error"`（`:25226`）——`grep -A2` 只覆盖 2 行，`json.dumps(indent=2)` 下 `status` 落到第 3 行就会漏判。
- 实测后果：PATH 缺 Homebrew 时 GitHub 侧报 `unsupported platform: github`，而 Gitee 已创建成功 → 命令整体非零退出，issue 却已存在；按退出码重试就会产生重复 issue。

## 影响
① Gitee 侧：本地 frontmatter / `platform_state` / scan-state 全显示「已同步/open」，平台上没有对象；issue 可追溯性（本架构核心承诺）在 Gitee 侧 100% 失效，且因跳过逻辑自锁而不自愈。② GitHub 侧：真实故障被翻译成「不支持该平台」，排障方向被误导；更危险的是「已创建但命令报失败」的假故障会诱导重试，直接制造重复 issue（本机构自身就会踩）。

## 修复方案
1. `platform-adapter.py:200-206`（GitHub）与 `:501-502`（Gitee）的 `detect()` 区分四类原因：未安装（`FileNotFoundError`）、未认证（`gh auth status` 失败）、超时、无仓库权限；把 stderr 摘要带进结果，不再一律 `return False`。
2. `create_issue()`（`:728-737`）的 `unsupported platform` 分支改为按探测失败原因产出可诊断文案（如 `github: not installed (gh: command not found)`）；`_probe_handler` 缓存失败原因而不只是 `None`。
3. `platform-adapter.py:1318-1323` 的 `create-issue` 改为**按平台独立汇报**：输出每平台的 `status` 与 `issue_id/url`，部分成功用独立退出码（建议 0=全部创建、3=部分创建、1=全部失败），并把已创建的平台 id 交给调用方落盘。
4. `freely:25213` 与 `:25226` 的文本 grep 改为解析 JSON（读每平台 `status`）；部分成功时把已创建平台写入 frontmatter 的 `platform_ids`，只对失败平台保留待同步。
5. `bin/issue-sync:338-342`、`:495/:500`、`:793-794` 与 token / 仓库身份一并收口（与 #4154 的契约收口同一改动）：删掉 `:299-305` 的 awk 与 4 处 `GITEE_TOKEN` 判断，统一走 `platform-adapter.py` 与 `gitee-issue.py:47-55`；回调契约统一为 `{"output": ...}`，失败非零退出。
6. 写入顺序：先拿到远端 id 再写 `platform_state`；缺 id 一律视为待同步，不允许静默跳过。

## 验收标准
- RED：`PATH=/usr/bin:/bin:/usr/sbin:/sbin` 下执行 `python3 platform-adapter.py create-issue ...`，断言错误信息包含 `gh: command not found`（或 `FileNotFoundError` 摘要）而**不是** `unsupported platform: github`；当前输出后者。
- RED：`gh` 已安装但未登录时，断言该平台报「未认证」而非 `False`；当前四类原因不可区分。
- RED：一个平台必然失败 + 一个平台成功，断言输出同时列出两者 `status`（`created` 带 `issue_id`、`error` 带原因），退出码为「部分成功」而非统一 1；当前只报整体失败。
- RED：让某平台 `status` 落在 `json.dumps(indent=2)` 的第 3 行，断言 `cmd_feedback` 仍能判定该平台失败；当前 `grep -A2`（`freely:25226`）漏判。
- GREEN：`grep -n "grep -A2" runtime/freely` 在 `cmd_feedback` 内无命中（已改为 JSON 解析）。
- GREEN：制造一次 Gitee 失败后 `platform_state` 保持原值、`freely-cycle` 报 `sync_pending`，重试后能自愈，且平台侧不产生重复 issue。
