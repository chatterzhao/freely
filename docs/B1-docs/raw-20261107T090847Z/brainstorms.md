# Brainstorms: raw-20261107T090847Z

## 问题（R9 评审期间自举发现，已按规范立项）

`hooks/README.md` 宣称三层治理，R9 补上了第一层提交期阻断，但第三层 `governance-check` 的 post-merge receipt 审计仍是坏的：`audit_current_protected_branch_merge_receipt()` 的 `merge_path` allowlist 只认旧值 `merge-guarded|merge-guarded-complete`，而 `pr-merge-guarded` 写入的是 `pr-merge-guarded*`。更糟的是脚本 `set -euo pipefail` 在更早的检查处提前退出，这条误报在真实运行中根本不出现——「既有假阳性又不生效」双重失真。

## 证据

- 真实 develop HEAD `0ad3941ff` 是 2-parent 受保护 merge，receipt 为 `Freely-Merge-Path: pr-merge-guarded` / `Freely-Bypass-Mode: forbidden` / `Freely-Source-Branch: fix/...`。
- 单独抽取 audit 函数体在真实 develop 执行：`[FAIL] ... unknown Freely-Merge-Path 'pr-merge-guarded'`，`PROBE_ERRORS=1`。
- 完整 `./bin/governance-check`（develop）只有 5 条预存 `[FAIL] missing file`，既无该 receipt 诊断也无末尾汇总行，退出码 1 → 审计层未运行。
- 历史取值统计：旧值 `merge-guarded` 1205 / `merge-guarded-complete` 84 / `merge-guarded-break-glass` 23；新值 `pr-merge-guarded` 675 / `pr-merge-guarded-complete` 8。两代都在历史里，不能只认一代。
- 提前退出根因（隔离空仓库实测）：`entries=()` 在 `set -u` 下 `for entry in "${entries[@]}"` 报 `unbound variable`（line 874）；另有 `check_entry_naming` 在 fail 后 `return 1`、三个 check 函数对缺失文件跑 `rg`（rc=2 成为函数最后一条命令）也会触发 `set -e` 中断。

## 证伪（确认为未被覆盖的独立缺陷）

现有 open issue 中仅 #4147（R9，commit-msg 接线）提及 `governance-check`/receipt，其验收标准是「自复查不再是唯一校验点」，不含 allowlist 不一致与控制流失真；#4151 是测试证据链/CI 执行，#4146 是 shim fail-open。三者均不覆盖 → 用 `./bin/freely feedback` 创建 `raw-20261107T090847Z` / #4211 / IKTNCE，排入 goal R9.5，在 R9 完成后紧接做。

## 关键设计

1. allowlist 同时接受两代合法值（break-glass 仍走独立 ledger，无差别放宽）。
2. 修复 `set -e` 提前退出时**不删除也不削弱任何检查**：所有 check 仍照常调用 `fail()`/`warn()` 记录错误，只把「函数的返回码」与「错误已记录」解耦；空 `entries` 用 `#entries[@]` 守卫；audit 调用 `|| true`。
3. 新增回归测试：隔离 git 仓库构造真实 2-parent merge，覆盖新式/旧式/非法/缺失 receipt 与「完整脚本仍跑到汇总」。
4. 不改 `pr-merge-guarded` 写入值（675+ 历史）、不改 R9 刚接线的 `commit-msg.sh`、不改 backfills/break-glass ledger。

## 自举评审

本轮未发现「现有 open issue 未覆盖」的新缺陷；2 个预存红测试归 #4151。本 issue 自身即为上一轮自举发现的闭环。
