---
raw_id: raw-20261108T141300Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（issue 证据在 develop `ed4a9ffea` 上逐条复核）

| 证据点 | 实测 | 结论 |
|---|---|---|
| `raw-issue-pull` 物化丢 severity | `bin/raw-issue-pull` 无 severity；真源 `sync/platform-adapter.py::pull_raw_issue` 的 `fm = {key: payload.get(key) for key in RAW_METADATA_FIELDS}` 只取严格 21 字段 | 成立 |
| 契约支持第 22 字段 | `raw_metadata_contract.py` 已有 `SEVERITY_FIELD` / `VALID_SEVERITIES` / `resolve_severity` / `new_raw_metadata(severity=...)`，注释明确「optional, appended last」 | **已就绪**（R15 留下的能力，缺的只是物化接线） |
| `raw_reconciliation` 排除 severity | `canonical_projection` 仍 `startswith(("phase/","severity/"))`，注释写明「materialisation does not write the severity frontmatter field」 | 成立，权宜仍在 |
| 平台副本 labels 可读 | `_discover_one` 返回 `**details`，`fetch_issue` 提供 `labels`；`readable[plat]["labels"]` 可用 | 成立 |

结论：这是一个**接线缺口**，不是能力缺口。契约、标签读取、可选字段校验都已在仓库里，只差物化时把标签写回 frontmatter 并恢复比较。

## 方案方向

### 方向 A：从平台 labels 解析（选中）

- `severity_from_replicas(readable)`：遍历每个可读副本的 `severity/*` 标签，大小写归一（`severity/p0` → `P0`），只认 P0/P1/P2。
- 两个**不同的显式值** → 抛 `ValueError`，由 `pull_raw_issue` 传播，物化失败（fail-closed，不静默猜）。
- 一方缺标签、一方有值 → 采用有值方，同时把缺失打到 stderr（`[severity] ... no severity/* label`）。这是「可诊断」而非「静默猜」：历史 raw、R16.5 PARTIAL 副本、R59 GitHub 副本缺失都合法地没有标签，若一律报错会让所有存量 raw 无法开工。
- 无标签 → 不写字段，保持 21 字段零改写。

### 方向 B：从平台 body 的 frontmatter 复制 severity

- `feedback create` 确实把 severity 写进平台 body 的 frontmatter；`payload.get("severity")` 可取。
- 缺点：body 是创建时快照，平台标签才是分诊时被修改的权威视图；且历史 raw 的 body 可能不带 frontmatter。单纯靠 body 无法保证「本地与平台标签一致」。
- 本轮**不采用**作为主路径，但 `fm` 仍从 payload 复制严格字段，body 里的 severity 即使存在也会被标签解析结果覆盖（最终以标签为准）。

### 方向 C：恢复 `canonical_projection` 的 severity 比较

- 移除 `severity/` 排除，保留 `phase/`（phase 是创建时快照，平台从不更新）。
- 风险核查：`canonical_projection` 有第二指纹机制，本地 record 无 `labels` 字段时 local-vs-platform 跳过标签维度；恢复后主要强化 **platform-vs-platform** 比较——正好是「双平台优先级一致」的机器证明。
- 实测 6 个相关测试与 `bin/test-all --ci` 全绿，未出现历史 divergence。

## 被否决

- **一次性回填所有历史 raw 的 severity**：issue 明确「无 severity 标签的历史 raw 保持 21 字段不重写」；回填需要逐条判断平台标签，且会制造大规模 diff。
- **把 severity 加进 `RAW_METADATA_FIELDS` 变成必需第 22 字段**：契约注释已论证会拒绝所有存量 strict 文档。
- **一方缺标签也 fail-closed**：会让 R59（GitHub 副本缺失）等存量 raw 全部无法开工位，与现有 sync-debt 降级机制冲突。

## fidelity 基线

- RED 必须走**真实 `pull_raw_issue`**（只 mock 平台读取），断言生成的 `issue.md` 里没有 `severity`。
- GREEN 必须由单一所有者 `parse_issue_text` + `resolve_severity` 读到 P0（不是 grep 一下字段）。
- 冲突断言必须真的抛 `ValueError`；legacy 零改写与 projection 区分 P0/P1 作为反向守卫。

## 价值判定

- 不过时：三条证据在 develop `ed4a9ffea` 上全部仍成立。
- 不被覆盖：#4187（feedback 创建时写 severity）已关闭且只覆盖 create 路径；#4230（GitHub 标签缺失）明确把本条列为残余风险；#4252 是状态文件协议，#4254 是派发/SSE，均无关。
- 高价值（吃狗粮杠杆）：每一轮 `wt-create` 都会物化一次，**P0/P1 在开工那一刻就退回 P2**，分诊排序因此失真。
