# Tasks: I-20261125T071429Z-A

- issue_id: I-20261125T071429Z-A
- phase_state: done_b2_ibm

## T1 — adapter 只读副本枚举
- [ ] `find_open_replicas_by_local_id(local_id)`：复用 `list_open_issue_records()`，按标题过滤
- [ ] 过滤规则：标题含 `local_id` 且含 `[I-`；排除 `[RAW-` 标题与其他 I-* id
- [ ] degraded（任一平台读失败）→ `ok=False`，不得当成空列表
- [ ] CLI `verify-local-id <local_id>`：JSON 输出；0=无 OPEN 且可读，3=存在 OPEN，1=不可读
- [ ] 只读：不产生任何平台写

## T2 — wt-close 门禁取证
- [ ] Phase 2.5 对每个 completed child 调 `verify-local-id`
- [ ] 存在 OPEN → 拒绝，打印平台 + 编号 + 修复命令
- [ ] 不可读 → 拒绝（fail-closed），打印重试命令
- [ ] `--skip-platform` 需 `--reason`，缺失即拒绝并说明
- [ ] 保持 write-free

## T3 — 关闭通道对账
- [ ] CLI `close-local-id <local_id> <platform_ids_json>`：枚举 OPEN 副本与映射并集后关闭
- [ ] `raw_lifecycle_effects.close_linked` 改走 `close-local-id`
- [ ] 任平台未 closed → 非零且不写 `platform_state`

## T4 — 去吞错
- [ ] `cmd-batch.sh` 去掉 `cmd_close_linked ... || true`，汇总失败并最终非零
- [ ] `pr-merge-guarded` 捕获 batch rc，非零即中止合并并给修复命令

## T5 — 去重复创建
- [ ] `_already_on_platform` 增加平台侧判定（按 local_id 枚举，open/closed 均算存在）
- [ ] 存在未映射副本时跳过 create 并提示交给 close-local-id

## 验证
- [ ] AT-001 RED（develop 基线）→ GREEN（工位）
- [ ] `test-all --ci` 全绿
- [ ] runtime 行数预算不受影响（未改 runtime/freely）
