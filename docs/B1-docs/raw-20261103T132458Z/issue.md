---
schema_version: '1'
local_id: raw-20261103T132458Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132458Z-A
platform_ids:
  github:
    issue_id: '4146'
    url: https://github.com/chatterzhao/freely/issues/4146
    synced_at: ''
  gitee:
    issue_id: IKSPQ0
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ0
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:24:58Z'
updated_at: '2026-11-07T08:45:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T08:40:00Z'
closeout_note: ''
---

# fix: 门禁 fail-open 把环境缺失翻译成通过

workflow_kind: fix

## 根因
门禁脚本把「拿不到判断依据」实现成「跳过并返回 0」，与「通过」共用同一个退出码；shim 层又把「真身脚本缺失」实现成 `exit 0`。于是环境异常与真实通过不可区分。

## 证据
- shim 层整体 fail-open（最强一处）：`.githooks/pre-commit:1-15` 模板为「找到真身就 exec，找不到就 `exit 0`」（`:7` `[[ -x ... ]]`、`:8` exec、`:15` `exit 0`），同一模板覆盖 `pre-push` / `pre-merge-commit` / `reference-transaction` / `pre-rebase` / `post-rewrite` → 真身缺失时整套客户端门禁静默成功（本次复核读完全部 15 行）。
- `docs/system/workspace/hooks/pre-commit.sh:6-12`：hooksPath 不符时打印 `[HOOK] BLOCKED` 但无 `exit 1`。
- 同文件 `:153` `[[ -f "./bin/worktree-common.sh" ]] || exit 0`；`:245/:300/:317` 用 `[[ -x ./bin/governance-merge-gate ]]` 守卫 checkpoint-guard 与 pretests-gate → 可执行位丢失（Windows 检出 / zip 解包 / `core.fileMode=false`）→ 主门禁静默跳过。
- `bin/pr-create-guarded:207-208`、`:226-227`、`:259-265`、`:297-334`：门禁缺失/异常一律 `[WARN] ... skipping`。
- `docs/system/workspace/scripts/quality/checkpoint-guard:7` `FAIL_ON_REQUIRED=0` + `:233` 仅 `--fail-on-required` 才 `exit 2`，而 `pre-commit.sh:302` 不传该参数 → 恒 0，`:312-322` 为死代码。
- `bin/check-file-size` 全仓无调用点（grep 仅命中自身），实测 `Errors: 6`，且 `:53-55` 只扫 `*.sh/*.py`，漏掉最大的 26,823 行无扩展名文件。
- 反 `--no-verify` 未接线：`.githooks/bin/git:1-25` 实现了剥离 `--no-verify`，但全仓 grep `githooks/bin` 零命中（无安装器、无 PATH 注入）→ `git commit --no-verify` 仍可绕开全部客户端门禁。

## 影响
四种都不需要攻击、只需要一次环境异常或一次图省事：① 缺一个可执行位就关掉 checkpoint / pretests 两道门并返回 0；② `.githooks` 真身缺失时全部客户端 hook 返回 0；③ `[WARN] skipping` 让缺失的门禁与通过的门禁在日志里同样「正常」；④ `--no-verify` 无拦截。门禁的存在性与有效性彻底脱钩。

## 修复方案
1. `.githooks/pre-commit:7` 的 `[[ -x ... ]]` 改 `[[ -f ... ]]`（`bash file` 不需要执行位）；`:15` 的 `exit 0` 改 `exit 1`；同模板族（pre-push 等）一并改。
2. `docs/system/workspace/hooks/pre-commit.sh:6-12` 补 `exit 1`（或 `exit 2` 表示环境不可用）；`:153` 的 `|| exit 0` 改为失败；`:245/:300/:317` 的 `-x` 守卫改 `-f` 且缺失即 `exit 2`。
3. 统一退出码约定：0=通过、1=不通过、2=环境不可用（环境不可用按不通过处理）；`pr-create-guarded` 的 `[WARN] skipping` 全部改为该约定。
4. `checkpoint-guard` 默认 `FAIL_ON_REQUIRED=1`，或由 `pre-commit.sh:302` 显式传 `--fail-on-required`。
5. 要么把 `.githooks/bin` 接进 PATH，要么删掉并在文档中停止宣称「无法绕过」。

## 验收标准
- RED：把 `docs/system/workspace/hooks/pre-commit.sh` 改名（隔离副本）后 `git commit`，断言被拒；当前 shim 走 `:15 exit 0` 放行。
- RED：`chmod -x bin/governance-merge-gate` 后执行 `pre-commit.sh`，断言非零；当前静默跳过。
- RED：`checkpoint-guard` 在缺 required 产物时默认返回非零；当前返回 0。
- GREEN：`grep -n "exit 0" .githooks/pre-commit` 无命中；`pr-create-guarded` 中每处 `skipping` 都伴随非零退出。
- GREEN：`check-file-size` 在 `runtime/freely`（26,823 行）上被触发并报错。
