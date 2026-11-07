# Brainstorms: raw-20261103T132509Z

## 问题

`docs/system/workspace/hooks/commit-msg.sh`（130 行、mode 100644）是孤儿：`.githooks/` 无 `commit-msg` 条目、全仓无引用。trailer 校验因此退化为 `pr-merge-guarded:763-766` 写入方自己复查，手工 `git merge` 后自填 trailer 即可让 merge commit 结构上「看起来合规」。`hooks/README.md:41` 宣称的三层治理实际缺第一层。

## 决策：选方案 1（接线）而非删除

README 已宣称三层、实现完整只差接线；删除实现会削弱治理并需把文档改成「仅事后审计」，方向与「优秀的 freely」相反。依赖 R8 已完成的 `-f` shim 模板。

## 评审中的关键事实与偏差

1. `commit-msg.sh` 的 trailer 校验**只在 `is_merge_commit()` 为真时**执行；普通 commit 走通用规范后 `exit 0`。issue 验收标准写「develop 上普通 `git commit -m chore: x` 缺 trailer 应被拒」与实现不符，RED 改为「develop 上**手工 merge commit** 缺 trailer 被拒」。
2. 真实历史 25 条 commit 逐条验证通用规范（subject ≤100 / 不以句点结尾 / 第二行空行 / 无行尾空格）**0 违规**；guarded merge 均带完整 trailer，接线不会误伤正常提交。
3. **自锁风险**：`is_protected_branch` 原含 `test-pre-merge-*`，实测接线会拦每轮 test 工位 sync merge。收窄为 `main|develop`；AGENTS.md 明确 test 工位是丢弃式沙箱、允许 merge/cherry-pick。
4. **探针实证**：`git merge --continue` 会触发 commit-msg hook，且 `FREELY_GUARDED_MERGE_COMPLETION=1` 与 `freely-guarded-merge-state` 均可见；手工 merge 两者皆无 → 天然的独立校验点，使自填 trailer 也被拒。
5. **修复中发现的真源缺陷**：trailer 提取用 `grep|tail`，在 `set -euo pipefail` 下缺 trailer 会让管道失败、脚本在打印拒绝原因前静默退出；且所有拒绝 heredoc 走 stdout（git 吞 hook stdout）。改为 `sed -n ...p` + 全部重定向 stderr。

## 关键设计

- 新增 `.githooks/commit-msg`，逐字节复用 R8 fail-closed 模板（HOOK_NAME 驱动、用 `-f`、缺真身 `exit 2`），天然兼容 100644 真身。
- `commit-msg.sh`：trailer 校验收窄到 develop/main；新增受控 handshake 校验（env + state 文件三字段 + source/target 与 trailer 一致）；修复 pipefail 静默退出与 stderr 路由。
- `hooks/README.md` 补「commit-msg 提交期阻断（已接线）」小节，三层表述名副其实。
- 新增 `test-commit-msg-wireup`（static 8 + 6 个隔离 git 仓库行为用例，14 项）。

## 自举评审（已按规范立项）

评审中发现 `governance-check:369` 的 `merge_path` allowlist 只认旧的 `merge-guarded*`，会把 675+ 个合法 `pr-merge-guarded` merge 判为 unknown；且脚本 `set -e` 提前退出使该审计层实际不运行。逐条证伪：现有 open issue 只有 #4147 自身提到 receipt，其范围是本轮接线；#4151 是测试执行链，均不覆盖。故用 `freely feedback` 创建 **`raw-20261107T090847Z` / #4211 / IKTNCE**（P1），排入 goal **R9.5**，本 PR 不夹带修复。
