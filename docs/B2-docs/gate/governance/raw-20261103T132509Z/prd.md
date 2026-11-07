# PRD: 接线 commit-msg 提交期阻断

- issue_id: I-20261103T132509Z-A
- source_raw: raw-20261103T132509Z
- workflow_kind: fix
- milestone: M-20261103T132509Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

把孤儿 `commit-msg.sh` 接进 hook 链，补齐 `hooks/README.md:41` 宣称的三层治理第一层；同时用受控 handshake 挡住「手工 merge 后自填 trailer」。

## 唯一改动范围

1. 新增 `.githooks/commit-msg`（复用 R8 fail-closed shim 模板）。
2. `docs/system/workspace/hooks/commit-msg.sh`：受控 handshake 校验、trailer 校验收窄到 develop/main、修复 pipefail 静默退出与 stderr 路由。
3. `docs/system/workspace/hooks/README.md`：补已接线说明。
4. 新增回归测试 `test-commit-msg-wireup`。

## 不退化边界

- `post-checkout` 逐字节不变；`governance-check` / `pr-merge-guarded` 逐字节不变。
- 真实历史 25 条 commit 通用规范 0 违规；guarded merge 全部带完整 trailer。
- test-pre-merge sync merge 不被拦；普通 commit 正常；通用 message 规则保留。
- 自举发现 #4211 排入 goal R9.5，本 PR 不夹带。

## 功能需求

- FR-1: shim 用 `-f`、缺真身 exit 2，兼容 100644 真身。
- FR-2: develop/main merge 缺 trailer 被拒并打印原因；自填 trailer 无 handshake 被拒。
- FR-3: 合法 guarded merge 通过；test 沙箱 merge 通过；普通 commit 通过。
- FR-4: README 三层表述与实现一致。
- FR-5: 回归覆盖 6 个隔离仓库场景 + 静态契约 + 13 个回归基线对比。

## 验收

AT-001 基线 RED 9 失败 / 5 既有能力 PASS → GREEN 14/14；13 个回归基线对比 0 新增失败；真实工位 commit/PR/merge 链路无自锁。
