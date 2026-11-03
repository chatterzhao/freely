---
b1_id: B1-20261102T103216Z
phase_state: completed
source_raw: raw-20261102T103216Z
source_url: https://github.com/chatterzhao/freely/issues/4119
produced_candidate: C-20261102T103216Z-A
created_at: 2026-11-02
---

# B1_IBM: 受控调用方的身份识别不再依赖 ps

## 1. Input

- raw issue：`raw-20261102T103216Z`（GitHub #4119 / Gitee IKSE3I）。
- 现象：`wt-close` 删除远程分支时被 pre-push 拦截；`wt-create` 创建受控分支时被 reference-transaction 拦截。
- 环境：本机沙箱对 `ps` 返回 `operation not permitted`，两个 hook 都靠 `ps` 遍历父进程识别调用方。

## 2. Problem

hook 的设计意图是“只允许 wt-create 建受控分支、只允许 wt-close 删远程分支”。实现方式是用 `ps` 看父进程命令行。一旦 `ps` 不可用（沙箱、容器、精简系统），识别恒失败，**连被授权的封装命令也被拦**，形成“门禁把钥匙锁在门里”。

## 3. Discovery

- `.githooks/{reference-transaction,pre-push}` 只是包装层，实际执行 `docs/system/workspace/hooks/*.sh`；改错文件不会生效（本次踩过）。
- `reference-transaction.sh` 的 `_caller_is_wt_create/_caller_is_wt_close` 与 `pre-push.sh` 的删除分支都调用 `ps -o comm=/args=/ppid=`。
- 当前分支创建被拦，导致无法用正常流程修复自己——鸡生蛋。

## 4. Options

| 选项 | 内容 | 评价 |
|---|---|---|
| A（选中） | 封装命令在调用 git 前设置显式标记；hook 先看标记，再看 `ps` | 小、可测、不削弱意图；直接 `git push --delete` / 手工 `worktree add -b` 仍被拦 |
| B | 用 `/proc` 或 `sysctl` 替代 `ps` | macOS 无 `/proc`，`sysctl` 解析脆弱；仍依赖平台 |
| C | 去掉 hook 的调用方检查 | 等于放弃门禁，拒绝 |

## 5. Decision

- 采用 A，并**把 reference-transaction 一并修**：两个 hook 是同一根因，只修 pre-push 仍然建不出工位。
- 标记名：`FREELY_WT_CREATE=1`（wt-create）、`FREELY_WT_CLOSE=1`（wt-close 预留）、`FREELY_ALLOW_REMOTE_BRANCH_DELETE=1`（wt-close 删除远程分支）。
- 只由封装命令设置；用户手工 export 同 name 仍可绕过，但这是显式行为，审计可查（与 `FREELY_SKIP_*` 同类风险）。

## 6. Scope 变更说明

raw 只写了 wt-close 删远程分支；B1 发现 wt-create 的分支创建被同一根因阻断，故把 reference-transaction 纳入同一 candidate。范围扩大有明确证据（本次建工位失败日志）。

## 7. 风险

- 标记可被手工伪造；缓解：只在封装命令内设置，hook 保留 `ps` 作为第二判据，且直接命令仍默认拦截。
- 旧 hook 若被其他工具直接调用，行为不变。
