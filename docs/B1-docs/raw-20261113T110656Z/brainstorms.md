## 0. 设计意图审计
### B0 前置广搜
- 关键词族：`implementation-in-bin` → `scripts/bin-projections.yaml`、`bin/check-bin-projection`；`raw-issue-pull` / `deploy-skills` / `issue-sync-bootstrap` → `tests/test-raw-issue-pull-parity.py`、`docs/B2-docs/gate/platform/raw-20261105T121046Z`（sha256 验收）。
- 三类分层：当前生效 = bin/ 中的业务实现 + registry 债务条目；权威恢复点 = `scripts/README.md` 的「bin 只做投影」；历史 = R32.5 的 22/13 判定。
- 矛盾清单：bin/ 承担业务逻辑违反 README；registry 明确写了迁移目标域；本批只迁 3 条，不碰其他 10 条。
- 二元决策：继续——按 raw 建议批次 ① 迁移 sync/ + skills/ 三条。
### 外部锚点
- `scripts/README.md`: bin/ 投影层；`bin/check-bin-projection` 的 shrink 规则；R32.5 判定 13 条应迁移。
- 判定：实现未完成（债务），不是设计问题。
- 影响面：3 个 bin 入口、3 个 scripts 真源、registry、投影一致性锁、既有 parity 测试。
## 0.1 四问
Q1 代码分层；Q2 scripts 拥有实现，bin 只转发；Q3 不改 dispatcher；Q4 AT 断言 ≤8 行、真源存在、registry 删除、checker 全绿。
## 1. 决策
批次①：raw-issue-pull → scripts/sync/；issue-sync-bootstrap → scripts/sync/；deploy-skills → scripts/skills/。bin 入口 5 行 exec。剩余 10 条另立 raw 分两批。
