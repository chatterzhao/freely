# PRD: 物化时写入达标 H1 并提供安全回填命令

- issue_id: I-20261104T082542Z-A
- source_raw: raw-20261104T082542Z
- workflow_kind: fix
- milestone: M-20261104T082542Z-A
- story: platform/issue-parity（复用既有 story，epics-map.svg 无需改动）

## 目标

消除「每个新 raw issue 首次 PR 必被 `content_diverged` 阻断」的固定人工成本，且不破坏 Q2 刚收敛的标题达标与身份兼容能力。

## 唯一改动范围

1. `docs/system/workspace/scripts/sync/raw_title_contract.py` 新增纯函数 `local_heading_title(raw_key, title)`。
2. `platform-adapter.py::pull_raw_issue()` 落盘时在 frontmatter 之后写入一个 H1（幂等）。
3. 新增 `bin/raw-issue-backfill-h1`（默认 dry-run 的回填命令）。
4. 新增回归测试 `test-materialize-h1`。

## 不退化边界

- `canonical_raw_title()` / `is_canonical_raw_title()` / `platform_title()` 行为不变。
- `created_at` 反推兼容分支保留，仅作诊断；本地 `raw_key` / `target_dir` 不漂移。
- `_resolve_raw_identity()` 单条兜底、`issue-sync._platform_title()` 自动达标、`feedback edit` 规范化均不改动。
- 不改写 700 份历史 raw 语料（本 PR 只交付命令）。

## 功能需求

- FR-1: `local_heading_title()` 返回「平台 canonical title 去掉 `[RAW-<key>] ` 前缀」的纯标题，单行、无前缀、空值兜底；对非时间戳形状的历史 key 也必须正确。
- FR-2: `pull_raw_issue()` 写入 H1；body 已有 `# ` 行时不重复注入；重复 pull 仍只有一个 H1；frontmatter 与正文其余部分逐字节保留。
- FR-3: 回填命令默认 dry-run 不写文件；标题只来自 `issue_title` frontmatter 或平台 replica；无来源则 SKIP；已有 H1 的文件不动；`--apply` 原子写、幂等。
- FR-4: 回归测试覆盖物化 H1、幂等、非标准 key、Q2 兼容、回填 dry-run/apply。

## 非功能需求

- 真实双平台副本物化后，本地与平台 `canonical_projection` 的 fingerprint 完全一致。
- 805 份真实 issue.md 的 Q2 既有函数新旧对比 0 差异。
- 7 个相关回归测试零新增失败。

## 明确不纳入

批量执行 700 份历史回填、统一历史 raw key 格式、修改 `canonical_raw_title()` 的 `_STALE_PREFIX` 正则、改动 `issue-sync` / `feedback edit` / `wt-create` 的既有逻辑。

## 验收

见 `verification/pre-tests.md` 与 `verification/test-evidence/AT-001-RED.log` / `AT-001-GREEN.log`。
